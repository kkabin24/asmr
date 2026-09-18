#!/usr/bin/env python3
"""썸네일 배치 생성 — 한 장씩, 긴 텀을 두고 (flow 계정 보호).

SKILL+ §4「flow 어뷰징 방지」를 따른다:
  - 단일 레인·직렬(동시성 1) — 동시 발사 가능성 자체를 0으로
  - 장당 긴 인위적 텀(기본 180초) — §4-1 실측에서 동시성 3 + 스태거 6초로도
    297씬 중 65씬이 UNUSUAL_ACTIVITY에 걸렸다. 코드 기본값(~18초)은 이 배치엔 과하다.
  - 내장 스로틀도 §4 권장 보수치로 올려 이중 안전(FLOW_STAGGER_SEC/FLOW_LANE_COOLDOWN_SEC)

사용법:
    python scripts/image/thumb_batch.py --channel sleep [--interval 180] [--port 3850]
    python scripts/image/thumb_batch.py --channel sleep --only 01_hotel_warm,02_apartment_rain

프롬프트는 channels/{채널}/prompts/_build/ (thumb_prompt.py 로 먼저 빌드),
출력은 channels/{채널}/projects/_images/ (git 제외).

이미 있는 png 는 건너뛴다(--force 로 무시). 진행 상황은 stdout 에 한 줄씩.

★UNUSUAL_ACTIVITY 가 뜨면 **즉시 전체 배치를 중단한다** (2026-09-06 사용자 지시).
  텀을 늘려 계속하지 않는다 — 어뷰징 플래그가 뜬 계정에 계속 쏘는 것은
  §4 가 말하는 '예방'의 정반대이고 계정을 태운다. 중단 후 사람이 판단한다.
"""

import argparse
import os
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
GEN = ROOT / "scripts" / "image" / "generate_image.py"


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--channel", default="sleep", help="channels/ 아래 채널 id")
    ap.add_argument("--out-dir", default=None, help="기본 channels/{채널}/projects/_images")
    ap.add_argument("--interval", type=float, default=180.0, help="장 사이 텀(초). 기본 180")
    ap.add_argument("--port", default=None, help="flow 레인 포트(단일). 기본은 채널 settings.json image.flow.ports[0]")
    ap.add_argument("--only", default="", help="id 목록(쉼표). 미지정 시 _build 전부")
    ap.add_argument("--force", action="store_true", help="이미 있는 png 도 다시 생성")
    args = ap.parse_args()

    BUILD = ROOT / "channels" / args.channel / "prompts" / "_build"
    prompts = sorted(BUILD.glob("*.txt"))
    if args.only:
        want = {x.strip() for x in args.only.split(",") if x.strip()}
        prompts = [p for p in prompts if p.stem in want]
    if not prompts:
        log(f"빌드된 프롬프트가 없다 — 먼저 scripts/assets/thumb_prompt.py --channel {args.channel} --all")
        return 1

    if args.out_dir:
        out_dir = pathlib.Path(args.out_dir) if os.path.isabs(args.out_dir) else ROOT / args.out_dir
    else:
        out_dir = ROOT / "channels" / args.channel / "projects" / "_images"
    out_dir.mkdir(parents=True, exist_ok=True)

    port = args.port
    if not port:
        try:
            import json
            cfg = json.loads((ROOT / "channels" / args.channel / "config" / "settings.json").read_text(encoding="utf-8"))
            port = str(((cfg.get("image") or {}).get("flow") or {}).get("ports", [3847])[0])
        except Exception:
            port = "3847"

    env = dict(os.environ)
    env["FLOW_PORTS"] = port
    env.setdefault("FLOW_STAGGER_SEC", "10")        # §4 권장 보수치
    env.setdefault("FLOW_LANE_COOLDOWN_SEC", "20")

    interval = args.interval
    todo = [p for p in prompts if args.force or not (out_dir / f"{p.stem}.png").exists()]
    skipped = len(prompts) - len(todo)
    log(f"대상 {len(todo)}장 (완성분 건너뜀 {skipped}) · 레인 {port} · 텀 {interval:.0f}초 · 직렬")

    ok = fail = 0
    for i, p in enumerate(todo, 1):
        out = out_dir / f"{p.stem}.png"
        log(f"({i}/{len(todo)}) {p.stem} 생성 시작")
        r = subprocess.run([sys.executable, str(GEN), "--engine", "flow", str(p), str(out)],
                           env=env, capture_output=True, text=True, timeout=900)
        tail = (r.stdout + r.stderr).strip().splitlines()
        tail = tail[-1] if tail else ""
        if r.returncode == 0 and out.exists():
            ok += 1
            log(f"({i}/{len(todo)}) ✓ {out.name}  {out.stat().st_size:,} bytes")
        else:
            fail += 1
            log(f"({i}/{len(todo)}) ✗ 실패 — {tail}")
            if "UNUSUAL" in (r.stdout + r.stderr).upper():
                # ★즉시 중단 (2026-09-06 사용자 지시). 텀을 늘려 계속하지 않는다.
                log("  ★★UNUSUAL_ACTIVITY 감지 — 배치를 즉시 중단한다 (SKILL+ §4 · 계정 보호)")
                log(f"  성공 {ok} / 실패 {fail} / 남은 {len(todo) - i}장은 생성하지 않았다")
                log("  이 계정을 충분히 쉬게 둔 뒤, 사람이 판단해서 다시 시작할 것.")
                log("  (완성분은 건너뛰므로 같은 명령을 다시 돌리면 이어서 진행된다)")
                return 2

        if i < len(todo):
            log(f"  다음 장까지 {interval:.0f}초 대기")
            time.sleep(interval)

    log(f"완료 — 성공 {ok} / 실패 {fail} → {out_dir}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
