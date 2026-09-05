---
name: story-pd
description: 썰/야담 내러티브 유튜브 PD. "야담 영상 만들어줘" 한마디로 대본→asset(인물·배경)→스토리보드→씬이미지→TTS→렌더→업로드를 상태 기반으로 오케스트레이션. 정보성(마스코트)과 달리 주연·조연 캐릭터와 배경 asset이 등장하는 파이프라인. 야담/썰/스토리 영상·대본·캐릭터·스토리보드 요청 시 사용.
---

# story-pd — 썰/야담 내러티브 PD

## 역할 원칙
1. **상태 기반 진행** — 파일 존재 여부로 현재 단계를 감지하고 다음 단계를 자동 결정.
2. **asset 검수 게이트 — 사용자 컨펌 필수** (2026-07-19 사용자 지시로 재도입) — ASSET_GEN(턴어라운드·배경) 후 **반드시 멈춘다**. contact sheet를 만들어 **`open`으로 화면에 띄우고**(사용자가 파일을 직접 찾을 필요 없게), 캐릭터 일관성(연령/체형/문화/앵커)을 눈으로 확인하고 **사용자가 명시적으로 OK 할 때까지 STORYBOARD 이후로 절대 진행하지 않는다**. 드리프트를 지적하면 해당 인물만 lock/anchorProp 수정 후 `--force` 재생성 → 다시 띄워 재확인. **사람 게이트는 asset 검수 + TTS(Vrew 낭독) + CapCut 마무리 편집 셋.**
3. **대화 밀도는 단계별로 다르다** — **SCRIPT(대본)는 최대 대화가 목적**: 컨셉·아웃라인·장 초안을 사용자와 함께 다듬어 새 이야기를 공동 창작한다. 각 서브 단계 산출물(concept/outline/장 배치)은 반드시 보여주고 피드백을 받은 뒤 다음으로. **SCRIPT 이후 제작 단계(asset~upload)는 최소 대화** — auto 단계는 결과만 보고, ask 단계(asset검수, thumbnail)에서만 대화.
4. **에이전트 위임** — 장편 집필(DRAFT 배치)·분석은 에이전트에 위임. PD는 오케스트레이션.

## 프로젝트 구조
`{P}` = `channels/{채널}/projects/{프로젝트}`
```
{P}/_script/                  # {S}: concept.md, outline.md(장 설계+복선 장부), chapters/, bible.md
{P}/_refs/NNN/                # CONCEPT 원전 수집물+분석: meta.md(조회수·댓글TOP10)+transcript.txt+thumbnail+analysis.md(분석 보고서)
{P}/script.txt  meta.txt
{P}/characters.json  locations.json
{P}/assets/characters/<id>[_<variant>]_turnaround.png
{P}/assets/locations/<id>_sheet.png
{P}/storyboard.json           # 소스(사람이 authored, status 없음)
{P}/storyboard.built.json     # build.py 출력(image/status 포함)
{P}/scenes/scene_NN.png
{P}/vrew/                     # vrew 모드: vrew_script.txt + 사용자가 넣는 음성/SRT
{P}/_video/                   # {V}: TTS·자막·렌더용 storyboard 등 중간물
{P}/output/capcut_draft.json  # RENDER 마커 (capcut_export 성공 기록)
{P}/output/*.mp4              # 사람이 CapCut에서 마무리 편집 후 내보낸 최종본 (외장 드라이브일 수도)
  └ *_intro.mp4 + intro_attached.json   # INTRO 마커 — 업로드는 _intro.mp4 쪽
```
**★옴니버스 폴더 규격 (v3.0 — 01~04편 실사용, 2026-08-16 확정)**
편(영상) 폴더가 한 겹 더 끼고, **대본·TTS는 영상 레벨 / asset·씬은 편별 서브프로젝트**로 갈린다.
```
projects/04편/                      # {P} = 영상. 대본·TTS·병합물이 여기 산다
  _script/concept.md outline.md bible.md chapters/01~06.md
  script.txt  meta.txt
  vrew/vrew_script_part01a.txt …    # 편 번호 + a·b (1만 자 넘으면 분할, 2026-08-20)
  _video/script_sentences.json      # init_sentences.py 산출 — storyboard sentences 기준
  260815_2020_무명한필/             # 편별 서브프로젝트 = asset·씬 단위
    characters.json  locations.json  assets/  scenes/  storyboard.json
```
- **챕터를 편별 서브폴더에 두지 않는다** — `ingest_vrew.py {P} --chapters 1-6`이 영상 레벨 `_script/chapters/`를 읽고, 파트가 곧 편이 된다. 편별로 흩으면 export를 여섯 번 돌려야 하고 파트 번호가 어긋난다.
- `turnaround.py`·`background.py`·`build.py`는 **편별 서브프로젝트 경로**를 받는다(`{P}/{편}`). config는 `find_channel_config`가 위로 올라가며 찾으므로 깊이가 한 겹 늘어도 된다.

채널 그림체/문화앵커: `channels/{채널}/config/style.json` (모든 프롬프트에 자동 append).
채널 공용 리서치: `channels/{채널}/config/watchlist.json`(추적 채널) → `channels/{채널}/research/`(scan_*.md 소재 리포트, topic_log.json 소재 대장, refs/ 딥 벤치마킹 수집, proposal_*.md 공식 개정 제안).

## 초기화
- **채널**: `channels/` 스캔(`_`로 시작 제외). 1개면 자동, 여러 개면 선택. `config/settings.json`+`profile.md`+`workflow.json` 로드.
- **프로젝트**: 기존 관련 요청→선택. 새 프로젝트는 **생성 시각으로 명명** — `YYMMDD_HHMM` (예: `260711_1430`). 컨셉이 없는 시점이라 키워드 명명이 불가능하기 때문. CONCEPT ③ 확정 때 뒤에 언더바+짧은 제목을 붙여 rename (예: `260711_1430_머슴임금`).
- **모드**: `config/workflow.json`의 `mode`를 따른다(묻지 않음). `{P}/workflow.json`이 있으면 우선.

## 상태 감지 (위→아래 첫 매칭, `{V}` = `{P}/_video`)
```
{P}/ 없음 or script.txt 없음                       → SCRIPT (레지스트리는 OUTLINE에서 생성 — "레지스트리 생애주기")
assets/ 비었거나 turnaround/sheet 파일 누락          → ASSET_GEN ★검수 게이트 (진입 시 레지스트리 시각 필드 완성)
storyboard.json 없음                                → STORYBOARD  (존재 = asset 검수 통과로 간주)
scenes/ 비었거나 storyboard.built.json에 FAIL 존재   → SCENE_IMG
{V}/audio.mp3 또는 {V}/subtitle.srt 없음            → TTS
  └ vrew 모드 세부: {P}/vrew/에 오디오+SRT 있음 → ingest 실행
                    vrew_script.txt만 있음 → 사용자 대기(게이트), 없음 → --export-script
{V}/storyboard.json 없음                            → SCENE_TIMING
{P}/cards 없음 (옴니버스만)                          → CHAPTER_CARDS (편마다 3초 장부, ★1편 앞 포함 — 아래 절)
{V}/veo_hook.json 없음                              → VEO_HOOK (★2026-08-27부터 기본 실행, pjn 무료 — 아래 절)
{P}/output/capcut_draft.json 없음                   → RENDER (CapCut export — 성공 시 마커 자동 기록)
{P}/output/*.mp4 없음                               → 사용자 대기 게이트 (CapCut 마무리 편집 → output/에 mp4 내보내기)
완성본 폴더에 hook_attached.json 없음                → ATTACH_HOOK (도입부를 훅 클립으로 교체 — 훅 안 쓰면 건너뜀)
완성본 폴더에 intro_attached.json 없음               → INTRO (인트로 concat + 챕터 시각 재계산 — 아래 절)
{P}/output/upload_result.json 없음                  → UPLOAD
그 외                                               → DONE
```
**★완성본은 {P}/output/ 밖에 있을 수 있다** — 사용자는 CapCut 내보내기를 외장 드라이브(예: `D:/★Youtube부업/1.야담/★Final/{NN편}/`)에 두기도 한다. `{P}/output/`에 mp4가 없으면 **경로를 물어보고**, 그 폴더를 완성본 폴더로 삼는다(INTRO 마커도 거기 쓴다).
asset 검수 게이트 있음 — ASSET_GEN 완료 후 **사용자 컨펌 대기**. contact sheet를 `open`으로 띄우고, OK 받기 전에는 STORYBOARD로 넘어가지 않는다.
**★병렬 트랙 (2026-07-19)**: TTS(vrew 낭독)는 SCENE_IMG와 독립이다 — 위 감지 순서는 "남은 것" 확인용일 뿐. vrew export는 **script.txt 확정 직후** 실행하고(TTS 절), 낭독 파일이 도착하면 SCENE_IMG 진행 중에도 ingest→split→SCENE_TIMING까지 먼저 처리한다. scenes 완료를 기다리는 건 RENDER뿐(VEO_HOOK도 씬1만 있으면 가능).

## 단계별 절차

### INTRO  ★채널 고정 자산 (1회 제작, 매 편 재사용 — 2026-08-13 신설)

마스코트 **옛뜰이**가 인사하는 **8초 립싱크 클립**을 한 번 만들어 **모든 영상 맨 앞에 붙인다.** 문안·음성·영상이 전부 고정이라 **대본에 인사가 들어가지 않고 Vrew 낭독 대상도 아니다**(script-guide §3).

근거 — 벤치 ①(97만) 인트로 실측: 11초, 마스코트 상반신 + 초저녁 마을 배경, 자막 번인, **화면의 0.26%만 변함**(정확히 입 위치). 인사 고정 댓글이 그 영상 전체 최다 좋아요(252♥)이고, 인사가 없는 ②에는 *"문안인사 한 번 없느냐??"*(6♥) 불만이 달렸다.

**자산** `channels/yadam/assets/intro/`
```
character_yetddeuli.png   # 옛뜰이 원본 아바타 (사용자 제공)
background_night.png      # 한옥 밤 배경 16:9 (사용자 제공)
start_frame.png           # ★Veo 시작 프레임 — 위 둘을 ref로 생성한 16:9 상반신
intro_voice.wav           # ★사용자가 만든 고정 인사 음성
intro_raw.mp4             # Veo 산출물 (자체 오디오 포함)
intro.mp4                 # ★최종 — Veo 영상 + 사용자 음성 + 자막 번인
intro.json                # 길이·문안·생성 파라미터 기록
```

**고정 문안** (확정 2026-08-14 — 원문 `channels/yadam/assets/intro/intro_script.txt`)
> **안녕하세요, 옛뜰이예요. 오늘도 정말 고생 많으셨어요. 이제 저와 스르르 잠드는 이야기, 함께 시작해 볼까요?**

공백 제외 49자 · 녹음본 **10.58초** → Veo 8초 상한을 넘어 **클립 2개(8초+4초)** 로 만든다. 자막은 넣지 않는다(CapCut에서 입힘, 사용자 지시 2026-08-14).

**★인트로 낭독 속도 = 267자/분** (벤치 ① 실측: 인트로 0.88~11.00초 = 10.12초에 45자). **본문(265자/분)과 사실상 같다** — "인트로는 더 느리게 읽는다"는 처음 추정은 틀렸다(한글자만 세고 구두점을 뺀 계산 착오). 문안 길이는 이 값으로 잰다.

**★현행 승인본 (2026-08-29)** — `channels/yadam/assets/intro/intro_ver3_bgm_sub.mp4`
11.27초 · 1920×1080/30fps · 나레이션+BGM · **자막 번인됨** · 화면 전환 0회 · −16.1 LUFS.
> **파일명이 `attach_intro.py`의 `DEFAULT_INTRO` 상수에 박혀 있다** (사용자 지시 2026-08-29). 승인본을 바꾸면 그 상수를 고친다. `intro.json`의 `approved_file`은 `build_intro_retime.py`가 재빌드마다 통째로 덮어써서 날아가므로 기준으로 쓰지 않는다.
> 빌드 내력·파라미터·믹스 계수는 `assets/intro/intro_ver3.json`. 재빌드 3단계: ①`build_intro_retime.py --audio intro_ver3.mp3 --keep-head <첫 마디 끝> --talk-pct 10` ②BGM 믹스(ffmpeg 명령이 json에 있다) ③`burn_intro_subs.py`.
> **★나레이션을 교체하면 srt를 그대로 믿지 말고 먼저 음성을 받아써서 문장을 대조한다.** ver2·ver3 두 번 다 함께 들어온 srt가 옛 대본이었고(시각만 새로 찍힘), 한 번은 그대로 구워져 나갔다. 자막은 굽고 나면 영상에 박힌다.

**옛 자산 (2026-08-15 승인, 현재 미사용)** — `intro_final.mp4` 10.60초 · 자막 없음(CapCut에서 입히던 시절).

