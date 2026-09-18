"""Vrew 낭독본(mp3+srt)에 silence_cues.json 의 무음을 되살려 넣는다 (수면명상 후처리 A안).

Vrew에서는 문장만 이어 낭독하고, 여기서 문장 경계마다 `silence_after` 초의 무음을 삽입한다.
SRT 큐 ↔ silence_cues.json lines[] 를 텍스트로 매칭하므로 Vrew가 마침표에서 클립을 쪼갰거나
짧은 문장을 한 클립에 합쳤어도 따라간다(합친 경우 안쪽 무음은 넣을 수 없어 경고).

입력: {P}/vrew/silence_cues.json + 낭독 mp3/wav + srt
출력: {P}/_video/audio.wav (렌더용 무손실), audio.mp3 (확인용), subtitle.srt (시프트된 자막),
      timing.json (문장별 시작/끝, 총 길이)

Usage:
    python3 scripts/tts/insert_silences.py channels/sleep/projects/bodyscan_01 --audio bodyscan_draft.mp3 --srt bodyscan_draft.srt
    python3 scripts/tts/insert_silences.py {P} --audio narration.mp3 --srt narration.srt --scale 0.8   # 정적 길이를 일괄 80%로
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("--audio", required=True, help="{P}/vrew/ 안의 낭독 파일명")
    ap.add_argument("--srt", required=True, help="{P}/vrew/ 안의 자막 파일명")
    ap.add_argument("--scale", type=float, default=1.0, help="무음 길이 배율 (기본 1.0)")
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

    chunks, new_cues, timing, pos, cursor = [], [], [], 0.0, 0.0
    for g in groups:
        st, en = g["cues"][0]["start"], g["cues"][-1]["end"]
        seg = pcm[at(st):at(en)]
        chunks.append(seg)
        seg_sec = len(seg) / FRAME / RATE
        for c in g["cues"]:
            off = cursor + (c["start"] - st)
            new_cues.append({"start": off, "end": off + (c["end"] - c["start"]), "text": c["text"]})
        timing.append({"i": [l["i"] for l in g["lines"]], "section": g["lines"][-1]["section"],
                       "text": " ".join(l["text"] for l in g["lines"]),
                       "start": round(cursor, 3), "end": round(cursor + seg_sec, 3),
                       "silence_after": round(g["lines"][-1]["silence_after"] * a.scale, 3)})
        cursor += seg_sec
        sil = int(round(g["lines"][-1]["silence_after"] * a.scale * RATE)) * FRAME
        chunks.append(b"\x00" * sil)
        cursor += sil / FRAME / RATE

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
        "speech_seconds": round(total_in, 3), "silence_seconds": round(sil_total, 3),
        "total_seconds": round(total_out, 3), "narration_end": round(total_out, 3),
        "sentences": timing}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"✓ {wav}  발화 {total_in/60:.1f}분 + 무음 {sil_total/60:.1f}분 = 총 {total_out/60:.1f}분 ({fmt_ts(total_out)})")
    print(f"✓ {out/'audio.mp3'}  (확인용 192k)")
    print(f"✓ {out/'subtitle.srt'}  {len(new_cues)}큐 시프트")
    print(f"✓ {out/'timing.json'}")


if __name__ == "__main__":
    main()
