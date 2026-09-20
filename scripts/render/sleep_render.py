#!/usr/bin/env python3
"""수면 명상 영상 렌더 — 도입 이미지 1장 + 나레이션 + 백색소음 → 2시간 mp4.

벤치마크(에일린 K_LEbhHLCbk) 실측을 그대로 재현한다:
  화면: 이미지를 어둡게 시작(평균 밝기 ~15%) → 잠깐 유지 → 3분에 걸쳐 검정으로 페이드 → 끝까지 검정
  소리: 나레이션(10~16분) → 끝나기 직전부터 백색소음 페이드인 → 2시간까지 루프

사용법:
    python scripts/render/sleep_render.py --channel sleep \
        --image channels/sleep/projects/01/opening.png \
        --narration channels/sleep/projects/01/narration.mp3 \
        --noise channels/sleep/assets/noise/rain_soft.mp3 \
        --out channels/sleep/projects/01/output/01_bodyscan_2h.mp4

    --noise 를 생략하면 channels/{채널}/assets/noise/ 의 첫 음원을 쓴다.
    --total / --fade 등 수치는 channels/{채널}/config/settings.json video.* 가 기본값.
    --thumb-out 을 주면 썸네일용 1280x720 JPG 도 같이 낸다(원본 밝기, 글자 없음 — 문구는 사람이).
    --bgm 을 주면 나레이션 밑에 음악을 깐다(0초부터 루프). --bgm-tail 로 나레이션 뒤 얼마나 끌지(-1=끝까지, 벤치 2020 방식).

검정 화면 2시간은 x264 가 거의 0 비트로 압축하므로 파일이 크지 않다.
"""

import argparse
import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
AUDIO_EXT = {".mp3", ".wav", ".m4a", ".flac", ".ogg", ".aac"}


def sh(cmd, **kw):
    print("$", " ".join(str(c) for c in cmd), flush=True)
    return subprocess.run([str(c) for c in cmd], check=True, **kw)


