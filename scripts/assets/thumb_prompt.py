#!/usr/bin/env python3
"""썸네일 이미지 프롬프트 빌더 (수면 명상 채널).

문구는 사람이 나중에 얹는다 — 이 프롬프트는 **글자 없는 이미지**만 만든다.
`_style.txt`(그림체) + 시대 앵커 + scenes.json 의 scene + 한국 앵커 + `_frame.txt`(구도·여백·금지)
를 순서대로 이어 붙여 완성 프롬프트 파일을 만든다.

사용법:
    python scripts/assets/thumb_prompt.py --all
    python scripts/assets/thumb_prompt.py --id 01_rainy_temple
    python scripts/assets/thumb_prompt.py --id 01_rainy_temple --show   # 파일로 안 쓰고 화면에만

출력: docs/thumbnail-prompts/_build/{id}.txt  (git 제외 — 언제든 다시 만든다)
이어서:
    python scripts/image/generate_image.py docs/thumbnail-prompts/_build/{id}.txt out.png
"""

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "docs" / "thumbnail-prompts"
BUILD = SRC / "_build"


def load():
    data = json.loads((SRC / "scenes.json").read_text(encoding="utf-8"))
    style = (SRC / "_style.txt").read_text(encoding="utf-8").strip()
    frame = (SRC / "_frame.txt").read_text(encoding="utf-8").strip()
    return data, style, frame


def compose(scene, data, style, frame):
    era = data["_eras"].get(scene["era"])
    if era is None:
        raise SystemExit(f"알 수 없는 era: {scene['era']!r} (scenes.json _eras 확인)")
    return "\n".join([
        style,
        f"Scene: {scene['scene'].strip()}",
        era,
        data["_anchor_korea"],
        frame,
    ])


def main():
    ap = argparse.ArgumentParser(description="썸네일 프롬프트 빌더")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true", help="12편 전부 빌드")
    g.add_argument("--id", help="scenes.json 의 id 하나만 빌드")
    ap.add_argument("--show", action="store_true", help="파일로 쓰지 않고 화면에만 출력")
    args = ap.parse_args()

    data, style, frame = load()
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
            print(f"===== {s['id']}  ({s['ko']}) =====")
            print(text)
            print()
            continue
        BUILD.mkdir(parents=True, exist_ok=True)
        out = BUILD / f"{s['id']}.txt"
        out.write_text(text, encoding="utf-8")
        print(f"{out.relative_to(ROOT)}  ← {s['ko']}")

    if not args.show:
        print()
        print("다음:  python scripts/image/generate_image.py "
              f"{(BUILD / '<id>.txt').relative_to(ROOT)} <출력.png>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
