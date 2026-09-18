#!/usr/bin/env python3
"""
Flow 이미지 생성 클라이언트 — labs.google Flow 내부 API(aisandbox-pa)로 무료 생성.

flow_token_server.py(상주 데몬)에서 access token + reCAPTCHA 토큰을 받아
  uploadImage(참조 이미지들 → mediaId)  →  flowMedia:batchGenerateImages  →  upsampleImage(2K)
를 호출하고 결과 이미지를 out_path 에 저장한다. API 키 불필요.

기본 모델 banana(NARWHAL) — banana-pro(GEM_PIX_2)와 캐릭터 일관성 동급이면서 일일 쿼터가
훨씬 느슨함(A/B 실측 2026-07). 해상도는 upsampleImage 2K 업스케일로 확보(기본 켜짐).

generate_image.py 의 engine=="flow" 경로에서 import 되어 run() 이 호출된다.
단독 실행도 가능:
    python3 scripts/image/flow_client.py <prompt_file> <out.png> [ref1 ref2 ...] [--model banana] [--ratio 16:9] [--upscale 2K]

의존성: 표준 라이브러리만. Chrome + flow_token_server 데몬 + 확장 필요.
"""
import argparse
import base64
import hashlib
import json
import os
import ssl
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ENDPOINT_BASE = "https://aisandbox-pa.googleapis.com/v1"

MODELS = {
    "imagen4": "IMAGEN_3_5",
    "banana": "NARWHAL",
    "banana2": "NARWHAL",
    "banana-pro": "GEM_PIX_2",
}
ASPECT_MAP = {
    "1:1": "IMAGE_ASPECT_RATIO_SQUARE",
    "16:9": "IMAGE_ASPECT_RATIO_LANDSCAPE",
    "9:16": "IMAGE_ASPECT_RATIO_PORTRAIT",
    "4:3": "IMAGE_ASPECT_RATIO_LANDSCAPE_FOUR_THREE",
    "3:4": "IMAGE_ASPECT_RATIO_PORTRAIT_THREE_FOUR",
}

UPLOAD_CACHE_FILE = pathlib.Path.home() / ".flow-proxy" / "uploads.json"
UPLOAD_CACHE_TTL_MS = 6 * 3600 * 1000  # mediaId 재사용 유효기간(보수적 6시간)

_UUID_RE = re.compile(r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}")


class FlowError(RuntimeError):
    pass


def _ssl_context() -> "ssl.SSLContext | None":
    """Windows 인증서 저장소를 우회한 TLS 컨텍스트.

    ★2026-09-06 이식 — generate_image.py 에만 있던 우회가 flow 경로엔 없어서
    flow 생성이 `[ASN1: NOT_ENOUGH_DATA] not enough data` 로 전량 실패했다.
    Windows 저장소에 ASN1 이 깨진 항목이 하나라도 있으면
    ssl.create_default_context() 가 _load_windows_store_certs 에서 죽는다.
    certifi 번들을 cafile 로 직접 주면 저장소를 아예 안 읽는다.
    """
    cafile = os.environ.get("SSL_CERT_FILE")
    if not cafile:
        try:
            import certifi
            cafile = certifi.where()
        except Exception:
            return None
    try:
        return ssl.create_default_context(cafile=cafile)
    except Exception:
        return None


_SSL = _ssl_context()



FLOW_ORIGIN = "https://flow.google.com"
# flow.google.com 페이지의 WIZ_global_data.K21R3e — boq 프론트가 aisandbox-pa 에 붙일 때 쓰는 공개 API 키.
# 페이지 소스에 그대로 노출된 값이라 비밀이 아니다. 바뀌면 env FLOW_API_KEY 로 덮어쓴다.
FLOW_API_KEY = os.environ.get("FLOW_API_KEY", "AIzaSyDSjGxWlo68HcGt6mbaIq9YbkKhFQnt3sk")


def _sapisidhash(sapisid: str, origin: str = FLOW_ORIGIN) -> str:
    """Google 내부 API 표준 인증. Authorization: SAPISIDHASH {ts}_{sha1("{ts} {SAPISID} {origin}")}"""
    ts = int(time.time())
    digest = hashlib.sha1(f"{ts} {sapisid} {origin}".encode()).hexdigest()
    return f"SAPISIDHASH {ts}_{digest}"