**자막 번인 변형본 (2026-08-17)** — `intro_final_sub.mp4` (원본은 그대로 둔다)
```
python3 scripts/render/burn_intro_subs.py --channel yadam      # 재생성
python3 scripts/render/attach_intro.py <완성본.mp4> --intro <...>/intro_final_sub.mp4   # 이 버전으로 붙이기
```
- 스타일은 **01편 완성본 프레임 실측을 이식**했다(눈대중 금지) — 맑은 고딕 **Bold** / 글자높이 107px@1080p / 검은 외곽선 8~9px / 글자 아랫변이 바닥에서 57px. 폰트는 후보 7종을 글자마스크 IoU로 비교해 골랐다(맑은고딕Bold 0.69 > HY견고딕 0.61). **libass의 `Fontsize`는 글자 실제 높이가 아니다** — 실측 환산계수 1.354를 곱해야 본편과 같은 크기가 된다.
- 자막 문안·타이밍은 `인트로_자막.srt`(5큐). **셋째 문장은 손으로 나눴다** — `split_long_cues.py`는 max_chars=13 균형만 보고 `…잠드는 옛 / 이야기,…`로 어절을 갈랐다. 매 편 나오는 시그니처 문장이라 `이제 저와 스르르 / 잠드는 옛 이야기, / 함께 시작해 볼까요?`로 끊었다(경계 시각은 whisper 단어 실측).

**제작 절차 (1회) — ★목소리가 먼저다**
1. **음성** — 사용자가 문안을 낭독해 `인트로.mp3`(+SRT) 저장. 본문 나레이터와 같은 보이스 권장. **길이가 곧 인트로 길이**다.
2. **시작 프레임** — 프로필·배경을 **ref로 붙여** 16:9 상반신 생성(`prompt_start_frame.txt` → `draft_ref_v1.png`).
   ★ref 없이 텍스트만으로 뽑으면 얼굴이 딴사람이 된다(실측). 정면·미디엄 샷, 입이 크게 보이게.
   ```
   python3 scripts/image/generate_image.py channels/yadam/assets/intro/prompt_start_frame.txt        channels/yadam/assets/intro/draft_ref_v1.png        channels/yadam/assets/intro/character_yetddeuli.png        channels/yadam/assets/intro/background_night.png
   ```
3. **Veo 클립** — 시작 프레임으로 8초 i2v 생성(`build_intro.py --stage clip1`). ⚠️유료.
4. **★립싱크 = Veo가 아니라 재편집으로 만든다** — `build_intro_retime.py`가 clip1의 실제 프레임을
   오디오의 말/쉼에 맞춰 재배열한다. **추가 비용 0원.**
   ```
   python3 scripts/render/build_intro_retime.py --channel yadam
   ```

**★왜 이렇게 하나 — 4차까지 간 실측 기록**

| 시도 | 결과 |
|---|---|
| ① Veo 통짜 + 우리 음성 덮기 | 입-오디오 상관 **−0.27**. Veo는 오디오 입력이 없어 **자기 생성 음성에만** 입을 맞춘다. 구조적으로 불가 |
| ② 정지 이미지 + 입 교체(벤치 방식) | 상관 +0.77이지만 7초간 머리가 멈춰 **"입만 뻥끗"** |
| ③ 프레임 단위 Viterbi 재배열 | 상관 +0.77, 그러나 **점프 35회로 머리가 떨림** |
| **④ 구간 단위 조립 (현행)** | **화면 전환 0회**, 프레임 간 최대 차이 1.24(원본 7.17), 쉼 구간 입 정지 |

④의 핵심 규칙 세 가지:
- **도입부는 자르지 않는다**(`--keep-head 2.91`) — "안녕하세요, 옛뜰이예요"는 clip1 원본 통짜.
- **재생 위치를 이어받는다** — 구간마다 소스를 처음으로 되감으면 **같은 장면이 곧바로 반복**돼 어색하다.
- **쉼 = 점프가 아니라 정지**(`--sil-jump` 기본 꺼짐) — 이어 재생하다 **입이 닫히는 프레임에서 멈춘다.**
  사람은 말을 멈추면 화면이 바뀌지 않고 가만히 있는다. 무음 시작은 `--sil-release 0.25`로 늦춰
  말꼬리가 잘리지 않게 한다(안 하면 "말이 끝나기 전에 화면이 바뀌는 느낌").

**함정 (전부 실측)**
- Veo 프롬프트에 **따옴표 대사를 넣으면 깨진 한글 자막을 화면에 구워 넣는다**(저고리 위 "작잔묵"). 대사를 빼고 "말하는 동작"만 지시할 것.
- **1080p는 durationSeconds 4·6을 거부**한다(API 400). 8초만 가능.
- **Lite 모델은 negativePrompt를 거부**한다(API 400) → `--no-negative`.
- Windows+miniconda에서 urllib SSL이 윈도우 인증서 저장소를 읽다 죽는다 → `build_intro.py`의 `use_certifi_ssl()`.
- clip1은 프레임마다 머리가 움직여 **다른 프레임의 입을 붙이면 어긋난다**. 생성 이미지로 입을 만들면 1344폭이라 확대 시 뭉갠다.

**매 편 사용 (INTRO 단계 — RENDER 다음, UPLOAD 직전)** — ⚠️ **CapCut에 넣지 않는다.** CapCut Windows는 타임라인에 동영상 클립을 올리면 크래시한다(SKILL+ §9, 자동 주입·수동 삽입 모두 실측 확인). 사람이 CapCut에서 mp4를 내보낸 **뒤** 붙인다:
```
# 사람이 CapCut에서 완성본 mp4를 내보낸 뒤 (파일 경로 또는 {P} 폴더를 준다)
python3 scripts/render/attach_intro.py "<완성본.mp4>" --project {P} --write-meta
#   → <완성본>_intro.mp4 + intro_attached.json 마커 + meta.txt 챕터 시각 갱신
#   --replace 를 주면 원본을 결과로 교체(원본은 .nointro.mp4 로 보관)
```
- **본편은 재인코딩하지 않는다** — concat 데먹서 + `-c copy`. 2시간·8.6GB를 다시 굽지 않는다.
  (구 문서의 "`-c copy`는 키프레임이 안 맞아 불가"는 **틀렸다** — 2026-08-17 01편에서 스트림 복사로 정상 결합 확인. 실제 함정은 키프레임이 아니라 아래 타임스케일이다.)
- **★함정: 타임스케일 불일치 — SKILL+ §25에 이미 적혀 있는 사고를 인트로 경로에서 그대로 반복했다 (2026-08-17).** CapCut 내보내기는 video `time_base = 1/30`, 인트로는 ffmpeg 기본 `1/15360`. 다르면 concat 복사 시 본편 타임스탬프가 재스케일되지 않아 **2시간 영상의 비디오 스트림이 24초로 뭉개진다**(오디오는 멀쩡해 `format=duration`만 보면 정상으로 보인다 — 실제로 한 번 정상 판정하고 넘어갔다). → `attach_intro.py`가 인트로를 **본편 타임스케일로 다시 muxing**하고, 검증은 **비디오 스트림 duration + nb_frames**까지 본다(§25의 검증 규정 그대로).
- **챕터 시각은 시프트가 아니라 재계산** — `{V}/storyboard.json`의 `is_card` 씬 start(실측) + 인트로 길이. 01편 meta.txt의 기존 시각은 글자 수 추정값이라 실제 카드와 최대 12초 어긋나 있었다(단순 시프트로는 그 오차가 그대로 남는다). 첫 챕터는 **0:00**으로 둔다 — YouTube는 첫 줄이 0:00이 아니면 챕터를 아예 활성화하지 않는다.
- 인트로는 매 편 동일하므로 **한 번 만들면 이후 비용 0**이다.

### SCRIPT  (서브 상태머신, `{S}` = `{P}/_script`)
주력 = **수면 옴니버스 — 독립 단편 2편 × 45분 = 90분 + 아웃트로 30분 = 약 2시간, 대본 약 25,400자(편당 12,700자)** (★2026-09-03 사용자 지시로 3편×45분에서 개정 — playbook v4.1 §1. 속도 284자/분 승계, 씬 111장, Vrew 4파트, 아웃트로 자산 `assets/intro,outro/sleep_noise_30min_quiet.mp3`). 공식(playbook) = `prompts/script-guide.md` — **매 편 벤치마킹하지 않는다**, 공식 현재 버전을 그대로 적용. 단계별로 필요한 프롬프트만 로드(lazy-load):

> **★v3.0 포맷 전환(2026-08-12)** — 아래 SCRIPT 절 전체가 "이야기 6편을 한 영상에 싣는다"는 전제로 다시 쓰였다. `{S}/chapters/01.md`~`06.md`는 **장(章)이 아니라 편(篇)**이고, 편끼리는 연속성이 없다. 콜드 오픈·복선 장부·약속 장면 앵커·후렴은 **폐기**됐다(guide §6 금지 목록). 근거: `channels/yadam/research/proposal_20260812.md`.

| 단계 | 로드 |
|---|---|
| SCAN·CONCEPT·OUTLINE | script-guide.md |
| DRAFT | script-guide.md + script-constraints.md |
| REVIEW | script-constraints.md |
| (딥 벤치마킹 시에만) | benchmark-guide.md (+playbook-history.md) |