def probe_duration(path: pathlib.Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", str(path)], capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def leading_silence(path: pathlib.Path, thresh_db: float = -50.0) -> float:
    """파일 맨 앞 무음 길이(초). BGM 앞 여백을 잘라 0초부터 바로 들리게 하는 데 쓴다."""
    r = subprocess.run(["ffmpeg", "-v", "info", "-t", "10", "-i", str(path),
                        "-af", f"silencedetect=noise={thresh_db}dB:d=0.2", "-f", "null", "-"],
                       capture_output=True, text=True)
    import re
    m = re.search(r"silence_start: (-?[\d.]+).*?silence_end: ([\d.]+)", r.stderr, re.S)
    return float(m.group(2)) if m and float(m.group(1)) <= 0.05 else 0.0


def load_settings(channel: str) -> dict:
    p = ROOT / "channels" / channel / "config" / "settings.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def pick_noise(channel: str) -> pathlib.Path:
    d = ROOT / "channels" / channel / "assets" / "noise"
    cands = sorted(p for p in d.iterdir() if p.suffix.lower() in AUDIO_EXT) if d.exists() else []
    if not cands:
        raise SystemExit(f"백색소음 음원이 없다: {d}  (README.md 참고해 음원을 올려주세요)")
    return cands[0]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--channel", default="sleep")
    ap.add_argument("--image", required=True, type=pathlib.Path)
    ap.add_argument("--narration", required=True, type=pathlib.Path)
    ap.add_argument("--noise", type=pathlib.Path, default=None)
    ap.add_argument("--out", required=True, type=pathlib.Path)
    ap.add_argument("--thumb-out", type=pathlib.Path, default=None)
    ap.add_argument("--total", type=float, default=None, help="완성본 길이(초). 기본 settings video.total_seconds")
    ap.add_argument("--hold", type=float, default=None, help="이미지 유지(초) — 페이드 시작 전")
    ap.add_argument("--fade", type=float, default=None, help="검정으로 페이드(초)")
    ap.add_argument("--brightness", type=float, default=None, help="도입 이미지 밝기 배율(0~1)")
    ap.add_argument("--noise-gain", type=float, default=None, help="소음 dB (나레이션 대비)")
    ap.add_argument("--noise-fade", type=float, default=None, help="소음 페이드인(초)")
    ap.add_argument("--bgm", type=pathlib.Path, default=None, help="나레이션 밑에 까는 음악 (0초부터 루프)")
    ap.add_argument("--bgm-gain", type=float, default=None, help="BGM dB (나레이션 대비). 기본 settings video.bgm_gain_db (-14)")
    ap.add_argument("--bgm-tail", type=float, default=None,
                    help="나레이션 끝난 뒤 BGM 을 몇 초 더 끌다 페이드아웃할지. -1 이면 끝까지 루프(벤치 2020 방식). 기본 settings video.bgm_tail_seconds (60)")
    ap.add_argument("--bgm-fade", type=float, default=None, help="BGM 페이드아웃(초). 기본 20")
    ap.add_argument("--bgm-offset", type=float, default=None, help="BGM 앞을 몇 초 건너뛸지. 기본: 파일 앞 무음을 자동 감지해 잘라냄")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise SystemExit("ffmpeg/ffprobe 가 PATH 에 없다")

    st = load_settings(args.channel)
    v = st.get("video") or {}
    r = st.get("render") or {}
    total = args.total or float(v.get("total_seconds", 7200))
    hold = args.hold if args.hold is not None else float(v.get("opening_image_hold_seconds", 30))
    fade = args.fade if args.fade is not None else float(v.get("opening_fade_seconds", 180))
    bright = args.brightness if args.brightness is not None else float(v.get("opening_brightness", 0.55))
    n_gain = args.noise_gain if args.noise_gain is not None else float(v.get("noise_gain_db", -6))
    n_fade = args.noise_fade if args.noise_fade is not None else float(v.get("noise_fade_in_seconds", 20))
    fps = int(r.get("fps", 30)); W = int(r.get("width", 1920)); H = int(r.get("height", 1080))
    lufs = float(r.get("loudness_lufs", -18))

    b_gain = args.bgm_gain if args.bgm_gain is not None else float(v.get("bgm_gain_db", -14))
    b_tail = args.bgm_tail if args.bgm_tail is not None else float(v.get("bgm_tail_seconds", 60))
    b_fade = args.bgm_fade if args.bgm_fade is not None else float(v.get("bgm_fade_out_seconds", 20))

    noise = args.noise or pick_noise(args.channel)
    for p in (args.image, args.narration, noise, *( [args.bgm] if args.bgm else [] )):
        if not p.exists():
            raise SystemExit(f"파일 없음: {p}")

    narr_len = probe_duration(args.narration)
    noise_start = max(0.0, narr_len - n_fade)     # 나레이션 끝나기 n_fade 초 전부터 소음 페이드인
    if narr_len + 5 > total:
        raise SystemExit(f"나레이션({narr_len:.0f}s)이 완성본 길이({total:.0f}s)보다 길다")

    print(f"나레이션 {narr_len/60:.1f}분 · 소음 {noise.name} 은 {noise_start/60:.1f}분부터 {n_fade:.0f}초 페이드인 · "
          f"화면 {hold:.0f}초 유지 후 {fade:.0f}초 페이드 → 검정 · 완성 {total/60:.0f}분")
    if args.bgm:
        bgm_end = total if b_tail < 0 else min(total, narr_len + b_tail)
        b_off = args.bgm_offset if args.bgm_offset is not None else leading_silence(args.bgm)
        print(f"BGM {args.bgm.name} {b_gain:+.0f}dB · 앞 {b_off:.2f}초 건너뛰고 0초부터 루프, "
              f"{bgm_end/60:.1f}분에 끝({b_fade:.0f}초 페이드아웃)" + (" — 끝까지" if b_tail < 0 else ""))

    # ── 렌더 전략 ────────────────────────────────────────────
    # 검정 화면이 2시간의 97% 다. 이미지를 21만 프레임 동안 매번 디코드·스케일하면 2.5x 밖에 안 나와
    # 2시간에 48분이 걸린다. 그래서 세 조각으로 나눈다:
    #   seg1 = 이미지 유지+페이드 (몇천 프레임)   seg2 = lavfi 검정 (디코드 없음, 매우 빠름)
    #   → 스트림 복사로 이어붙이고, 소리는 따로 만들어 마지막에 mux.
    # ★밝기는 곱셈(colorchannelmixer)으로 낮춘다. eq=brightness 는 덧셈이라 리미티드 레인지의
    #   검정(Y=16)을 그 아래로 밀어, 이후 fade 가 "검정을 향해" 섞이면서 밝기가 올라가는 역전이 생겼다(실측).
    work = args.out.parent / f".{args.out.stem}_work"
    work.mkdir(parents=True, exist_ok=True)
    seg1_len = hold + fade + 1.0
    seg1 = work / "seg1.mp4"; seg2 = work / "seg2.mp4"; vcat = work / "video.mp4"; aud = work / "audio.m4a"

    vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
          f"format=rgb24,colorchannelmixer=rr={bright}:gg={bright}:bb={bright},"
          f"fade=t=out:st={hold}:d={fade}:color=black,format=yuv420p,fps={fps}")
    cmd_seg1 = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-stats",
                "-loop", "1", "-framerate", str(fps), "-i", args.image,
                "-vf", vf, "-t", str(seg1_len), "-an",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-tune", "stillimage",
                "-pix_fmt", "yuv420p", "-r", str(fps), seg1]
    cmd_seg2 = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-stats",
                "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={fps}",
                "-t", str(total - seg1_len), "-an",
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "30",
                "-pix_fmt", "yuv420p", "-r", str(fps), seg2]
    concat_list = work / "concat.txt"
    concat_list.write_text("file '%s'\nfile '%s'\n" % (seg1.name, seg2.name), encoding="utf-8")
    cmd_cat = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
               "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy", vcat]

    # 소리: [0]=나레이션 그대로, [1]=소음 루프 → 페이드인 → 게인 → 시작 지연, [2]=BGM(선택) → 합침 → 길이 → 끝 페이드 → 라우드니스
    af = (f"[0:a]aresample=48000,aformat=channel_layouts=stereo[narr];"
          f"[1:a]aresample=48000,aformat=channel_layouts=stereo,"
          f"afade=t=in:st=0:d={n_fade},volume={n_gain}dB,"
          f"adelay={int(noise_start*1000)}|{int(noise_start*1000)}[noise];"
          )
    inputs = ["-i", args.narration, "-stream_loop", "-1", "-i", noise]
    mix_in = "[narr][noise]"
    n_mix = 2
    if args.bgm:                                   # [2]=BGM 루프 → 게인 → bgm_end 에서 페이드아웃 → 자름
        inputs += ["-stream_loop", "-1", "-i", args.bgm]
        af += (f"[2:a]atrim=start={b_off},asetpts=PTS-STARTPTS,"
               f"aresample=48000,aformat=channel_layouts=stereo,volume={b_gain}dB,"
               f"afade=t=out:st={max(0.0, bgm_end - b_fade)}:d={b_fade},atrim=0:{bgm_end}[bgm];")
        mix_in += "[bgm]"
        n_mix = 3
    af += (f"{mix_in}amix=inputs={n_mix}:duration=longest:normalize=0,"
           f"atrim=0:{total},afade=t=out:st={total-15}:d=15,"
           f"loudnorm=I={lufs}:TP=-1.5:LRA=11,aresample=48000[a]")
    cmd_aud = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-stats",
               *inputs, "-filter_complex", af, "-map", "[a]", "-t", str(total),
               "-c:a", "aac", "-b:a", "160k", aud]
    cmd_mux = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
               "-i", vcat, "-i", aud, "-map", "0:v", "-map", "1:a",
               "-c", "copy", "-shortest", "-movflags", "+faststart", args.out]
    steps = [("1/5 도입 이미지 세그먼트", cmd_seg1), ("2/5 검정 세그먼트", cmd_seg2),
             ("3/5 영상 이어붙이기", cmd_cat), ("4/5 소리 합성", cmd_aud), ("5/5 mux", cmd_mux)]

    if args.thumb_out:
        tcmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", args.image,
                "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720",
                "-q:v", "2", args.thumb_out]
    if args.dry_run:
        for name, c in steps:
            print(f"[{name}]")
            print("  " + " ".join(str(x) for x in c))
        return 0

    args.out.parent.mkdir(parents=True, exist_ok=True)
    for name, c in steps:
        print(f"── {name}", flush=True)
        sh(c)
    shutil.rmtree(work, ignore_errors=True)
    if args.thumb_out:
        args.thumb_out.parent.mkdir(parents=True, exist_ok=True)
        sh(tcmd)
        print(f"썸네일 → {args.thumb_out}")
    print(f"완료 → {args.out}  ({args.out.stat().st_size/1e6:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