def _auth_headers(token) -> dict:
    """token 이 str 이면 옛 OAuth Bearer, dict(authMode=sapisid) 면 새 Flow 의 쿠키 인증.

    ★2026-09-18 — Flow 가 flow.google.com(boq 앱)으로 재작성되며 OAuth 토큰을 버렸다.
    번들에 Bearer/accessToken 이 0회, SAPISIDHASH/X-Goog-AuthUser 가 있다. 이 헤더 묶음이 그 재현이다.
    """
    if isinstance(token, dict) and token.get("authMode") == "sapisid":
        return {
            "Authorization": _sapisidhash(token["sapisid"]),
            "Cookie": token["cookies"],
            "Origin": FLOW_ORIGIN,
            "Referer": FLOW_ORIGIN + "/",
            "X-Goog-AuthUser": str(token.get("authuser", "0")),
            "X-Goog-Api-Key": FLOW_API_KEY,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        }
    h = {"Origin": "https://labs.google"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def _post(url: str, payload: dict, token=None, timeout: int = 600) -> dict:
    headers = {"Content-Type": "application/json", **_auth_headers(token)}
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout, context=_SSL) as resp:
        return json.loads(resp.read())


def daemon_token(port: int) -> tuple[str, str | None]:
    """데몬에서 access token + projectId 획득."""
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/token", timeout=20) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise FlowError(f"토큰 없음: {body}. 확장에서 Connect 했는지 확인.") from e
    except urllib.error.URLError as e:
        raise FlowError(
            f"토큰 데몬(:{port})에 연결 실패 — 먼저 실행: "
            f"python3 scripts/image/flow_token_server.py --port {port}"
        ) from e
    if data.get("authMode") == "sapisid":
        return data, data.get("projectId")          # dict 자체가 자격 (SAPISIDHASH 계산용)
    return data["accessToken"], data.get("projectId")


def acquire_lane(ports: list[int], timeout: float = 300.0) -> int:
    """놀고있는 레인(데몬 포트)을 하나 잡아 반환. 전부 바쁘면 대기 후 재시도."""
    import random
    deadline = time.time() + timeout
    order = list(ports)
    while time.time() < deadline:
        random.shuffle(order)   # 편중 방지
        for p in order:
            try:
                with urllib.request.urlopen(
                    urllib.request.Request(f"http://127.0.0.1:{p}/acquire", data=b"{}", method="POST"),
                    timeout=5,
                ) as resp:
                    if json.loads(resp.read()).get("ok"):
                        return p
            except urllib.error.URLError:
                continue   # 이 레인 데몬이 안 떠있음 — 다음 레인
        time.sleep(1.5)
    raise FlowError(f"모든 레인이 사용 중/미기동 (ports={ports})")


def release_lane(port: int) -> None:
    try:
        urllib.request.urlopen(
            urllib.request.Request(f"http://127.0.0.1:{port}/release", data=b"{}", method="POST"),
            timeout=5,
        ).read()
    except urllib.error.URLError:
        pass


def daemon_recaptcha(port: int) -> str:
    """데몬 경유로 확장에서 reCAPTCHA 토큰 획득(블로킹)."""
    try:
        with urllib.request.urlopen(
            urllib.request.Request(f"http://127.0.0.1:{port}/get-recaptcha", data=b"{}", method="POST"),
            timeout=40,
        ) as resp:
            data = json.loads(resp.read())
    except urllib.error.URLError as e:
        raise FlowError(f"reCAPTCHA 요청 실패(데몬 :{port}): {e}") from e
    if data.get("error"):
        raise FlowError(data["error"])
    return data["token"]


def _load_upload_cache() -> dict:
    try:
        return json.loads(UPLOAD_CACHE_FILE.read_text())
    except (OSError, json.JSONDecodeError):
        return {}


def _save_upload_cache(cache: dict) -> None:
    try:
        UPLOAD_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        UPLOAD_CACHE_FILE.write_text(json.dumps(cache))
    except OSError:
        pass