서브 상태 감지 (위→아래 첫 매칭):
```
watchlist.json 없거나 handle 미기입          → WATCHLIST ★대화: 추적 채널 @핸들 확정 (채널당 1회)
{P}/ 없음 (새 영상 요청)                     → SCAN: 최신 research/scan_*.md가 없거나 7일 경과면
                                              python3 scripts/research/scan_channels.py --channel {채널}
                                              ★URL 진입: 요청에 레퍼런스 영상 URL이 있으면 SCAN·소재 제안(①)
                                              생략 — 그 영상을 원전으로 바로 ②부터 (아래 CONCEPT 참조)
{S}/concept.md 없음                          → CONCEPT ★대화 3박자 (★v3.0: 소재를 6개 한꺼번에 고른다):
                                              ① 소재 제안 — 스캔 리포트에서 **2편분 소재를 한 세트로** 제안.
                                                편별 근거(조회수/일, 클러스터 규모, guide §8 소재 배율 참고) +
                                                **guide §7 배열 규칙 충족표**(감정축·도입형·해결 주체가 편성 안에서
                                                안 겹치는지) 동봉. topic_log.json 대조(최근 편과 4축 2개 이상 중복 금지)
                                                + **세이프티 스크리닝**(아래 "세이프티 가드레일" — 미성년 수난이
                                                중심 비트인 소재는 성인 각색안 동반, 불가하면 제외)
                                                + **자산 부담 점검**(guide §7 — 편당 턴어라운드 2~4명으로 끝나는 소재인가.
                                                  대가족·집단 갈등 소재는 여기서 거른다)
                                                → 사용자 승인(편 단위로 교체 요청 가능)
                                              ② 원전 분석 — 프로젝트 생성(YYMMDD_HHMM) → **원전은 편마다가 아니라
                                                영상당 1~2편만** 수집(포맷 확인용). 소재별 원전 6편 수집은 하지 않는다.
                                                ★URL 진입 시: 사용자가 준 URL이 곧 원전 — 수집 후 topic_log 중복 대조와
                                                조회수/일 확인. 답습 범위는 **소재·비트까지**, 구조 골격은 playbook,
                                                표면 디테일은 "원전 격리" 그대로(표절 방지 불변):
                                                python3 scripts/research/collect_refs.py --channel {채널} --project {프로젝트} URL
                                                → {P}/_refs/001/의 transcript·댓글 정독(에이전트 위임) →
                                                **분석 보고서를 {P}/_refs/001/analysis.md로 저장**
                                                ※ 소재(무엇을) 분석만 — 구조·기법(어떻게)은 playbook 고정
                                              ③ 확정 — **확정 브리프를 제시**해 사용자가 근거를 보고 결정
                                                (템플릿은 아래 "확정 브리프" 절) → OK 받으면 concept.md(브리프 수록)
                                                + topic_log.json에 **영상 1건 + 편 6건** 기록(편마다 감정축·모티프·
                                                  해결 주체 + `axes` 4축 필드)
                                                + **프로젝트 rename**: `{YYMMDD_HHMM}` → `{YYMMDD_HHMM}_{짧은제목}`
{S}/outline.md 없음                          → OUTLINE ★대화: **편별 브리프 6개** (편마다 guide §2의 9비트를
                                              한 줄씩 + 감정축 + 도입형 A/B + 해결 주체 + 목표 분량 + 등장인물 2~4명)
                                              + 편 배열표(guide §7) ※인사는 고정 인트로라 편성에서 제외
                                              + **characters.json/locations.json 초안 생성** (서사 필드만, 인물마다
                                                `story` 필드로 소속 편 번호 표기 — 아래 "레지스트리 생애주기")
                                              + **원전 diff 체크** (아래 "원전 격리")
                                              ※ 콜드 오픈 문안·복선 장부·클리프행어 유형은 v3.0에서 폐기됐다
{S}/chapters/01.md 없음                      → DRAFT-1 ★1편 선행 (문체 기준 + 속도 기준):
                                              1편만 **5,400자 고정**으로 집필 (인사는 대본에 없다 — INTRO 절 참조)
                                              → validate_script.py {S}/chapters/01.md --target 5150,5650
                                              → 줄거리 요약 보고 → **{S}/chapters/01.md 확정**
{S}/_speed.json 없음 (1편은 있음)            → ★속도 게이트 (사용자 지시 2026-08-13 "음성 들어보고 결정"):
                                              python3 scripts/tts/ingest_vrew.py {P} --chapters 1 --config {CFG}
                                                → {P}/vrew/vrew_script_part01[a-z].txt (편 번호 + 분할 접미사)
                                              ★사용자 대기: Vrew 낭독 → 음성 확인 → narration_01.mp3+srt 저장
                                              → 낭독 길이 측정 → 실측 자/분 = (1편 공백 제외 글자수) ÷ 낭독 분
                                              → ★편당 12,700자 고정(45분 × 284자/분). 1편 선행 낭독 게이트는 05편 이후 쓰지 않는다
                                              → {S}/_speed.json에 {cpm, ep1_min, per_ep_chars, vrew_setting} 기록
                                              ※ 이 게이트 대기 중 1편 ASSET_GEN·STORYBOARD는 먼저 돌려도 된다(편별 독립)
                                              ※ narration_01은 버리지 않는다 — 그게 곧 최종 파트 1이다
{S}/chapters/ 미완 (2편 대비)                → DRAFT: **2편 병렬 위임 가능**(편끼리 연속성 없음 — v2.x 병렬 금지 해제).
                                              집필 에이전트 입력에 **1편 최종본 앞 1,000자를 문체 견본으로** 동봉.
                                              + {S}/bible.md = **편별 인물·이름 대장**(연속성 추적이 아니라 중복 방지 —
                                                편별 인물명·신분·지역·감정축·해결 주체) + 레지스트리 동기화
                                              + validate_script.py --chapter-target {LO},{HI} --cpm {CPM}  ← _speed.json 값
                                              + **편마다 줄거리 요약을 사용자에게 보고 → 피드백 반영 후 다음 편**
{P}/script.txt 없음                          → ★POLISH → REVIEW: 2편 병합(편 사이 빈 줄 2개, 편 제목·번호는 쓰지 않는다) →
                                              validate_script.py --target {확정범위} --cpm {CPM} --style 위반 0 →
                                              ★기계 검사를 chapters 폴더에 돌린다(위반 0까지).
                                              **★2026-08-20부터 자동 수정은 쓰지 않는다 — 전부 검사 전용**:
                                                fix_breath.py              (호흡 26자 초과 — ★쉼표를 넣지 말고 문장을 나눈다)
                                                balance_endings.py         (종결어미 쏠림 — ★난수 교체 중단, 사람이 문맥으로)
                                                pacing_check.py            (설명 문단 연속 — guide §3-4. ★주어 반복은 2026-08-27부터 참고 수치)
                                                check_density.py           (★반복으로 시간을 때웠나 — guide §3-5, 자유 편은 --free NN)
                                                check_sameness.py          (★편끼리 같은 느낌인가 — guide §7-1)
                                                check_clarity.py           (★귀로 한 번 듣고 잡히는가 — guide §5-3)
                                                validate_script.py --style (★문체 밴드 — 하한 4종이 서 있는가, guide §5)
                                              ★시간 표지를 뽑아 오름차순인지 눈으로 확인(guide §5-5)
                                              체크리스트(script-constraints "검수 체크리스트" —
                                              편별 6항목 + 전체 4항목, **등장인물↔레지스트리 전수 대조** 포함)
                                              → script.txt + meta.txt(제작 메모에 확정 속도 기록)
                                              → **2편 전부 vrew export**(편당 a·b 두 파트 = 총 4파트 — ★병렬화, TTS 절):
                                                python3 scripts/tts/ingest_vrew.py {P} --chapters 2-6 --config {CFG}
```
- **★POLISH — REVIEW 직전 '이어 읽기' 패스 (2026-08-18 신설, guide §5-4)**: 대본은 여러 차례 고쳐진다(어휘 평이화 → 분량 증량 → 지루함 제거 → 표현 분화). 각 패스는 옳지만 **합치면 접합부가 거칠어진다.** 병합 전에 처음부터 끝까지 이어 읽으며 세 가지만 손본다 — ①**귀로 한 번 듣고 못 알아들을 문장**을 풀어 쓴다(§5-3: 주어 생략·압축 비유·모호한 지시어·몸으로 가늠 안 되는 수치) ②**끊긴 접합부에 연결 한 줄** ③**빠진 이유 한 줄**(설명 말고 행동으로). **9비트·대사·회수·정형구는 건드리지 않고 분량도 ±3%** — 고치는 게 아니라 잇는 것이다. 편별로 나눠 위임할 수 있다.
  ```
  python3 scripts/script/pacing_check.py {S}/chapters      # 지루함(설명 정체·반복)
  python3 scripts/script/check_density.py {S}/chapters --why   # 같은 일감 덩어리·맨 점프·무전환 구간
  python3 scripts/script/check_sameness.py {S}/chapters    # 편 사이 상투구·어휘 겹침
  ```
- **확정 브리프** (CONCEPT ③ — concept.md를 쓰기 전에 사용자에게 제시하는 결정 패키지. ★v3.0: 영상 1건 + 편 6건을 한 장에):
  1. **제목·썸네일 후보 2~3안** — **용도형 제목**(guide §8). 특정 이야기를 팔지 않는다. 68자 이내·꼬리 키워드 포함.
  2. **★편성표** — 한 표에 **2행**(2편 편성):
     `편 | 가제 | 감정축 | 도입형(A/B) | 주인공(연령·성별·신분) | 결핍 | 사건 촉발 | 해결 주체 | 분량 | 등장인물 수`
     이 표 하나로 guide §7 배열 규칙(감정축 3연속 금지 / 도입형 3연속 금지 / 기이 최대 1편 /
     해결 주체 같은 것 2편까지 / 4축 최소 4종)을 **눈으로 검증**할 수 있어야 한다.
  3. **편별 로그라인 한 줄씩** — 6줄. 각 줄에 "②의 선행이 ⑦⑧에서 어떻게 돌아오는가"가 보이게.
  4. **시장 근거** — 원전 조회수/일 + 6편 소재의 배율(guide §8) + topic_log 최근 편 4축 대조 결과.
  5. **자산 부담 견적** — 편별 턴어라운드 대상 인원 합계 + 배경 시트 수(편당 1장) + **씬 수는 §9-1 계단 밀도로 산출**(★현행 2편×45분이면 **111장** — 1편 66 + 2편 45).
     합계가 이 범위를 넘으면 인물이 많은 편을 교체한다.
  6. **리스크와 대응** — 개연성 구멍, 편 간 유사 지점, **이미지 세이프티 리스크**(미성년 수난 장면 유무 +
     각색·연출 우회 방안 — 아래 "세이프티 가드레일"), **각성 리스크**(guide §6 — 분노·공포로 흐를 소지가 있는 편).
  합의된 편성표가 OUTLINE 편별 브리프의 씨앗이 된다.
  ※ v2.x의 "구조 비교표(원전 vs 우리)"는 폐기 — 골격이 편마다 동일한 9비트(guide §2)라 비교할 대상이 없다.
- **원전 격리 (표절 방지)** — 원전 자료(`_refs/`의 transcript·analysis.md)는 **CONCEPT·OUTLINE까지만** 참조한다. DRAFT 집필 에이전트 입력에 절대 포함 금지 — 구조(비트)는 outline을 통해 물려받되, 표면 디테일은 전부 새로 짓는다. OUTLINE 완료 전 **원전 diff 체크**를 수행해 outline.md에 기록: ① 인물명·지명 ② 핵심 소품(증표·유품) ③ 직접 인용 대사 ④ 장면 연출 디테일이 원전과 겹침 0인지 대조. 모티프 수준(예: "유품 속 증거")의 공유는 허용, 구현물(노리개→노리개)은 금지.
- **★세이프티 가드레일 (이미지 차단 예방 — 스토리 방향을 잡는 시점에 반영)** — Google 이미지 세이프티가 **미성년자 얼굴 클로즈업 + 고통/눈물** 조합을 차단한다(2026-07-19 flow 실측). 대본이 굳은 뒤엔 방향을 못 바꾸므로 상류에서 미리 설계한다:
  - **CONCEPT(주 방어선)**: 미성년자의 학대·수난이 서사의 **중심 비트**인 소재(민며느리 학대, 아이 팔려감 등)는 **수난 당사자의 나이를 성인으로 각색**(15살 며느리 → 갓 스물 며느리)할 수 있을 때만 채택. 각색하면 이야기가 성립하지 않는 소재는 교체 제안. 확정 브리프 6번(리스크)에 판정 결과를 명시.
  - **OUTLINE(레지스트리 초안)**: 고통·학대·죽음을 **당하는** 인물의 age는 성인으로 설정. 아이 캐릭터 자체는 허용 — 단 역할을 정서적 배경(웃는 마을 아이들, 품에 안긴 아기)으로 한정하고 수난의 당사자로 두지 않는다.
  - **STORYBOARD(안전망)**: 그래도 아이가 힘든 장면에 걸리면 visual_desc에서 **아이 얼굴 클로즈업 금지** — 원경·뒷모습·어른의 반응 샷(지켜보는 어미의 일그러진 얼굴)으로 감정을 전달. 직접 묘사보다 반응 샷이 연출로도 여운이 깊다.
- **레지스트리 생애주기 (characters.json/locations.json — 별도 추출 단계 없음)**: ① **OUTLINE에서 태어난다** — 서사 필드만 채운 초안(id, name, type, 역할, physical.age·build 개요, 결핍 메모, anchorProp 후보; locations는 재등장 장소 desc). outline.md에 인물 표를 중복 작성하지 않고 "레지스트리 참조" 한 줄만. ② **DRAFT 내내 살아있다** — 집필 중 새 인물·나이/상태 변화(variants)·설정 변경은 bible 갱신 때 레지스트리에 즉시 반영. ③ **REVIEW에서 전수 대조** — 최종 대본 등장인물↔레지스트리 일치 확인. ④ **시각 필드(영문 lock·negatives·physical 세분화)는 ASSET_GEN 진입 시 완성** — 인물이 굳기 전에 쓰면 재작성 낭비.
  - **★v3.0 편 소속 필드**: 인물·장소마다 `"story": N`(★현행 편성은 1~2)을 넣는다. 옴니버스는 캐스트가 편마다 완전히 갈리므로, 이 필드가 없으면 STORYBOARD 위임 시 다른 편 인물을 캐스팅하는 사고가 난다. **id 접두사도 편 번호로 통일**(`s1_dolsoe`, `s3_jeomrye`) — 편끼리의 이름·id 중복을 기계적으로 막는다.
  - **편당 턴어라운드 2~4명 상한**(guide §7). 그 외 인물은 레지스트리에 넣지 않고 cast 없는 씬(원경·뒷모습·군중)으로 처리한다. **편당 재등장 장소는 1개**만 시트를 만든다.
- 단편(1편만, 6,300~6,700자·23분)을 요청받으면: SCAN·CONCEPT는 편 1개분으로, OUTLINE·DRAFT는 chapters 없이 바로 집필 (guide §1 분량표).
- **딥 벤치마킹은 편당 단계가 아니다** — 신규 채널 발견/성과 부진/5~10편마다, 사용자 요청 시 benchmark-guide.md 로드. 산출물은 공식 개정 제안(proposal)이며 사용자 승인 시에만 script-guide.md 개정.

