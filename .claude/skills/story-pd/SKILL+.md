# SKILL+ — story-pd 사용자 오버라이드

`SKILL.md`(원본)는 **그대로 유지**한다. 이 파일은 사용자가 추가·변경하고 싶은 규칙만 모은 것으로,
"야담 영상 만들어줘" 등 story-pd 실행 시 **SKILL.md와 함께 이 파일도 읽고, 아래 규칙을 우선 적용**한다.
(원본 playbook 개정 절차와 무관하게, 사용자가 직접 관리하는 커스텀 레이어.)

---

## 0. ⛔ 절대 규칙 — D: 드라이브(외장하드)는 건드리지 않는다

**D:\ 드라이브의 기존 파일·폴더를 삭제·수정·덮어쓰기·이동하지 말 것** (사용자 명확화 2026-07-26: "원래 D에 있는 것들을 수정 또는 삭제하지 말라는 뜻"). D:는 사용자가 최종 영상·백업을 보관하는 외장하드다.
- **새 파일을 D:에 저장(쓰기)하는 것은 OK** — 최종 산출물(최종 mp4 등)을 D:에 새로 저장해도 된다. 단 **기존 파일을 덮어쓰지 말고**(새 이름으로), 기존 것을 지우거나 고치지 말 것.
- 기존 D: 파일 삭제·정리가 필요해 보여도 **제안만** 하고 실행은 사용자에게 맡긴다. (예: `D:\CapCutData` 같은 내가 만든 쓰레기 복사본도 지우려면 사용자에게 확인.)
- D: 읽기는 자유(base mp4 읽어 concat 등).
- 공간 확보(삭제)는 **C:에서만** 한다.

---

## 1. 편 도입 — 3문장 안에 인물·처지·결핍 (★2026-08-12 v3.0으로 대체)

> **폐기됨**: 아래 원문은 "콜드 오픈 첫 문장에 모순/충격을 박아라"였다. **v3.0 수면 옴니버스 전환으로 콜드 오픈 자체가 사라졌다** — 벤치마크 2편 모두 미끼·모순 선언·질문 봉인이 0회였고, 궁금증은 각성 장치라 수면 콘텐츠와 상충한다. 근거: `channels/yadam/research/proposal_20260812.md`.

**현행 규칙 = `prompts/script-guide.md` §3.**
- 편 첫 **3문장 안에 인물·처지·결핍**을 다 준다. 그다음 곧바로 "그러던 어느 날"로 사건에 들어간다.
- 도입형 두 가지를 6편 안에서 3:3으로 섞는다 — **A형(정형: "옛날 옛적 한 마을에 …가 살았습니다")** / **B형(장면: "장맛비가 퍼붓던 어느 여름이었습니다")**. 1편은 B형, 6편은 A형 고정.
- **결말을 흘리지 않는다.** "이 일이 그의 팔자를 뒤바꿔 놓을 줄은 몰랐습니다"는 각성 장치다.
- A형 첫 문장 틀을 편마다 바꾼다 — 6편이 다 "옛날 옛적 어느 고을에"면 벤치 ②의 최다 좋아요 댓글이 지적한 그 지루함이 된다.
- 편의 첫 씬은 여전히 **주인공이 또렷이 보이는 구도**(썸네일 후보). 다만 익스트림 구도 강제는 없앤다.

<details><summary>구 v2.x 원문 (참고용)</summary>

콜드 오픈 첫 문장을 분위기·이미지 묘사로 시작하지 말고 상황의 모순/충격을 요약해 곧바로 제시한다. ❌ "야윈 손이 안방 문고리를 어루만졌습니다" / ✅ "병든 아내가, 남편이 새로 들인 어린 첩에게, 제 손으로 안방을 내주었습니다". 부당함은 3박자 열거로 부각.
</details>

## 2. CTA — 넣지 않는다 (★2026-08-12 v3.0으로 대체)

> **폐기됨**: 아래 원문은 "엔딩 CTA를 이야기 배경으로 각색해 댓글을 유도하라"였다. **벤치마크 2편 모두 구독·좋아요·댓글 CTA가 0회**다(①은 도입 인사 2문장만, ②는 인사조차 없음). 자는 사람에게 버튼을 누르라고 하지 않는다.

**현행 규칙 = `prompts/script-guide.md` §3·§4.**
- 영상 맨 앞 **인사 2~3문장(100자 이내)**만 둔다. 구독·좋아요·알림 요청 금지.
  > 안녕하세요. 오늘도 참 고생 많으셨지요. 이 밤 따뜻한 옛이야기 들으며 편안히 쉬어 가세요. 그럼 첫 번째 이야기 시작합니다.
- 편 사이에는 아무것도 넣지 않는다. 앞 편 정형구가 끝나면 곧바로 다음 편 첫 문장.
- **마지막 6편 뒤에도 아웃트로를 넣지 않는다** — 닫는 정형구로 그냥 끝난다(벤치 ① 실측 아웃트로 0초).
- 참여 유도가 필요하면 **대본이 아니라 고정 댓글**로 한다(벤치 ①의 최다 좋아요 댓글이 채널 본인의 인사 고정 댓글이었다 — 252 likes).

<details><summary>구 v2.x 원문 (참고용)</summary>

"이 이야기는 충청도 어느 고을에 오늘날까지 전해 옵니다. 그런데 이 이야기, 지금 어느 고을에서 듣고 계신가요? 사시는 곳 이름을 댓글에 살짝 남겨 주시고요." + "다음 이야기로 다시 찾아뵙겠습니다".
</details>

---

## 3. Windows 환경 · 파이프라인 트러블슈팅 (재발 방지 체크리스트)

이 저장소 스크립트는 macOS/Linux 기준이라 이 Windows 머신에선 아래 문제가 반복된다.
**파이썬 스크립트를 부를 때마다 먼저 이 환경 세팅을 앞세운다** (PowerShell은 호출 간 env가 유지 안 되니 매번):

```powershell
$env:PYTHONUTF8="1"; $env:PYTHONIOENCODING="utf-8"; $env:PYTHONPATH="c:\Users\goodb\Desktop\gogogo2-youtube\scripts\_pytools"; $env:PATH="C:\miniconda\Library\bin;"+$env:PATH
```
- 파이썬 인터프리터 = `python` (miniconda). `python3`는 없음 — 단 `C:\miniconda\python3.exe` shim이 있어 스크립트 내부 `subprocess(["python3",...])`는 동작한다(**지워지면 씬 생성 전량 실패 → 재생성**).

### 단계별 알려진 문제 → 조치