def upload_ref(path: pathlib.Path, token: str, project_id: str, port: int, use_cache: bool = True) -> str:
    """참조 이미지 업로드 → mediaId. (projectId, 파일 sha256) 캐시로 재업로드 회피."""
    raw = path.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    key = f"{project_id}:{sha}"
    now = int(time.time() * 1000)
    cache = _load_upload_cache() if use_cache else {}
    hit = cache.get(key)
    if hit and hit.get("ts", 0) + UPLOAD_CACHE_TTL_MS > now:
        return hit["mediaId"]

    data = _post(
        f"{ENDPOINT_BASE}/flow/uploadImage",
        {"clientContext": {"projectId": project_id, "tool": "PINHOLE"},
         "imageBytes": base64.b64encode(raw).decode()},
        token=token, timeout=120,
    )
    media_id = (data.get("media") or {}).get("name")
    if not media_id:
        raise FlowError(f"업로드 응답에 mediaId 없음: {json.dumps(data)[:300]}")
    cache[key] = {"mediaId": media_id, "ts": now}
    _save_upload_cache(cache)
    return media_id


def batch_generate(prompt: str, image_inputs: list[dict], token, project_id: str,
                   recaptcha: str, model: str, ratio: str, seed: int | None) -> list[dict]:
    if isinstance(token, dict) and token.get("wiz"):
        if image_inputs:
            print("주의: 새 Flow(boq) 경로에서 참조 이미지는 아직 미지원 — 무시하고 진행", file=sys.stderr)
        return _batch_generate_boq(prompt, token, project_id, recaptcha, model, ratio, seed)
    client_ctx = {
        "projectId": project_id,
        "tool": "PINHOLE",
        "sessionId": ";" + str(int(time.time() * 1000)),
    }
    if recaptcha:   # ★새 Flow(sapisid)에서 reCAPTCHA 를 못 받으면 없이 시도한다
        client_ctx["recaptchaContext"] = {"token": recaptcha, "applicationType": "RECAPTCHA_APPLICATION_TYPE_WEB"}
    payload = {
        "clientContext": client_ctx,
        "mediaGenerationContext": {"batchId": _uuid4()},
        "useNewMedia": True,
        "requests": [{
            "clientContext": client_ctx,
            "imageModelName": MODELS.get(model, "NARWHAL"),
            "imageAspectRatio": ASPECT_MAP.get(ratio, "IMAGE_ASPECT_RATIO_LANDSCAPE"),
            "structuredPrompt": {"parts": [{"text": prompt}]},
            "seed": seed if seed is not None else _rand_seed(),
            "imageInputs": image_inputs,
        }],
    }
    data = _post(f"{ENDPOINT_BASE}/projects/{project_id}/flowMedia:batchGenerateImages",
                 payload, token=token, timeout=600)
    return extract_images(data)



# ── 새 Flow(flow.google.com, boq 앱) batchexecute 경로 ─────────────────────────
# ★2026-09-18 실측(브라우저 캡처): 새 앱은 aisandbox-pa 를 직접 부르지 않는다.
#   POST https://flow.google.com/_/AiSandboxAngularFrontend/data/batchexecute
#        ?rpcids=ogiZ0b&source-path=/project/{pid}&bl={cfb2h}&f.sid={FdrFJe}&hl=ko&_reqid=N&rt=c
#   body: f.req=[[["ogiZ0b","<args json>",null,"generic"]]]&at={SNlM0e}
#   인증 = 같은 사이트 쿠키 + at(XSRF). Authorization 헤더 없음. reCAPTCHA 토큰은 args 안에 들어간다.
#   옛 JSON API 의 필드가 그대로 protobuf 배열 자리로 옮겨졌다(아래 주석의 인덱스는 캡처 기준).
BOQ_ENDPOINT = "https://flow.google.com/_/AiSandboxAngularFrontend/data/batchexecute"
BOQ_RPC_GENERATE = "ogiZ0b"
BOQ_TOOL_PINHOLE = 22
BOQ_ASPECT = {"16:9": 3, "9:16": 2, "1:1": 1}     # 3=LANDSCAPE 는 캡처로 확인(1376x768). 나머지는 추정.


def _boq_client_ctx(project_id: str, recaptcha: str | None) -> list:
    ctx = [None, BOQ_TOOL_PINHOLE, None, None, None, project_id, None, None, None, None, None]
    if recaptcha:
        ctx[10] = [recaptcha, 1]          # [토큰, applicationType WEB]
    return ctx


