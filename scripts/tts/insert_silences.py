"""Vrew 낭독본(mp3+srt)에 silence_cues.json 의 무음을 되살려 넣는다 (수면명상 후처리 A안).

Vrew에서는 문장만 이어 낭독하고, 여기서 문장 경계마다 `silence_after` 초의 무음을 삽입한다.
SRT 큐 ↔ silence_cues.json lines[] 를 텍스트로 매칭하므로 Vrew가 마침표에서 클립을 쪼갰거나
짧은 문장을 한 클립에 합쳤어도 따라간다(합친 경우 안쪽 무음은 넣을 수 없어 경고).

입력: {P}/vrew/silence_cues.json + 낭독 mp3/wav + srt
출력: {P}/_video/audio.wav (렌더용 무손실), audio.mp3 (확인용), subtitle.srt (시프트된 자막),
      timing.json (문장별 시작/끝, 총 길이)

★문장 안 끊어읽기(2026-09-19, 레퍼런스 TRQV5h0XMns 실측 반영): 기본으로 켜져 있다.
쉼표·대시·안쪽 마침표 자리에서 TTS가 실제로 쉰 무음 구간(≥0.18s)을 찾아 레퍼런스 길이(쉼표 1.3s / — 2.0s)까지
늘린다. 재녹음 없이 TTS 자체 쉼을 연장. 근처에 실제 무음이 없으면 그 자리는 건너뛴다(말 중간을 절대 자르지 않는다).
구두점 예상 시각은 큐 안 글자 위치 비례로 잡는다 — whisper 단어 json 을 `--words` 로 주면 더 정밀해지지만 필수는 아니다.

Usage:
    python3 scripts/tts/insert_silences.py {P} --audio 01_bodyscan.mp3 --srt 01_bodyscan.srt --scale 0.5
    python3 scripts/tts/insert_silences.py {P} --audio narration.mp3 --srt narration.srt --scale 0.8   # 문장 간 정적만, 80%로
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys

RATE, CH, BPS = 48000, 2, 2            # s16le 48k stereo — Vrew 출력과 동일
FRAME = CH * BPS


def norm(s: str) -> str:
    return re.sub(r"[^0-9A-Za-z가-힣]", "", s)


def parse_srt(path: pathlib.Path):
    txt = path.read_text(encoding="utf-8-sig")
    cues = []
    for block in re.split(r"\n\s*\n", txt.strip()):
        rows = block.strip().splitlines()
        if len(rows) < 3:
            continue
        m = re.match(r"(\d+):(\d\d):(\d\d)[,.](\d{3})\s*-->\s*(\d+):(\d\d):(\d\d)[,.](\d{3})", rows[1])
        if not m:
            continue
        v = [int(x) for x in m.groups()]
        st = v[0] * 3600 + v[1] * 60 + v[2] + v[3] / 1000
        en = v[4] * 3600 + v[5] * 60 + v[6] + v[7] / 1000
        cues.append({"start": st, "end": en, "text": " ".join(rows[2:]).strip()})
    return cues


def fmt_ts(sec: float) -> str:
    ms = round(sec * 1000)
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def match_groups(lines, cues):
    """큐들을 대본 문장 단위로 묶는다 → [{lines:[..], cues:[..]}]. 텍스트 정규화 후 그리디 누적."""
    groups, i, j = [], 0, 0
    while i < len(lines) and j < len(cues):
        gl, bl = [lines[i]], norm(lines[i]["text"]); i += 1
        gc, bc = [cues[j]], norm(cues[j]["text"]); j += 1
        while bl != bc:
            if len(bc) < len(bl):                       # Vrew가 문장을 여러 클립으로 쪼갬
                if not bl.startswith(bc) or j >= len(cues):
                    break
                gc.append(cues[j]); bc += norm(cues[j]["text"]); j += 1
            else:                                       # Vrew가 여러 문장을 한 클립에 합침
                if not bc.startswith(bl) or i >= len(lines):
                    break
                gl.append(lines[i]); bl += norm(lines[i]["text"]); i += 1
        if bl != bc:
            sys.exit(f"✗ 텍스트 불일치 — 대본 {[l['i'] for l in gl]}: {bl[:40]!r} / SRT: {bc[:40]!r}\n"
                     f"   Vrew에서 문장을 지우거나 새로 썼는지 확인. silence_cues.json 을 다시 생성했는지도.")
        groups.append({"lines": gl, "cues": gc})
    if i < len(lines) or j < len(cues):
        sys.exit(f"✗ 남은 항목 — 대본 {len(lines)-i}문장 / SRT {len(cues)-j}큐 가 짝을 못 찾음")
    return groups


BREAK_RE = re.compile(r"[,，]$|[—…]$|\.$")


def break_targets(token: str, a) -> float | None:
    """대본 토큰 끝의 구두점 → 그 뒤에 만들 쉼 길이(초). 없으면 None."""
    t = token.rstrip()
    if t.endswith(("—", "…")):
        return a.dash_pause
    if t.endswith((",", "，")):
        return a.comma_pause
    if t.endswith("."):
        return a.period_pause                     # 그룹 안쪽 마침표 (Vrew가 쪼갠 문장)
    return None


def intra_pauses(group, words, pcm, a):
    """그룹(문장) 안의 쉼표·대시·마침표 자리에서 (삽입 시각, 삽입 초, 토큰) 목록을 만든다.

    ★TTS가 실제로 쉰 구간(무음 ≥ MIN_PAUSE)만 늘린다 (2026-09-19 개정).
      종전에는 whisper 단어 끝 근처에서 "가장 조용한 지점"을 잘랐는데, 한국어 ㄱ/ㄷ/ㅂ 앞 무성 폐쇄
      구간(50~100ms)이 조용해서 `내려놓|고` 처럼 음절 사이를 자르는 사고가 났다.
      이제는 구두점의 예상 시각(글자 위치 비례, whisper 있으면 그걸로) 근처의 실제 무음 구간에
      스냅하고 그 한가운데에 무음을 끼운다. 근처에 무음 구간이 없으면 건너뛴다."""
    st, en = group["cues"][0]["start"], group["cues"][-1]["end"]
    text = " ".join(l["text"] for l in group["lines"])
    merged = []
    for t in text.split():                       # 구두점만 있는 토큰("—")은 앞 토큰에 붙인다
        if not norm(t) and merged:
            merged[-1] += t
        else:
            merged.append(t)
    offs, acc = [], 0
    for t in merged:
        acc += len(norm(t)); offs.append(acc)

    # 구두점별 예상 시각
    est = {}
    gw = [w for w in words if w["s"] >= st - 0.05 and w["e"] <= en + 0.05 and norm(w["w"])] if words else []
    wacc = sum(len(norm(w["w"])) for w in gw)
    use_words = gw and abs(wacc - acc) <= max(2, acc * 0.3)
    for k, tok in enumerate(merged[:-1]):
        if break_targets(tok, a) is None:
            continue
        if use_words:
            want, run = offs[k] * wacc / acc, 0
            for w in gw:
                run += len(norm(w["w"]))
                if run >= want - 0.5:
                    est[k] = w["e"]; break
        else:
            est[k] = st + (en - st) * offs[k] / acc   # 글자 위치 비례

    pauses = detect_pauses(pcm, st, en)
    out, skipped, used = [], [], set()
    for k, t_est in est.items():
        tok, target = merged[k], break_targets(merged[k], a)
        cand = [(abs((p0 + p1) / 2 - t_est), i) for i, (p0, p1) in enumerate(pauses)
                if i not in used and abs((p0 + p1) / 2 - t_est) <= SNAP_WINDOW]
        if not cand:
            skipped.append(f"'{tok}' 근처 무음 없음")
            continue
        _, i = min(cand)
        used.add(i)
        p0, p1 = pauses[i]
        need = target - (p1 - p0)
        if need <= 0.05:
            continue
        out.append(((p0 + p1) / 2, need, tok))
    out.sort()
    return out, ("; ".join(skipped) if skipped else None)


MIN_PAUSE = 0.18        # 이보다 짧은 무음은 자음 폐쇄일 수 있어 안 건드린다
PAUSE_RMS = 250         # ≈ -42 dBFS
SNAP_WINDOW = 0.9       # 예상 시각 ± 이 범위 안의 무음 구간만 후보


def detect_pauses(pcm: bytes, t0: float, t1: float, win: float = 0.01):
    """[t0,t1] 안에서 RMS < PAUSE_RMS 가 MIN_PAUSE 이상 이어지는 구간 → [(start,end)]. 큐 양끝에 닿은 건 제외."""
    from array import array
    f0, f1 = int(t0 * RATE), int(t1 * RATE)
    buf = array("h"); buf.frombytes(pcm[f0 * FRAME:f1 * FRAME])
    step = int(win * RATE) * CH
    quiet = []
    for i in range(0, len(buf) - step + 1, step):
        e = sum(x * x for x in buf[i:i + step])
        quiet.append((e / step) ** 0.5 < PAUSE_RMS)
    runs, i = [], 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]:
                j += 1
            s_, e_ = t0 + i * win, t0 + j * win
            if e_ - s_ >= MIN_PAUSE and i > 0 and j < len(quiet):
                runs.append((s_, e_))
            i = j
        else:
            i += 1
    return runs


def fade_edges(piece: bytes, ms: float = 5.0) -> bytes:
    """조각 양끝에 짧은 페이드 — 잘린 자리의 클릭 방지."""
    from array import array
    buf = array("h"); buf.frombytes(piece)
    n = min(int(RATE * ms / 1000) * CH, len(buf) // 2)
    for k in range(n):
        g = k / n
        buf[k] = int(buf[k] * g)
        buf[-1 - k] = int(buf[-1 - k] * g)
    return buf.tobytes()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("--audio", required=True, help="{P}/vrew/ 안의 낭독 파일명")
    ap.add_argument("--srt", required=True, help="{P}/vrew/ 안의 자막 파일명")
    ap.add_argument("--scale", type=float, default=1.0, help="문장 사이 무음 배율 (기본 1.0)")
    ap.add_argument("--words", default=None, help="(선택) {P}/vrew/ 안의 whisper 단어 json — 구두점 예상 시각 정밀도만 올린다. 없으면 글자 위치 비례")
    ap.add_argument("--no-intra", action="store_true", help="문장 안 끊어읽기 끄기 (문장 간 정적만)")
    ap.add_argument("--comma-pause", type=float, default=1.3, help="쉼표 뒤 쉼 목표(초). 레퍼런스 실측 1.2~1.5")
    ap.add_argument("--dash-pause", type=float, default=2.0, help="— / … 뒤 쉼 목표(초). 레퍼런스 실측 2.0~2.1")
    ap.add_argument("--period-pause", type=float, default=1.5, help="문장 안쪽 마침표 뒤 쉼 목표(초)")
    ap.add_argument("--out", default="_video")
    a = ap.parse_args()

    P = pathlib.Path(a.project_dir)
    vrew = P / "vrew"
    out = P / a.out
    out.mkdir(exist_ok=True)

    cues_json = json.loads((vrew / "silence_cues.json").read_text(encoding="utf-8"))
    lines = cues_json["lines"]
    cues = parse_srt(vrew / a.srt)
    print(f"대본 {len(lines)}문장 / SRT {len(cues)}큐")

    groups = match_groups(lines, cues)
    for g in groups:
        if len(g["lines"]) > 1:
            lost = sum(l["silence_after"] for l in g["lines"][:-1])
            print(f"⚠ 문장 {[l['i'] for l in g['lines']]} 이 한 큐로 합쳐짐 — 안쪽 무음 {lost}초는 넣지 못함")

    pcm = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(vrew / a.audio), "-f", "s16le", "-acodec", "pcm_s16le",
         "-ar", str(RATE), "-ac", str(CH), "-"], capture_output=True, check=True).stdout
    total_in = len(pcm) / FRAME / RATE

    def at(sec: float) -> int:
        return min(len(pcm), int(round(sec * RATE)) * FRAME)

    words = json.loads((vrew / a.words).read_text(encoding="utf-8")) if a.words else None
    intra_total, intra_n, intra_skipped = 0.0, 0, []

    chunks, new_cues, timing, cursor = [], [], [], 0.0
    for g in groups:
        st, en = g["cues"][0]["start"], g["cues"][-1]["end"]
        pauses = []
        if not a.no_intra:
            pauses, why = intra_pauses(g, words, pcm, a)
            if why:
                intra_skipped.append((g["lines"][0]["i"], why))
        # 그룹을 쉼 지점에서 쪼개 사이사이에 무음을 끼운다
        g_start_out, pos, inserted = cursor, st, []
        for cut, need, _tok in pauses:
            piece = fade_edges(pcm[at(pos):at(cut)])
            chunks.append(piece); cursor += len(piece) / FRAME / RATE
            sil = int(round(need * RATE)) * FRAME
            chunks.append(b"\x00" * sil); cursor += sil / FRAME / RATE
            inserted.append((cut, sil / FRAME / RATE)); pos = cut
            intra_total += need; intra_n += 1
        piece = fade_edges(pcm[at(pos):at(en)]) if pauses else pcm[at(pos):at(en)]
        chunks.append(piece); cursor += len(piece) / FRAME / RATE

        def out_time(t):                     # 원본 시각 → 출력 시각 (이 그룹 안)
            return g_start_out + (t - st) + sum(ins for c, ins in inserted if c <= t)

        for c in g["cues"]:
            new_cues.append({"start": out_time(c["start"]), "end": out_time(c["end"]), "text": c["text"]})
        timing.append({"i": [l["i"] for l in g["lines"]], "section": g["lines"][-1]["section"],
                       "text": " ".join(l["text"] for l in g["lines"]),
                       "start": round(g_start_out, 3), "end": round(cursor, 3),
                       "intra_pauses": [{"after": tok, "added": round(need, 2)} for _c, need, tok in pauses],
                       "silence_after": round(g["lines"][-1]["silence_after"] * a.scale, 3)})
        sil = int(round(g["lines"][-1]["silence_after"] * a.scale * RATE)) * FRAME
        chunks.append(b"\x00" * sil)
        cursor += sil / FRAME / RATE

    if not a.no_intra:
        print(f"문장 안 끊어읽기: {intra_n}곳에 총 {intra_total:.1f}초 추가 (쉼표 {a.comma_pause}s / 대시 {a.dash_pause}s / 마침표 {a.period_pause}s)")
        for i, why in intra_skipped:
            print(f"  ⚠ 문장 {i}: {why}")

    raw = b"".join(chunks)
    wav = out / "audio.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(RATE), "-ac", str(CH), "-i", "-",
                    str(wav)], input=raw, check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-codec:a", "libmp3lame", "-b:a", "192k",
                    str(out / "audio.mp3")], check=True)

    srt_txt = "".join(f"{n}\n{fmt_ts(c['start'])} --> {fmt_ts(c['end'])}\n{c['text']}\n\n" for n, c in enumerate(new_cues, 1))
    (out / "subtitle.srt").write_text(srt_txt, encoding="utf-8")

    total_out = len(raw) / FRAME / RATE
    sil_total = sum(t["silence_after"] for t in timing)
    (out / "timing.json").write_text(json.dumps({
        "source_audio": a.audio, "source_srt": a.srt, "silence_scale": a.scale,
        "intra_pause_seconds": round(intra_total, 3),
        "speech_seconds": round(total_in, 3), "silence_seconds": round(sil_total, 3),
        "total_seconds": round(total_out, 3), "narration_end": round(total_out, 3),
        "sentences": timing}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"✓ {wav}  발화 {total_in/60:.1f}분 + 끊어읽기 {intra_total/60:.1f}분 + 문장 간 무음 {sil_total/60:.1f}분 = 총 {total_out/60:.1f}분 ({fmt_ts(total_out)})")
    print(f"✓ {out/'audio.mp3'}  (확인용 192k)")
    print(f"✓ {out/'subtitle.srt'}  {len(new_cues)}큐 시프트")
    print(f"✓ {out/'timing.json'}")


if __name__ == "__main__":
    main()