| 증상 | 원인 | 조치 |
|---|---|---|
| 모든 스크립트 `UnicodeDecodeError: cp949` | 한글 UTF-8 파일을 cp949로 읽음 | `PYTHONUTF8=1` |
| 콘솔 출력 crash (✓/✗ 유니코드) | cp949 콘솔 | `PYTHONIOENCODING=utf-8` |
| 이미지·업로드 `[ASN1: NOT_ENOUGH_DATA] _ssl.c` | Windows 인증서 스토어 손상 → **모든** 파이썬 HTTPS 실패 | `PYTHONPATH`에 `scripts/_pytools` (certifi로 교체하는 `sitecustomize.py`) |
| ffmpeg `FileNotFoundError [WinError 2]` | ffmpeg가 PATH에 없음 | `C:\miniconda\Library\bin`을 PATH 앞에 prepend |
| turnaround/background/build `PER_MODEL_DAILY_QUOTA_REACHED` | flow 무료 계정 하루 ~15장 한도 소진 | 다음날 재시도 / 유료 / 레인 추가. 실패분은 build 체크포인트가 이어서 생성 |
| flow 생성 전 `reCAPTCHA` 대기·`SW 붙는중` | Chrome Flow 탭이 데몬에 미연결 | Flow 탭 열고 확장 Connect. `curl localhost:3847/status`가 `connected:true`인지 |
| build 다수 `모든 레인이 사용 중` / `WinError 10053` | 동시성 ~5인데 flow 레인 1개 → 충돌 | **`build.py --concurrency 1`** (직렬 생성) |
| 씬 이미지 `PUBLIC_ERROR_UNSAFE_GENERATION` (HTTP 400) | 안전필터 오작동(어린 인물 + 밤 + "intimate"/침실 뉘앙스 등) | visual_desc를 **소품·사건 중심으로 리워딩**('intimate'·'alone in the bedroom' 등 제거) 후 `build.py --only N` 재생성 |
| split_long_cues 가 몇 시간째 안 끝남 / `whisper FileNotFoundError` | whisper 단어 실측을 돌리고 있음 (또는 CLI 미설치) | **`--no-whisper`** — 아래 §3-1 참조. **이 채널은 whisper를 쓰지 않는다** |
| Vrew 산출물이 mp4만 있음 | Vrew가 영상으로 내보냄(오디오 트랙만, 자막 트랙 없음) | ffmpeg로 오디오 추출 → **srt와 같은 basename**으로 저장(`영상.mp4`→`영상.mp3`), mp4는 `vrew/_raw/`로 치움 |
| Vrew srt가 없음 | 자막을 별도로 안 내보냄 | Vrew에서 자막을 **.srt로 별도 export** 요청(영상+자막 둘 다 필요) |
| ingest `쌍 개수 불일치` 에러 | vrew/ 최상단에 구버전 녹음이 남아 audio/srt가 2쌍 | 구버전을 `vrew/_raw/`로 이동, 최상단엔 **새 audio+srt 1쌍만** |
| capcut 드래프트가 안 열리거나 빈 채 | CapCut Windows는 `draft_content.json`을 읽는데 스크립트가 `draft_info.json`만 씀 | (패치됨 — 둘 다 기록). 구프로젝트면 `draft_info.json`→`draft_content.json` 복사 |
| capcut_export가 macOS 경로 못 찾음 | `~/Movies/CapCut/...` 하드코딩 | (패치됨 — win32면 `%LOCALAPPDATA%\CapCut\...`) |
| **CapCut에 옛 자막/내용이 계속 되살아남** ★가장 헷갈림 | ① CapCut가 **열린 채** 갱신하면 자기 메모리의 옛 버전으로 도로 덮어씀 ② 첫 열람 때 `Timelines\<UUID>\`로 마이그레이션 후 **거기서** 읽음(최상단 파일 수정 무효) | **CapCut 완전 종료**(트레이·프로세스 전부) 후 갱신. 이미 꼬였으면: 드래프트 폴더 삭제 → `root_meta_info.json`에서 항목 제거 → **새 이름으로 재생성**(uuid4라 새 draft id → 캐시·마이그레이션 분리). 예: `..._v2` |

### 3-1. ⛔ whisper 금지 — `split_long_cues`는 **항상 `--no-whisper`** (사용자 지시, 재확인 2026-08-03)

**이 채널은 whisper를 쓰지 않는다.** 설치돼 있든 아니든, 성능이 되든 안 되든 **묻지 말고 `--no-whisper`를 붙인다.**

```powershell
python scripts/tts/split_long_cues.py {P} --config {CFG} --no-whisper --apply
```

- **원본 SKILL.md는 whisper 단어 실측을 기본으로 서술하고, 위 표도 원래 "미설치 시 폴백"으로만 적혀 있었다. 그 표현 때문에 실제로 사고가 났다** — 2026-08-03 이름석자에서 whisper가 설치돼 있다는 이유로 그냥 돌렸고, 76분 오디오에 medium 모델 CPU 추론이 붙어 **18분을 쓰고도 진행률 0**이었다(추정 총 3~4시간). 강제 종료하고 `--no-whisper`로 재실행하니 **수 초 만에 완료**.
- **폴백이 아니라 기본값이다.** `--no-whisper`는 음절 비례로 타이밍을 나누지만 **`cue_range`·`start`·`end`를 그대로 기록**하므로 **scene_timing은 정밀 모드로 동작한다.** 잃는 것은 쉼표 호흡의 중앙값 ~300ms 보정 하나뿐이고, 수면·낭독 콘텐츠에서 체감되지 않는다.
- **실측 (이름석자, 76.3분 / 1,213큐 입력)**: `--no-whisper`로 최종 **2,113큐 · 최대 13자 · 13자 초과 0 · 2줄 큐 0 · 837문장 전부 cue_range 기록.** 품질에 문제 없음.
- whisper를 굳이 쓰고 싶은 상황이 생기면 **사용자에게 먼저 물어본다.** 기본은 언제나 끈다.

### 순서·원칙 (요약)
- **`split_long_cues`에는 항상 `--no-whisper`** (§3-1).
- **capcut_export는 CapCut가 완전히 종료된 상태에서만** 실행 (위 ★ 항목이 가장 자주 재발).
- Vrew 재녹음으로 대본이 바뀌면: script.txt 수정 → **storyboard.json의 sentences 재매핑**(문장 수/인덱스 이동 반영) → vrew 재수합 → split_long_cues `--no-whisper --apply` → scene_timing(경계 검수) → capcut_export. 훅/엔딩만 바뀌면 **씬 이미지는 재생성 불필요**(기존 컷이 새 나레이션에도 맞으면).
- 파이프라인 스크립트를 편집할 땐 뒤에서 참조되는 변수를 지우지 말 것(예: `draft_path`).

---

## 4. flow 어뷰징 방지 — 요청 텀 스로틀 (UNUSUAL_ACTIVITY 대응) ★계정 보호

**증상:** flow 이미지 생성 중 `PUBLIC_ERROR_UNUSUAL_ACTIVITY`(HTTP 403 PERMISSION_DENIED). labs.google 이 비정상 활동으로 감지해 잠시 막는 것. **일시적 레이트/어뷰징 플래그이며 영구 밴이 아님**(직렬·저속으로 재시도하면 대개 통과). 단, 반복되면 계정이 위험해지므로 **속도를 낮춰 예방**하는 게 원칙.

**원인:** 같은 IP에서 여러 버너 계정(레인)이 **동시에** 요청을 쏘거나(병렬 concurrency↑), 한 계정이 **텀 없이 연속** 발사할 때. 실측: concurrency 3 병렬 → 걸림 / concurrency 1 직렬 재시도 → 통과.

**조치 (코드에 내장됨, `flow_client.py`):** 두 겹 스로틀이 `run()`에 배선돼 있고 env로 조절/비활성한다.
- **레인간 시차** `_global_stagger` — 전 계정 공용 파일락(`~/.flow-proxy/stagger.lock` + `last_request.json`)으로 어떤 두 요청도 최소 간격 이상 벌린다. 프로세스가 계정마다 따로 뜨므로(subprocess) 파일 기반 조율. → `FLOW_STAGGER_SEC` (기본 6초, 지터 +0~40%). **"동시에 여러 계정에 안 나가게".**
- **레인내 쿨다운** `_lane_cooldown` — 한 계정이 이미지 하나를 끝낸 뒤 레인을 반납하기 **전에** 텀(레인이 busy로 잡혀있는 동안 sleep → 같은 계정 즉시 재점유·연속발사 차단). → `FLOW_LANE_COOLDOWN_SEC` (기본 12초, 지터 +0~40%). **"계정 안에서도 완료 후 인위적 텀".**
- 둘 다 **지터**로 기계적 패턴을 흩뜨린다. `=0` 이면 해당 스로틀 비활성.

**권장 운용 (야담 배치):**
- **`build.py --concurrency 1`** (직렬)로 돌리는 게 가장 안전. 레인이 여러 개여도 stagger가 알아서 벌리지만, 직렬이면 동시 발사 가능성 자체가 0.
- 기본값(stagger 6s + cooldown 12s)이면 이미지당 유효 텀 ~18초+지터. **급하지 않으면 기본 유지**. 더 보수적으로 가려면:
  ```powershell
  $env:FLOW_STAGGER_SEC="10"; $env:FLOW_LANE_COOLDOWN_SEC="20"
  ```
- 이미 UNUSUAL_ACTIVITY가 뜬 계정은 **몇 분 쉬게** 두고, 실패분만 **단일 레인(`FLOW_PORTS=3847`)·concurrency 1**로 이어서 생성(build/turnaround 체크포인트가 SKIP(exists)로 완성분은 건너뜀).
- 계정 3개(3847/3848/3849)를 다 열어도, **동시에 셋이 쏘게 하지 말 것** — stagger가 시차를 주지만 concurrency로 상한도 같이 낮추면 이중 안전.

### 4-1. 실측 (2026-07-20 옹기과부 297씬 배치) — 진짜 병목은 reCAPTCHA
- **concurrency 3 + STAGGER 6s + COOLDOWN 12s로도 UNUSUAL 65씬 발생.** 결과: OK 158 / reCAPTCHA-eval-failed→UNUSUAL_ACTIVITY(403) 65 / reCAPTCHA timeout 67 / 연결끊김 6. → **스태거만으로는 부족**, 동시성 3은 무료 flow reCAPTCHA엔 여전히 과함.
- **`PUBLIC_ERROR_UNUSUAL_ACTIVITY`의 정체는 "reCAPTCHA evaluation failed"** — Google이 reCAPTCHA 토큰 신뢰점수를 낮게 매겨 반려하는 것. 계정 밴이 아니라 **봇 판정**. 일시적(쉬면 회복). 영구 밴과 구분.
- **daemon.log로 UNUSUAL 판단 금지** — daemon.log는 reCAPTCHA/SW 브리지만 찍고 **API 403은 안 남긴다**. 진짜 실패 원인은 `storyboard.built.json`의 씬별 `status`에 있다(build 종료 후). 배치 중엔 build stdout이 파일 리다이렉트 시 **블록 버퍼링**돼 0바이트로 보이니, 진행 확인은 **scenes/*.png 디스크 개수**로.
- **처방:** ① 재시도는 **concurrency 1~2**로 낮춘다 ② **Chrome Flow 탭 3개를 포그라운드/활성** 유지(백그라운드 탭은 SW가 스로틀돼 reCAPTCHA timeout 급증) + 화면 절전 끄기 ③ UNUSUAL이 뜬 직후가 신뢰점수 최저 → **몇 시간~다음날 쉬었다 재개**하면 통과율↑ ④ 하루 안에 확실히 끝내야 하면 그 프로젝트만 유료 gemini(reCAPTCHA·데몬 불필요, UNUSUAL 위험 0).
- build.py는 `storyboard.built.json` status로 **완료분 SKIP·실패분만 이어감**(체크포인트) — 며칠 나눠 돌려도 안전, `--only` 불필요.
- **레인(계정) 귀속 (2026-07-20 추가):** `flow_client.py`가 `[lane <port>]` 마커를 stdout·stderr에 찍고 build.py가 파싱해 씬별 `lane` 필드로 built.json에 기록(성공·실패 모두, live 출력에도 `lane=<port>`). → 배치 후 **"어느 계정이 UNUSUAL/거절을 받았나"를 집계 가능**(status에 실패 사유 + lane에 포트). 특정 계정만 실패가 몰리면 그 계정이 저신뢰/불안정 → 풀에서 빼면 됨. daemon.log는 3데몬이 한 파일에 섞여 찍혀 포트 분리 불가하니 **built.json의 lane 필드로 판단**.
- **build.py 동시성 캡은 settings.json `ports` 길이 기준** (env FLOW_PORTS 아님) — settings ports=[3847,3848]이면 `--concurrency 3`을 줘도 2로 자동 캡("flow 레인 N개 — 동시성 X→N 자동 캡" 출력). 반면 하위 generate_image.py는 FLOW_PORTS env로 레인 풀을 정함. **동시성(build.py)과 계정 풀(env)이 별도**임에 주의 — env로 3계정 넣어도 settings가 2면 동시 2로 돈다.

---

## 5. 업로드 메타 — 썸네일·제목·설명문 (대박 채널 벤치마킹 공식) ★2026-07-25 삼월이

**대원칙:** 업로드 직전 최신 `channels/yadam/research/scan_*.json`에서 **조회수/일(`views_per_day`) 상위**를 뽑아 실제 대박물의 썸네일·제목을 벤치마킹한 뒤 만든다. 감(感) 금지, 실측 우선. 채널 브랜드명 = **옛뜰야담**, 문의/이메일 = **yettulyadam@gmail.com**.

### 5-1. 썸네일 벤치마킹 워크플로우
- scan JSON `rows` → `views_per_day` 내림차순 상위 15 → 썸네일 다운로드(`https://i.ytimg.com/vi/{id}/maxresdefault.jpg`, 실패 시 `hqdefault.jpg`) → PIL로 라벨(순위·조회수·채널) 붙인 **콘택트시트 그리드 1장** 만들어 사용자에게 전달·같이 분석.
- ⚠️ **miniconda Windows SSL 버그**: 순수 urllib 다운로드 시 `ssl.create_default_context()`가 `[ASN1: NOT_ENOUGH_DATA]`로 죽는다(Windows 인증서 스토어 로딩). 우회 = `ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE` (공개 썸네일이라 안전).
- 다운로드 자료는 세션 임시폴더 말고 **사용자 접근 가능 폴더**(예: `D:\6.Youtube부업\1.야담\벤치마크_썸네일_YYYYMMDD\`)로 복사해 전달.

### 5-2. 썸네일 문법 (야담 대박물 실측)
- **2줄이 대세**(3줄 거의 없음). 윗줄 = 상황/설정(흰색), 아랫줄 = **핵심 반전 키워드만 형광(노랑/초록) + 제일 크게**.
- **대사 인용("…")형이 최강**(TOP7 중 절반). 특히 **부모의 수수께끼 유언형**(예 "아들아 쫄딱 망한 척하여라", 79만회)이 강력 — 죽어가는 부모의 알쏭달쏭한 말 + "왜?" 유발. 삼월이도 아비 유언형("네가 본 숫자는 절대 잊지 말거라")으로 확정.
- **호기심 갭 = 결과만 보여주고 방법/이유는 감춤**("~한 이유", "~한 한마디", "~되는데").
- **인물 2명 표정 대비 클로즈업**(한쪽 담담/한쪽 충격·식은땀).
- 폰트 = **초굵은 고딕**(검은고딕/여기어때 잘난체), 검정 외곽선 필수. 규격 1280×720, 2MB 이하.
- 넣는 곳 = `{P}/output/thumbnails/`. upload.py는 **이름 정렬 첫 PNG**를 자동 선택 — 대문자 `F`가 소문자보다 앞서니 최종본을 **`Final_...png`**로 두면 재료 파일(face_·thumb_clean)이 있어도 최종본이 잡힌다.

### 5-2-1. ★`output/thumbnails/`는 항상 만들고, 씬 이미지 후보를 미리 복사해 둔다 (사용자 지시 2026-08-04)
SCENE_IMG가 끝나면 **묻지 말고** `{P}/output/thumbnails/`를 만들고, 씬에서 뽑은 **썸네일 후보 이미지를 원본 그대로 복사**해 둔다.
- **문구를 이미지에 굽지 않는다.** 후보는 씬 png 원본 그대로 두고, 문안은 **대화로만 추천**한다(합성은 사용자가 한다).
- 파일명 규칙: `cand1_scene14_2인대비.png` 처럼 **`cand<순위>_scene<번호>_<한줄설명>`**. 추천 순위가 곧 정렬 순서가 되게 한다.
- 최종본은 사용자가 **`Final_...png`**로 넣는다 — `F`(0x46)가 `c`(0x63)보다 앞서므로 후보가 남아 있어도 최종본이 선택된다. **후보를 지울 필요가 없다.**
- 후보 고르는 기준(§5-2 순): ① **인물 2명 표정 대비**(한쪽 담담 / 한쪽 충격) ② 악역 단독 경악 클로즈업 ③ 훅 씬1(제목·콜드오픈과 통일) ④ 절정 대치. 보통 3~4장.

### 5-3. 제목 ★2026-08-12 v3.0으로 대체 — **용도형**
> **폐기**: 구 규칙은 "짧게 한 문장 후킹 + 인라인 해시태그 5개"(예: "거지 떼라 욕먹던 처녀를 며느리로 들인 시어머니의 소름 돋는 안목 #옛날이야기 …")였다. **옴니버스에서는 제목이 특정 이야기를 약속하면 안 된다** — 나머지 5편이 "다른 영상"이 되기 때문. 벤치마크 2편 모두 소재가 아니라 **용도**를 판다.

- 구조 = **`[용도 문구] + [분량 표기] | [장르 꼬리 키워드]`**, 68자 이내, 앞 40자가 용도 문구.
  > `일단 틀어놓으면 스르르 잠드는 옛이야기 여섯 편 2시간 20분ㅣ야담ㅣ옛날이야기ㅣ오디오북ㅣ수면동화`
- **꼬리 키워드는 파이프(ㅣ) 형식으로 되돌린다** — 인라인 해시태그는 "한 편을 파는" 제목에 맞는 문법이고, 용도형 제목에는 검색 키워드 나열이 맞는다(벤치 2편 모두 파이프·나열형).
- 소재 키워드는 **1개까지만** 허용(6편 중 가장 강한 편). 썸네일↔제목 통일 규칙도 적용하지 않는다 — 썸네일은 6편 중 아무 장면이나 가장 그림이 되는 것.

### 5-4. 설명문 (경쟁 채널 벤치마킹 포맷)
순서: `인사말("안녕하세요! 옛뜰야담입니다") → 📜 후킹 한 줄 → 📖 줄거리(스포 직전까지) → ⏱ 타임라인(챕터) → 🔍 역사적 배경 → 💬 댓글 유도(이야기 배경 활용, §2) → 저작권/브랜드 아웃트로 → 문의: yettulyadam@gmail.com → #해시태그 줄`.
- ⚠️**설명문은 반드시 인사말로 시작한다** (사용자 확정 2026-07-29). 구 포맷은 맨 위에 이메일을 한 번 더 넣었는데,
  유튜브 설명란은 **접힌 상태에서 첫 두어 줄만 보인다.** 그 귀한 자리를 이메일이 차지하면 후킹 한 줄이 밀려 안 보인다.
  이메일은 하단 `문의:` 줄에만 둔다(중복 금지).
- **타임라인 챕터 계산**(YouTube 자동 챕터 = 00:00 시작·3개↑·오름차순): `storyboard.json` act별 첫 씬의 `sentences[0]` idx → `_video/sentences.json['sentences'][idx].words[0].start`(원본 나레이션 실측 시각) → veo 훅을 쓴 경우에만 **오프셋 +0.833s**(§6) 더해 `MM:SS`/`H:MM:SS`. 첫 챕터만 00:00 고정.
- **★v3.0 옴니버스: 챕터 = 편.** `act: "story1"`~`"story6"`인 씬이 챕터 시작점이고, 챕터 7개(00:00 인사 + 6편)가 나온다. **챕터가 곧 목차이자 이 영상의 핵심 UX** — 자다 깬 시청자가 편을 골라 되돌아간다. 라벨은 후킹 소제목이 아니라 **편의 내용을 알려주는 담백한 제목**으로("나무꾼과 산속의 비", "며느리의 첫 밥상").

### 5-5. meta.txt 업로드 파싱 규약 (필수 숙지)
- upload.py는 **[제목](첫 줄) · [설명문] 전체 · 설명문 내 `#태그`**만 읽는다. **[썸네일 문구]·[제작 메모]는 업로드 안 됨**(내부 기록용).
- 태그 = 설명문 안 모든 `#키워드` 자동 수집 → 설명문 맨 아래 해시태그 줄을 반드시 남긴다.
- 영상이 output/ 밖(D드라이브 등)이면 `upload.py --video "절대경로"`로 지정(기본은 `{P}/output/*.mp4` 자동탐색).
- 최초 1회 인증: `python scripts/upload/auth.py --channel yadam`(브라우저 OAuth). 사전 `pip install google-auth-oauthlib google-api-python-client google-auth`. 업로드는 기본 `--privacy private`.
- ⚠️**채널 최초 업로드 함정 — OAuth가 되어도 API가 꺼져 있으면 못 올린다** (2026-07-29 혼주석 실측).
  · 증상: `token.json`이 멀쩡한데 업로드가 **HTTP 403 `accessNotConfigured`** 로 죽는다.
    메시지 = `YouTube Data API v3 has not been used in project <번호> before or it is disabled.`
    upload.py가 지수 백오프로 10회 재시도하므로 **약 13분을 통째로 날린 뒤** 실패한다.
  · 원인: OAuth 클라이언트(client_secret.json)를 만든 **GCP 프로젝트에서 YouTube Data API v3가 미활성**.
    인증(누구인지)과 API 활성화(무엇을 쓸 수 있는지)는 별개다. auth.py가 성공해도 이건 안 잡힌다.
  · 조치: `https://console.developers.google.com/apis/api/youtube.googleapis.com/overview?project=<번호>`
    에서 **사용 설정** → **몇 분 대기**(전파 시간) → 재시도. 프로젝트 번호는 에러 메시지에 찍힌다.
  · **사람만 할 수 있다** — 브라우저 콘솔 작업이라 PD가 대신 못 한다. 채널 첫 업로드 전에 미리 확인할 것.
  · 같은 GCP 프로젝트를 쓰는 다른 편도 전부 같은 이유로 실패하므로, 하나가 이 에러면 **나머지는 돌리지 말고 대기**.

## 6. veo 훅 오디오 보정 + 앞부분 갈아끼우기 ★2026-07-25 삼월이

- **veo(flow) 립싱크 훅은 원본 내레이션보다 ~8-9dB 작다**(실측: veo mean -27.4dB / 내레이션 mean -18.9dB). 그대로 붙이면 앞부분만 소리 작게 들림. → `ffmpeg -af volumedetect`로 앞 8초 vs 내레이션 구간 비교해 확인.
- **보정(전체 재렌더 불필요):** 이미 스플라이스한 최종본에 **앞 8초 오디오만 +9dB**, 영상은 스트림 복사 →
  `ffmpeg -i spliced.mp4 -c:v copy -af "volume=volume=2.818:enable='lt(t,8.0)'" -c:a aac -b:a 192k -ar 44100 -ac 2 -movflags +faststart out.mp4`(오디오만 재인코딩 → 몇 분). +9dB 후 veo peak -12.1dB→-3dB로 클리핑 없음.
- **앞부분 갈아끼우기(원본 이미 CapCut 추출 완료 시 재렌더 회피):** veo 8초 + 원본[콜드오픈 이후]를 concat **필터**로 재인코딩(스트림 복사는 키프레임이 7.167s에 안 맞아 불가). veo가 콜드오픈 7.167s를 대체 → 이후 전 구간 시간축 **+0.833s** 시프트(= 8 − 7.167). 타임라인 챕터(§5-4)에 이 오프셋 반영.
- **CRF 재인코딩 용량 감소는 정상**: CapCut 원본(~9.7Mbps, 10.3GB)을 x264 CRF18로 재인코딩하면 ~4.8Mbps(5.2GB)로 절반. 정지이미지+자막 위주라 육안 무손실, 게다가 유튜브가 어차피 재압축 → 화질 손실 아님, 업로드도 빨라짐.

### 6-1. ★전체 재인코딩 하지 말 것 — 앞 10초만 굽고 나머지는 스트림 복사 (2026-08-04 실측)
§6의 "concat 필터로 전체 재인코딩"은 **76분 영상에서 70분 이상 걸리고, 백그라운드 작업이 중간에 죽으면 통째로 날아간다.** 실제로 당했다 — 32분(43%) 지점에서 잘려 `moov atom not found`로 1GB 쓰레기만 남았다. **전량 재인코딩은 이제 쓰지 않는다.**

**대신: 스플라이스 지점 다음 키프레임까지만 재인코딩하고, 그 뒤는 `-c copy`.** CapCut 출력은 **키프레임이 5초 간격**이라 손해가 거의 없다.

```bash
# 1) 키프레임 확인 (7.2s 다음 키프레임 = 10.0s)
ffprobe -v error -select_streams v:0 -skip_frame nokey \
  -show_entries frame=pts_time -read_intervals "%+60" -of csv=p=0 원본.mp4

# 2) head = veo(8.0s) + 원본[스플라이스지점 → 다음 키프레임]  ★원본 코덱 파라미터에 맞춘다
ffmpeg -i veo.mp4 -ss 7.200 -to 10.000 -i 원본.mp4 -filter_complex \
 "[0:v]setpts=PTS-STARTPTS,fps=30,scale=1920:1080,setsar=1[v0];[0:a]asetpts=PTS-STARTPTS,aresample=44100[a0];\
  [1:v]setpts=PTS-STARTPTS,fps=30,scale=1920:1080,setsar=1[v1];[1:a]asetpts=PTS-STARTPTS,aresample=44100[a1];\
  [v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" \
 -c:v libx264 -profile:v high -level 4.0 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
 -preset slow -crf 17 -c:a aac -b:a 192k -ar 44100 -ac 2 -video_track_timescale 30 -y _head.mp4

# 3) concat 데먹서 + inpoint 로 이어붙이기 (스트림 복사 — 5.6GB 임시파일 불필요)
printf "file '_head.mp4'\nfile '원본.mp4'\ninpoint 10.0\n" > _concat.txt
ffmpeg -f concat -safe 0 -i _concat.txt -c copy -movflags +faststart -y 최종_hook.mp4
```

- **실측: 70분+ → 8분.** (head 인코딩 수십 초 + 스트림 복사 8분, 5.5GB)
- **`inpoint`가 핵심** — concat 데먹서가 파일별 시작점을 받으므로 뒷부분을 따로 잘라낼 필요가 없다.
- **코덱 파라미터를 반드시 원본에 맞춘다** (`ffprobe`로 profile/level/pix_fmt/sample_rate 확인). 특히 **오디오 샘플레이트** — CapCut 출력은 44100Hz인데 Veo 클립은 48000Hz라 head에서 `aresample=44100`으로 맞추지 않으면 concat 복사가 깨진다.
- 길이 검산: `head길이 + (원본길이 − inpoint)`. 오차 수십 ms는 오디오 프레임 정렬이라 정상.
- 부수 효과: **원본을 다시 굽지 않으므로 화질 손실이 앞 10초 외에는 0**이고 용량도 그대로다(§6의 "절반으로 준다"는 전량 재인코딩 때 이야기).
- ffmpeg/ffprobe = `C:\miniconda\Library\bin\` (PATH 아님, 앞세워야 함).

---

## 7. VEO 훅 클립 ↔ 낭독 음량 통일 (필수 — 안 하면 훅만 튐)

VEO 립싱크 클립은 **자체 네이티브 오디오**라 Vrew 낭독과 라우드니스가 다르다. 그대로 씬1에 주입하면 **훅만 갑자기 크거나 작게** 들려 시청자가 초반에 이탈한다.

- **실측 (2026-07 옹기과부, flow veo-fast):** VEO 클립 **-23.4 LUFS** vs Vrew 낭독 **-15.5 LUFS** → 클립이 **~8 LUFS(≈8dB) 더 조용**. veo-fast 클립은 낭독보다 조용하게 나오는 경향.
- **규칙:** capcut 주입/렌더 전에 **VEO 클립 오디오를 낭독(`{V}/audio.mp3`)의 통합 라우드니스에 맞춘다.** 목표는 낭독 LUFS(측정값) 또는 유튜브 기준 **-14 LUFS**로 **둘 다** 통일.
  - 측정: `ffmpeg -i <파일> -af ebur128=peak=true -f null -` → `Integrated loudness I:` 확인.
  - 보정(클립을 낭독에 맞추기): `ffmpeg -i veo_hook_scene01.mp4 -af loudnorm=I=-15.5:TP=-1.5:LRA=11 -c:v copy veo_hook_scene01_norm.mp4` (I=낭독 실측값). 또는 단순 게인 `-af volume=+8dB`.
  - **주입 전에 정규화본으로 교체**하거나, capcut에서 씬1 클립 볼륨을 +Δdb 조정.
- **순서 주의:** 낭독 `audio.mp3`가 만들어진 뒤(ingest 후) 그 LUFS를 기준으로 클립을 맞춘다. 클립을 먼저 뽑았으면 ingest 후 보정 → 그 다음 veo_hook 재실행(주입).

## 8. VEO 클립 규격 자동 맞춤 (Veo는 24fps·720p로 나온다)

**Veo 출력 규격은 우리가 못 정한다** — Veo 모델이 **네이티브 24fps**로 뽑고(gemini든 flow든 30fps 불가), **flow veo-fast는 720p** 고정(gemini API는 resolution=1080p 지정 가능하나 GEMINI_API_KEY 필요). 그래서 클립이 프로젝트(보통 1080p/30fps)와 어긋난다.
- **증상:** 규격 불일치 클립을 CapCut이 미리보기에서 실시간 업스케일+프레임변환하다 **불안정 환경에서 재생 순간 죽는다**(옹기과부 2026-07 실측 — 720p/24fps 클립).
- **처방(내장, 2026-07-26):** `veo_hook.py`가 **생성 직후 `settings.json render`(width/height/fps)로 자동 재인코딩**(`conform_to_render`, ffmpeg scale+fps, 음량 불변). 이미 맞으면 생략(idempotent). `--no-conform`으로 끔. ffmpeg/ffprobe PATH 필요.
- Veo가 처음부터 30fps 생성은 불가 → **"생성은 Veo 규격 → 파이프라인이 렌더 규격으로 변환"이 정답.** (24→30은 프레임 복제라 8초 훅엔 무영향)

## 9. ⚠️ VEO 클립을 CapCut 드래프트에 자동 주입하지 말 것 (Windows export 크래시)

**capcut_export의 veo 콜드오픈 자동 주입(씬1 video_path + 오디오 트림 + 클립/스틸 분할)은 Windows CapCut을 죽인다.** 조건부가 아니라 **무조건 금지**다 — 아래 2차 실측으로 확정됐다.

### 9-0. ★2차 실측으로 확정 (2026-07-29 놋골무) — 규격·엔진 문제가 아니다
1차(옹기과부 2026-07-26)는 **flow 엔진 720p/24fps** 클립이라 "규격 불일치가 원인 아니냐"는 가설이 남아 있었다. 놋골무에서 그 가설을 **정면으로 시험했고 기각됐다**:
- 조건: **gemini 엔진**(`veo-3.1-lite-generate-preview`) · **1080p 네이티브** · `conform_to_render`로 **1920×1080/30fps 재인코딩 완료** · 낭독에 맞춰 **−14.4 LUFS 정규화 완료**. 즉 규격·음량 결함이 하나도 없는 클립.
- capcut_export는 정상 종료했고 로그도 깨끗했다 — `veo 콜드오픈: 클립 8.0s 자체 오디오 사용, 대사 큐 3개 리타이밍, 이후 자막 -0.44s 시프트`.
- 그런데 **CapCut에서 열자 또 창이 꺼졌다.**
- **결론: 원인은 클립 규격도 엔진도 아니고, 주입된 드래프트 구조(클립+스틸 분할 트랙, 오디오 트림) 자체다.** 엔진이 무엇이든, 규격을 아무리 맞춰도 주입하면 죽는다. 더 시도하지 말 것.
- 부수 관찰: 크래시 뒤 **CapCut 좀비 프로세스가 10개 남는다.** 그대로 다음 export를 돌리면 `root_meta_info.json`이 꼬이므로 `Get-Process *CapCut* | Stop-Process -Force`로 정리하고, **새 이름**으로 재생성할 것(크래시 세션 캐시 격리).

- **처방:** RENDER 시 **씬1 video_path를 제거(None)하고** capcut_export 실행 → **veo 주입 없는 드래프트**(스틸 씬1). 그러면 삼월이와 동일 구조라 export 정상.
  - `{V}/storyboard.json` 씬1 `video_path=null` 로 세팅 후 capcut_export (출력에 "veo 콜드오픈" 안 뜨면 성공).
- **veo 훅은 사용자가 CapCut에서 수동 추가**: `{V}/veo_hook_scene01.mp4`(규격·음량 맞춤 완료)를 타임라인 맨 앞에 얹고, 그 구간 내레이션은 음소거/트림. 자막 선두 큐는 클립 대사에 맞춰 둔다(옹기과부는 이미 "저것이…").
- veo_hook.py의 클립 생성·규격맞춤·음량맞춤은 그대로 쓰되, **capcut 주입만 건너뛴다**(추후 Windows 검증되면 자동 주입 복구 검토).

**★2026-07-29 갱신 — 수동 삽입도 크래시한다. CapCut에는 veo 클립을 아예 넣지 말 것.**
혼주석에서 gemini(Veo 3.1 Lite, 1920×1080/30fps로 규격 변환 완료)로 뽑은 클립을 **사용자가 CapCut 타임라인에 직접 얹었는데도 창이 그대로 꺼졌다.** 즉 문제는 `capcut_export`의 주입 방식이 아니라 **CapCut Windows가 이 클립을 타임라인에 올리는 것 자체**다. 규격(1920×1080/30fps/AAC 48k)을 맞춰도 마찬가지.

- **확정 워크플로우 = 후처리 스플라이스.** CapCut 드래프트는 **끝까지 veo 없이 스틸만**으로 두고, 사람이 CapCut에서 mp4를 내보낸 **뒤에** ffmpeg로 앞부분을 갈아끼운다(§6).
- `veo_hook.py` 실행 후 **렌더 storyboard 씬1의 `video_path`를 반드시 다시 `null`로 되돌릴 것** — 안 그러면 나중에 `capcut_export`를 재실행할 때 주입이 살아난다.
- 스플라이스 지점은 **훅 대사를 덮는 선두 큐들의 끝 시각**이다(`subtitle.srt`에서 확인). 혼주석 실측: 큐1~3이 0.000~6.100s(`"한 번만…"`/`"우리 아버지인 척 해주세요"`/`"오늘 하루만요."`)였고 클립이 8초라 **이후 전 구간 +1.900s 시프트**.
- 시프트 값은 **§5-4 타임라인 챕터 계산에 반드시 반영**한다.
- 스트림 복사(`-c copy`)는 키프레임이 안 맞아 불가 → concat **필터**로 재인코딩(CRF18). 용량이 절반으로 줄어드는 건 정상(§6).
- **훅 8초 구간의 자막**: 원본 앞 6.1초를 잘라내므로 CapCut이 구워 넣은 선두 자막도 함께 사라진다. 클립 프롬프트가 `no subtitles`라 훅에는 자막이 없게 된다 — 필요하면 스플라이스 전에 클립에 직접 구워 넣을 것.

## 10. VEO 훅 대사 커스터마이즈 (유튜브 수위 조절)

훅 대사는 **`{V}/veo_hook_prompt.txt`의 따옴표 대사가 진실**이다(대본 첫 대사와 달라도 됨). `veo_hook.py`는 매니페스트 `dialogue`를 **프롬프트에서 추출**(대본 재추출로 덮어쓰지 않음, 2026-07-26 수정) → PD가 프롬프트 대사를 다듬으면 클립 발화 + capcut 콜드오픈 매칭 기준이 그걸로 간다.
- **유튜브 리스크:** 욕설("년" 등)이 **첫 7초 음성/자막·제목·썸네일**에 오면 수익화(노란딱지)·연령제한 위험(밴은 서사 맥락이라 거의 없음). → **VEO 클립 대사만 수위 낮추고**(본문 나레이션은 유지 가능), 제목·썸네일엔 욕설 금지.
- **수위 조절 시 3곳을 함께 맞춰라** (콜드오픈 매칭·자막 정합): ① `veo_hook_prompt.txt` 대사 ② `{V}/subtitle.srt`의 그 대사를 덮는 선두 큐(들) 텍스트 — **큐 개수·타이밍은 그대로, 텍스트만** 교체(개수 바뀌면 씬 매핑 밀림) ③ `veo_hook.json`의 `dialogue`(veo_hook 재실행하면 프롬프트에서 자동 반영). 셋이 일치해야 capcut가 `veo 콜드오픈: … 자체 오디오 사용`으로 조립(불일치 시 `⚠️ 매칭 실패 — 음소거 클립 폴백`).

## 11. CapCut 데이터는 exFAT 외장/정션에 못 둔다

CapCut `User Data`(드래프트+캐시)를 **exFAT 외장하드로 옮기거나 정션(junction)** 걸면 **"비정상적인 모듈 충돌"로 실행 즉시 죽는다**(CEF 등이 exFAT의 파일잠금·권한을 못 씀, 옹기과부 2026-07 실측). 정션 대상이 exFAT면 특히 위험.
- **캐시를 외장으로 빼려면 외장이 NTFS여야 한다**(exFAT면 불가 — 포맷 필요, 데이터 삭제 주의).
- **최종 mp4 내보내기 destination은 exFAT 외장 OK**(큰 단일 파일은 exFAT도 지원). 캐시는 C:(NTFS)에 두고 편집 후 CapCut 캐시 정리, 최종본만 외장으로.
- 드래프트 삭제로 C: 확보 시: 그 프로젝트의 **최종 mp4가 외장/업로드에 있는지 먼저 확인**(없으면 편집본 유실). 이미지+오디오 프로젝트는 영상 푸티지물보다 편집 캐시가 훨씬 가볍다.

---

## 12. 자막 = 폰트 10 고정 + 줄넘김 안 나게 짧게 쪼갠다 (사용자 확정 2026-07-26)

- **자막 폰트 크기 = 10** (`settings.capcut.subtitle.font_size=10`) — 앞으로 모든 야담 프로젝트 기본. (자세한 위치는 §13.)
- **폰트 10에서 한 줄은 ~20 display자(공백 포함)까지** 들어간다(폰트7=29자 fit → 10=~20자, 옹기과부 실측 기반 추정). 그 이상이면 2줄로 넘어감.
- **자막은 폰트 10에서 줄넘김이 안 나도록 짧게 쪼갠다** → `settings.subtitle.max_chars`(split_long_cues용, **비공백 글자수** 기준).
- **★확정값 = 13** (2026-08-02, 사용자 지시). 아래는 이름석자 대본 **834문단 전수 시뮬레이션 실측**이다(`chunk_text`를 대본에 직접 돌려 display 칸수를 잰 것):

  | max_chars | 큐 수 | **최장** | 평균 | 20칸 초과 |
  |---|---|---|---|---|
  | 12 | 2,262 | 18칸 | 11.3 | 0 |
  | **13 ★확정** | **2,094** | **20칸** | **12.3** | **0** |
  | 14 (구 권장) | 1,934 | **21칸** | 13.4 | 1 |
  | 20 (코드 기본) | 1,459 | 29칸 | 18.0 | 321 |

  - 폰트 10 한 줄 용량은 **~20칸**(`line_max_width` 0.9 반영 시 ~22칸). 14는 최장 21칸이 나와 **경계선을 넘는다** — 그래서 13으로 내렸다.
  - **폰트를 11 이상으로 올리면 12로 다시 내릴 것.** 반대로 폰트 9 이하로 내리면 15~16까지 올려도 된다.
  - 88분 기준 큐 2,094개 = 분당 24개(2.5초에 하나). 수면 콘텐츠 속도로 무리 없다.
- **⚠️ Vrew 화면의 줄넘김은 최종 자막이 아니다** (2026-08-02 사용자 문의). `--export-script`는 **대본 한 문단 = 한 줄**로 내보내므로 Vrew가 그걸 클립 하나로 잡아 제 미리보기에서 접는다. 최종 자막은 **ingest 후 `split_long_cues`가 다시 쪼갠 결과**다. Vrew에서 두 줄로 보인다고 설정을 건드릴 필요 없다 — 판단은 반드시 **split_long_cues 산출물(`subtitle.split.srt`)** 이나 CapCut 드래프트로 한다.
  - 검사 스니펫: `chunk_text(줄, max_chars)`를 vrew_script에 직접 돌려 `max(len(c))`를 재면 생성 전에 미리 알 수 있다.
- **적용 시점:** split_long_cues 단계(자막 분할)에서 max_chars가 반영되므로, **미래 프로젝트는 자동 적용**. 이미 분할된 프로젝트(옹기과부 등)는 재분할해야 반영되지만 — **옹기과부는 그냥 진행**(20자 분할·폰트10, 긴 줄 2줄 허용, 사용자 지시).

## 13. 자막 스타일 설정은 `settings.capcut.subtitle` (함정)

**자막 폰트 크기·색·외곽선·배경은 `settings.json`의 `capcut.subtitle` 블록에 있다** (capcut_export.py 1658행 `settings.get("capcut")` → 803행 `capcut_config.get("subtitle")`). **최상위 `settings.subtitle`이 아니다** — 그건 `max_chars`(자막 20자 분할)·`fps`용으로 split_long_cues/scene_timing이 쓴다.
- 폰트 키우려면 `capcut.subtitle.font_size` 수정 (옹기과부 실측: 기본 7.0 → 10.0). `settings.subtitle.font_size`를 고치면 **아무 효과 없다**(2026-07-26 삽질).
- 같은 블록: `text_color`(#FFFFFF) · `border_color`(#000000) · `border_width`(0.08) · `background_alpha`(0.0=배경없음, 검은배경 원하면 0.7).
- **`line_max_width` = 자막 박스 가로 폭**(캔버스 대비 비율, capcut_export 텍스트 material의 `line_max_width` 필드). 기본 0.82(=폭 82%, 양쪽 각 9% 여백)라 자막이 화면 끝단까지 안 간다. **야담 채널은 0.9로** 넓힘(여백 5%씩, 양쪽으로 살짝 확장 + 줄넘김↓, 사용자 지시 2026-07-26). 더 넓히려면 값↑(단 1.0 넘지 말 것). 코드는 `cfg.get("line_max_width", 0.82)`로 설정 반영.
- **바꾼 뒤 반드시 드래프트 검증**: `draft_content.json`의 `materials.texts[0].content` 안 `"size"` 값이 바뀌었는지 확인(안 바뀌면 엉뚱한 블록 고친 것).

## 14. 멀티파트 Vrew 병합 — 파트 경계 자막 겹침 (해결됨)

멀티파트 낭독(vrew_script_partNN)을 ingest가 이어붙일 때, **프레임 스냅·오프셋 반올림으로 앞 파트 마지막 자막이 다음 파트 첫 자막과 수 프레임 겹칠 수 있다**(옹기과부 2026-07-26: part3↔4 경계 5120초에서 0.07s 겹침 → 자막 2개가 잠깐 동시 표시). 파트 수만큼 경계가 있어 **모든 멀티파트 프로젝트의 잠재 이슈**.
- **처방(내장 2026-07-26):** `ingest_vrew.py`가 병합 후 **겹침 자동 제거**(앞 큐 end를 다음 큐 start로 트림). 미래 프로젝트는 자동 해결. 이미 만든 subtitle.srt는 한 번 클램프 재적용 필요(앞 큐 end 트림).
- 확인: subtitle.srt에서 `cue[i].start < cue[i-1].end`인 쌍이 없어야 함.

## 15. 캐릭터 일관성 3종 — 턴어라운드 구도 + 씬 negatives + 동일인물 지시 ★2026-07-26 사용자 확정

**깃풀로 날아갈 수 있는 코드 수정이므로 여기에 기록.** `turnaround.py` / `build.py` 두 파일. 아래가 사라졌으면 다시 넣을 것.

### 15-1. 턴어라운드는 **허리 위(waist-up) 4뷰**가 기본 — 기준 이미지 = soha_turnaround
출력이 **1344×768 고정**이라 4뷰로 나누면 한 칸이 **336px**뿐이다.
- **전신 4뷰 → 얼굴 세로 ~90px** = 홍채·속눈썹이 물리적으로 안 그려진다(어떤 프롬프트를 써도 밋밋).
- **허리 위 4뷰 → 얼굴 ~250px** = 세로 2.7배, **면적 7배**. 실측으로 확연히 좋아짐.
- 근거: 씬 100장 내내 시청자가 추적하는 건 **얼굴**이고, 옷·색은 lock 텍스트로 잠글 수 있다. **통제하기 어려운 쪽에 픽셀을 몰아준다.**

**구현:** `turnaround.py`의 `FRAMING` dict + `turnaround_prompt(..., framing="waist")`. 기본값 `waist`.
```python
FRAMING = {"waist": "four WAIST-UP views ... the FACE IS LARGE ...", "full": "four FULL-BODY views ..."}
```
**예외 — `characters.json`에 `"framing": "full"`** 을 넣으면 그 인물만 전신:
- anchorProp이 **하반신**에 있는 인물(발목에 맨 색 끈 등 — 허리 위로 자르면 앵커가 사라진다)
- **실루엣 자체가 앵커**인 인물(삼월이 "가장 작고 마른 실루엣")
- variant별로도 지정 가능(`variants.<v>.framing`).

### 15-2. 씬 프롬프트에 **인물별 negatives**를 넣는다 (기존엔 턴어라운드에만 걸렸음)
`build.py`가 예전엔 `visual_desc + style.preset + style.negative`만 조립해서, **`negatives`가 씬 100장에 하나도 안 걸렸다.** 턴어라운드 1장만 방어되고 씬은 무방비 → 아이가 성인으로, 마님이 젊고 날씬하게 드리프트.

**★뭉쳐서 붙이면 안 된다 (실제로 겪은 버그).** 씬 끝에 전 인물 negatives를 한 줄로 몰면 늙은 마님의 `not young`과 젊은 하인의 `not old`가 같이 들어가 **서로 충돌**한다. → **인물별로 lock 바로 뒤 괄호에** 붙인다:
```python
who = r["lock"] + (f" ({', '.join(negs)})" if negs else "")
desc = desc.replace("{" + r["base"] + "}", who)
```
variant 우선순위는 turnaround와 동일(`variants.<v>.negatives` > 캐릭터 레벨).

### 15-3. ref를 붙이는 것만으로는 부족 — **"같은 얼굴로 그려라" 지시**를 씬에 넣는다
턴어라운드 ref를 첨부해도 프롬프트에 `identical`·`reference`·`same face`가 **한 마디도 없었다**(옹기과부 씬 297개 전수 확인). 모델은 ref를 참고 자료로만 쓰고 얼굴 유지율이 떨어진다. `build.py`에서 ref가 있을 때만 추가:
> The attached character sheet(s) are the definitive reference for the people in this scene — render each character with the **SAME face, hairstyle, body proportions and outfit** as their reference sheet. **Same person, not a look-alike.**

`anchorProp`도 씬에 재확인시킨다(`Keep these identifying features clearly visible: ...`) — 보통 lock에 녹여 쓰지만 누락된 프로젝트가 있어 안전망.

**★게이트는 `ref_paths`가 아니라 `char_refs`(인물 시트 수)로 걸 것 — 실제로 낸 버그.**
`ref_paths`에는 **location sheet(배경 시트)도 섞여 있다.** 게이트를 `if ref_paths`로 걸면 `cast: []`인데 배경 시트만 붙은 씬에도 "render each character with the SAME face"가 발화한다. 옹기과부 297씬 중 **31씬(10.4%)** 이 해당했고, 그중 씬8은 `visual_desc`가 **"No people"** 인 무인 establishing shot인데 바로 뒤에 "the people in this scene"이 붙었다 — 의도적으로 비운 컷에 인물이 끌려 들어온다.
```python
char_refs = 0
...
    if p.exists(): ref_paths.append(str(p)); char_refs += 1     # 인물 시트만 카운트
ref_paths = ref_paths[:max_refs]
char_refs = min(char_refs, len(ref_paths))                      # 캡에 잘린 경우 보정
identity = (...) if char_refs else ""                           # ← ref_paths 아님
```
수정 후 재검증: 오발화 31 → **0**, cast 있는 씬 260 = identity 방출 260.

### 15-4. 검증 방법 (수정 후 반드시)
```powershell
python scripts/assets/turnaround.py <프로젝트> --only <id> --dry-run   # 프롬프트에 WAIST-UP 있는지
```
`build.py`는 dry-run이 프롬프트를 파일로 쓰므로, cast 2명 이상인 씬의 `scenes/_pNN.txt`에서 확인:
- 인물마다 `(not ..., not ...)` 괄호가 **각각** 붙었는가 (한 줄로 뭉쳐 있으면 15-2 버그)
- `Same person, not a look-alike` 가 있는가
- **`cast: []`인 씬에 `Same person...`이 붙지 않았는가** (붙으면 15-3의 게이트 버그)
- 옹기과부 297씬 회귀 결과(2026-07-26 최종): 정상 조립 297 / negatives 누락 0 / identity 오발화 0.

**기타 방어 (2026-07-26 검증에서 추가):**
- `turnaround.py`의 framing 값은 `full`/`FULL`/`full-body`/`full_body`/`fullbody`를 모두 흡수하고, 모르는 값이면 **stderr 경고 후 waist**로 간다(조용히 흡수하면 하반신 앵커가 소리 없이 잘린다).
- `turnaround.py`의 `run()`은 try/except로 감쌌다 — 인물 하나의 잘못된 필드가 배치 전체를 죽이면 **이미 과금된 다른 인물의 결과 보고까지 통째로 유실**되기 때문.

### 15-5. 미형(예쁨)은 style.json이 아니라 **인물 lock**에 넣는다
- style.json에 `beautiful`을 박으면 **악역·노인·거지까지 미형**이 되어 인물 구분이 무너진다.
- 반대로 **실사 방향으로 밀면 얼굴이 평범해진다** — `semi-realistic`, `realistic anatomy`, `photographic` 계열 어휘는 미형을 깎는다. **웹툰 양식화 자체가 미형 장치**(큰 눈·작은 코·또렷한 선·셀 음영).
- 주연 lock에 넣을 어휘: `strikingly beautiful` / `large luminous almond eyes with long lashes and crisp catchlights` / `clear fair skin with subtle blush` / `small straight nose and soft full lips`. 남주는 `handsome` + 날카로운 턱선·높은 콧대.
- **남녀 lock의 서술 밀도를 맞출 것** — 남자 lock에 눈·피부 묘사를 빼먹으면 여자만 예쁘게 나온다(2026-07-26 실측).

## 16. 분량 = 140분 · 옴니버스 6편 · 씬 112장 (사용자 확정 2026-08-12)

> **⛔ 이 절의 씬 수치는 폐기됐다 (2026-08-22).** 씬 예산은 러닝타임 × 0.8이 아니라 **구간별 간격(계단 밀도)**으로 뽑는다 — script-guide §9-1이 현행이다. 편성도 05편부터 3편 × 45분으로 바뀌었다. 아래는 6편 × 23분 시절의 기록으로만 읽을 것. ("★SKILL.md보다 우선" 표기도 이 절에 한해 해제한다.)

**v3.0 수면 옴니버스 전환으로 90분 단일 서사에서 140분 6편 옴니버스로 바뀌었다.**

| | 구 확정값(90분 단일) | **현 확정값(v3.0)** |
|---|---|---|
| 영상 길이 | 90분 | **140분 (2:20:00)** |
| 구성 | 단일 대하 서사 1편 | **독립 단편 6편 × 23분** |
| 대본 분량 | 2.5만자 | **37,000자** (1편 5,400 + 2~6편 6,300×5 + 인사 100) |
| 낭독 속도 | 280자/분 | **265자/분** (Vrew 속도 한 단계 하향) |
| 총 씬 수 | ~90씬 | **112장** (1편 16 + 2~6편 19×5) |

### ★★낭독 속도 — 자사 실측은 280자/분이다 (반드시 읽을 것)

| 편 | 공백 제외 | 실제 낭독 | 실측 속도 |
|---|---|---|---|
| 이름석자 (2026-08-02) | 21,035자 | 76.3분 | **276자/분** |
| 흰종이 (2026-08-12) | 21,368자 | 75.5분 | **283자/분** |

- **두 편이 같은 값을 냈다 — 자사 Vrew 기본 속도 = 약 280자/분.** 240자/분은 이 사용자에게 맞지 않는다.
- v3.0의 계획값 **265자/분은 벤치마크 ①(264자/분) 실측치**이며, 수면 톤에 맞춰 **의도적으로 기본보다 느리게** 잡은 값이다. **낭독 전에 Vrew 속도를 한 단계(약 0.95배) 낮춰야 한다.**
- **속도를 안 낮추면**: 37,000자 ÷ 280 = **132분(2:12)** — 목표보다 8분 부족. 그때는 대본을 **39,200자**(편당 6,600자)로 잡는다.
- 어느 쪽으로 갈지 **REVIEW에서 확정**하고 meta.txt 제작 메모에 적는다. **1편 낭독 직후 실측 속도를 재계산해 2~6편 분량에 반영**한다.
- `validate_script.py` 값: 전체 `--target 36000,38000 --cpm 265`, 편별 `--chapter-target 5300,6400 --cpm 265`.

### 씬 예산

- **112장 = 러닝타임(140분) × 0.8.** 한 장당 약 75초. 벤치마크는 5.1~6.0컷/분(593~854장)으로 훨씬 촘촘하지만, **밀도-조회수 무관 실측**(자사 23편 상관 +0.09)과 비용을 근거로 저밀도를 유지하기로 확정했다.
- **★v3.0: "앞이 촘촘하고 뒤가 성긴 기울기"(구 §34)는 폐기.** 콜드 오픈이 없어졌고 벤치 2편 모두 밀도 곡선이 평탄했다. 편별로 균등하게 19장씩 주고, 편 안에서만 완만히 기울인다(②우연한 사건 4장 ↔ ⑦⑧⑨ 각 1장 — script-guide §9).
- **코드 제한이 아니다** — `build.py`는 storyboard.json에 든 만큼 다 뽑는다. STORYBOARD 단계에서 PD가 지키는 규칙이다.
- **전 씬 Ken Burns가 저밀도의 전제**다(CapCut 마무리 편집에서 반드시 적용).
- 이미지 비용 감각: 씬 112장 + 턴어라운드 12~24장 + 배경 6장 ≈ **140장 × 약 55원 ≈ 7,700원** (나노바나나1 기준).

## 17. 씬 톤은 `scene_preset` — 턴어라운드 톤과 분리돼 있다 ★2026-07-26 확정

**턴어라운드(흰 배경 평면 시트)와 씬(조명·입체감 필요)은 필요한 렌더링 어휘가 다르다.** 그런데 style.json은 원래 `preset` 하나를 셋 다(turnaround/background/build)에 붙였다. 씬용 어휘를 넣으면 확정된 시트 톤이 깨지므로 **필드를 분리했다.**

| 필드 | 누가 읽나 | 확정 근거 |
|---|---|---|
| `preset` / `negative` | turnaround.py, background.py | 소하 턴어라운드 |
| **`scene_preset` / `scene_negative`** | **build.py만** | `_soha_scene_v2.png` |

`build.py`: `preset = style.get("scene_preset") or style["preset"]` — 없으면 기존대로 폴백하므로 다른 채널은 영향 없음.

**scene_preset 작성 시 절대 규칙 두 가지 (둘 다 실제로 당한 것):**
1. **조명 방향·시간대를 넣지 말 것.** `chiaroscuro`, `deep falloff shadows`, `film-still color grading`을 넣었더니 **모든 씬이 밤으로 끌려갔다**(v3·v5 실측). 시간대·광원은 씬별 `visual_desc`가 정한다. scene_preset에는 "빛이 얼굴을 어떻게 조각하는가"(콧대 그림자·광대 볼륨·턱밑 음영·터미네이터)만 쓴다.
2. **후광 금지 문구를 반드시 넣을 것.** `a bright silver-white edge tracing the crown`류를 쓰면 머리·어깨 실루엣 전체에 흰 테두리가 둘러져 **후광처럼 보인다**(사용자 지적). `no glowing white outline around the figure, no halo or aura, no backlit silhouette glow, no bloom`을 scene_negative에 유지.

또한 scene_negative의 **`Eyes must not be solid black blobs without iris detail`** 이 눈을 검은 덩어리에서 벗어나게 한 핵심 문구다 — 빼지 말 것.

## 18. 제목·썸네일 규칙 + 편 도입 (★2026-08-12 v3.0으로 대체)

> **폐기됨**: 아래 18-1/18-2 원문은 "썸네일이 판 그림을 콜드 오픈 20~30초 안에 박아라 / 훅 다음 10분 설명 금지"였다. **v3.0에서 콜드 오픈·약속 장면 앵커가 폐기되고 제목이 특정 장면을 팔지 않게 되면서 전제가 통째로 사라졌다.** 근거: `channels/yadam/research/proposal_20260812.md`.

### 18-1. 제목은 소재가 아니라 용도를 판다 (현행)
벤치마크 실측: `듣기만해도 스르르 잠이드는 옛이야기|귀가 심심할땐 옛이야기|민담|오디오북|전래동화` / `일단 틀어놓으면 스르르 잠이 오는 옛날 이야기 3시간 연속 | …`
- 구조 = **`[용도 문구] + [분량 표기] | [장르 꼬리 키워드]`**. 앞 40자가 용도 문구.
- **분량을 숫자로 밝힌다**("2시간 20분 연속", "옛이야기 여섯 편") — 자는 사람에게 길이는 스펙이다.
- 꼬리 키워드 `ㅣ야담ㅣ옛날이야기ㅣ오디오북ㅣ수면동화ㅣ수면유도`를 매 편 동일 형식으로. 총 68자 이내, 말줄임표 금지.
- 소재 키워드 1개는 넣어도 된다(6편 중 가장 강한 편의 것). 그 이상은 안 된다 — 제목이 특정 이야기를 약속하는 순간 나머지 5편이 "다른 영상"이 된다.
- **썸네일은 6편 중 아무 장면이나 가장 그림이 되는 것으로.** 제목이 장면을 약속하지 않으므로 **일치 검사 항목 자체가 없다.**

### 18-2. 편 도입 — §1 참조 (현행)
콜드 오픈이 없으므로 "첫 10분 이탈 방어"도 없다. 편마다 3문장 안에 인물·처지·결핍을 주고 "그러던 어느 날"로 사건에 들어간다(script-guide §3). **1편만 다른 편보다 짧게**(5,400자) 잡아 첫 20분에 완결감을 준다 — 구 "1장을 70~80%로" 규칙이 여기로 옮겨 왔다.

<details><summary>구 v2.3 원문 (참고용 — 단일 대하 서사 전용)</summary>

18-1: 제목·썸네일 핵심 명사구를 3~4번째 문단에 그림으로 박는다. 놋골무 v3에서 "잠든 척 시험하는 대감"이 6번째 문단에 말로만 스쳐 v4에서 4번째로 이동.
18-2: 브릿지 2문장 상한 / 1장은 사건으로 연다 / 1장을 표준의 70~80%로 / 1장 끝 대사 클리프행어 / 후렴 1회 소진. 근거는 황도야담 `riUpGgMw0O0`이 훅 직후 7분을 배경 나열로 소진해 곡선이 평평했던 것.
</details>

### 18-3. OUTLINE 검수 체크리스트 (DRAFT 진입 전 PD가 자문) ★v3.0

**편성 전체**
1. 6편 편성표(감정축 / 도입형 / 주인공 / 결핍 / 사건 촉발 / 해결 주체)가 다 채워졌는가?
2. **감정축 3연속 금지 / 도입형 3연속 금지 / 기이 최대 1편 / 해결 주체 같은 것 2편까지**를 지키는가?
3. 주인공 신분·연령이 **최소 4종**, 결핍이 **최소 4종**인가? (6편이 다 "가난한 총각"이면 반려)
4. 해결 주체가 6편 다 "관아·귀인"으로 고정되지 않았는가? — 응징은 외부가 하되 **그 외부를 불러온 것은 주인공의 행동**이어야 한다.
5. 인물 이름·지역·닫는 정형구가 6편 사이에 겹치지 않는가?
6. **자산 견적** — 편당 턴어라운드 대상 2~4명인가? 합계 12~24장, 배경 6장 안인가? (넘으면 인물 많은 편을 교체)
7. 제목이 **용도형**이고 꼬리 키워드 포함 68자 이내인가?
8. `topic_log.json` 최근 편과 4축 중 **2축 이상 겹치는 편이 없는가**?

**편별 (6편 각각)**
9. 첫 3문장에 **인물·처지·결핍**이 다 있는가? 결말을 흘리지 않았는가?
10. 9비트(script-guide §2) 중 **②우연한 사건 / ④부탁·결단 / ⑧마음이 닿음 / ⑨봉인**이 다 있는가?
11. **②의 선행이 ⑦⑧에서 회수**되는가? (이 포맷의 유일한 복선)
12. ⑥의 역풍이 **작은가** — 주인공이 파멸하지 않는가?
13. **악인이 무대에 오르지 않는가** — 주인공과 직접 대면·모욕하는 장면이 없는가? (있으면 소문·전언으로 바꾼다)
14. 닫는 정형구가 있고, 앞 편과 **같은 정형구가 아닌가**?
15. **금지 목록**(script-guide §6) — 후렴·클리프행어·미끼·시점 교차·패턴 인터럽트·CTA가 **0건**인가?
16. 1편이 가장 짧은가(5,400자)? 편별 편차가 ±10% 안인가?

> **사후 검증 예정**: v3.0은 벤치마크 2편 실측(개정 문턱 충족)이지만 **자사 성과로는 미검증**이다. 첫 업로드 후 ① **편 경계(23·47·71·94·118분)에서 이탈 계단이 생기는지** ② 첫 3분 유지율 ③ 조회율로 검증한다. 편 경계 이탈이 뚜렷하면 편 사이에 "다음 이야기입니다" 한 줄 브릿지를 넣는 것이 1차 처방.

## 18. 턴어라운드 4뷰는 '단어'가 아니라 '각도'로 못박는다 ★2026-07-26 혼주석 실측

`turnaround.py`의 뷰 지시가 원래 `"front, 3/4, side, back"` 한 줄이었다. **모델이 3/4와 side를 구분하지 못해 2·3번을 좌우 옆모습(서로 거울상)으로 뽑는다.** 실질 4뷰가 아니라 3뷰가 되고, 정작 씬에서 가장 많이 쓰이는 **3/4 각도 참조가 통째로 빠진다.**

- 실측(혼주석 11장): 유상근·탁 참봉은 2·3번이 완전한 거울상, 막동·탁문규는 **같은 방향 옆모습이라 거의 중복**이었다.
- **처방(내장, `turnaround.py`의 `_VIEWS`):** ① **칸 수를 강제**하고 ② 각 뷰를 **도수 + 보이는 것**으로 정의하고 ③ 거울 금지를 명시한다. 셋 다 있어야 한다.
  - `"EXACTLY FOUR panels of equal width filling the whole canvas edge to edge, evenly spaced, all four present — not three, not five."` ← **이게 없으면 3칸만 그리고 끝내는 경우가 나온다**(실측 1회).
  - (1) FRONT 정면, 두 귀 보임 / (2) THREE-QUARTER **45도**, **두 눈 다 보이되** 먼 쪽 눈썹·뺨이 콧대에 일부 가림, 한쪽 귀 숨김 / (3) FULL PROFILE **90도**, **한 눈만** 보이고 코·입이 실루엣 / (4) BACK 정후면, 얼굴 없음
  - `"four DIFFERENT rotation angles of one continuous turn. Do NOT mirror any view, do NOT repeat the same angle twice, and views 2 and 3 must be clearly distinguishable."`
- **1회 생성으로 다 되지는 않는다.** 혼주석 실측: 일괄 재생성에서 11장 중 10장 성공, 남은 1장(유상근)은 **3회 더 돌려서** 통과했다(실패 양상 = 1·2번이 둘 다 정면 / 3칸만 생성). **갓·두건처럼 머리 실루엣이 뚜렷한 인물이 잘 나오고, 맨상투에 이목구비가 평범한 인물이 잘 실패한다.**
- **검수는 반드시 개별 png를 확대해서** 볼 것. contact sheet 축소본에서는 1·2번 중복이 잘 안 보인다.
- **`--force` 재생성은 얼굴이 바뀐다**(시드가 다름). 이미 검수 통과한 시트를 다시 뽑을 땐 사용자에게 먼저 알릴 것. variant가 있는 인물은 `--only <id>`가 **base와 variant를 함께** 재생성하므로, 한쪽만 고치고 싶어도 둘 다 바뀐다는 점에 주의.

## 19. `characters.json`에 `turnaround` 필드가 없으면 씬에 ref가 한 장도 안 붙는다 ★함정

`turnaround.py`는 시트 경로를 `assets/characters/{id}_turnaround.png`로 **자동 유추**하지만, **`build.py`는 `characters.json`의 명시적 `turnaround` 필드만 읽는다**(`resolve_cast`의 `char.get("turnaround")`). 유추하지 않는다.

- 그래서 **variants가 없는 인물**은 시트 파일이 멀쩡히 있어도 씬 프롬프트에 ref가 안 붙고, `char_refs=0`이라 §15-3의 "same face" 지시까지 통째로 빠진다. **조용히 실패한다 — 에러가 안 난다.**
- 혼주석 실측: 96씬 중 **19씬**이 여기 걸렸고 그중 주인공(막동)이 포함이었다.
- **처방:** variants 없는 인물마다 `"turnaround": "assets/characters/<id>_turnaround.png"` 를 **명시**한다. (variants 인물은 `variants.<v>.turnaround`가 이미 있으므로 무사)
- **검증:** `build.py --dry-run` 후 `scenes/_pNN.txt`에서 **cast가 있는 씬 전부에 `Same person, not a look-alike`가 있는지** 세어 볼 것. 하나라도 없으면 이 필드 누락이다.

## 20. 씬 `visual_desc`에는 시간대와 계절을 반드시 박는다 ★§17의 필연적 짝

§17이 **scene_preset에서 조명 방향·시간대를 금지**했기 때문에(넣으면 전 씬이 밤으로 끌린다), **시간대·계절을 정하는 곳은 씬별 `visual_desc` 하나뿐이다.** 여기 비워 두면 모델이 임의로 정한다.

- 혼주석 실측: 96씬 중 **37씬에 시간대 어휘가 아예 없었고**, 계절 어휘도 73씬에 없었다. 첫 생성인 씬1이 **새벽 대본인데 주황빛 황혼**으로, **늦겨울인데 감이 달린 감나무**로 나왔다.
- **처방 3종:**
  1. **모든 씬에 시간대 어휘를 하나 이상** 넣는다 (`dawn/morning/midday/afternoon/dusk/night/lantern light` 등).
  2. **모든 야외 씬에 계절을 명시**한다 (`Deep autumn.` / `Deep winter: frozen bare ground, no leaves.` / `Early spring: branches still bare.`). 서사가 여러 계절에 걸치면 **장별로 계절 문장을 고정**해 두고 일괄 주입하는 편이 안전하다.
  3. **새벽·아침 씬에는 반드시 반대 시간대 금지구를 붙인다** — `"This is PRE-DAWN / EARLY MORNING light — NOT sunset, NOT dusk, NOT a golden-hour orange sky, NOT evening."` `"early morning light"`만으로는 석양으로 끌려간다(실측).
- 열매·꽃처럼 계절이 드러나는 소품은 **씬별로 상태를 지정**한다(`still hung with unpicked orange fruit` vs `bare branches with no fruit`). 같은 나무가 장마다 달라야 한다.
- ⚠️ **계절 문장을 일괄 주입하는 스크립트를 쓸 때, 판정 키워드에 `persimmon`·`ripe` 같은 소품 단어를 넣지 말 것.** 감나무를 언급했다는 이유로 "계절이 이미 명시됨"으로 오판해 그 씬만 주입에서 빠진다(혼주석 실측 4씬). 판정은 `autumn|winter|spring|summer|frost|snow`처럼 **계절 자체를 가리키는 단어로만** 한다.
- `bare persimmon branches`라고 써도 **감이 달려 나온다.** 계절 문장이 함께 없으면 약하다 → `completely bare leafless branches with ABSOLUTELY NO FRUIT on them` + 계절 문장을 같이 붙일 것.

## 22. 씬이 '흰 배경 위 액자 그림'으로 나오는 것을 막아라 (full-bleed 강제) ★2026-07-28 실측

혼주석 96씬 배치에서 **2장(씬11·85)이 흰 여백 안에 액자처럼 그려져** 그대로는 쓸 수 없었다. 해상도는 1344×768로 정상이라 파일 크기·개수 점검으로는 안 걸린다.

- **처방(내장, `style.json` `scene_negative`):**
  `"The artwork must fill the entire frame edge to edge — no white margin, no border, no frame or matte around the picture, not a framed illustration placed on a white background, no letterboxing, no black bars."`
- **자동 검수:** 배치 후 전 씬의 **네 변 6px 평균 밝기**를 재서 최소값이 235를 넘으면 흰 프레임이다. 96장을 눈으로 훑는 것보다 확실하다.
  ```python
  a = np.asarray(Image.open(f).convert('L'), float)
  e = [a[:6,:].mean(), a[-6:,:].mean(), a[:,:6].mean(), a[:,-6:].mean()]
  if min(e) > 235: print(f, "흰 프레임")
  ```
- 걸린 씬만 `build.py --only <id> --force`로 재생성하면 된다(체크포인트라 나머지는 건드리지 않음).

## 23. 아동 인물 클로즈업은 '두신비'를 명시하지 않으면 어른 얼굴이 된다 ★2026-07-28 씬1 실측

**같은 인물이 원경·미디엄에서는 아이로, 클로즈업에서는 10대 중후반~성인으로 나온다.** 얼굴만 크게 잡히면 모델이 몸 비율 단서를 잃고 성인 얼굴로 해석하기 때문. 씬1(Veo 립싱크 시작 프레임 = 썸네일급)은 반드시 클로즈업이라 정면으로 부딪힌다.

- **처방 — 클로즈업 visual_desc에 두신비를 말로 박는다:**
  `"a LARGE ROUND HEAD on narrow bony shoulders, soft full round cheeks, a SHORT ROUNDED CHIN and a small snub nose. Render the SAME young child's face as the attached reference sheet. NOT a teenager, NOT a youth, NOT a young adult, NO defined adult jawline, NO adult cheekbones, NOT a long narrow face."`
- **프레임을 넓히는 것으로 해결하려 하지 말 것.** 허리 위까지 물리면 얼굴은 어려지지만 ① 립싱크에 필요한 입 크기를 잃고 ② **손 동작이 무너진다**(실측: 도포 자락을 놓고 제 옷섶을 쥐었다). 정답은 **타이트 프레임 유지 + 두신비 문구 추가**다.
- **접촉·파지 동작은 '누구의 옷인지'까지 못박는다.** `"a fold of black robe cloth"` 정도로는 제 옷을 쥔 그림이 나온다 →
  `"HIS TWO SMALL FISTS ARE CLOSED AROUND A THICK FOLD OF DEEP INK-BLACK SILK ROBE that belongs to a tall adult standing right beside him — the cloth is BUNCHED AND CRUMPLED INSIDE HIS GRIP and pulled taut toward the adult at the left edge of frame. He is clutching SOMEONE ELSE'S garment, NOT his own collar."`
- 씬1은 **5회 재생성**해서 통과했다. 훅 한 장이므로 그만한 값어치가 있지만, **처음부터 위 세 요소(두신비·타이트 유지·파지 대상 명시)를 넣으면 1~2회로 끝난다.**

## 21. 씬 `cast`에 넣은 인물은 `visual_desc`에 `{id}` placeholder가 반드시 있어야 한다

`build.py`는 `desc.replace("{id}", lock+negatives)`로 치환한다. **cast에는 있는데 placeholder가 없으면 lock도 negatives도 한 글자도 안 들어간다** — ref만 붙고 텍스트 방어가 통째로 빠진다.

- 반대로 **얼굴이 안 나오는 컷**(손만, 뒷모습만, 옷자락만)은 **cast에서 빼는 게 맞다.** 넣으면 의도적으로 비운 프레임에 인물이 끌려 들어온다.
- **검증:** dry-run 산출 프롬프트에 `{` 로 시작하는 **미치환 placeholder가 0개**인지, 그리고 **인물별 `(NOT ...)` 괄호 수 ≥ cast 수**인지 확인.

## 24. 🚫 **[폐기 — 2026-09-06]** Veo 훅은 gemini + **Veo 3.1 Lite**로 (flow는 무료 계정에서 안 된다) ★2026-07-28 확정

> **🚫 이 절의 결론은 폐기됐다 (2026-09-06 사용자 지시 · CLAUDE.md 「절대 금지」 절).** `GEMINI_API_KEY`로는 **영상을 절대 만들지 않는다.** 훅 영상 엔진은 **무료 `pjn` 하나뿐**이고, pjn이 안 되면 **훅을 포기하고 스틸 도입으로 간다.** 아래 단가·모델 비교는 **이력 보존용**이며 실행 근거가 아니다. (flow가 무료 계정에서 안 된다는 관찰만 여전히 유효하다.)

**flow(labs.google)의 Veo 영상 생성은 Google AI Pro/Ultra 구독 기능이다.** 무료 계정으로 연결한 레인에서는 애초에 권한이 없어 실패한다 — **밴이 아니라 권한 문제**이므로 §4-1의 UNUSUAL_ACTIVITY(봇 판정)와 혼동하지 말 것. 이미지 생성(나노바나나)은 무료 계정으로 되지만 **영상은 다르다.**

**Gemini API 8초 클립 단가** (2026-07 실측 조회):

| 모델 | 모델 ID | 720p | 1080p |
|---|---|---|---|
| **Veo 3.1 Lite** ★기본 | `veo-3.1-lite-generate-preview` | $0.40 (~560원) | **$0.64 (~900원)** |
| Veo 3.1 Fast | `veo-3.1-fast-generate-preview` | — | $1.20 (~1,700원) |
| Veo 3.1 Standard | `veo-3.1-generate-preview` | — | $3.20 (~4,500원) |

- Lite도 **네이티브 오디오 + image-to-video + 4/6/8초 + 1080p**를 다 지원한다 → 립싱크 훅 요건 충족.
- **1080p를 쓸 것.** 씬 이미지를 1920×1080으로 통일해 두므로(§22 크롭) 720p를 쓰면 훅 8초만 흐릿해진다.
- **Lite는 이코노미 등급이라 립싱크 정확도가 Fast보다 떨어질 수 있다.** 먼저 Lite로 뽑고, 입이 안 맞으면 `model`만 Fast로 올려 `--force` 재생성(최악 900+1,700원).
- 생성 성공분만 과금된다. Veo는 무료 티어가 없다.
- **`--prompt-only`는 과금 0원** — 설정이 제대로 물렸는지(`{V}/veo_hook.json`의 engine/model/resolution/dialogue/start_frame) 먼저 이걸로 확인하고 본 생성으로 갈 것.

## 25. 훅 스플라이스 실전 — 12초만 재인코딩 + 타임스케일 함정 ★2026-07-29 혼주석 실측

§9대로 CapCut에는 veo를 넣지 않으므로, **사용자가 내보낸 mp4 앞부분을 ffmpeg로 갈아끼우는 것이 마지막 공정**이다. 82분 6GB 파일을 전부 재인코딩하면 CPU로 몇 시간이지만, **앞 12초만 재인코딩하고 나머지는 스트림 복사하면 7분**이면 끝난다.

### 절차

1. **앞 조각 만들기** = veo 클립(8초) + 원본[대체끝 → 다음 키프레임] 을 concat 필터로 재인코딩.
   혼주석 실측: 훅 대사가 0~6.1초, 원본 키프레임이 5초 간격(0/5/10/15…)이라 **원본 6.1~10.0초(3.9초)를 다리로 붙여 11.9초 조각**을 만들었다.
2. **concat demuxer + `inpoint`로 본편을 직접 이어붙인다** — 6GB 중간 파일을 안 만든다(C: 여유가 부족할 때 필수).
   ```
   file 'C:/…/_head12.mp4'
   file 'D:/…/원본.mp4'
   inpoint 10.0
   ```
   `ffmpeg -f concat -safe 0 -i list.txt -c copy -movflags +faststart out.mp4`
3. 경로는 **정슬래시 절대경로**로. bash heredoc·sed로 만들면 백슬래시가 깨지니 **파이썬 스크립트 파일로 생성**할 것.

### ★★ 타임스케일이 다르면 조용히 망가진다 (가장 위험)

조각과 본편의 **video `time_base`가 다르면** concat 복사 시 DTS가 비단조가 되고, ffmpeg가 `+1 tick`씩 강제 보정하면서 **뒷부분 전체가 몇십 초로 뭉개진다.**

- 혼주석 실측: 조각을 `1/15360`으로 만들었더니 **컨테이너 duration은 4932초로 정상인데 영상 스트림은 21.41초**였다. 후반부 프레임 추출이 전부 실패. 검증 없이 넘겼으면 6GB짜리 재생 불가 파일을 업로드할 뻔했다.
- **CapCut Windows 산출물은 video `time_base = 1/30`** (audio 1/44100). 조각을 만들 때 **`-video_track_timescale 30`** 으로 맞출 것.
- 증상 신호: 실행 로그에 `Non-monotonic DTS` 가 **수천 건**(정상은 1건).

### 반드시 할 검증 (컨테이너 duration만 보면 속는다)

```bash
ffprobe -v error -show_entries stream=codec_type,duration,nb_frames -of default=nw=1 out.mp4
```
- **영상 스트림 duration**이 `원본 − 대체구간 + 클립길이` 와 일치하는가
- **nb_frames** 가 `원본프레임 − 대체구간×fps + 클립초×fps` 와 일치하는가
  (혼주석: 147,910 − 183 + 240 = **147,967** ✓)
- 후반부(예: 2000s, 4900s) 프레임이 실제로 추출되는가

> 첫 실행이 비정상적으로 빨리 끝나고 `moov atom not found`가 나면 파일 잠금 문제다 — **그대로 재실행**하면 된다.

### 훅 8초 자막 굽기

원본 앞부분을 잘라내면 CapCut이 구워 넣은 선두 자막도 사라지고, 클립은 `no subtitles`로 생성되므로 **훅에 자막이 없어진다.** 넣으려면 **스플라이스 전에 클립에 직접 굽는다.**

1. **타이밍은 클립의 실제 발화 구간을 측정해서 잡는다** — 원본 큐 시각을 비례 스케일하면 어긋난다.
   ```bash
   ffmpeg -i clip.mp4 -af "silencedetect=noise=-25dB:d=0.2" -f null -
   ```
   (앰비언트가 깔려 있어 `-38dB`로는 안 잡힌다. `-25dB` 권장)
   혼주석 실측: 0.47~1.35 / 1.75~3.64 / 5.78~7.20 — 세 어절이 명확히 분리됐다.
2. **★libass는 `PlayResY=288` 기준이라 FontSize를 1080 기준으로 쓰면 3.75배로 나온다.**
   CapCut 자막(`capcut.subtitle.font_size=10`)과 크기를 맞추려면:
   ```
   force_style='FontName=Malgun Gothic,FontSize=30,Bold=1,
     PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,
     BorderStyle=1,Outline=2.4,Shadow=0,Alignment=2,MarginV=17'
   ```
   (FontSize 58로 했더니 화면 절반을 덮고 2줄로 넘어갔다. 20은 반대로 작았다.)
3. 크기 검증은 **글자당 가로 폭**으로 한다 — 하단 밴드의 흰 픽셀 가로 범위 ÷ 글자 수. 혼주석: veo 84px/자 vs CapCut 90px/자로 맞췄다.

## 25. ★늘어지지 않게 쓴다 — 문장·문단 규칙 (2026-08-02 사용자 지시, ★2026-08-12 v3.0 조정)

**사용자 지시 원문:** *"초반 부분 좀 더 재미있게 써야 할 거 같아. 초반에 이탈하는 사람들이 많아서, 너무 지지부진 끌지 않고 계속 흥미진진하게 가야 해."*

> **★v3.0 조정**: 이 절은 90분 단일 서사에서 "초반 이탈"을 막으려고 만든 규칙이다. v3.0 옴니버스에서는 **긴장을 올리는 항목(25-4 판 뒤집기, 25-5 악역 행동)이 script-guide §6 금지 목록과 충돌**한다 — 수면 콘텐츠는 각성시키면 진다. **늘어짐을 막는 항목(25-2 몽타주 금지, 25-3 설명 상한, 25-6 문단 리듬)만 살리고 긴장 항목은 아래처럼 바꿨다.**

### 25-1. 저긴장 구간 상한 — "5분 규칙" (v3.0에서 완화)
- **사건 없이 흘러가는 구간이 연속 1,300자(≈5분)를 넘지 않는다.** (구 700자·3분에서 완화 — 편이 23분이고 잔잔함이 상품이다.)
- 여기서 **사건**이란 셋 중 하나다: ① 누가 무엇을 **해서 상황이 바뀐다** ② **새 정보가 인물의 처지를 흔든다** ③ **대사로 대화가 오간다**(충돌이 아니어도 된다 — v3.0 변경).
- 사건이 아닌 것: 배경 설명 · 인물 소개 · 회상 · 시간 경과 요약 · 나레이터 해설.
- 검사법: 편을 문단 단위로 훑으며 **사건 문단에 표시**하고, 표시 없는 구간이 1,300자를 넘으면 그 자리에 **대사 한 덩어리**를 넣는 것이 가장 싸고 안전한 처방이다(대사 비율 목표 20%와도 맞는다).

### 25-2. ⛔ 몽타주 금지 — 요약형 시간 경과를 장면으로 바꾼다
가장 흔한 늘어짐의 정체는 **"~하곤 했습니다" 몽타주**다. 여러 날을 뭉쳐 요약하면 사건이 사라지고 화면도 안 나온다.
- ❌ "배우는 것이 빨랐습니다. 한 번 그은 획을 잊지 않았지요. 열흘 걸릴 것을 닷새에 받아 갔습니다."
- ✅ **그중 하루를 골라 장면으로 쓴다.** 특정한 밤, 특정한 글자, 특정한 대사, 그리고 **작은 사고 하나**.
- 원칙: **"여러 번 그랬다"를 쓰고 싶으면, 그 여러 번 중 가장 위험했던 한 번을 쓴다.**

### 25-3. 설명은 세 문단 연속 금지 — "샌드위치 규칙"
- 배경·내력·제도 설명이 **연속 3문단을 넘기지 않는다.** 넘길 것 같으면 반으로 잘라 **사건 사이에 끼워** 넣는다.
- 나레이터 개입 문단("여기서 잠깐 짚고 갈 것이 있습니다" 류)은 **장당 1회, 3문장 이내.**
- 설명은 **궁금해진 다음에** 준다(§1-1). 아직 안 궁금한 정보는 **그 정보가 필요해지는 장까지 미룬다.**

### 25-4. ~~장마다 판이 두 번 뒤집힌다~~ → **편마다 판이 한 번 부드럽게 바뀐다** (v3.0 대체)
> **폐기**: "장 끝 클리프행어 + 중간 소반전 = 장당 2회"는 각성 장치다. script-guide §6이 클리프행어를 금지한다.
- **편마다 판이 바뀌는 지점은 ⑥(결과 + 작은 역풍) 한 곳이다.** 일이 풀리는데 대가가 하나 따라오고, 주인공이 그 대가를 혼자 진다. 이것이 편의 감정 최고점.
- **역풍은 작아야 한다.** 주인공을 파멸시키지 않는다 — v2.x의 "바닥이 깊을수록 카타르시스"는 폐기.
- 비트 끝에 "그러나 그는 아직 알지 못했습니다"류를 붙이지 않는다. 각 비트는 **닫고** 다음을 연다.

### 25-5. ~~악역은 초반부터 행동한다~~ → **악인을 무대에 올리지 않는다** (v3.0 대체)
> **폐기**: 정반대로 뒤집혔다. 벤치마크 실측 — 악인은 소문·문서·전언으로만 존재하고 주인공과 직접 대면·모욕하는 장면이 거의 없다(돌쇠 편의 이판서는 대사 한 줄 없이 귀양을 간다).
- **갈등은 상황으로 만들고 대면으로 만들지 않는다.** 분노는 각성이다.
- 응징 장면은 **두세 문장으로 지나간다.** 분량은 그 뒤의 화해·보상에 준다.
- 황금률은 유지: 주인공은 직접 복수하지 않는다. 단 **응징을 불러온 것은 주인공의 행동**이어야 한다(돌쇠가 장부를 훔쳐 왔다).

### 25-6. 문단 리듬
- 문단은 **1~3문장**. 4문장을 넘는 문단이 연속으로 나오면 낭독이 늘어진다.
- 대사는 **문단을 따로** 준다. 개수는 §29(직접화법 상한)를 따른다 — **하한이 아니라 상한이다**(§29-0 참조).
- **장 첫 문단은 무조건 장면**(사람·행동·소리). 장 첫 문단을 설명으로 여는 것을 금지한다 — §1-1의 1장 규칙을 **모든 장으로 확대**한다.

### 25-7. DRAFT 자가 검수 (편마다 — 위반 시 그 편을 고치고 넘어간다) ★v3.0
1. 사건 없는 최장 구간이 **1,300자 이하**인가?
2. 요약형 몽타주("~하곤 했습니다")가 **0개**인가? (있으면 그중 하루를 골라 장면으로 교체)
3. 연속 설명 문단이 **3개 이하**인가? 나레이터 개입이 편당 1회인가?
4. **판이 바뀌는 지점이 ⑥ 한 곳**인가? 역풍이 작은가? 클리프행어가 0개인가?
5. **악인이 무대에 오르지 않았는가?** 응징 장면이 세 문장 이내인가?
6. 편 첫 문단이 **장면 또는 인물 소개**인가(도입 3문장 규칙)?
7. 4문장 이상 문단이 **연속으로** 나오지 않는가? 대사 문단이 **§29 상한 이하**인가(단일 나레이션이면 ★편당 4~6개 · 따옴표 여섯 줄 — §29-7)?
8. **문체 수치**(script-guide §5) — `validate_script.py --style`로 7항목 확인(멀티 보이스면 `--voice multi`).
9. **금지 목록**(script-guide §6) 0건 — `validate_script.py`가 후렴·시점교차·패턴인터럽트·CTA를 에러로 잡는다.

> **적용 범위**: 25-1~25-6은 편 전 구간에 적용한다. 다만 **⑦보상·⑧닿음·⑨봉인 구간은 호흡을 늦춘다** — 여기가 이 채널이 파는 온기다. 늘어짐을 막는 규칙이지 빠르게 몰아치라는 규칙이 아니다.

## 26. 앵커에 '흔치 않은 한국 복식 명사'를 쓰지 말 것 — 전부 갓(gat)으로 흡수된다 ★2026-08-02 이름석자 실측

`anchorProp`을 **`wide-brimmed flat black woven beongeoji hat`**(벙거지)으로 잡았더니, 모델이 그냥 **갓을 그렸다.** negatives에 `NOT wearing a horsehair gat hat`을 **명시했는데도** 갓이 나왔다.

- **결과가 단순한 오류로 끝나지 않는다.** 그 인물(송 객주)이 이미 갓을 쓴 다른 인물(하 좌수)과 **머리 실루엣이 겹쳐**, 캐스트 내 앵커 축 중복이 되어 버렸다. 앵커 하나가 실패하면 **두 인물이 동시에 망가진다.**
- 같은 함정이 예상되는 어휘: `beongeoji`(벙거지) · `paeraengi`(패랭이) · `jeonrip`(전립) · `sagat`(사갓) 류. 모델이 "조선 남자 + 챙 있는 검은 모자"를 전부 갓의 변형으로 수렴시킨다.
- **처방 — 있는 것으로 지정하지 말고 없는 것으로 지정한다.** 모자로 구분하려다 실패하면, 그 인물은 **모자를 아예 벗긴다.**
  ```
  "he wears NO hat at all — instead a thick black cloth headband is tied tightly around
   his forehead with the knot at the back, and his grey topknot sits bare and fully visible above it"
  negatives: "NOT wearing ANY hat", "NOT wearing a wide-brimmed hat of any kind", "NOT wearing a scholar's cap"
  ```
  1회 재생성으로 통과했다. **`NOT wearing a gat` 하나로는 부족하고, `NOT wearing ANY hat`처럼 범주 전체를 닫아야 먹는다.**
- 안전한 머리 앵커(실측 통과): **갓**(가장 안정적) · **유건**(각진 검은 사각모 — 갓과 확실히 구분됨) · **이마 두건 + 맨상투** · **모자 없음 + 낮게 묶은 머리**.
- **캐스트 설계 시**: 머리 축은 **최대 2명까지만** 쓰고(갓 1명 + 유건/두건 1명), 나머지는 색·얼굴·실루엣 축으로 뺀다.

**함께 얻은 실측 — 턴어라운드 4뷰 성공률 (gemini, 인물 8·총 19장 생성)**

| 인물 유형 | 결과 |
|---|---|
| 갓·유건·두건 등 **머리 실루엣이 뚜렷한** 인물 | 1회에 4뷰 통과 |
| **맨상투 + 평범한 이목구비** (곽서방) | **4회 돌려도 1·2번이 계속 같은 정면** → 실질 3뷰로 수용 |
| 여성·안경 등 특징이 강한 인물 | 1회 통과 |

§18의 관찰이 그대로 재현됐다. **맨상투 조연은 3뷰로 끝날 각오를 하고**, 재시도는 2~3회에서 끊는 것이 비용상 합리적이다(3/4 뷰가 없어도 정면·프로필·후면이 있으면 씬에서 버틴다). 주연이면 끝까지 돌린다.

## 25. 한 작품 안에서 그림체가 갈리는 원인은 lock의 **어휘 계열**이다 ★2026-08-02 산가지 실측

§15-5는 "남녀 lock의 **서술 밀도**를 맞출 것"까지만 말한다. **그것만으로는 부족하다.** 밀도를 맞춰도 **어휘 계열**이 다르면 인물마다 렌더링이 갈린다.

**실제로 당한 것 (산가지):** 여자 주인공은 웹툰 미형 어휘(`strikingly beautiful` / `large luminous almond eyes` / `clear fair skin` / `subtle blush` / `soft full lips`)만 받아 **깨끗한 웹툰**으로 나왔고, 아버지·유모·노인은 나이와 고생을 **피부 질감 어휘**로 표현해서(`deeply lined` / `weathered` / `sun-darkened` / `subsurface glow` / `crow's feet` / `sagging`) **반실사 페인팅**으로 나왔다. 사용자가 "남자랑 여자랑 그림체가 너무 다르다"고 지적. lock 어휘 감사 결과:

| 인물 | 실사 어휘 | 미형 어휘 |
|---|---|---|
| 차무던(여) | 0~1 | **8** |
| 차중석(남) | **5** | 2 |
| 오 행수·점례 어멈 | 2~3 | **0** |
| 표석구·너울댁·사또 | 0 | 0 (style.json 기본값에 방치) |

→ 한 작품에서 그림체가 **세 갈래**로 갈렸다.

### 규칙
1. **모든 인물 lock에 동일한 렌더링 블록을 넣는다.** 주연·조연·악역·노인 구분 없이 한 글자도 다르지 않게. 예:
   > `Drawn in clean Korean webtoon style exactly like the rest of the cast: SMOOTH FLAT-TONED SKIN with soft gradient shading and NO photographic skin texture and NO visible pores, large glossy eyes with crisp bright catchlights and clearly separated lashes, a small neat nose, fine thin even lineart and simple clean facial planes.`
2. **나이·고생·계급은 피부가 아니라 다른 데서 표현한다** — 머리색(반백/백발), 수염, 자세(굽은 등·처진 어깨), 실루엣, 옷. **피부 질감 어휘 전면 금지.**
   - ❌ `deeply lined weathered face`, `sun-darkened skin`, `subsurface glow`, `crow's feet`, `sagging cheeks`
   - ✅ `SILVER-GREY hair`, `a short neatly trimmed GREY BEARD`, `hollow cheeks under high cheekbones`, `a noticeably BENT BACK`
3. **negatives에도 공통 스타일 금지구를 전원 추가**: `NOT photorealistic` / `NOT a semi-realistic painting` / `NO rough or textured skin` / `NO visible skin pores or heavy wrinkle rendering`.
4. **미형 어휘(§15-5)는 여전히 주연에게만** — 그건 "예쁨"의 문제고, 여기 §25는 "렌더링 계열"의 문제다. 둘은 별개 축이다. 악역에게 `strikingly beautiful`은 안 넣되, 렌더링 블록은 **넣는다**.

### 검수 (ASSET_GEN 진입 시, 생성 전에)
lock 문자열에서 아래 두 목록의 히트 수를 세어 **인물 간 편차가 없는지** 확인한다. 실사 어휘가 한 명이라도 잡히면 그 인물만 튄다.
- 실사: `weathered` `deeply lined` `finely lined` `sun-darkened` `sun-browned` `subsurface glow` `wrinkled` `crow's feet` `sagging` `fine detail`
- 미형: `strikingly beautiful` `luminous` `crisp catchlights` `clear fair skin` `subtle blush` `soft full lips` `glossy` `separated lashes`

> **기준 인물을 정하고 거기에 맞춘다** — 산가지에서는 차무던(여주)이 기준이었다. 새 프로젝트도 주연 한 명의 lock을 먼저 확정하고, 나머지를 그 렌더링 블록에 복사해 맞추는 순서로 간다.

## 27. 씬 배치는 반드시 '1~2장 파일럿'부터 — 30씬에서 잡은 것 3종 ★2026-08-02 이름석자

111씬을 한 번에 돌리지 않고 **1~2장(30씬)만 먼저 뽑았더니 나머지 81씬에 그대로 번졌을 문제가 셋** 나왔다. 파일럿 비용은 ~1,600원, 전량 재생성이었으면 ~6,000원. **앞으로 장편 씬 배치는 항상 첫 1~2장을 파일럿으로 돌리고 검수한 뒤 나머지를 간다.**

### 27-1. 문서 클로즈업에 **현대 한글이 박힌다** (가장 치명적)
`style.json scene_negative`에 `No text, no letters, no numbers`가 이미 있는데도, **씬 `visual_desc`가 "dense vertical brushed characters"처럼 글자를 그리라고 요구하면 negative가 무력화된다.** 실측: 문서 클로즈업에 **읽히는 현대 한글**이 그대로 렌더링됐다 — 조선 문서 고증이 깨지고 화면 자막과도 충돌한다.
- **처방(검증됨) — 씬 `visual_desc` 끝에 붙인다.** negative가 아니라 **positive 쪽에서** 막아야 한다.
  ```
  IMPORTANT — all writing visible anywhere in this image must be ILLEGIBLE: soft indistinct vertical
  brush marks and ink strokes that merely SUGGEST old Korean brush calligraphy, with NO readable glyph
  of any kind. NO Hangul, NO modern Korean alphabet, NO Chinese characters that can actually be read,
  NO Latin letters, NO numerals, NO watermark, NO caption.
  ```
- 적용 대상 판정: `characters|writing|brushed|columns of|register|ledger|deed|document|petition|notice|signboard` 정규식으로 훑으면 된다. 이름석자는 **111씬 중 46씬**이 걸렸다.
- 재생성 결과 한글이 사라지고 **한자풍의 읽을 수 없는 붓글씨**로 나왔다 — 야담 소품으로 오히려 더 맞다.
- 부수 조치로 `scene_negative`에도 `no Hangul, no modern Korean alphabet, no legible glyphs`를 넣었지만 **이것만으로는 못 막는다.** 근본은 visual_desc 쪽이다.

### 27-2. 레터박스는 프롬프트로 못 막는다 — **후처리로 자른다** (무과금)
§22가 `scene_negative`에 full-bleed 문구를 넣었는데도, 30씬 중 **7장**에 상하 균일 띠가 생겼다. 문구를 더 강화해 재생성해도 **같은 씬에서 재발**했다.
- **처방: `scripts/render/fix_letterbox.py` (신규).** 균일 띠를 검출해 잘라내고 원본 종횡비로 센터 크롭 후 원해상도로 리사이즈. **과금 0원, 결정적.** 원본은 `.orig.png`로 보존.
  ```
  python3 scripts/render/fix_letterbox.py {P}/scenes          # 검사만
  python3 scripts/render/fix_letterbox.py {P}/scenes --apply  # 실제 크롭
  ```
- **★검출 기준을 느슨하게 잡지 말 것 (실제로 당함).** 처음에 `std<6, 밝기<40 또는 >225`로 잡았더니 **흰 회벽 클로즈업과 어두운 부엌 벽을 띠로 오판해 실제 화면을 268px·169px 잘라냈다.** 기준을 `std<2.5, <12 또는 >250`으로 조이니 오탐 0, 진짜 띠 7장만 남았다. 진짜 레터박스는 **순수 0 또는 255**에 가깝다.
- SCENE_IMG 배치 뒤 **항상 한 번 돌리는 것을 기본 절차로** 삼는다.

### 27-3. "아침"이라고 써도 **노을로 드리프트한다** — 색을 직접 지정해야 한다
§20이 시킨 대로 `This is MORNING light — NOT sunset, NOT dusk, NOT evening.`을 넣었는데도, 사당 아침 씬이 **주황빛 노을 하늘**로 나왔다. **시간대 단어와 금지구만으로는 부족하다.**
- **처방(검증됨) — 하늘 색과 빛의 색온도를 직접 못박는다.**
  ```
  This is MID-MORNING light: the sky is a PALE COOL BLUE-GREY with thin white cloud, and the sunlight is
  CLEAN AND WHITE, not warm. The sun is HIGH, casting short shadows. There is NO orange, NO amber, NO pink,
  NO peach and NO golden tone anywhere in the sky or on the walls.
  NOT sunset, NOT sunrise, NOT dusk, NOT golden hour, NOT evening.
  ```
- 재생성하니 하늘이 파란 회색으로 돌아왔다. **액자 구조에서 특히 중요** — 프레임 복귀 씬이 원래 씬과 다른 시간대로 나오면 "돌아왔다"는 신호 자체가 깨진다. 이름석자는 아침 씬이 **38개**라 전량 문구를 교체했다.
- 일반화: **`NOT X` 금지구는 약하다. `색·방향·높이`를 양성으로 지정하는 문장이 훨씬 강하다.**

## 26. `cast: []` 씬은 얼굴을 환각한다 — build.py가 프리셋을 갈아끼운다 ★2026-08-02 산가지 실측

**증상:** 무인 풍경·군중 원경·소품 클로즈업처럼 `cast`가 빈 씬에서, **있지도 않은 얼굴이 사진처럼 그려져** 화면 절반을 차지한다. 산가지 실측 — cast 없는 19씬 중 **7씬**(9·10·14·90·105·116·122)이 이렇게 깨졌다. 씬9는 `visual_desc`에 `No people`이라고 썼는데도 사진 같은 여자 얼굴이 들어왔다.

**근본 원인:** `build.py`가 `scene_preset`을 **씬에 인물이 있든 없든 통째로** 붙인다. 그런데 그 프리셋의 절반 이상이 **얼굴 렌더링 지시**다 — *"The light in the scene MODELS the face… the iris shows ring texture and radial fibers… tear-film glint along the lower lash line… Skin rendered in continuous painterly gradients with subsurface glow…"*. 인물 시트가 붙은 씬은 그 시트가 그림체를 잡아 주지만, **cast가 비면 참조 그림이 0장이라 모델이 그 지시를 만족시킬 얼굴을 스스로 만들어 넣고, 잡아 줄 앵커가 없으니 사진풍으로 그린다.**

**처방 (코드에 내장, 2026-08-02):** `build.py`가 `char_refs == 0`일 때 `style.json`의 `scene_preset_nocast` / `scene_negative_nocast`로 갈아끼운다. 해당 필드가 없는 채널은 기존 동작 그대로다.
- `scene_preset_nocast` — 얼굴 렌더링 블록과 `shallow depth of field…behind the subject`(원경에서 배경이 뭉개지는 원인)를 뺀다.
- `scene_negative_nocast` — `NO LARGE FACE ANYWHERE IN THE IMAGE` 이하 큰 얼굴 금지구를 넣는다. **배경 인물 자체는 허용** — 금지 대상은 프레임에 끼어드는 초상화급 얼굴이다.

## 27. 씬 배치 뒤 `check_scenes.py`를 반드시 돌린다 (흰 액자 + 레터박스)

§22의 흰 액자 검사는 **네 변 평균 밝기만** 봐서 **검은 띠를 못 잡는다.** 그리고 레터박스는 `scene_negative`에 full-bleed 금지구를 **두 번** 넣어도 계속 나온다 — 산가지 127씬 중 **17장(13%)**, 같은 날 이름석자 30씬 중 6장. 텍스트로는 못 막는 모델 습성이니 **검출해서 고치는 것이 정답**이다.

```powershell
python scripts/render/check_scenes.py {P}          # 검사만 (--only 목록을 찍어 준다)
python scripts/render/check_scenes.py {P} --fix    # 재생성으로 안 잡히는 씬의 띠를 잘라낸다
```
- 오탐 억제 3조건: ① 거의 완전 균일(std<2) ② 극단 밝기(<15 or >240) ③ 띠 경계에서 평균 점프(>25). 의도적으로 어두운 컷(암전 배경 클로즈업)은 안 걸린다.
- **운용 순서:** 검사 → `build.py --only … --force` 재생성 → 재검사. 산가지 실측 **17 → 8 → 3 → 2**로 줄었고, 끝까지 버틴 2장(둘 다 와이드 establishing 컷)은 `--fix`로 해결했다. **3라운드 넘게 굽지 말고 `--fix`로 넘길 것.**
- `--fix`는 띠를 잘라내고 정확히 16:9로 되맞춘 뒤 원본을 `scenes/_orig/`에 남긴다. 얇은 테두리는 리사이즈 후에야 검출되므로 **크롭→리사이즈→재검사를 반복**하도록 되어 있다. 흰 액자는 그림 자체가 액자라 크롭으로 못 고치니 재생성 대상으로 남긴다.

> ⚠️ **씬 이미지를 다시 뽑았으면 CapCut 드래프트를 재생성해야 한다** — 드래프트는 export 시점의 이미지를 복사해 간다. 이미 CapCut으로 한 번 연 드래프트라면 `Timelines\<UUID>\`가 생겨 같은 이름 재생성 시 옛 내용이 되살아나므로 **반드시 새 이름**(`_v2`)으로 뽑는다(§3 ★).

## 28. 반복 상투구 전면 폐지 ★2026-08-06 사용자 지시 (★2026-08-12 v3.0에서 전면 채택됨)

**사용자 지시 원문:** *"본론에 조금 빨리 들어가면 좋을 거 같아. 지루해서 초반에 이탈하는 사람 막고 싶어. 반복문구 사용하지 말고."*

> **★v3.0 정리**: 이 지시는 벤치마크 실측(2026-08-12)에서 **정면으로 확증됐다** — 후렴 0회, "바로 그때였습니다" 0회(②), 콜드오픈 0. 사용자 판단이 시장보다 먼저 갔다. 그래서 v3.0은 28-3을 예외 없이 채택했고(script-guide §6 금지 목록), **28-1(콜드오픈 60초 상한)은 콜드오픈 자체가 폐기되어 무효**가 됐다. 28-2(용어 설명 문단 금지)는 그대로 유효하다.

### 28-1. ~~콜드오픈 분량 상한~~ — 콜드오픈 폐기로 무효 (v3.0)
편 도입은 **3문장**이다(script-guide §3). 아래 표는 단일 대하 서사 시절의 기록으로만 남긴다.

`script-guide.md` §1①은 "첫 5~8문장, **약 1분**"이라 하고, §6 분량 배분은 "콜드 오픈+브릿지 **800~1,200자**"라고 적혀 있다. 800자는 240자/분 기준 **3분 20초**로, 같은 문서 안에서 **3배 차이**가 난다. 실제 집필은 늘 340~540자였다.

**자사 실측 (2026-08-06, script.txt 첫 문단부터 본문 진입까지):**

| 편 | 콜드오픈 | 브릿지 | 본문 진입 |
|---|---|---|---|
| 혼주석 | 376자 / 1:34 | 92자 | 1:57 |
| 놋골무 | 364자 / 1:31 | 68자 | 1:48 |
| 산가지 | 536자 / 2:14 | — | 2:30 |
| 이름석자 | 267자 / 1:07 | 70자 | 1:24 |

**확정값 (§6·§1① 수치를 이걸로 덮어쓴다):**

| 구간 | 상한 |
|---|---|
| 콜드오픈 | **5~6문단 / 180~200자 / 45~50초** |
| 브릿지 | **1문단 / 40자 / 10초** (채널 인사 한 줄 + 시간·장소 되감기 한 문장) |
| **본문 진입** | **60초 이내** |

- 썸네일 그림은 여전히 **3번째 문단(20초 지점)** 에 그림으로 도착시킨다(§18-1). 짧아졌다고 뒤로 밀지 말 것.
- 첫 문장은 **따옴표 대사**로 연다 — veo_hook.py가 script.txt의 첫 따옴표 대사를 훅 대사로 추출한다.

### 28-2. ⛔ 진짜 이탈 지점은 콜드오픈이 아니라 그 직후의 '용어 설명 문단'

혼주석은 브릿지를 지나자마자 **제도 설명 문단**이 들어갔다 — *"사창이란 흉년을 대비해, 나라가 곡식을 맡아 두는 창고입니다. 봄에 백성에게 꾸어 주고, 가을에 거두어들이지요."* 훅으로 끌어 놓고 3분째에 용어 강의를 듣게 되는 구조다. §18-2가 금지한 그대로인데도 실제 대본에서 재발했다.

- **"A란 ~입니다" 정의 문단을 전면 금지한다.** 제도·직역·물건 설명은 **행동 속에서 한 마디씩** 흘린다.
  - ❌ "저주지란 관아 공문서에 쓰는 두꺼운 닥종이입니다. 반드시 관에서 지정한 지장이…"
  - ✅ (포교가 곳간을 뒤지는 중에) "관아 문서는 삼십 년째 이 집 종이만 씁니다."
- 검사법: 1장에서 **동사가 없는 문단**(상태·정의만 있는 문단)을 세어 0인지 확인한다.

### 28-3. ⛔ 반복 상투구 폐지 — playbook §2 리텐션 툴킷의 일부를 무효화한다

아래 셋은 **쓰지 않는다.** playbook §2·§6는 장편에 후렴 5~6회를 요구하지만 **이 지시가 우선한다.**

1. **"~는 아직 알지 못했습니다" 후렴 → 0회.** (혼주석·놋골무·이름석자는 콜드오픈에서만도 1회씩 썼다.)
2. **"바로 그때였습니다" 정형 트리거 → 0회.**
3. **떡밥 리마인드 시 같은 문장 재사용 → 금지.** 다시 꺼낼 땐 **새 각도·새 정보**로 꺼낸다.

**~~대체 장치~~ → v3.0에서는 대체하지 않는다.** 구 대체 장치(장 끝 대사 클리프행어 / 새 사실 투입 / 시점 교차)는 전부 각성 장치라 script-guide §6이 함께 금지한다. **비트는 그냥 닫고 다음을 연다** — "닫는 힘"을 따로 만들 필요가 없다(벤치 2편 모두 클리프행어 0).

**예외 하나 — 편당 회수 1개는 유지한다.** ②의 무심한 선행이 ⑦⑧에서 돌아오는 것(script-guide §2). 이것은 상투구 반복이 아니라 이 포맷의 유일한 복선이며 효과가 정반대다. 후렴 금지와 혼동하지 말 것. 단 **v2.x의 "토씨까지 같은 묘사로 회수"는 편 길이(23분)에 안 맞아 폐기**됐다.

## 29. ⛔ 직접화법 상한 **2.5% · 편당 여섯 줄** — 단일 화자 낭독이라는 전제를 잊지 말 것 ★2026-08-15 하향 확정

> **★현행 확정값 = 2.5% / 편당 따옴표 여섯 줄 (사용자 지시, 2026-08-15 — 29-7).** 아래 29-0·29-6은 4%였던 직전 판이고, 29-1~29-5는 처음 25%로 잡았던 1차 초안이다. **29-7이 최종 규칙이다.**

> (직전 판 기록) **4% (사용자 지시, 2026-08-08).** 아래 29-1~29-5는 처음 25%로 잡았던 1차 초안이며, 사용자가 *"직접화법을 확 줄여야 해, 4프로 이하로. 왜냐하면 나레이터 한 명이 계속 말하는 구조잖아"* 라고 확정했다. **29-6이 최종 규칙이다.**

### 29-0. ★2026-08-12 벤치마크 실측 — 이 규칙의 진짜 변수는 "보이스가 몇 개냐"다 (유지)

벤치마크 2편이 이 축에서 정확히 갈렸고, 원인은 **낭독 보이스 수**로 확인된다.

| | 벤치 ① 이야기 들려주는 새벽 | 벤치 ② 옛날이야기 보따리 |
|---|---|---|
| 낭독 | **단일 나레이터** (YouTube ASR 화자 전환 마커 **0개**) | **대사에 별도 보이스** (마커 **584개**) |
| 직접대사 문장 비율 | **4.0%** | **22.3%** |
| 성과 | 97.3만 (7만 구독) | 67.0만 (9.4천 구독) |

- **4% 규칙은 벤치 ①에 의해 독립적으로 확증됐다** — 최상위 성과작(97만)이 단일 나레이터로 정확히 4.0%다. 사용자 판단이 시장 실측과 일치한다.
- **22%는 멀티 보이스일 때만 성립하는 값이다.** 단일 나레이터로 22%를 쓰면 한 사람이 모든 배역을 연기하는 톤이 되어 무너진다.
- **따라서 §29의 4% 상한은 v3.0에서도 그대로 유지한다.** 바꾸려면 먼저 **Vrew 멀티 보이스를 채택**해야 한다.
- **Vrew에 자동 화자 배정 기능은 없다** — 클립을 골라 목소리를 바꾸는 수동 작업이다. 채택 시 부담: 편당 대사 문단 20~25개 × 6편 ≈ **120~150 클립을 수동 재지정**. 보이스는 나레이터+남+여 3종 이내로 제한할 것. **출력은 여전히 mp3 1개 + SRT 1개라 파이프라인 변경은 없다**(SKILL.md TTS 절).

### 29-7. ★2026-08-15 하향 확정 — **2.5% / 편당 여섯 줄** (이것이 현행 최종값)

v3.0 공식대로 4%를 정확히 맞춰 쓴 첫 실제 대본(260815_1639_업어준아이 1편 · 252문장 중 대사 9~10줄)을 읽고 사용자가 판단했다 — *"나레이터를 한 명만 쓸 거라 대사가 너무 많으면 어색할 거 같아."*

- **상한 = 문장의 2.5%, 편당 따옴표 여섯 줄** (6,300자 편 기준). 5,400자인 1편도 같다.
- **벤치 ①의 4.0%는 성과 상한이 아니라 관측값이다.** "4%까지 안전"이지 "4%가 최적"이 아니다. 단일 나레이션에서 더 누르면 잃는 것이 없다 — 낮게 쓴 대본을 늘리기는 쉽고, 높게 써 놓고 한 사람이 읽으면 톤이 무너진다.
- **남기는 자리 넷 (v3.0 판 — 아래 29-6의 목록은 v2.x용이라 폐기)**: ④부탁의 핵심 한마디 / **★도량 장면의 한마디**(§0, 이 편의 대표 대사) / ⑦보상에서 상대가 인정하는 한마디 / ⑧닿음의 한마디.
- **먼저 지우는 것**: 인사·감사·설명·안내·주고받기. *"고맙습니다"* 대신 *고맙다는 말만 되풀이했습니다*.
- **끝까지 남기는 것**: 아이·노인의 한 낱말 부름("아저씨!", "아버지"). 짧아서 낭독 톤을 흔들지 않고 회수 앵커로 기능한다. **긴 대사부터 지운다.**
- 검증: `validate_script.py --style` single 모드 상한이 3%로 조여져 있다.

### 29-6. 최종 규칙과 근거 (2026-08-08 판 — 상한 수치는 29-7이 대체, 남기는 자리 목록은 v2.x용)

**규칙**
- **직접화법(따옴표) 문단 ≤ 전체 문단의 4%.** 장편 90분(문단 약 680개) 기준 **따옴표 스물다섯 줄 안팎**.
- **직접+간접 합계는 20% 안팎**까지 허용(혼주석 19.2% / 놋골무 16.3%가 검증된 값).
- 간접화법을 늘리는 것만으로는 부족하다 — **주고받기 구조 자체를 요약 서술로 눌러야** 한다.

**따옴표를 남기는 자리 (이것만)**
1. 콜드 오픈 훅 대사 (veo_hook.py가 첫 따옴표 대사를 추출하므로 **반드시 첫 문단**)
2. 테마 대사와 그 반향
3. 장 끝 클리프행어 한 줄
4. 대반전에서 악역이 제 입으로 자멸하는 한마디
5. 응보 장면의 토씨 회수
6. 인물의 전환점이 걸린 한마디 (붕대를 풀며 "발틀은 두 사람이 잡는 것이오" 류)

**타 채널 원전 실측 (2026-08-08, `_refs/001/transcript.txt` 종결어미 판별)**

| 원전 채널 | 대사 문장 비율 | 대사 글자 비중 |
|---|---|---|
| **황도야담** (놋골무 원전 · 스캔 827편 중 7위) | 7.5% | **5.7%** |
| 야담마을 (흰종이 원전 · 10.7만회) | 19.7% | 14.2% |
| 옹기과부 원전 | 22.4% | 17.8% |
| 월하야담 (혼주석 원전) | 21.7% | 18.0% |
| 달빛야담 (산가지 원전) | 31.2% | 26.4% |
| 파랑새야담 (이름석자 원전) | 42.0% | 36.8% |

→ 폭이 5.7%~36.8%로 넓지만, **가장 낮은 황도야담이 성과는 가장 좋았다.** 4% 기준은 이 데이터와 어긋나지 않는다.
→ ⚠️ **yt-dlp로 받은 자동 자막(json3)으로는 재지 말 것.** 구두점이 없어 문장 분리가 안 되고 60%대 허수가 나온다. 반드시 `collect_refs.py`가 받은 구두점 있는 자막으로 잰다.

**흰종이 교정 이력 (같은 대본, 세 번 잼)**

| 시점 | 직접화법 문단 비율 | 직접+간접 |
|---|---|---|
| 1차 집필 | 45.5% | 55%+ |
| 2차 (따옴표만 줄임) | 15.7% | 28.7% |
| **확정** | **3.4%** | **19.9%** |

→ **2차의 교훈**: 따옴표를 떼고 "~고 했습니다"로 바꾸는 것만으로는 부족했다. 주고받는 구조가 그대로 남아 여전히 대화극으로 읽혔다. **오간 말을 한 문단으로 요약**해야 서술이 된다.

**검사 (DRAFT 배치마다 · REVIEW 필수)**
```python
import re
paras = [x.strip() for x in re.split(r'\n\s*\n', open(p, encoding='utf-8').read()) if x.strip()]
direct = [x for x in paras if x.lstrip().startswith('"')]
print(len(direct) / len(paras) * 100)   # 4 넘으면 위반
```
배치 보고에 **직접화법 비율과 직접+간접 합계를 둘 다** 적는다. 하나만 재면 2차 때처럼 속는다.

---

## 29(구). 1차 초안 — 상한 25%안 (2026-08-08, 같은 날 4%로 대체됨)

**사용자 지적 원문:** *"우리가 화자가 한 명이라 대화가 이렇게 많으면 어색할 거 같은데, 이게 예전 규칙에는 없었는데 왜 갑자기 대화 대사가 늘어난 거지?"*

### 29-1. 실측 — 편마다 올라가고 있었다 (2026-08-08 전수 측정)

`script.txt`에서 따옴표로 시작하는 문단을 센 것이다.

| 편 | 대사 문단 비율 | 대사 글자 비중 |
|---|---|---|
| 혼주석 | 2.7% | 0.5% |
| 놋골무 | 9.7% | 4.9% |
| 산가지 | 22.4% | 14.5% |
| 이름석자 | 31.3% | 23.9% |
| **흰종이 (교정 전)** | **45.5%** | **36.7%** |

**추세가 문제다.** 2026-08-02에 §25-6(*"대사 문단이 장당 최소 12개"*)이 들어간 직후 편인 이름석자가 31%로 뛰었고, 흰종이에서 45%까지 갔다. **§25-6은 하한인데 목표처럼 쓰였다.**

### 29-2. 공식은 원래 정반대를 말한다

`script-guide.md` §5:
> **대사는 간접화법 위주, 결정적 순간만 직접 인용.** 직접 대사는 짧게(1~2문장) — **단일 나레이션 전제이므로** 대사도 나레이터가 자연스러운 호흡으로 읽는다.

이 조항이 §25-6에 밀려 사문화됐다. **§5가 우선이다.**

### 29-3. 단일 화자에서 대사가 많으면 실제로 이렇게 망가진다

1. **화자 구분이 사라진다** — 따옴표 문단이 셋 넷 연속되면, 한 목소리로 들을 때 누가 말하는지 놓친다. 나레이터가 배역을 나눠 연기하지 않기 때문.
2. **자막이 산만해진다** — max_chars 13자(§12)로 쪼개지므로 대사 한 줄이 큐 두세 개로 갈라진다.
3. **낭독이 탁구처럼 들린다** — 짧은 문단이 억양 변화 없이 계속 튄다. 수면 콘텐츠에 치명적.

### 29-4. 확정 규칙

- **대사 문단은 전체 문단의 25%를 넘지 않는다.** 권장 구간 **18~22%**(산가지 22.4%가 검증된 상단).
- **대사 글자 비중 15% 내외.**
- **§25-6의 "장당 최소 12개"는 하한이며, 이 상한과 함께 읽는다.** 장당 12~25개 사이.
- **연속 대사 문단 3개 이상 금지** — 사이에 행동·서술 문단을 넣는다.
- **직접 인용은 아래에만 쓴다:**
  - 콜드 오픈 훅 대사(veo 클립용 — 첫 따옴표 대사가 자동 추출된다)
  - 장 끝 클리프행어 대사
  - 테마 대사와 그 반향
  - 대반전에서 악역이 제 입으로 자멸하는 한마디
  - 응보 장면의 토씨 회수
  - 인물의 성격이 한 줄로 드러나는 결정적 대사
- **그 밖의 정보 전달·상황 설명은 전부 간접화법으로.**
  - ❌ `"보름 뒤면 감영으로 올려 보낸다."`
  - ✅ `이방은 보름 뒤면 감영으로 올려 보낸다고 했습니다.`
- **화자를 서술로 명시한다.** 단일 낭독이므로 "~가 말했습니다 / ~가 되물었습니다"를 아끼지 않는다. 대사 앞뒤에 화자 표지가 없으면 청자가 잃는다.
- **간접화법은 직접 대사보다 길다.** 전환해도 자수는 줄지 않으니 분량 걱정 없이 바꿀 것.

### 29-5. 검사 방법 (DRAFT 배치마다 · REVIEW 필수)

```python
import re
paras = [x.strip() for x in re.split(r'\n\s*\n', open(p, encoding='utf-8').read()) if x.strip()]
dial = [x for x in paras if x.lstrip().startswith('"')]
print(len(dial) / len(paras) * 100)   # 25 넘으면 위반
```
- **25%를 넘으면 그 장을 고치고 넘어간다.** 배치 보고에 이 수치를 항상 적는다.
- 연속 대사 검사: 따옴표로 시작하는 문단이 **3개 이상 연달아** 나오는 구간이 0인지 확인.

## 30. 씬 `visual_desc`에 **표정을 지정하지 않으면 전원이 같은 얼굴로 나온다** ★2026-08-11 흰종이 실측

**사용자 지적:** *"인물들의 표정이 너무 다 똑같은 거 같아."*

`style.json`의 `beautiful idealized faces`와 인물 lock의 고정 얼굴 묘사가 합쳐지면, 모델은 **"예쁜 무표정"을 기본값**으로 그린다. 격노·오열·경악 장면에서도 얼굴이 평온하다. 흰종이 파일럿 32장 전수 확인 결과 표정 변화가 사실상 없었다.

### 30-1. 전 씬 공통 — 표정 지시구를 cast 있는 씬에 무조건 넣는다

```
FACIAL EXPRESSION MATTERS: give every person a specific, strongly readable expression for this
exact moment, built from the EYEBROWS (raised, drawn together, one lifted), the EYELIDS (wide,
narrowed, half closed), the MOUTH SHAPE (open, pressed thin, corners up or down, teeth showing)
and the SET OF THE JAW. Different characters in the same picture must NOT share the same
expression. Do NOT draw a calm neutral pretty default face.
```
- **부위를 하나하나 지정하는 것이 핵심.** "sad expression" 같은 추상어는 안 먹는다. 눈썹·눈꺼풀·입모양·턱 네 가지를 명시해야 얼굴이 움직인다.
- **"한 화면의 두 인물이 같은 표정이면 안 된다"**를 명시할 것. 안 그러면 둘 다 같은 얼굴이 된다.

### 30-2. 주요 비트는 씬별로 감정을 따로 지정한다

공통 지시구만으로는 "표정이 있긴 한데 아무 표정"이 된다. 훅·최저점·대반전·응보 등 **드라마가 걸린 씬은 인물별 감정을 한 줄씩** 쓴다.
```
{kang_seobang}'s face is wrecked with rage and guilt, mouth twisted;
{dani} sits blank and hollow, past crying.
```
실측(흰종이 씬69): 남편은 눈썹이 치켜올라가고 입을 벌려 소리치는 격노, 아내는 눈을 내리깔고 무릎에 손을 모은 텅 빈 얼굴 — **한 화면에서 표정이 완전히 갈렸다.**

### 30-3. 감정 지정은 **cast와 대조 검증**할 것

씬별 감정을 id로 키잉하면 씬 번호가 밀렸을 때 **cast에 없는 인물을 부르게 된다**(흰종이에서 66개 중 17개가 어긋났다). 빌더에서 자동 검증하고, 안 맞으면 그 씬만 건너뛰고 공통 지시구만 적용한 뒤 **어긋난 목록을 출력**한다.
```python
need = set(re.findall(r'\{([a-z_]+)\}', EMO[sid]))
have = {c.split(':')[0] for c in cast}
if need <= have: desc += ' ' + EMO[sid]
else:            EMO_SKIP.append((sid, sorted(need - have), sorted(have)))
```

---

## 31. 글자 금지구는 **문서 씬이 아니라 전 씬에** 넣는다 ★2026-08-10 흰종이 실측

§27-1은 "문서 클로즈업 씬에 ILLEGIBLE 지시를 넣으라"고 했다. **그것으로는 부족했다.**

흰종이 파일럿 32장에서, **문서를 요구하지 않은 씬(작업장·마당)에도 벽과 족자에 읽히는 한자가 박혔다.** 원인은 **배경 시트 ref**다 — 지소 시트에 종이·문서가 많아 그 ref가 글자를 끌고 온다. 씬 `visual_desc`가 글자를 한 마디도 요구하지 않아도 뚫린다.

**처방: doc 여부와 무관하게 117씬 전부에 아래를 붙인다.**
```
CRITICAL RULE ABOUT WRITING: there must be NO READABLE WRITING ANYWHERE in this image. Any paper,
document, book, scroll, wall, screen, signboard, banner or cloth that would normally carry writing
must be either COMPLETELY BLANK or covered only with soft indistinct smudged vertical brush strokes
that merely SUGGEST ink without forming a single readable character. ABSOLUTELY NO Chinese
characters, NO Hanja, NO Hangul, NO modern Korean alphabet, NO Japanese characters, NO Latin
letters, NO numerals, NO signboard text, NO hanging text scrolls, NO writing on the walls, NO
watermark, NO caption, NO title card. If in doubt, leave the surface BLANK.
```
- **`NO Chinese characters`와 `NO Hanja`를 따로 써야 한다.** 기존 문구의 `NO readable Chinese characters`는 "읽을 수 없으면 된다"로 해석돼 또렷한 한자가 나왔다.
- **`NO writing on the walls` / `NO hanging text scrolls`가 핵심** — 문서가 아니라 배경 소품에서 새어 나온다.
- 재생성 결과 4씬 전부 백지 또는 흐릿한 붓자국으로 정리됐다.

---

## 32. 소품 고증은 **없는 것을 명시**해야 잡힌다 — 등잔 실측 ★2026-08-10

씬1에서 `a small brass oil lamp`라고만 썼더니 **서양식 유리 케로신 랜턴**이 나왔다. 조선 마당에 유리 등이 서 있으면 고증이 통째로 깨진다.

**처방 — 등불이 나오는 모든 씬에 자동으로 붙인다:**
```
Every lamp in this image is a TRADITIONAL KOREAN JOSEON LAMP: a shallow ceramic or brass oil
saucer holding a burning wick with an open naked flame, set on a low wooden stand, or a simple
oiled-paper lantern on a wooden frame. NO Western glass kerosene lantern, NO glass chimney or
glass globe, NO metal railroad lantern, NO hurricane lamp, NO candle in a glass jar.
```
- **§26(벙거지→갓)과 같은 원리다.** 있는 것("놋 등잔")만 쓰면 모델이 아는 흔한 물건으로 수렴한다. **없는 것(유리 갓·유리 통·서양 랜턴)을 범주째 닫아야** 잡힌다.
- 같은 함정이 예상되는 소품: 촛대·화로·가마솥·문고리·자물쇠. 씬에 나오면 "서양식 ○○ 아님"을 함께 쓸 것.
- 빌더가 `lamp|lantern|lamplight` 정규식으로 자동 주입하게 해 두면 한 곳만 고치고 빠뜨리는 사고가 없다.

---

## 33. 흰 액자·레터박스는 프롬프트로 못 막는다 — `fix_letterbox.py`를 기본 공정으로 ★2026-08-11 실측

`style.json scene_negative`에 full-bleed 금지구를 **두 번** 넣고 웹툰 프리셋으로 갈아탄 뒤에도, 흰종이 117씬 중 **21장(18%)** 에 흰 여백·띠가 생겼다. 재생성해도 같은 씬에서 재발한다.

- **씬 배치 직후 `fix_letterbox.py --apply`를 무조건 돌린다.** 과금 0원, 결정적. 원본은 `.orig.png`로 보존된다.
- **`.orig.png` 백업을 `scenes/_orig/`로 치울 것.** 안 치우면 `check_scenes.py`가 백업까지 검사해서 "아직 21장 남았다"는 허위 경고가 뜬다(2026-08-11에 실제로 헷갈렸다).
- 순서: `build.py` → `fix_letterbox.py --apply` → `.orig.png` 이동 → `check_scenes.py`(0건 확인) → `contact_sheet.py`.

## 34. ★씬 밀도 — **편 안에서만 기울인다** (2026-08-12 사용자 지시, 같은 날 v3.0으로 조정)

**사용자 지시 원문:** *"초반에는 화면이 조금 많이 바뀌어도 되는데 중후반부는 사진을 많이 안 써도 되긴 해. 즉 모두 일정하게 사진을 뽑는 게 아니라 후반부로 갈수록 한 화면에 런타임을 길게 잡아줘. 너무 차이 나게는 하지 말고."*

> **★v3.0 조정**: 이 지시는 "영상 전체가 하나의 이야기"일 때의 기울기다. **옴니버스에서는 영상 후반이 곧 5·6편의 도입부**라 전체 기울기를 걸면 마지막 편이 텅 빈다. 그리고 벤치마크 2편 모두 **전체 밀도 곡선이 평탄**했다(①은 훅 스파이크조차 없음).
>
> **적용 방식: 편 사이는 균등(각 19장), 편 안에서만 기울인다.**
> - 편별 배분: 1편 16장 + 2~6편 각 19장 = **112장**(§16).
> - 편 안 기울기: ②우연한 사건 4장(가장 촘촘) → ③④⑤ 2~3장 → ⑦⑧⑨ 각 1장(가장 성김). 씬당 평균은 편 앞쪽 **60초** → 편 뒤쪽 **90~100초**. **첫 비트 : 마지막 비트 ≈ 1 : 1.6.**
> - 아래 34-1 표(8장 기준 35초→80초)는 **단일 대하 서사 전용**이며 v3.0에서는 쓰지 않는다.

### 34-1. ~~씬당 평균 지속시간 기울기 (8장 기준)~~ — 단일 서사 전용, v3.0 미적용

| 장 | 씬당 평균 | 성격 |
|---|---|---|
| 1장 | **35~40초** | 훅·이탈 방어 구간, 가장 촘촘 |
| 2장 | 45초 | 약속 장면 |
| 3장 | 50초 | |
| 4장 | 55초 | |
| 5장 | 60초 | 최저점 |
| 6장 | 68초 | |
| 7장 | 72초 | |
| 8장 | **75~80초** | 해소·에필로그, 가장 성김 |

- **첫 장 : 마지막 장 ≈ 1 : 2.** 그 이상 벌리지 말 것("너무 차이 나게는 하지 말고").
- **한 씬 상한**: 초·중반 90초 / 후반(6~8장) **120초**. 그 이상은 정지화면이 버티지 못한다.
- 장 수가 8이 아니면 위 값을 선형 보간한다.

### 34-2. 예외 두 곳 — 기울기보다 우선한다

1. **콜드 오픈과 1장 훅** — 문장 1~2개당 한 씬(§STORYBOARD). 표의 35초보다 더 촘촘해도 된다.
2. **대반전·응보의 결정적 순간** — 시연·폭로가 벌어지는 몇 컷은 후반이라도 **30~40초**로 조인다. 대신 **같은 장의 나머지를 더 길게 잡아 장 총량은 지킨다.**

### 34-3. ⛔ 쪼개기와 병합은 항상 같이 한다 (2026-08-12 흰종이 사고)

**흰종이에서 예산 76씬(75.5분×분당1)에 117씬을 만들어 54% 초과했다. 약 2,250원이 그냥 나갔다.**
원인은 **긴 씬을 쪼개기만 하고 총량을 되돌리지 않은 것**이다. 18문장(1분 30초)짜리 씬 11개가 지루하다고 판단해 쪼갰는데, 그만큼 짧은 씬을 합치지 않았다.

- **⛔ 씬 예산 = 구간별 간격으로 뽑는다 (★2026-08-22 개정 — 아래 ×0.8 하드캡은 폐기).** 1편 0~5분 20초 · 5~20분 40초 · 20분~끝 60초 / 2편 이후 0~5분 30초 · 5분~끝 60초 (guide §9-1). 3편×43분이면 158장. 종전 규칙 "낭독 시간(분) × 0.8"은 편 안에서 어디가 촘촘해야 하는지를 말해 주지 못했다.
- 상한 계산은 **목표 분량이 아니라 실제 예상 낭독 시간**으로 한다. 흰종이는 90분을 전제로 117을 잡았는데 실제가 75.5분이라 초과율이 두 배로 뛰었다. §16의 속도(v3.0 계획값 265자/분, Vrew 기본이면 280자/분)로 먼저 예상 시간을 낸 뒤 상한을 잡을 것.
- **긴 씬을 쪼개서 총량이 상한을 넘으면, 넘긴 만큼 30초 미만 씬을 이웃과 병합해 되돌린다.** 쪼개기와 병합은 항상 한 쌍이다.
- **★편별로 따로 센다.** 총량만 맞추면 한 편이 25장, 다른 편이 13장이 되는 사고가 난다. 편당 19±2장을 지킨다.

### 34-4. STORYBOARD 보고에 반드시 적을 것

```
총 씬 수 N / 상한 M(=예상 분×0.8) / 초과율 X%
편별 씬 수 6줄 (편당 19±2인지) + 편별 씬당 평균 지속시간
```
숫자를 안 적으면 흰종이 때처럼 "30% 초과"라고 보고해 놓고 실제로는 54% 초과인 사고가 난다.

<!-- 이후 추가하고 싶은 커스텀 규칙은 여기에 계속 덧붙이세요. -->

## 10. ⚠️ CapCut 미리보기가 검은 화면 — 경로에 한글이 있으면 이미지를 못 읽는다 (2026-08-28 06편 실측)

**증상:** 드래프트는 정상적으로 열리고 타임라인·자막도 다 보이는데 **미리보기만 통째로 검다.** 오류 메시지가 없어 원인이 안 보인다.

**원인:** `Resources/` 복사본 경로에 비ASCII 문자가 있으면 CapCut Windows가 그 이미지를 로드하지 못한다. 두 군데서 한글이 섞여 들어왔다.
- **복사본 파일명** — 옴니버스는 편마다 `scene_01.png`가 따로 있어 이름이 겹친다. 종전 코드는 충돌 시 **상위 폴더명을 접두사**로 붙였는데 그 폴더 이름이 한글이라 `260821_0100_업어온아이_scene_01.png`가 됐다.
- **드래프트 이름** — `--name yadam_06편` 처럼 한글이 들어가면 폴더 경로 전체가 비ASCII가 된다.

**처방(내장, 2026-08-28):** `capcut_export.py`가 복사본을 **`m0001_scene_01.png` 꼴(순번 + ASCII 필터)** 로 짓는다 — 충돌도 순번으로 원천 차단된다. **드래프트 이름도 ASCII로 준다**(`--name yadam_06`).

**점검:** 내보낸 뒤 `draft_content.json`의 `materials.videos[].path`에 비ASCII 문자가 0개인지 본다. 정상 재생되던 단편(07편)은 복사본이 `scene_01.png`라 우연히 전부 ASCII였다 — 그래서 옴니버스에서만 터졌다.
