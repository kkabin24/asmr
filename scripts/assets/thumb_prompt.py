#!/usr/bin/env python3
"""도입 이미지(=썸네일) 프롬프트 빌더.

문구는 사람이 나중에 얹는다 — 이 프롬프트는 **글자 없는 이미지**만 만든다.
`channels/{채널}/prompts/` 의
  _style.txt(화풍) + scenes.json 의 scene + _anchor + _frame.txt(구도·인물·금지)
를 순서대로 이어 붙여 완성 프롬프트를 만든다.

★2026-09-18 갈아엎음: 종전 docs/thumbnail-prompts(조선 회화)는 폐기.
  sleep 채널은 실사 사진 톤 — 조선·웹툰·캐릭터 앵커가 프롬프트 어디에도 들어가지 않는다.

사용법:
    python scripts/assets/thumb_prompt.py --channel sleep --all
    python scripts/assets/thumb_prompt.py --channel sleep --id 01_hotel_warm
    python scripts/assets/thumb_prompt.py --channel sleep --id 01_hotel_warm --show

출력: channels/{채널}/prompts/_build/{id}.txt  (git 제외 — 언제든 다시 만든다)
      ★_build 가 채널 폴더 안에 있어서 generate_image.py 가 위로 올라가며
        channels/{채널}/config/settings.json(레인 포트 등)을 찾는다.
이어서:
    python scripts/image/generate_image.py channels/{채널}/prompts/_build/{id}.txt out.png
"""

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]


def paths(channel: str):
    src = ROOT / "channels" / channel / "prompts"
    if not (src / "scenes.json").exists():
        raise SystemExit(f"프롬프트 소스가 없다: {src / 'scenes.json'}")
    return src, src / "_build"


def load(src: pathlib.Path):
    data = json.loads((src / "scenes.json").read_text(encoding="utf-8"))
    style = (src / "_style.txt").read_text(encoding="utf-8").strip()
    frame = (src / "_frame.txt").read_text(encoding="utf-8").strip()
    return data, style, frame


def compose(scene, data, style, frame):
    parts = [style, f"Scene: {scene['scene'].strip()}"]
    if data.get("_anchor"):
        parts.append(data["_anchor"])
    parts.append(frame)
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser(description="도입 이미지 프롬프트 빌더")
    ap.add_argument("--channel", default="sleep", help="channels/ 아래 채널 id (기본 sleep)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true", help="scenes.json 전부 빌드")
    g.add_argument("--id", help="scenes.json 의 id 하나만 빌드")
    ap.add_argument("--show", action="store_true", help="파일로 쓰지 않고 화면에만 출력")
    args = ap.parse_args()

    src, build = paths(args.channel)
    data, style, frame = load(src)
    by_id = {s["id"]: s for s in data["scenes"]}

    if args.id:
        if args.id not in by_id:
            print(f"없는 id: {args.id}", file=sys.stderr)
            print("가능한 id: " + ", ".join(by_id), file=sys.stderr)
            return 1
        targets = [by_id[args.id]]
    else:
        targets = data["scenes"]

    for s in targets:
        text = compose(s, data, style, frame)
        if args.show:
            print(f"===== {s['id']}  ({s['ko']}) =====\n{text}\n")
            continue
        build.mkdir(parents=True, exist_ok=True)
        out = build / f"{s['id']}.txt"
        out.write_text(text, encoding="utf-8")
        print(f"{out.relative_to(ROOT)}  ← {s['ko']}")

    if not args.show:
        print(f"\n다음:  python scripts/image/generate_image.py "
              f"{(build / '<id>.txt').relative_to(ROOT)} <출력.png>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