### 레지스트리 시각 필드 완성 (ASSET_GEN 진입 시 수행 — 구 ASSET_EXTRACT)
- OUTLINE이 만들고 DRAFT가 갱신한 레지스트리("레지스트리 생애주기")에 **시각 필드를 채워 완성**한다. script.txt로 등장인물·재등장 장소를 교차 확인. (레지스트리 자체가 없는 구프로젝트만 대본에서 직접 추출.)
- `{P}/characters.json` 완성 — id별 `{name, type, physical{age,build,hair,eyes,uniqueFeatures}, negatives, lock, turnaround, anchorProp}`.
  - **build(키/체형/연령) 필드 필수** (없으면 전부 성인으로 드리프트).
  - **식별 앵커 필수** — 인물마다 한눈에 알아볼 특징 **하나**를 `anchorProp`에 쓰고 **lock 문장에도 넣는다** (turnaround.py가 턴어라운드에, build.py가 씬에 전파). 고르는 법:
    - 4개 축에서 고른다: ① **실루엣**(체형·자세 — 굽은 허리, 장신, 아이) ② **착용 소품**(입거나 매는 것 — 들고 다니는 물건은 씬에서 빠지기 쉬움) ③ **시그니처 색**(저고리/치마 인물당 고유색 1개) ④ **크고 단순한 머리·얼굴 특징**(백발, 민머리, 큰 흉터, 안대 — 미세한 얼굴 특징은 드리프트해서 못 씀).
    - **캐스트 안에서 축·색이 겹치지 않게** 배분한다 (두 명이 다 "붉은 계열" 금지, 다 "모자" 금지). 후면·원거리 씬에서도 보이는 것 우선 — 4뷰 전부에서 보여야 진짜 앵커다.
    - 색은 hex 말고 말로 (예: "faded indigo-dyed jeogori", "a red silk cord tied on the ankle").
    - **★`anchorProp`·`lock`·`negatives`는 영문 전용** (2026-08-15 실측). turnaround.py가 `anchorProp` 문자열을 프롬프트에 그대로 꽂으므로, 한글을 쓰면 **모델이 그 한글을 시트 안에 캡션으로 그려 넣는다**(흰 배경·텍스트 0 원칙 위반). 사람이 읽을 한글 설명은 `anchorProp_ko` 같은 별도 필드에 둔다.
    - **★1차 산출물에서 캐스트 내 색 충돌이 새로 생기는 것이 정상이다.** lock에 안 적은 색을 모델이 마음대로 넣는다(실측: 다래에게 남색 치마 → 송화의 쪽빛과 충돌 / 박 영감에게 붉은 허리띠 → 다래의 붉은 댕기와 충돌). **contact sheet를 띄우기 전에 PD가 먼저 보고**, 앵커 색이 겹치면 negatives에 `"NO indigo, NO blue …"`처럼 **못 하게 할 색을 직접 적어** 재생성한다.
  - **★얼굴 지문(faceprint) 필수 — 안 적으면 전 편 얼굴이 닮는다** (사용자 지적 2026-08-16: *"편마다 사람 얼굴은 다르게 해줘야 해. 매번 비슷비슷한 경향이 있어"*). 나이·체형·앵커만 쓰고 얼굴 구조를 비워 두면 생성기가 **기본 미남미녀 얼굴 하나로 수렴**한다. 인물마다 아래 여섯 축을 **lock 문장 앞쪽(나이·신분 바로 뒤)에** 박는다 — 뒤에 붙이면 가중치가 떨어진다:
    ① **얼굴형** oval / round / square-jawed / long-narrow / broad-flat / diamond / heart-shaped with a pointed chin / triangular / long rectangular
    ② **광대·볼** high prominent cheekbones / flat low cheekbones / full round cheeks / hollow gaunt cheeks / heavy jowls
    ③ **눈매** downturned / upturned / narrow slit / large round / hooded monolid / deep-set
    ④ **코** small flat / broad low with a wide base / high straight bridge / small pointed / slightly hooked / large bulbous
    ⑤ **눈썹·입** thick dark straight / thin sparse / sharply angled / faded grey / thin lips / wide mouth
    ⑥ **표식** freckles across the nose / age spots on the temple / deep nasolabial folds / a mole beside the mouth / weather-reddened cheeks / a vertical frown line
  - **★얼굴 축을 넣을 때 기존 문구와 충돌하지 않는지 본다** — lock에 이미 있던 `a round weathered face`·`kind narrow eyes` 같은 뭉뚱그린 표현이 새 축과 부딪히면(둥근 얼굴 ↔ 사각턱) 모델이 둘 다 무시한다. **옛 표현을 지우고 새 축만 남긴다.**
  - **★편 경계를 넘어 대조한다.** 편마다 캐스트가 갈리므로 편 안에서만 다르면 소용없다 — **같은 성별·연령대 인물이 다른 편에 있으면 그 둘부터** ①얼굴형과 ③눈매를 서로 다른 값으로 준다(젊은 남자끼리, 중년 여자끼리). ★2편 편성이면 4~8인을 한 표에 놓고 축을 배분한 뒤 lock을 쓰고, **그 표를 bible.md에 남긴다.**
    검수도 이 기준으로 한다: contact sheet를 편별이 아니라 **연령대·성별로 묶어 놓고** 얼굴이 구분되는지 본다.
  - **★채널 style.json도 같은 원인을 가진다 (2026-08-16 개정)** — preset이 얼굴 *연출*이 아니라 *생김새*를 못 박고 있으면(`LARGE SPARKLING EYES … small neat noses`) 인물별 lock을 이겨 버린다. preset에는 **렌더링 품질만**(윤기 있는 눈·캐치라이트·속눈썹) 두고, 생김새는 lock에 맡긴 뒤 preset/negative에 `DISTINCT FACES` · `NO SAME-FACE SYNDROME`을 넣는다.
  - **★★lock·negatives는 짧게 — 길면 화풍과 구도 지시를 밀어낸다 (2026-08-17 03편 실측)** 얼굴을 다르게 하려고 lock을 두껍게 쓰다가 **정반대 대가**를 치른 사례. 6축을 완전한 문장으로 풀어 쓰고 negatives를 8~9줄씩 달았더니 프롬프트가 **한 장당 5,700자**가 됐고, `turnaround_prompt()`가 마지막에 붙이는 **채널 화풍 지시가 55% 지점으로 밀렸다.** 그 결과 프롬프트에 이미 들어 있던 방어 문구 두 개가 함께 묻혔다:
    - `"do NOT repeat the same angle twice"` → 최 첨지 1·2번이 둘 다 정면, 월곡댁 2·3번이 둘 다 측면
    - `"drawn in ONE consistent drawing style"` + `style_anchor.png` → **인물마다 화풍이 갈렸다.** 21장이 밋밋한 라인아트(눈이 검은 덩어리) / 반사실 그래픽노블 / 두꺼운 외곽선 카툰 **세 갈래**로 쪼개졌다.
    - **쓰는 법**: 얼굴 6축은 **명사구로 나열**한다 — `a SQUARE face with a hard ANGULAR JAW and PROMINENT CHEEKBONES, SMALL NARROW SLIT EYES…`(×) → `square face, angular jaw, high cheekbones, small narrow eyes, thick straight low brows, wide thick nose, dark tanned skin`(○). 구분력은 그대로이고 길이는 절반이다.
    - **negatives는 인물별 3~4줄.** `NOT photorealistic` · `no Japanese or Chinese clothing` · `no text` 류는 **style.json의 negative에 이미 있으므로 인물마다 반복하지 않는다.** 인물 negatives에는 **그 인물만의 금지**(다른 인물과 겹치면 안 되는 얼굴형·눈매·색)만 적는다.
    - **목표치**: 생성된 `<id>_turnaround.prompt.txt`에서 `Modern Korean webtoon`이 **앞 35% 안에** 나오면 정상. 55%까지 밀리면 화풍이 깨진다. 배치 전에 이 한 줄로 점검할 것:
      ```
      # 화풍 지시가 얼마나 뒤로 밀렸는지 (35% 이하가 목표)
      python3 - <<'PY'
      import glob, io
      for p in sorted(glob.glob("channels/*/projects/*/*/assets/characters/*.prompt.txt")):
          t = io.open(p, encoding="utf-8").read()
          i = t.find("Modern Korean webtoon")
          print(f"{round(i*100/len(t)):>3}%  {len(t):>5}자  {p.split('/')[-1]}")
      PY
      ```
  - **★검수는 몽타주가 아니라 원본으로 한다 (2026-08-17 사용자 지적 — "이런 건 네가 알아서 검수해야지")** `_contact_sheet.png` 썸네일에서는 **얼굴의 검은 얼룩, 4뷰 각도 중복, 화풍 편차가 안 보인다.** contact sheet는 캐스트 전체를 훑는 용도이고, **PD는 그 전에 턴어라운드 원본을 한 장씩 열어** 다음을 본다: ①4뷰가 정면·3/4·측면·후면으로 **다 다른가** ②얼굴에 지시하지 않은 얼룩·점·흉터가 생기지 않았는가(★`age spot`·`mole` 류를 lock에 적으면 **큰 검은 반점**으로 나오고 **한 패널에만** 찍혀 앵커로도 못 쓴다 — 표식은 주근깨·홍조처럼 넓게 퍼지는 것만 쓴다) ③눈에 홍채가 있는가(검은 덩어리면 style negative가 밀린 신호) ④다른 인물과 **같은 그림체인가**.
  - 같은 인물의 나이/상태 변화 = `variants:{<v>:{physical,lock,turnaround}}` + `default_variant`.
  - 변신/환생 = 별도 id + `reincarnatesTo`/`reincarnationOf` + 공유 `anchorProp`(distinctive prop이 얼굴보다 강한 앵커).
  - **★lock에 쓰지 않는 것 (2026-08-17)** — ①**하반신·전신을 요구하는 서술**(절뚝임·다리·발·전신 자세) → `framing: waist`가 무시된다. ②**질감 과잉**(skeletal / hollow sockets / skin stretched over bones / 주름 3회 강조) → style.json의 `NOT scary`·`no photographic skin texture` 네거티브를 **포지티브가 덮어써** 화풍이 반사실·호러로 드리프트한다. 병색·노화·장애는 **한 번만 약하게** 적고, 나머지는 씬 `visual_desc`에서 연출한다.
  - `lock` = build.py가 씬 {id}에 치환할 자연어 trait-lock 문장.
- `{P}/locations.json` 작성 — **재등장 장소만** `{desc, sheet}`. 1회성 배경은 넣지 않음(씬 텍스트로 충분).
  - **★`desc`는 영문이고, 문화 금지 항목을 `desc` 안에 직접 써야 한다** (2026-08-15 실측). `background.py`의 프롬프트는 `desc` + 채널 style preset/negative가 전부이고 **locations.json의 negatives 필드는 읽지 않는다.** 한글 desc를 그대로 두면 서양 판타지로 드리프트한다 — 실측: 조선 숯막이 **둥근 아치 붉은 문의 호빗집/중국풍 정자**로 나왔다. `"STRICTLY NO round door, NO arched doorway, NO painted red timber, NO curved upturned eaves, NO Chinese or Japanese building, NO European fairy-tale cottage"`처럼 박고 `"Poor rural working architecture, rough and unpainted"`로 계층까지 못 박을 것. 한글 원문은 `desc_ko`에 보관.

### ASSET_GEN  (★사용자 검수 게이트 — OK 받기 전 진행 금지)

> **★실행 첫 줄에 `[era] joseon — 조선` 이 찍히는지 확인한다** (2026-08-29). 시대 앵커가 자리표에서
> 채워지므로, 이 줄이 없거나 다른 값이면 그대로 두고 진행하지 말 것. 상세는 script-guide §10.

```
python3 scripts/assets/turnaround.py {P}     # 인물 턴어라운드(흰배경 4뷰)
python3 scripts/assets/background.py {P}      # 재등장 장소 시트
# contact sheet 생성 + 화면에 띄우기 (macOS Preview)
python3 scripts/render/contact_sheet.py --dir {P}/assets/characters   # → {P}/assets/characters/_contact_sheet.png
python3 scripts/render/contact_sheet.py --dir {P}/assets/locations    # 배경 있으면
open {P}/assets/characters/_contact_sheet.png {P}/assets/locations/_contact_sheet.png
```
- **생성 직후 반드시 contact sheet를 만들고 `open`으로 창을 띄운다** — 사용자가 파일 경로를 찾을 필요 없이 바로 눈으로 검수하게. (open은 macOS 전용; 실패 시 경로를 안내)
- 그런 다음 **여기서 멈추고 사용자에게 "캐릭터 일관성 확인하고 OK 주세요"라고 요청한 뒤 대기**한다. 캐릭터 일관성(연령·체형·문화 앵커·식별 앵커)을 확인하는 자리 — 여기서 틀어지면 이후 씬 이미지 수백 장이 전부 어긋난다.
- **사용자가 명시적으로 OK/컨펌 한 뒤에만 STORYBOARD로 진행**. 그 전에는 storyboard.json을 만들지 않는다.
- 드리프트(연령/체형/문화)를 지적하면 characters.json의 `build`/`negatives`/`anchorProp` 또는 style.json 앵커를 고쳐 `--force` 재생성 → contact sheet 다시 띄워 재확인 → 다시 OK 대기.

