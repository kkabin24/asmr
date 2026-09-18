"""수면명상 템플릿(channels/sleep/templates/*.md) → Vrew 낭독용 폴더 생성.

야담 채널의 ingest_vrew.py --export-script 와 같은 자리({P}/vrew/)에 만들되,
명상 대본은 `[정적 N]` 무음 마커가 콘텐츠의 절반이라 처리가 다르다:
  - Vrew는 마커를 그대로 읽어 버리므로 vrew_script.txt 에서는 **제거**한다.
  - 대신 문장별 "뒤에 올 무음 길이"를 silence_cues.json 에 보존한다.
    (낭독 후 SRT 기준으로 무음을 다시 끼워 넣는 후처리의 근거)

Usage:
    python3 scripts/tts/export_meditation_vrew.py channels/sleep/templates/bodyscan_v1.md channels/sleep/projects/bodyscan_01
"""
import argparse
import json
import pathlib
import re

SECTION_RE = re.compile(r"^##\s+(?P<title>.+?)(?:\s+\((?P<ts>\d+:\d\d)\))?\s*$")
SILENCE_RE = re.compile(r"^\[정적\s+(\d+)\]$")
STOP_HEADINGS = ("## 편집 노트",)


def parse_template(path: pathlib.Path):
    """→ (lines, meta). lines = [{i, section, text, silence_after}]"""
    lines, section, title = [], None, path.stem
    for raw in path.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if not s:
            continue
        if s.startswith("# "):
            title = s[2:].strip()
            continue
        if any(s.startswith(h) for h in STOP_HEADINGS):
            break
        m = SECTION_RE.match(s)
        if m:
            section = m.group("title")
            continue
        m = SILENCE_RE.match(s)
        if m:
            if lines:
                lines[-1]["silence_after"] += int(m.group(1))
            continue
        if s.startswith((">", "---", "*(", "#")):
            continue
        lines.append({"i": len(lines) + 1, "section": section, "text": s, "silence_after": 0})
    return lines, title


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("template")
    ap.add_argument("project_dir")
    a = ap.parse_args()

    tpl = pathlib.Path(a.template)
    vrew = pathlib.Path(a.project_dir) / "vrew"
    vrew.mkdir(parents=True, exist_ok=True)

    lines, title = parse_template(tpl)
    spoken = "\n".join(l["text"] for l in lines) + "\n"
    (vrew / "vrew_script.txt").write_text(spoken, encoding="utf-8")

    chars = len(re.sub(r"\s", "", spoken))
    silence = sum(l["silence_after"] for l in lines)
    cues = {
        "template": str(tpl).replace("\\", "/"),
        "title": title,
        "line_count": len(lines),
        "spoken_chars_nospace": chars,
        "silence_total_sec": silence,
        "_comment": "silence_after = 이 문장 낭독이 끝난 뒤 넣을 무음(초). 마지막 문장의 값은 나레이션 종료→백색소음 페이드인 전 여유.",
        "lines": lines,
    }
    (vrew / "silence_cues.json").write_text(json.dumps(cues, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"✓ {vrew / 'vrew_script.txt'}  ({len(lines)}문장, 공백 제외 {chars:,}자 — Vrew 한도 1만 자 이내, 한 프로젝트로 낭독)")
    print(f"✓ {vrew / 'silence_cues.json'}  (무음 합계 {silence}초 = {silence // 60}분 {silence % 60}초)")


if __name__ == "__main__":
    main()