def _batch_generate_boq(prompt: str, auth: dict, project_id: str, recaptcha: str | None,
                        model: str, ratio: str, seed: int | None) -> list[dict]:
    wiz = auth.get("wiz") or {}
    for k in ("at", "fsid", "bl"):
        if not wiz.get(k):
            raise FlowError(f"페이지 토큰({k}) 없음 — Flow 탭을 열어둔 채 확장에서 Reconnect")
    ctx = _boq_client_ctx(project_id, recaptcha)
    req = [None, None, None,
           seed if seed is not None else _rand_seed(),   # [3] seed
           BOQ_ASPECT.get(ratio, 3),                      # [4] aspect
           MODELS.get(model, "NARWHAL"),                  # [5] model
           None,
           ctx,                                           # [7] clientContext
           [[[prompt]]],                                  # [8] structuredPrompt.parts[].text
           None, None, None,
           _uuid4().upper(),                              # [12] batchId
           _uuid4().upper()]                              # [13] requestId
    args = [None, [req], 1, ctx, [_uuid4().upper()]]      # outer: [_, requests, 1, clientContext, [sessionId]]
    freq = json.dumps([[[BOQ_RPC_GENERATE, json.dumps(args, ensure_ascii=False, separators=(",", ":")), None, "generic"]]],
                      ensure_ascii=False, separators=(",", ":"))
    qs = urllib.parse.urlencode({
        "rpcids": BOQ_RPC_GENERATE, "source-path": f"/project/{project_id}",
        "bl": wiz["bl"], "f.sid": wiz["fsid"], "hl": "ko",
        "_reqid": str(_rand_seed() % 900000 + 100000), "rt": "c",
    })
    body = urllib.parse.urlencode({"f.req": freq, "at": wiz["at"]}).encode()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Cookie": auth["cookies"],
        "Origin": FLOW_ORIGIN, "Referer": FLOW_ORIGIN + "/",
        "X-Same-Domain": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "*/*",
    }
    r = urllib.request.Request(f"{BOQ_ENDPOINT}?{qs}", data=body, headers=headers, method="POST")
    with urllib.request.urlopen(r, timeout=600, context=_SSL) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    return _parse_boq_images(raw)


def _parse_boq_images(raw: str) -> list[dict]:
    """batchexecute 응답 → [{"type":"url","url":…,"media_id":…}]. 형식: )]}' 접두 + (길이/JSON 청크 반복)"""
    text = raw.lstrip()
    if text.startswith(")]}'"):
        text = text[4:]
    payload = None
    for m in re.finditer(r'\[\["wrb\.fr".*?\]\][\r\n]', text, re.S):
        try:
            for item in json.loads(m.group(0)):
                if item[0] == "wrb.fr" and item[1] == BOQ_RPC_GENERATE:
                    if item[2] is None:
                        raise FlowError(f"생성 RPC 가 빈 응답을 돌려줌 (에러 필드: {json.dumps(item[5:7])[:300]})")
                    payload = json.loads(item[2])
        except json.JSONDecodeError:
            continue
    if payload is None:
        raise FlowError(f"batchexecute 응답에서 wrb.fr/{BOQ_RPC_GENERATE} 를 못 찾음: {raw[:300]!r}")
    out = []
    try:
        for media in payload[0]:                         # [0] = 생성된 미디어 목록
            media_id = media[0]
            info = media[6][0]
            url = info[13]                               # 서명된 이미지 URL
            if isinstance(url, str) and url.startswith("http"):
                out.append({"type": "url", "url": url, "media_id": media_id})
    except (IndexError, TypeError, KeyError) as e:
        raise FlowError(f"응답 구조가 예상과 다름({e}): {json.dumps(payload)[:400]}") from e
    if not out:
        raise FlowError(f"응답에 이미지 URL 없음: {json.dumps(payload)[:400]}")
    return out


def _media_uuid(value) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    match = _UUID_RE.search(value)
    return match.group(0) if match else value.rsplit("/", 1)[-1]


def _find_media_id(obj) -> str | None:
    """생성 응답에서 업스케일에 쓸 mediaId를 재귀 탐색(fifeUrl 옆의 mediaId/name/id 우선)."""
    if isinstance(obj, dict):
        if "fifeUrl" in obj:
            for key in ("mediaId", "name", "id"):
                found = _media_uuid(obj.get(key))
                if found:
                    return found
        found = _media_uuid(obj.get("mediaId"))
        if found:
            return found
        for child in obj.values():
            found = _find_media_id(child)
            if found:
                return found
    elif isinstance(obj, list):
        for child in obj:
            found = _find_media_id(child)
            if found:
                return found
    return None