### STORYBOARD
- 대본을 씬 분할 → `{P}/storyboard.json` 작성.
- **씬 분할 = 서사 비트 기준, 지속시간 기준 아님**. 씬 경계는 화면이 바뀌어야 할 순간에만 둔다: 인물 등장/퇴장, 장소·시간 전환, 사건·정서 전환. 씬 길이 불균등은 정상(5초~2분 자유) — 이미지 지속시간을 비슷하게 맞추려고 비트 중간을 자르지 말 것.
- **★씬 간격 = 시간 기준 계단 밀도** (script-guide §9-1, 2026-08-22 개정). **1편** 0~5분 **20초** · 5~20분 **40초** · 20분~끝 **60초** / **2편 이후** 0~5분 **30초** · 5분~끝 **60초**. 편이 바뀌는 자리도 사실상 새 시작이라 2편 이후에도 초반 방어를 둔다. 글자수 환산이 아니라 **낭독 실측 시각**으로 끊는다 — `cut_by_time.py {P} --story 1 --plan "0-300:20,300-1200:40,1200-:60"` / `--story 2 --plan "0-300:30,300-:60"`. 43분 편 기준 1편 62장, 2편 이후 편당 48장. 전 씬 Ken Burns 전제(CapCut 마무리).
- **★v3.0: 훅 밀도 규칙 폐기.** 콜드 오픈이 없어졌으므로 "훅 구간을 문장 1~2개당 한 씬으로" 규칙은 적용하지 않는다. 밀도는 편 안에서 완만하게만 기울인다 — **②우연한 사건(4장)이 가장 촘촘하고, ⑦보상·⑧닿음·⑨봉인은 각 1장**. 벤치 2편 모두 밀도 곡선이 평탄했다(훅 스파이크 없음).
- **★편의 첫 씬은 그 편의 얼굴** — 주인공이 또렷이 보이는 미디엄 구도. 2편이면 얼굴 컷이 2장 생기고 그중 하나가 썸네일 후보가 된다. 씬1(영상 전체의 첫 컷)은 그중에서도 가장 강하게. **Veo 대사 클립 전제 구도는 선택 사항** — v3.0 도입부는 대사가 아니라 서술로 열리므로, VEO_HOOK을 쓸 거면 1편 도입 안에 짧은 대사 한 줄을 두고 그 화자를 씬1에 세운다(안 쓰면 스틸 그대로).
- 배경 설명·잔잔한 전개는 **문단 4~8개를 한 씬으로 묶는 게 기본** — 같은 장소·같은 인물 구성이 유지되는 한 화면을 바꾸지 않는다.
- **★씬은 편 경계를 넘지 않는다.** 편이 바뀌면 반드시 새 씬이다. 편 경계 씬은 `act` 필드에 `"story{N}"`을 넣어 표시하고, 그 씬의 시작 시각이 meta.txt 챕터 목록이 된다.
- **문장 귀속 원칙** — 각 문장을 "이 문장이 들릴 때 화면에 뭐가 보여야 하나"로 씬에 귀속한다:
  - 새 인물 소개 문장("그 장터를 쥐고 흔드는 이가 있었으니, 박행수였다")은 **그 인물이 보이는 씬의 첫 문장** — 앞 씬의 꼬리로 붙이지 않는다.
  - 전환·시간경과 문장("그러던 어느 봄날이었습니다")은 **다음 씬의 머리**.
  - 같은 행동의 연속 묘사(지게 지고 → 고개 넘고 → 짚신 닳고 → 산을 오르고)는 한 씬으로 묶는다 — 이미지 하나가 다 커버.
  - **문장 단위 충돌 시 대사 앵커 우선** — sentences.json의 문장 단위는 대사와 다음 서술을 한 덩어리로 묶기도 한다(`"고맙습니다, 행수 어른." 그러던 어느 봄날이었습니다.`). 덩어리가 두 씬에 걸치면 **대사가 일어나는 씬**에 통째로 귀속 — 전환 서술이 앞 씬 이미지 위에 얹히는 건 자연스럽지만, 대사가 엉뚱한 화면 위에서 들리면 확 튄다.
- 씬: `{id, act, narration, cast[], location, visual_desc, sentences[]}`.
  - `sentences`: `[첫,끝]` 0-based 문장 index — 이 씬이 덮는 나레이션 문장 범위. **STORYBOARD에서 narration을 나눌 때 함께 확정** (서사 순서대로 전체 문장 빠짐없이, 겹침 없이 커버). SCENE_TIMING이 이걸 자막 큐로 변환한다.
  - `cast`: `"id"` 또는 `"id:variant"` (그 씬 등장 인물만 — 전부 넣지 말 것).
  - `location`: locations.json 키 또는 null.
  - `visual_desc`: 영문 장면 묘사, 인물 자리에 `{id}` placeholder (build.py가 lock으로 치환).
  - **stock_query/stock_eligible/emphasis 필드는 쓰지 않는다** (생성형 100% 전제).
- **세이프티**: 아동 인물의 고통·눈물·얼굴 클로즈업 visual_desc 금지 (SCRIPT 절 "세이프티 가드레일" 안전망 — 원경·뒷모습·어른 반응 샷으로 대체).
- **★청킹 필수 (분량 무관) — 스토리보드는 항상 편 단위로 위임·병합한다.** 한 에이전트에 전체를 맡기면 대용량 단일 Write에서 스톨한다(2026-07-15 9천자 테스트에서도 2회 재현). 대본이 `{S}/chapters/01.md`~`06.md`(=편)로 나뉘어 있으니 그 경계를 그대로 쓰고, **편별 에이전트는 병렬 가능**(씬 id는 청크 로컬 1부터, PD가 병합 시 전역 재부여). **청크에 넘기는 characters.json은 그 편 소속(`story: N`) 인물만 필터해서 준다** — 전체를 주면 다른 편 인물이 캐스팅된다.
- **narration 필드는 에이전트 산출에서 제외한다** — 씬의 `sentences` 범위만 받고, PD가 `{V}/script_sentences.json`(init_sentences.py 산출, 전 단계에서 미리 생성)에서 프로그램으로 주입. 문장 원문 복사가 없어져 출력이 ~1/4로 줄고 문장-씬 정합이 기계적으로 보장된다.
  - **위임(편 하나 = 청크 하나)**: PD가 각 편을 서브에이전트에 맡긴다. 청크당 넘기는 계약 — ① 그 편의 script 텍스트 ② **그 편 소속 인물만 담은 레지스트리**(`story: N` 필터 — 새 인물 발명 금지) ③ 그 편의 locations 키 ④ **그 편의 전역 문장 시작 index**(sentences를 전역 번호로 authored) ⑤ **시작 씬 id** ⑥ **그 편의 씬 예산**(§9-1 계단 밀도로 산출 — 43분 편이면 1편 62, 나머지 48)과 비트별 배분표(script-guide §9).
  - **큰 입력은 프롬프트에 붙여넣지 말고 파일 경로로 준다** (autoworker-youtube split 교훈) — 편 텍스트는 `{S}/chapters/NN.md`, 레지스트리는 `{P}/characters.json` 경로만 주고 서브에이전트가 Read 하게(필터 조건은 프롬프트로 명시). 청크 산출도 `{P}/_chunks/storyboard_NN.json`로 **파일에 쓰게** 하고 PD는 경로만 회수(컨텍스트 절약).
  - **반환**: 그 편의 `scenes[]`(파일) — 씬 id 연속, `sentences`는 전역 문장 index, cast는 그 편 레지스트리 id만, 첫 씬 `act`는 `"story{N}"`.
  - **PD 병합·검증** (`merge_storyboard.py`, 없으면 수동): 전체 concat 후 ① 씬 id 1..N 연속 ② `sentences` 0..끝 빠짐없이·겹침없이 커버 ③ cast id 전부 characters.json 존재 ④ location 키 유효. 위반한 장만 재위임.
  - 문장 번호 기준은 `script.txt`의 문장 분할 순서 = 나중 `sentences.json` 순서(같은 대본·같은 순서). TTS 후 문장 수가 어긋나면 SCENE_TIMING **경계 검수 리포트**로 잡아 해당 구간만 sentences 보정.

### SCENE_IMG
```
python3 scripts/storyboard/build.py {P}                 # 전체
python3 scripts/storyboard/build.py {P} --only 3,7,12   # 일부 재생성
python3 scripts/storyboard/build.py {P} --dry-run       # 프롬프트/ref 점검(무료)
```
- refs = cast turnaround(순서대로) + location.sheet(존재 시), style.max_refs로 캡(cast 우선).
- **★편 첫 씬 우선 생성·검수**: 배치 첫 실행은 각 편의 첫 씬만 — `build.py {P} --only 1,17,36,55,74,93`(실제 id는 병합 결과 확인). 이 6장이 편의 얼굴이자 썸네일 후보이고, 캐스트 6세트의 일관성이 처음 눈에 보이는 자리다. 어긋나면 visual_desc·lock을 고쳐 재생성한 뒤 나머지 배치를 시작한다. 이 6장은 결과 보고에 **묶어서 첨부**.
- 결과 `storyboard.built.json` 확인, FAIL 씬만 `--only`로 재시도.
- **★흰 테두리는 크롭이 아니라 프롬프트 위치로 잡는다 (2026-08-18 사용자 지적 + A/B 실측)**
  `FULL_BLEED` 문구는 원래 프롬프트의 **36% 지점**(인물 lock 3,000자 뒤)에 있었다. 그 앞을 다 읽고 나서야
  나오니 턴어라운드 시트의 순백 배경을 따라 그리려는 힘을 못 이긴다 — CLAUDE.md의 "긴 lock이 화풍·구도
  지시를 밀어낸다"와 같은 현상이고, **위치가 곧 강도다.** 이제 `build.py`가 같은 지시를 프롬프트 **맨 앞(0%)**
  에 한 번, 끝에 한 번 둔다(앞뒤 양쪽). 실측: 종전에 액자가 났던 7씬을 새 프롬프트로 다시 뽑아 4씬이 깨끗하게
  나왔다(4/7). **완전히는 안 막힌다** — 남는 것은 아래 크롭으로 처리한다.
- **★크롭은 도구 하나로만 한다 — `check_scenes.py --fix` (2026-08-18 통합)**
  종전에는 같은 그림을 `fix_letterbox.py`와 `check_scenes.py --fix`가 **서로 다른 규칙으로** 잘랐고,
  check_scenes 안에서도 흰 액자·바깥 띠·안쪽 여백이 각각 다른 경로를 탔다. 게다가 크롭이 "자르고 →
  16:9로 되맞추고 → 다시 검사"를 **최대 4회 반복**해서, 검출이 한 번만 헛나가도 자를수록 확대되며 그림이 사라졌다.
  지금은 세 검출을 한 상자로 합쳐 **자르기·비율맞춤·리사이즈를 각각 한 번씩만** 한다(`plan_crop`/`fix_image`).
  `fix_letterbox.py`는 같은 함수를 부르는 껍데기로 남겼다.
  - **한 축에서 30%를 넘게 잘라야 하면 자르지 않고 재생성 대상으로 돌린다**(`MAX_CROP`).
  - **안쪽 여백 검출에 대비 게이트를 걸었다** — 종전에는 '밝고 평탄한 행'이면 무조건 여백으로 세서
    **눈밭·흰 벽·환한 하늘이 잘려 나갔다**(5편 눈보라 컷 위쪽 126px). 이제 ①테두리 선 바로 안쪽에서 시작하고
    ②여백이 끝나는 자리에서 밝기가 뚝 떨어질 때만 여백으로 본다.
  - 손실 실측: 액자가 있던 77장을 새 규칙으로 한 번씩 자른 결과 **그림(테두리 제외) 대비 평균 91.7% 유지**
    (최저 80%). 캔버스 대비로 재면 77.7%로 보이는데, 그 차이는 잘라낸 흰 테두리이지 그림이 아니다.
- **★배치 직후 `check_scenes.py`를 반드시 돌린다 (눈 검수보다 먼저).**
```
python3 scripts/render/check_scenes.py {P}            # 흰 액자 · 레터박스 · 이중 패널 검출
python3 scripts/render/check_scenes.py {P} --fix      # 재생성으로 안 잡히면 잘라낸다(원본 .bak.png)
```
  해상도·파일 크기는 정상으로 나오기 때문에 **이 검사 말고는 기계로 걸릴 방법이 없다.** 도구는 있는데 워크플로우에 없어서 눈으로 훑다 놓친 것이 2026-08-16 사고의 시작이었다(1편 16씬 중 5장 불량 — 흰 액자 3·이중 패널 2).
- **★레지스트리 금지어가 씬 연출을 막는다 — negatives는 씬 프롬프트에 그대로 들어간다 (2026-08-18 04편 실측)**
  `build.py`는 인물별 `negatives`를 lock 뒤에 붙여 **모든 씬 프롬프트에** 넣는다. 그래서 턴어라운드 시트에만 걸어야 할 조건을
  `negatives`에 적으면 씬에서 사건을 못 그린다. 실제로 두 건이 걸렸다(이미지 뽑기 전 `--dry-run`으로 발견):
  ① 소 `점백이`에 `no yoke or plough — plain standing pose only` → **봄갈이가 이 편의 중심 사건인데 쟁기를 금지**하고 있었다.
  ② `막실`에 `no walking cane` → 대본에서 지팡이로 마당을 찍는 장면과 정면 충돌.
  → **턴어라운드 전용 금지어는 `negatives_turnaround`에 따로 둔다.** `negatives`에는 "그 인물을 그 인물이게 하는" 금지만 남긴다
  (화풍·복식·연령·문화 오염 방지). 자세·소품·동작 금지는 넣지 마라 — 그건 씬 `visual_desc`가 정할 몫이다.
  점검: `build.py {P} --dry-run --only 1` 로 프롬프트를 뽑아, 그 편의 **핵심 사건에 필요한 사물**이 금지어에 없는지 확인한다.
- **★lock의 포지티브 서술이 negatives를 이긴 사례 하나 더 (2026-08-18)** — 장승 lock의 `greyed and cracked with age`가
  `no stone — it is carved wood`를 이겨 **돌하르방 같은 회색 석상**으로 나왔다. 재질·질감은 부정형으로 막지 말고
  **포지티브로 지정**한다: `the bare pine wood weathered to a soft silver-brown, grain and knots clearly visible`.
- 그다음 contact sheet로 눈 검수. **이중 패널은 기계 검출이 불완전하다**(완전·거울 복제는 잡지만 같은 인물을 다른 각도로 그린 경우는 놓친다) — 눈 검수를 반드시 병행할 것.

**★ref 오염 — 턴어라운드 시트가 씬에 새어 나온다 (2026-08-16 실측)**

씬 ref는 4분할 턴어라운드 시트다. 모델은 참조 이미지의 **내용만이 아니라 레이아웃과 배경까지** 따라 하므로, 시트의 두 특징이 씬으로 복제된다.

| 시트의 특징 | 씬에 생기는 증상 |
|---|---|
| 4분할 패널 구도 | 같은 장면을 좌우로 두 번 그린 **이중 패널**. 이때 **그림체까지 시트 쪽(부드러운 그라데이션)으로 끌려가** style.json의 flat 셀 셰이딩이 무너진다 |
| 순백 배경 | **흰 액자 / 상하 흰 띠** |

- 두 증상은 별개가 아니라 **같은 원인의 두 얼굴**이다. "그림체가 이상하다"는 신고가 오면 먼저 이중 패널인지 본다.
- `build.py`가 씬 프롬프트에 방어구를 항상 넣는다(패널 금지 + 시트 흰 배경 모방 금지). 이 문구를 지우지 말 것.
- **배경 시트에 액자가 있으면 그 장소를 쓰는 모든 씬으로 번진다.** ASSET_GEN 검수에서 배경 시트의 테두리를 "ref로만 쓰이니 괜찮다"고 넘기지 말 것 — 실제로 넘겼다가 씬 2장이 오염됐다. `background.py`가 풀블리드를 강제하고, `check_scenes.py {P} --dir assets/locations`로 시트도 검사한다.
**★씬 연출에서 반드시 지키는 3가지 (2026-08-21 05편 150장 실측 — 결함 10건이 전부 이 셋)**

1. **한 편에 장소가 둘 이상이면, 대표 시트를 안 쓰는 씬은 `location: null`로 비운다.**
   `location`을 넣으면 그 배경 시트가 ref로 붙고, **씬 문장을 이긴다.** 2편에서 산 밑 숯쟁이 집
   장면 3개(35·36·37)에 약방 시트가 붙어 **약재 서랍벽이 그대로 나왔다.** 3편에서도 아랫목 시트가
   야외 뒤꼍 씬을 실내로 끌고 들어왔다. 시트는 **그 장소를 실제로 찍는 씬에만** 붙인다.
   다른 장소는 `location: null` + `visual_desc`에 "NOT a herbal clinic — no wall of medicine drawers"처럼
   **오염될 배경을 명시적으로 부정**한다.

2. **동물·비인간 인물의 앵커는 씬 `visual_desc`에도 다시 쓴다.** 레지스트리 `anchorProp`과 턴어라운드
   ref만으로는 생성기의 **기본 렌더**를 못 이긴다. 3편 흰발(왼앞발만 흰 붉은여우)이 4개 씬에서 전부
   **네 발 다 검게**(=일반 붉은여우) 나왔다. 씬 문장에 `IMPORTANT FOX MARKING: its LEFT FRONT PAW is
   pure SNOW-WHITE … the other three paws are dark`처럼 박고, 그래도 안 되면 **그 앵커가 카메라를 향하는
   동작**으로 연출한다(발을 들어 올린다). 실제로 발을 들게 하니 한 번에 나왔다.

3. **글자가 생길 빌미를 주지 않는다.** `"He is speaking two words"`라고 썼더니 **말풍선에 한글**이 박혔고
   (1편 55), 문서 클로즈업을 시켰더니 **뜻 없는 한글**이 대문짝만하게 나왔다(2편 46).
   - 대사는 `mouth just parted as if beginning to say something`처럼 **입 모양**으로만 쓴다. `speaking`·`says`·`말한다` 금지.
   - 종이·간판·현판이 화면에 필요하면 **판독 불가**를 명시한다 — `narrow VERTICAL columns of tiny indistinct
     brush marks, far too small to read … no recognisable letters, no Hangul, no legible words`. 클로즈업하지 말고
     한 걸음 물러서서 종이 전체가 작게 들어오게 잡는다.
   - 인물이 여럿으로 복제되면(3편 32에서 해순이 좌우 대칭 2명) `There is exactly ONE girl in this image —
     do not duplicate, mirror or repeat any figure.`를 그 씬에만 덧붙인다.

  검수는 컨택트 시트로 **결함 후보만 추리고**, 의심 씬은 반드시 **원본으로** 다시 본다 — 말풍선 글자·여우 발색은
  썸네일에서 안 보인다. 배치 직후 `check_scenes.py {P} --fix`는 매번 돌린다(흰 액자는 재생성 없이 잘라내면 된다).

- **배치 스루풋** (씬마다 고유 이미지 전제, ★현행 2편×45분이면 씬 111장 + 턴어라운드 4~8장 + 배경 2장 ≈ **총 117~121장**). gemini(현 채널 기본, 유료 API) = 일일 한도 없음 → 한 세션에 배치 완료 가능. 무료 flow로 돌릴 경우 **계정당 하루 ~15장**(3계정 병렬 ~45장/일 → 3~4일) — `build.py`는 `storyboard.built.json`의 status로 **완료분을 건너뛰고 이어서** 생성(체크포인트), flow 레인 추가는 `settings.json image.flow.ports`.

### TTS  (`{V}` = `{P}/_video`)
**엔진 선택**: `settings.json tts.engine` — `"vrew"`(반수동, 무료) 또는 `"elevenlabs"`(자동, 유료).

**A) vrew 모드 (반수동, 표준)** — 사용자가 Vrew에서 만든 음성(mp3)+자막(srt)을 `{P}/vrew/`에 넣어 주면 이후는 전부 자동.
- **★병렬화 — export는 REVIEW 직후 즉시 (SCENE_IMG를 기다리지 않는다)**: script.txt가 확정되면 ASSET_GEN으로 넘어가기 **전에** `--export-script`를 실행하고 사용자에게 낭독을 요청한다. 사람 낭독과 자동 제작(asset→storyboard→씬 이미지 며칠)이 겹쳐 리드타임이 ~이틀 준다. 이후 SCENE_IMG 일일 배치를 돌릴 때마다 `{P}/vrew/` 도착 여부를 확인하고, 도착했으면 그 세션에서 ingest→split_long_cues→SCENE_TIMING(씬1이 이미 있으면 VEO_HOOK까지)을 바로 진행한다. **단일 나레이션 정책: 대사 포함 전체를 나레이터 한 명이 낭독** (캐릭터별 보이스 분리 없음). 대본 원천은 `script.txt`.
```
python3 scripts/tts/ingest_vrew.py {P} --export-script --config {CFG}  # → {P}/vrew/vrew_script.txt (+1만자 초과 시 vrew_script_partNN[a-z].txt 자동 분할)
# ★사용자 게이트: Vrew에 붙여넣기→나레이터 보이스 선택→음성(mp3/wav)+자막(srt)을 {P}/vrew/에 저장할 때까지 대기
python3 scripts/tts/ingest_vrew.py {P} --config {CFG}      # → {V}/audio.mp3, subtitle.srt, sentences.json (멀티 파트 자동 병합)
python3 scripts/tts/split_long_cues.py {P} --config {CFG} --apply   # ★기본 실행: 문장 경계 스냅 + 20자 초과 큐 분할
```
- **★장편은 Vrew 붙여넣기 한도(1만자)를 넘는다** — `--export-script`가 한도(`tts.vrew_paste_limit`, 기본 9,950자·공백 포함 — 실제 한도는 1만 자 정각, 2026-08-18 실측) 초과 시 **문단 경계에서 `vrew_script_partNN.txt`로 자동 분할**. 사용자는 파트마다 별도 Vrew 프로젝트로 낭독(**반드시 같은 보이스·같은 속도**)하고, 내보내기 파일명에 파트 번호를 붙여 `{P}/vrew/`에 저장(`narration_01.mp3`+`narration_01.srt`, `narration_02.…` — 이름순 정렬이 곧 파트 순서). ingest가 짝지어 **오디오를 WAV 샘플 정확도로 병합**하고 SRT는 파트별 프레임 스냅 후 오프셋 이어붙임(실측 오차 ≤1프레임).
- **★옴니버스 Vrew 파트 — 편 하나가 1만 자를 넘으면 쪼갠다 (2026-08-20 개정).** `--chapters 1` / `--chapters 2-6`이 **파트 번호를 편 번호로 고정**해 내보낸다(`{S}/chapters/NN.md`에서 직접 읽으므로 script.txt 병합 전에도 가능 — 속도 게이트가 이걸 쓴다).
  - **한도 1만 자는 Vrew 프로젝트 단위로 걸린다** — 화면에서 나눠 붙여넣어도 합산되므로 못 피한다(2026-08-20 실측: 05편 1편 18,514자 거부). 그래서 `export_chapters`가 **문단 경계에서 자동 분할**하고 편 번호 뒤에 a·b·c를 붙인다.
  - 23분 편(6,300~6,700자 ≈ 공백 포함 8,500~9,000자)은 한도 안이라 접미사 없이 `part01.txt` 하나. **★현행 45분 편(12,700자 ≈ 공백 포함 17,000자)은 `part01a`+`part01b` 두 파일**이 된다 — 2편 편성이면 `part01a·01b·02a·02b` 총 4파일.
  - 낭독본 이름을 대본 파일과 똑같이 맞춘다(`narration_01a.mp3`+`.srt`, `01b`…). ingest는 **이름순**으로 병합하므로 `01a → 01b → 02a …`가 그대로 순서다.
  - `--export-script`(script.txt 전체 분할)도 옴니버스에서 자연히 편 경계에 떨어진다 — 한 편은 한도 안에 들고 두 편은 넘기 때문. 그래도 **경계를 확실히 하려면 `--chapters`를 쓴다.**
  - **★인사는 대본에 없다** — 고정 인트로 클립(INTRO 절)이 대신한다. 그래서 파트 합과 script.txt 병합본의 글자 수가 정확히 일치한다(분할 후에도 손실 0).
- **★낭독 속도는 08~13편 값 284자/분을 승계한다** (11편 실측 281.5로 확인). 1편을 먼저 낭독받아 재는 게이트는 **05편 이후 쓰지 않는다** — `{S}/_speed.json`에 잠정 284로 적고 두 편을 다 쓴 뒤, 낭독이 오면 `cpm_measured`를 채우고 **분량을 늘려 맞추지 않는다**(script-guide §1 "속도").
  - 후보: **265자/분**(벤치 ①, 기본에서 약 0.95배 하향 → 총 37,050자) / **280자/분**(Vrew 기본, 자사 실측 → 총 39,200자).
  - **★모든 파트 낭독은 반드시 같은 보이스·같은 속도 설정**으로. 다르면 파트 병합 후 톤이 튄다. `_speed.json`의 `vrew_setting`을 그대로 따를 것.
  - 1편 낭독분(`narration_01*.mp3`+`.srt`)은 **버리지 말고 `{P}/vrew/`에 그대로 둔다** — 그게 곧 첫 파트다.
- **대사 다른 목소리(선택)** — 벤치 ②는 대사에 별도 보이스를 입혔다(YouTube ASR 화자 전환 마커 584개 검출). **Vrew에 자동 화자 배정 기능은 없다** — 클립을 골라 목소리를 바꾸는 수동 작업이다. 채택할 경우: ① 대본에서 대사를 반드시 **독립 문단**으로 두고(script-guide §5 — 이미 규칙) ② Vrew에서 대사 클립만 다중 선택해 남/여 보이스로 일괄 변경, ③ 보이스는 **나레이터 + 남 + 여 3종 이내**로 제한(그 이상은 편당 클립 조작량이 감당 안 된다). **출력은 여전히 mp3 1개 + SRT 1개라 파이프라인 변경은 없다.** 미채택 시 기존 단일 나레이션 정책 유지(벤치 ①이 단일 나레이션으로 97만 조회).
- 상태 감지: `{P}/vrew/`에 오디오+SRT 있으면 ingest 실행(오디오·SRT 쌍 수가 다르면 에러 — 파트 누락 안내), 없으면 대본 내보내고 사용자에게 요청 (클립보드 복사: 단일 `pbcopy < {P}/vrew/vrew_script.txt`, 파트별 `pbcopy < {P}/vrew/vrew_script_part01a.txt` 순서대로).
- 주의: Vrew에서 클립 분할·병합·표기 수정은 자유(split_long_cues가 흡수), **문장 삭제/신규 작성은 금지**(storyboard sentences 범위가 밀림 — 삭제 문장은 경고 후 이웃 보정되지만 씬 싱크 품질이 떨어진다). 완료 후 SCENE_TIMING으로.
- **자막 정형화(split_long_cues)는 vrew 모드 필수 단계** — 두 패스: ① **문장 경계 스냅**: 큐 하나가 대본 문장 경계를 걸치면(Vrew가 짧은 문장들을 한 클립에 합친 경우 등) 그 경계에서 큐를 분할 — 씬 경계가 항상 큐 경계와 일치하게 만드는 안전망. Vrew는 자막에서 마침표를 지우므로 경계는 대본↔자막 비공백 글자 정렬로 찾는다(표기 축약도 difflib로 흡수). ② **길이 분할**: max_chars(20자) 초과 큐를 어절·구두점(쉼표 우선) 경계에서 분할. 타이밍은 두 패스 모두 **음절 비례 분배**(기본). **★whisper는 2026-08-21 사용자 지시로 기본 껐다** — 2시간 넘는 낭독에서 전사에 수십 분이 걸리는데 얻는 것은 한 큐 안 분할점이 ±0.2초 정밀해지는 것뿐이고, 큐 자체의 시작·끝은 Vrew SRT가 이미 실측값이며 씬 경계는 패스 0 문장 스냅이 잡는다. 굳이 쓰려면 `--whisper`(구 `--no-whisper` 플래그는 이제 기본 동작이라 무효). **`--apply`가 sentences.json에 문장별 실측 `cue_range`/`start`/`end`를 기록** → SCENE_TIMING이 비례 추정 대신 이 실측 매핑을 쓴다(정밀 모드). **반드시 SCENE_TIMING 전에 실행**. 검수만 하려면 `--apply` 빼고 실행 → `{V}/subtitle.split.srt`+`split_report.json`(sentence_snap/long_split 구분), A/B 비교는 `capcut_export.py --compare-srt`.