def extract_images(data: dict) -> list[dict]:
    media = data.get("media")
    if isinstance(media, list) and media:
        out = []
        for item in media:
            g = (item.get("image") or {}).get("generatedImage") or {}
            if g.get("fifeUrl"):
                out.append({"type": "url", "url": g["fifeUrl"], "media_id": _find_media_id(item)})
            elif g.get("encodedImage") or g.get("imageBytes"):
                out.append({"type": "base64", "data": g.get("encodedImage") or g.get("imageBytes"),
                            "media_id": _find_media_id(item)})
        if out:
            return out
    # 레거시 ImageFX 포맷 대비
    panels = data.get("imagePanels")
    if panels and panels[0].get("generatedImages"):
        return [{"type": "base64", "data": im["encodedImage"]} for im in panels[0]["generatedImages"]]
    raise FlowError(f"응답에서 이미지 추출 실패: {json.dumps(data)[:500]}")


def _download(item: dict, timeout: int = 120) -> bytes:
    if item["type"] == "url":
        with urllib.request.urlopen(item["url"], timeout=timeout, context=_SSL) as resp:
            return resp.read()
    return base64.b64decode(item["data"])


def upsample(media_id: str, resolution: str, token: str, project_id: str, port: int) -> bytes:
    """생성 이미지를 2K/4K로 업스케일(무료 티어, 별도 reCAPTCHA 필요). base64 디코드해 반환."""
    payload = {
        "mediaId": media_id,
        "targetResolution": f"UPSAMPLE_IMAGE_RESOLUTION_{resolution}",
        "clientContext": {
            "recaptchaContext": {"token": daemon_recaptcha(port),
                                 "applicationType": "RECAPTCHA_APPLICATION_TYPE_WEB"},
            "projectId": project_id,
            "tool": "PINHOLE",
            "userPaygateTier": "PAYGATE_TIER_ZERO",
            "sessionId": ";" + str(int(time.time() * 1000)),
        },
    }
    data = _post(f"{ENDPOINT_BASE}/flow/upsampleImage", payload, token=token, timeout=180)
    encoded = data.get("encodedImage")
    if not encoded:
        raise FlowError(f"업스케일 응답에 이미지 없음: {json.dumps(data)[:300]}")
    return base64.b64decode(encoded)


def _retry_wait(status: int) -> float | None:
    """상태코드별 재시도 대기(초). None = 재시도 불가."""
    if status == 403:
        return 30
    if status == 408:
        return 5
    if status == 429:
        return 120
    if 500 <= status < 600:
        return 5
    return None


def run(prompt: str, out_path: pathlib.Path, refs: list[pathlib.Path],
        model: str = "banana", ratio: str = "16:9", ports: list[int] | int = 3847,
        seed: int | None = None, max_retries: int = 3, upscale: str = "2K") -> int:
    """flow 경로 진입점. ports가 여러 개면 놀고있는 레인(계정)을 잡아 병렬 처리. 성공 0, 실패 비0.
    upscale: "2K"|"4K"|"" — 생성 후 upsampleImage 업스케일(실패 시 원본 저장, 기본 2K)."""
    port_list = [ports] if isinstance(ports, int) else list(ports)
    # 레인 임대 — 단일 포트면 그 포트, 멀티면 놀고있는 것 하나
    try:
        port = acquire_lane(port_list)
    except FlowError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    try:
        return _run_on_port(prompt, out_path, refs, model, ratio, port, seed, max_retries, upscale)
    finally:
        release_lane(port)