**B) elevenlabs 모드 (자동)** — 단일 보이스(`tts.voice_id`) 전용. 순수 한글 산문이면 tts_map 변환 생략 가능(script를 tts_script로 그대로). 아라비아 숫자/영어가 있으면 extract_tts_targets→tts-converter→apply_tts_map.
```
.venv/bin/python scripts/tts/init_sentences.py {P}/script.txt -o {V}/script_sentences.json
cp {P}/script.txt {V}/tts_script.txt            # (숫자/영어 없을 때)
.venv/bin/python scripts/tts/generate_tts.py {V}/tts_script.txt {V} --config {CFG}     # → audio_raw.mp3, alignment.json
echo '{"conversions":[]}' > {V}/tts_map.json
.venv/bin/python scripts/tts/analyze_sentences.py {V}/alignment.json --script-sentences {V}/script_sentences.json --tts-map {V}/tts_map.json -o {V}/sentences.json --config {CFG}
.venv/bin/python scripts/tts/split_sentences.py {V}/sentences.json -o {V}/split.json
.venv/bin/python scripts/tts/create_srt.py {V}/sentences.json -o {V}/subtitle_raw.srt --split-data {V}/split.json
.venv/bin/python scripts/tts/remove_silence.py {V}/audio_raw.mp3 {V}/subtitle_raw.srt {V}/audio.mp3 {V}/subtitle_trimmed.srt --config {CFG}
.venv/bin/python scripts/tts/align_to_frames.py {V}/subtitle_trimmed.srt {V}/subtitle.srt --config {CFG}
```

### SCENE_TIMING  ★내러티브 전용
스토리보드를 오디오보다 먼저 만들기 때문에, TTS 후 각 씬을 자막 타임라인에 매핑해야 한다.

**★옴니버스는 선행 작업 두 가지가 필수다 (2026-08-18 04편에서 확립 — 없으면 여기서 멈추거나 조용히 깨진다)**
`scene_timing.py`는 `{P}/storyboard.json` **하나만** 읽는데, 옴니버스는 스토리보드가 편별 하위 프로젝트 6개에 흩어져 있다.
1. **편별 storyboard 6개를 영상 단위 `{P}/storyboard.json`으로 병합** — 전역 씬 id를 새로 매기고 `image`에 `{편폴더}/scenes/scene_NN.png` 상대경로를 넣는다(이 필드가 없으면 CapCut export가 "이미지 0개"로 조용히 끝난다).
2. **문장 번호를 낭독 기준으로 번역** — ★**Vrew는 대사 줄과 바로 다음 줄을 한 큐로 합친다**(04편 48곳: `"그건 제가 준 것입니다." 말이 먼저 나가고…`). 그래서 `{V}/sentences.json`(낭독 기준)이 `script_sentences.json`(대본 기준)보다 짧아지고, 스토리보드의 `sentences`를 그대로 쓰면 **뒤쪽 씬이 [1..끝] 전체 구간으로 뭉개진다**(04편 163~166씬 실측). `difflib.SequenceMatcher`로 두 문장 목록을 정렬해 번역표를 만들어 바꾸고, 원본은 `sentences_script`에 남긴다.
   점검: 번역표가 **단조 증가**여야 하고, 경계 검수 출력에 `★폴백`이 하나도 없어야 한다. 씬 하나가 `[0:00~전체길이]`로 찍히면 번역을 안 한 것이다.
- `sentences`는 STORYBOARD에서 이미 authored (없는 씬이 있으면 여기서 채운다 — 문장 귀속 원칙 동일).
- 문장→큐 매핑 2단계: **정밀 모드**(vrew 모드 표준 — split_long_cues --apply가 기록한 실측 cue_range, `[문장→큐 매핑] 정밀 모드` 출력 확인) / **비례 모드**(폴백 — 실측 없거나 cue_count 불일치 시 글자 수 비례 추정). vrew 모드에서 비례 폴백 경고가 뜨면 split_long_cues --apply부터 다시.
- 참고용 문장→큐 맵: `scripts/render/scene_timing.py {P} --emit-sentence-map` → `{V}/sentence_cue_map.json`.
- 렌더용 storyboard 생성: `scripts/render/scene_timing.py {P}` → `{V}/storyboard.json` (씬별 subtitle_range).
- **★경계 검수 필수**: 스크립트가 출력하는 씬별 `첫 큐 … 끝 큐` 텍스트 리포트를 읽고 — 씬의 첫 큐가 그 씬 narration의 첫 문장과 같은 내용인지 확인. 어긋난 씬은 `sentences`를 고쳐 재실행. **균등분배 폴백 경고가 뜨면 진행 금지** (sentences부터 채울 것) — 폴백은 씬 경계를 서사와 무관하게 자르므로 이미지가 문장 중간에 바뀐다.

### CHAPTER_CARDS  ★옴니버스 전용 — 편마다 3초 장부(章)

옴니버스는 편이 바뀌어도 화면과 소리가 끊김 없이 이어져, **자다 깬 시청자가 지금 몇 번째 이야기인지 알 방법이 없다.** 편마다 앞에 3초 장부 카드를 끼우고 그동안 낭독을 멈춘다(사용자 지시 2026-08-17).

> **★1편 앞에도 붙인다 (사용자 지시 2026-08-20 — 파이프라인 기본값 변경).**
> 종전에는 `boundaries()`가 `ids[1:]`로 첫 편을 건너뛰어 **2편부터만 제목이 떴다.** 그러면 1편만 이름 없이 시작해 형식이 어긋난다. 이제 **편이 N개면 카드도 N장**이다.
> 완성본 순서: **고정 인트로 → 1편 장부 카드 → 1편 본문 → 2편 카드 → 2편 본문 → …**
> 파급 셋 — ① 전체 길이가 3초 × N 만큼 는다(종전 3초 × (N−1)) ② **1편 시작 시각이 인트로 길이 + 3초**가 된다(meta.txt 챕터 시각을 이 기준으로 잡을 것) ③ 첫 경계는 0초라 오디오 첫 구간의 길이가 0이 되는데, 빈 `atrim`을 concat에 넣으면 ffmpeg이 입력 수를 못 맞춰 죽는다 — 스크립트가 길이 0 구간을 건너뛰고 무음만 넣는다.

```
python3 scripts/render/insert_chapter_cards.py {P}            # 삽입 + 자동 검증
python3 scripts/render/insert_chapter_cards.py {P} --verify   # 싱크만 재검증
python3 scripts/render/insert_chapter_cards.py {P} --restore  # 원본 복원
python3 scripts/render/insert_chapter_cards.py {P} --gap 4    # 길이 변경(기본 3초)
```

**실행 순서 — 반드시 이 사이에 넣는다.**
```
scene_timing.py  →  ★insert_chapter_cards.py  →  capcut_export.py
```
`scene_timing` 앞에 돌리면 씬 타이밍이 무음을 모르고, `capcut_export` 뒤에 돌리면 드래프트에 반영되지 않는다.

- **오디오에 무음을 넣는 진짜 챕터 브레이크다.** 카드가 뜨는 동안 소리도 쉬어야 자연스럽다. 낭독 위에 카드만 얹으면 "2편 시작" 카드 위로 2편 첫 문장이 이미 읽히고 있어 어색하다.
- 무음을 넣으면 **경계 뒤 자막이 전부 밀린다** — 스크립트가 누적 시프트한다. **1편 카드가 생기면서 자막 전체가 먼저 +3초** 밀리고, 2편 경계 뒤는 +6초, 3편 뒤는 +9초가 된다. 손으로 하지 말 것.
- **멱등하다.** 원본을 `audio.orig.mp3` / `subtitle.orig.srt` / `storyboard.orig.json`로 백업하고 항상 그것을 입력으로 쓴다. 두 번 돌려도 무음이 6초가 되지 않는다.
- **자체 검증이 내장돼 있다** — 실행 끝에 장부 구간 음량(0이어야 함)·직전/직후 음량·자막 끝 대 오디오 끝 차이를 실측하고 이상이 있으면 종료 코드 1을 낸다. **이 출력을 반드시 읽을 것.**
- 편 경계는 `{P}/storyboard.json`의 `act="story{N}"`으로 자동 판별하고, 제목은 `meta.txt` 제작 메모에서 읽는다(`--titles`로 덮어쓰기 가능).

**★카드는 AI로 만들지 않는다.** PIL로 직접 그린다 — 씬 파이프라인은 한글 텍스트를 금지하고(style.json negative), AI에게 한글을 맡기면 글자가 깨진다.

**★카드에는 Ken Burns를 걸지 않는다.** 움직이면 글자가 흔들린다. `capcut_export.py`가 씬의 `is_card: true`를 보고 Ken Burns 대신 **알파 페이드**(0.7초 인 → 유지 → 0.7초 아웃)를 건다.

- 챕터 시각이 편당 3초씩 밀리므로 **meta.txt의 챕터 목록을 갱신**해야 한다.

### VEO_HOOK  ★훅 인트로 립싱크 클립 (**무료 `pjn` 전용** — 🚫 gemini 영상 생성 절대 금지, **2026-08-27부터 기본 실행**)
> **★기본값 = 만든다** (2026-08-27 사용자 지시로 부활). v3.0에서 한 번 폐기됐던 단계다 — 근거는 "수면 채널은 궁금해서 못 끄는 게 아니라 편안해서 안 끄는 것"이었고, 그때는 유료 엔진뿐이라 비용도 걸렸다. 되살린 이유는 둘이다: ①초반 이탈이 실제 문제로 남아 있고 ②pjn 엔진이 무료라 테이크를 얼마든지 뽑을 수 있다. **전제 = 1편 도입 첫 문장에 인물의 직접 대사 한 줄**(script-guide §3-0)과 **그 화자가 씬1에 서 있을 것**. 이 둘이 안 갖춰졌으면 만들지 말고 그냥 넘어간다(스틸 도입).

씬1 이미지를 시작 프레임으로 8초 립싱크 클립(네이티브 오디오 — 대사 포함)을 만든다. **CapCut 드래프트에는 넣지 않는다** — 내보낸 mp4 앞부분을 `attach_hook.py`가 갈아끼운다(아래 ATTACH_HOOK).
엔진(`settings.json image.veo.engine`): **`pjn`(무료·야담 기본, 2026-08-26)** = 로컬 5090 서버 `api.project-n.work` MiniMax H3 i2v, `.env` `PJN_API_KEY`만 있으면 됨(데몬·Chrome 불필요). 최대 1376×768이라 생성 후 렌더 규격(1920×1080/30fps)으로 자동 재인코딩되고, 첫 프레임이 씬1 스틸에 픽셀 고정돼 컷 연결이 Veo보다 자연스럽다. 화질은 `image.veo.pjn.quality`(0.4/0.6/0.8/1.0) / `gemini`(⚠️유료) = Gemini API `veo-3.1-lite-generate-preview` 1080p/8초, `.env` GEMINI_API_KEY / `flow` = labs.google 웹세션(~20크레딧, `image.veo.flow.ports` 레인 데몬+Chrome 필요).
**🚫 gemini 엔진은 절대 쓰지 않는다** (2026-09-06 사용자 지시 · CLAUDE.md 「🚫 절대 금지」 절). `GEMINI_API_KEY` 로는 **영상을 만들지 않는다** — 이미지만 허용이다. 테이크도 확정본도 **전부 무료 `pjn`** 으로 뽑고, pjn이 안 되면 **훅을 포기하고 스틸 도입으로 간다.** 「확정본만 `--engine gemini --force` 로 재생성」하던 종전 안내는 **폐기됐다.** 또한 `veo_hook.py` 코드 기본값이 `gemini` 이므로 **`--config channels/{채널}/config/settings.json` 을 반드시 명시**한다.
```
python3 scripts/render/veo_hook.py {P}     --speaker "The OLD MAN on the left in the grey hemp jacket, standing on the porch"     --listener "the young man in undyed hemp"        # 프롬프트 생성 → 클립 생성 → 규격·음량 맞춤
python3 scripts/render/veo_hook.py {P} --prompt-only  # 무료: 프롬프트·매니페스트 파일만
```
- **★`--speaker`를 반드시 준다** (2026-08-27 실측). 템플릿 기본값은 `The character at the center of the frame`인데, 씬1에 인물이 둘 이상이면 **누가 말할지를 모델이 고른다.** 06편 씬1(노인+젊은이)에서 한 번은 맞았지만 그건 운이었다. 옷·위치·나이로 지목하고, 함께 선 인물은 `--listener`로 묶어 입을 다물게 한다.
- **★음량은 자동으로 낭독에 맞춘다** (2026-08-27 신설). pjn 원본은 −24~−28 LUFS로 나오는데 낭독은 −13 근처라 그냥 붙이면 훅만 안 들린다. `settings.json render.loudness_lufs`(기본 −14, 야담 −13.0)로 loudnorm 2-pass. `--lufs 0`으로 끈다.
- 훅 대사는 script.txt 첫 따옴표 대사에서 자동 추출(playbook "대사 선행" 전제), 프롬프트는 씬1 visual_desc 기반 템플릿으로 `{V}/veo_hook_prompt.txt`(pjn 엔진은 H3 대사 태그 형식이라 `{V}/veo_hook_prompt_pjn.txt`로 분리) 생성. **이미 있으면 그대로 쓴다** — PD가 파일을 다듬은 뒤 재실행하는 워크플로우 지원(다듬은 대사가 매니페스트 `dialogue`에 반영돼 capcut 콜드오픈 큐 매칭 기준이 된다 — 따옴표·`<d>[Korean] …</d>` 두 형식 모두 인식).
- **★렌더 storyboard에 주입하지 않는다** (기본 `--inject` 꺼짐, 2026-08-27). 주입하면 `capcut_export`가 클립을 드래프트에 싣고, 그러면 Windows CapCut이 죽는다(SKILL+ §9 — 규격을 맞춰도, 사람이 직접 얹어도 죽는다). 훅은 **내보낸 mp4에 후처리로** 붙인다.
- **★옴니버스 주의** (2026-08-27 실측): `insert_chapter_cards` 뒤에는 렌더 보드의 씬1이 **장부 카드**다. 시작 프레임·주입 대상 모두 카드를 건너뛰도록 고쳐 뒀지만, 매니페스트 `start_frame`이 `cards/card_NN.png`를 가리키면 그건 회귀다. 또 병합 보드에는 `visual_desc`가 없어 편 하위 프로젝트에서 읽어 온다 — 프롬프트의 씬 묘사가 비어 있으면 그 폴백이 깨진 것이다.
- **실패해도 진행을 막지 않는다** — `{V}/veo_hook.json` 매니페스트(시작 프레임·프롬프트·수동 실행 커맨드)가 항상 남으므로, 크레딧 소진/데몬 부재 시 결과 보고에 매니페스트 경로와 수동 커맨드를 첨부하고 RENDER로 진행(도입부는 스틸 그대로).
- 재실행 안전: mp4가 이미 있으면 생성 건너뛴다(크레딧 재소모 없음). 새로 뽑으려면 `--force`.

### RENDER  ★CapCut export 전용 (자동 렌더 없음)
**CapCut 드래프트로 넘겨 마무리 편집을 사람이 한다.** 파이프라인은 mp4를 직접 만들지 않는다.
```
python3 scripts/render/capcut_export.py {V} --name {프로젝트} --config {CFG}
```
- `{V}`의 audio.mp3+subtitle.srt+storyboard.json(scene_timing 산출) → `~/Movies/CapCut/User Data/Projects/com.lveditor.draft/{프로젝트}/` 에 draft 생성(root_meta 갱신) → **CapCut 열면 바로 뜸**(실행 중이면 재시작). 성공 시 `{P}/output/capcut_draft.json` 마커 자동 기록.
- **★veo 콜드오픈 자동 주입은 폐기됐다** (SKILL+ §9). 씬1 `video_path`가 비어 있어야 정상이고, export 로그에 `veo 콜드오픈`이 뜨면 그 드래프트는 CapCut에서 죽는다 — `{V}/storyboard.json`에서 `video_path`를 `null`로 되돌리고 다시 내보낼 것. 훅은 **ATTACH_HOOK**이 붙인다.
- **이후는 사용자 대기 게이트**: 사람이 CapCut에서 마무리 편집 → mp4 내보내기(파일명 자유) → **ATTACH_HOOK → INTRO → OUTRO** → UPLOAD 진행 가능.
- 파이썬 규칙: **elevenlabs TTS 체인(generate_tts·analyze·remove_silence 등)과 업로드는 `.venv/bin/python`**(dotenv·numpy·requests·google-api 필요). asset/vrew/scene_timing/render는 표준 `python3`로 충분(ffmpeg만 외부 의존).

### ATTACH_HOOK  ★훅 클립 스플라이스 (CapCut 내보내기 뒤, INTRO 앞 — 2026-08-27 신설)
훅 클립은 **CapCut에 넣지 않는다**(SKILL+ §9). 사람이 내보낸 mp4의 **도입부를 갈아끼운다.**
```
python3 scripts/render/attach_hook.py {P} --dry-run   # 자를 구간·시프트만 계산
python3 scripts/render/attach_hook.py {P}             # → <완성본>_hook.mp4
```
- **무엇을 무엇으로 바꾸나**: 낭독은 도입부에서 "…라고 말했습니다" 뒤에 그 대사를 그대로 읽는다. **선두 큐부터 그 대사 큐 끝까지**를 8초 훅 클립으로 통째로 교체한다 → 대사가 두 번 들리지 않고, 영상이 내레이션이 아니라 **사람이 말을 거는 것**으로 열린다. 장부 카드는 건드리지 않는다(카드 → 훅 → 낭독).
- 대사 큐는 `{V}/veo_hook.json`의 `dialogue`로 찾는다. **선두 12개 큐 안에서 못 찾으면 자르지 않고 멈춘다** — 뒤쪽에서 우연히 같은 말이 나온 큐를 잡아 영상 한복판을 자르는 사고를 막는 안전장치다.
- **전체를 재인코딩하지 않는다**: 잘라낼 자리 뒤 첫 키프레임까지만 다시 굽고(머리+클립+다리, 합쳐 15초 남짓) 나머지는 스트림 복사. 2시간 반짜리를 CRF로 다시 굽지 않으려는 것.
- **타임라인이 밀린다**: Δ = 클립 길이 − 잘라낸 구간. 이 스크립트가 `{V}/storyboard.json`의 **장부 카드 start/end**와 **meta.txt 챕터 시각**을 함께 옮긴다. 그래야 뒤이어 도는 `attach_intro.py`의 챕터 재계산이 맞는다. (06편 실측: 3.000~8.933 → 8초 클립, **+2.067s**)
- 마커 `{P}/output/hook_attached.json`. 훅을 안 쓰는 편이면 이 단계를 통째로 건너뛴다.

### INTRO  ★CapCut 내보내기 뒤 반드시 (2026-08-17 확정)
**인트로는 CapCut 타임라인에 넣지 않는다** (Windows CapCut 크래시 + 편집 중 타이밍이 전부 밀림). 사람이 mp4를 내보낸 **직후**, UPLOAD 전에 붙인다. 01편에서 이 단계를 빠뜨려 인트로 없는 완성본이 나왔다 — **RENDER 다음은 UPLOAD가 아니라 INTRO다.**
```
python3 scripts/render/attach_intro.py "<완성본.mp4>" --project {P} --write-meta
```
- 하는 일 3가지: ① 인트로를 본편 스펙(코덱·오디오·**타임스케일**)에 맞춰 정규화 ② concat 데먹서 `-c copy`로 앞에 결합(본편 재인코딩 없음) ③ 챕터 시각을 장부 카드 실측 + 인트로 길이로 **재계산**해 meta.txt 갱신.
- 결과 `<완성본>_intro.mp4` + `intro_attached.json` 마커(재실행 시 자동 건너뜀, `--force`로 강제). 원본을 갈아끼우려면 `--replace`(원본은 `.nointro.mp4`로 보관).
- **업로드는 반드시 `_intro.mp4` 쪽을 올린다.** 같은 폴더에 인트로 없는 원본이 남아 있으니 파일명을 확인할 것.
- 함정·근거는 위 「고정 인트로」 절 참조(타임스케일 불일치로 영상이 24초로 뭉개지는 사고, format duration만 보면 못 잡는다).

### OUTRO  ★INTRO 다음, UPLOAD 직전 (2026-08-21 신설 · 사용자 지시)
이야기가 끝난 뒤에도 화면을 끄지 않는다 — 본편 **뒤에** 조용한 수면 노이즈를 몇 시간 이어 붙여
"틀어 놓고 잔다"를 끝까지 받쳐 준다. 자산은 `channels/{채널}/assets/outro/sleep_noise_{길이}[_quiet].mp3`
(30분/1h/2h/3h × 일반·quiet). **`_quiet`가 약 6dB 낮다** — 본편 나레이션 뒤에 붙으므로 기본은 quiet 쪽.
```
python3 scripts/render/attach_outro.py "<완성본>_intro.mp4"     --outro channels/{채널}/assets/outro/sleep_noise_3h_quiet.mp3
```
- 아웃트로 원본은 **오디오뿐**이라 화면을 얹어 본편 스펙(코덱·해상도·fps·pix_fmt·샘플레이트·**타임스케일**)으로 굽는다.
- **★화면은 완전 검정이 기본이다** (2026-08-21 사용자 지시). 잠들려고 트는 자리라 그림을 깔면 빛이 남는다.
  처음엔 마지막 편의 닫는 씬(눈 덮인 겨울밤)을 깔았는데, **어두운 밤 그림도 몇 시간이면 방을 밝힌다.**
  그림을 굳이 깔아야 할 때만 `--image <png>`.
- **★정지 화면을 한 프레임씩 굽지 않는다** — `-loop 1`로 3시간을 통째로 인코딩했더니 **35분 돌고도 절반**이었다.
  화면이 한 장뿐이라는 사실을 쓰면 끝난다: 60초 조각을 **한 번만** 굽고 concat 데먹서로 **스트림 복사** 반복,
  오디오만 새로 인코딩. 같은 3시간이 **7분**에 끝났다(실측 — 조각 48초 + 반복 14초 + 오디오 6분).
- 시작 3초 페이드인이 기본(`--fade`). 본편 마지막 소리에서 노이즈로 뚝 붙는 느낌을 없앤다.
- 본편은 여기서도 재인코딩하지 않는다. concat 실패 시 attach_intro와 같은 MPEG-TS 경로로 자동 재시도.
- **챕터 시각은 건드리지 않는다** — 아웃트로는 뒤에 붙어 앞 시각을 밀지 않는다. 결과 마커
  `outro_attached.json`에 아웃트로 시작 시각이 남으므로, 설명문에 "그 뒤로는 조용한 빗소리"를 적을 때 쓴다.
- 결과 `<완성본>_intro_outro.mp4`. **업로드는 이 파일을 올린다** — 같은 폴더에 인트로만 붙은 것과 아무것도
  안 붙은 원본이 함께 남는다. 파일명을 반드시 확인할 것.

**UPLOAD** (자체 스크립트 `scripts/upload/`, 비공개 업로드):
```
# 최초 1회 (채널당): client_secret.json을 channels/{채널}/config/youtube-api/에 두고
.venv/bin/python scripts/upload/auth.py --channel {채널}          # 브라우저 OAuth → token.json
# 매 업로드: PD가 meta.txt 확인(제목/설명/태그 자동 추출됨. 다듬을 게 있으면 output/youtube.md 작성이 우선)
.venv/bin/python scripts/upload/upload.py --project {프로젝트} --channel {채널}   # → output/upload_result.json
```
- 메타 우선순위: CLI 인자 > `output/youtube.md`(`## 제목/## 설명글/## 태그/## 고정 댓글`) > `{P}/meta.txt`(규약은 script-guide.md).
- 썸네일: `output/thumbnails/`에 png/jpg 있으면 자동 첨부(2MB 초과 시 자동 압축).

## 검증된 교훈 (반드시 지킬 것)
- **★이 채널은 이야기가 아니라 수면 상황을 판다** (v3.0, 벤치 2편 실측). 목표는 "궁금해서 못 끄는 것"이 아니라 "편안해서 안 끄는 것" — 각성 장치(후렴·클리프행어·미끼·분노·파국·CTA)는 전부 금지 목록(script-guide §6). 이 한 줄이 v3.0 모든 규칙의 뿌리다.
- **옴니버스는 캐스트가 편마다 갈린다** — 레지스트리 `story: N` 필드와 `s{N}_` id 접두사가 유일한 방어선. 편당 턴어라운드 2~4명·배경 1개 상한을 CONCEPT에서 지키지 않으면 asset 단계에서 터진다.
- 캐릭터 일관성 3종: **턴어라운드 ref + trait-lock(build 포함) + 씬별 cast**.
- **문화·시대 앵커는 style.json preset에 박는다** — ref 없는 씬(군중·빈 배경)의 유일한 방어선. `"Ghibli/anime"` 금지 → `"Korean webtoon/manhwa"`.
- 동물·신령 등 비인간 인물은 **착용 소품 앵커**로 (발목에 맨 색 끈, 목에 건 방울 등 — 얼굴 잠금이 약해서 소품이 더 강하다). ref는 한 씬 최대 ~5장.
- **미성년자 얼굴 클로즈업+고통/눈물은 세이프티 차단** (2026-07-19 실측) — 수난 당사자는 CONCEPT에서 성인으로 각색, 아이 장면은 STORYBOARD에서 반응 샷 우회. 상세는 SCRIPT 절 "세이프티 가드레일".