def _run_on_port(prompt: str, out_path: pathlib.Path, refs: list[pathlib.Path],
                 model: str, ratio: str, port: int,
                 seed: int | None, max_retries: int, upscale: str = "2K") -> int:
    try:
        token, project_id = daemon_token(port)
    except FlowError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if not project_id:
        print("error: projectId 미설정 — labs.google Flow 프로젝트 URL의 UUID를 "
              f"'curl -X POST localhost:{port}/set-project -d \\'{{\"projectId\":\"<UUID>\"}}\\''로 저장하거나 "
              "확장 Connect 후 재시도.", file=sys.stderr)
        return 2

    # 참조 이미지 업로드(캐시). 실패해도 ref 없이 진행하지 않고 명확히 실패시킴.
    try:
        image_inputs = [{"name": upload_ref(r, token, project_id, port)} for r in refs]
    except (FlowError, urllib.error.HTTPError, urllib.error.URLError, OSError) as e:
        print(f"error: 참조 업로드 실패: {e}", file=sys.stderr)
        return 1

    backoff = 5
    want_upscale = str(upscale or "").upper()
    for attempt in range(1, max_retries + 1):
        try:
            try:
                recaptcha = daemon_recaptcha(port)
            except FlowError as rc_err:
                if isinstance(token, dict):   # sapisid 모드: 새 Flow 탭엔 grecaptcha 가 없을 수 있다 → 없이 시도
                    print(f"reCAPTCHA 없이 시도 ({rc_err})", file=sys.stderr)
                    recaptcha = None
                else:
                    raise
            images = batch_generate(prompt, image_inputs, token, project_id,
                                    recaptcha, model, ratio, seed)
            first = images[0]
            buf = None
            tag = f"flow/{model}"
            if want_upscale in ("2K", "4K") and first.get("media_id") and not (isinstance(token, dict) and token.get("wiz")):
                try:
                    buf = upsample(first["media_id"], want_upscale, token, project_id, port)
                    tag += f"+{want_upscale}"
                except (FlowError, urllib.error.HTTPError, urllib.error.URLError, OSError) as exc:
                    print(f"업스케일 실패, 원본 저장: {exc}", file=sys.stderr)
            if buf is None:
                buf = _download(first)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(buf)
            print(f"saved {out_path}  ({out_path.stat().st_size} bytes)  [{tag}]")
            return 0
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")
            if e.code == 401:
                print("HTTP 401 — 인증 거절. 확장에서 Reconnect (구글 로그인 쿠키 갱신) 후 재시도.", file=sys.stderr)
                return 1
            wait = _retry_wait(e.code)
            if wait is not None and attempt < max_retries:
                print(f"HTTP {e.code} — {wait:.0f}s 후 재시도 ({attempt}/{max_retries})", file=sys.stderr)
                time.sleep(wait)
                continue
            print(f"HTTP {e.code} from Flow: {body[:800]}", file=sys.stderr)
            return 1
        except FlowError as e:
            # reCAPTCHA/추출 실패는 일시적일 수 있어 한 번 더
            if attempt < max_retries:
                print(f"{e} — 재시도 ({attempt}/{max_retries})", file=sys.stderr)
                time.sleep(backoff)
                backoff *= 2
                continue
            print(f"error: {e}", file=sys.stderr)
            return 1
        except (urllib.error.URLError, OSError) as e:
            print(f"network error: {e}", file=sys.stderr)
            return 1
    return 1


# ── 결정론 회피용 소도구(표준 random/uuid 사용) ─────────────────────────────
def _uuid4() -> str:
    import uuid
    return str(uuid.uuid4())


def _rand_seed() -> int:
    import random
    return random.randint(0, 2_147_483_647)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prompt_file", type=pathlib.Path)
    ap.add_argument("out_path", type=pathlib.Path)
    ap.add_argument("refs", nargs="*", type=pathlib.Path)
    ap.add_argument("--model", default="banana")
    ap.add_argument("--ratio", default="16:9")
    ap.add_argument("--ports", default="3847", help="데몬 포트(들). 쉼표구분 멀티계정 레인. 예: 3847,3848,3849")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--upscale", default="2K", help='업스케일 해상도: 2K(기본)|4K|"" (끄기)')
    args = ap.parse_args()
    ports = [int(x) for x in str(args.ports).split(",") if x.strip()]

    if not args.prompt_file.exists():
        print(f"error: prompt file not found: {args.prompt_file}", file=sys.stderr)
        return 2
    for r in args.refs:
        if not r.exists():
            print(f"error: ref not found: {r}", file=sys.stderr)
            return 2

    prompt = args.prompt_file.read_text(encoding="utf-8")
    return run(prompt, args.out_path, list(args.refs),
               model=args.model, ratio=args.ratio, ports=ports, seed=args.seed,
               upscale=args.upscale)


if __name__ == "__main__":
    sys.exit(main())
