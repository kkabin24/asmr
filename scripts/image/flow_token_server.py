#!/usr/bin/env python3
"""
Flow 토큰 브리지 데몬 — labs.google Flow 웹세션으로 무료 이미지 생성을 위한 상주 서버.

Chrome 확장(scripts/image/flow_extension/, flow-proxy MIT 이식)이
  1) 로그인 세션에서 OAuth access token(ya29...) + session cookie 를 뽑아 POST /auth 로 넘기고,
  2) 백그라운드에서 POST /get-recaptcha 요청이 들어오면 GET /need-recaptcha 폴링으로 감지 →
     grecaptcha.enterprise.execute() 실행 → POST /recaptcha-token 으로 토큰을 돌려준다.

이 데몬은 flow_client.py(이미지 생성 클라이언트)와 확장 사이의 중개자다.
토큰은 ~/.flow-proxy/token.json 에 저장(= flow-proxy 확장과 완전 호환).

한 번만 띄워두고(배치 도는 동안 상주) Chrome에 labs.google/fx/tools/flow 탭을
로그인 상태로 열어두면, 여러 generate_image.py 서브프로세스가 동시에 붙어 무료로 이미지를 뽑는다.

Usage:
    python3 scripts/image/flow_token_server.py [--port 3847]

상태 확인:  curl -s localhost:3847/status
"""
import argparse
import json
import pathlib
import ssl
import sys
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TOKEN_DIR = pathlib.Path.home() / ".flow-proxy"
TOKEN_FILE = TOKEN_DIR / "token.json"
SESSION_URL = "https://labs.google/fx/api/auth/session"
SESSION_COOKIE_NAME = "__Secure-next-auth.session-token"
RECAPTCHA_ACTION = "IMAGE_GENERATION"
RECAPTCHA_WAIT = 30.0  # 확장이 토큰을 돌려줄 때까지 클라이언트가 기다리는 최대 시간(초)

_file_lock = threading.Lock()
_log_lock = threading.Lock()
LOG_FILE = TOKEN_DIR / "daemon.log"


def dlog(msg: str) -> None:
    """관측용: stdout 버퍼링과 무관하게 전용 파일에 즉시 기록."""
    line = f"{time.strftime('%H:%M:%S')} {msg}\n"
    with _log_lock:
        try:
            TOKEN_DIR.mkdir(parents=True, exist_ok=True)
            with open(LOG_FILE, "a") as f:
                f.write(line)
                f.flush()
        except OSError:
            pass
    print(line, end="", flush=True)

# ── reCAPTCHA 직렬화 상태 ────────────────────────────────────────────────
# flow-proxy 확장은 요청 식별자(id) 없이 need→execute→post 계약만 안다.
# 그래서 동시 클라이언트를 turn_lock 으로 직렬화해 항상 한 건만 "needed" 로 둔다.
# (실제 이미지 생성은 계속 병렬 — 짧은 reCAPTCHA 취득 단계만 줄 세운다.)
_turn_lock = threading.Lock()
_poll_count = 0
_last_poll_log = 0.0
_wait_count = 0
_last_wait_log = 0.0
_need = False
_action = RECAPTCHA_ACTION
_result = None            # {"token": ...} | {"error": ...}
_result_ready = threading.Event()
_need_event = threading.Event()   # SW long-poll(/wait-recaptcha)를 깨우는 신호
_state_lock = threading.Lock()

# ── 레인 임대(lease) ── 멀티계정: 클라이언트가 놀고있는 데몬(레인)을 잡아 쓰고 반납.
_lease_lock = threading.Lock()
_busy = False
_busy_since = 0.0
LEASE_TIMEOUT = 240.0     # 이 시간 넘게 잡고있으면(크래시 등) 강제 회수


def read_token() -> dict:
    with _file_lock:
        if not TOKEN_FILE.exists():
            return {}
        try:
            return json.loads(TOKEN_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            return {}


def save_token(data: dict) -> None:
    with _file_lock:
        TOKEN_DIR.mkdir(parents=True, exist_ok=True)
        TOKEN_FILE.write_text(json.dumps(data, indent=2))


def now_ms() -> int:
    return int(time.time() * 1000)


def verify_token(tok: str) -> tuple[bool, str]:
    """Google tokeninfo 로 access token 이 실제로 살아 있는지 확인.

    ★2026-09-18 신설. Flow 가 flow.google.com 으로 옮겨간 뒤, labs.google 세션 엔드포인트가
    만료된 ya29 토큰을 그대로 돌려주는 경우가 생겼다. 데몬은 접두(ya29)만 보고 "Connected" 로
    받아줬고, 생성 단계에서야 401 이 났다. 여기서 걸러 팝업에 바로 이유를 보여준다.
    네트워크 오류면 (True, 'unverified') — 검증 실패로 막지는 않는다.
    """
    try:
        import certifi
        ctx = ssl.create_default_context(cafile=certifi.where())
    except Exception:
        ctx = None
    try:
        req = urllib.request.Request(f"https://oauth2.googleapis.com/tokeninfo?access_token={tok}")
        with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
            info = json.loads(r.read())
        return True, f"valid (expires_in={info.get('expires_in')}s)"
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read())
        except Exception:
            body = {}
        return False, body.get("error_description") or body.get("error") or f"HTTP {e.code}"
    except Exception as e:
        return True, f"unverified ({e.__class__.__name__})"


def refresh_via_cookie(session_cookie: str) -> str | None:
    """session cookie 로 labs.google 세션 엔드포인트에서 새 access token 획득(~30일 유효)."""
    req = urllib.request.Request(
        SESSION_URL,
        headers={"Cookie": f"{SESSION_COOKIE_NAME}={session_cookie}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
    except (urllib.error.URLError, json.JSONDecodeError, OSError):
        return None
    if data.get("error"):
        # 예: ACCESS_TOKEN_REFRESH_NEEDED — 세션이 죽은 토큰을 돌려주므로 신뢰 금지.
        # 브라우저에서 Flow 탭 새로고침 → 확장 Reconnect 로 새 쿠키를 받아야 한다.
        dlog(f"[refresh] 세션 에러: {data['error']} — Reconnect 필요")
        return None
    return data.get("access_token") or data.get("accessToken")


def get_valid_token() -> tuple[str | None, str]:
    """유효한 access token 반환. (token, note). 만료 5분 전이면 cookie 로 자동 리프레시.

    ★2026-09-18 — authMode == "sapisid" 면 access token 이 없다. 이 모드에서는
    SAPISID 쿠키가 곧 자격이고(요청마다 SAPISIDHASH 로 해시), 만료 개념도 다르다.
    "sapisid" 문자열을 토큰 자리에 돌려 connected 판정을 통과시키고, 실제 자격은 /token 이 준다.
    """
    data = read_token()
    if data.get("authMode") == "sapisid" and data.get("sapisid") and data.get("cookies"):
        return "sapisid", "sapisid"
    tok = data.get("accessToken")
    exp = data.get("expiresAt", 0)
    if tok and exp > now_ms() + 300_000:
        return tok, "cached"

    cookie = data.get("sessionCookie")
    if cookie:
        new = refresh_via_cookie(cookie)
        if new:
            data.update(accessToken=new, expiresAt=now_ms() + 3_600_000)
            save_token(data)
            return new, "refreshed"
        return None, "session cookie expired — 확장에서 Reconnect 필요"
    if tok:
        # 쿠키 없이 만료 임박한 토큰: 그래도 반환(1시간짜리). 곧 만료면 재연결 필요.
        return tok, "no-refresh-cookie"
    return None, "no token — 확장에서 Connect 필요"


def request_recaptcha(action: str = RECAPTCHA_ACTION) -> dict:
    """확장에 reCAPTCHA 토큰을 요청하고 결과를 기다린다(직렬화). {"token"} 또는 {"error"}."""
    global _need, _action, _result
    with _turn_lock:
        with _state_lock:
            _need = True
            _action = action
            _result = None
            _result_ready.clear()
        _need_event.set()          # SW long-poll 깨우기
        got = _result_ready.wait(RECAPTCHA_WAIT)
        with _state_lock:
            _need = False
            res = _result
        _need_event.clear()
        if not got or res is None:
            return {"error": "reCAPTCHA timeout — Chrome에 labs.google/fx/tools/flow 탭이 "
                             "로그인된 채 열려있고 확장이 로드됐는지 확인하세요."}
        return res


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # 조용히
        pass

    # ★2026-09-06 신설 — 진단용 요청 기록.
    # 종전에는 /auth 가 400 으로 거절돼도 아무 흔적이 안 남아,
    # "확장이 안 보낸 것"과 "보냈는데 거절된 것"을 구분할 수 없었다.
    # 폴링(/need-recaptcha, /wait-recaptcha)은 초당 여러 건이라 제외한다.
    _QUIET = ("/need-recaptcha", "/wait-recaptcha")

    def _rlog(self, extra: str = ""):
        if self.path in self._QUIET:
            return
        origin = self.headers.get("Origin", "-")
        dlog(f"[req] {self.command} {self.path}  origin={origin} {extra}".rstrip())

    def _cors(self):
        # PNA: 공개 사이트(labs.google) → loopback(localhost) 요청 허가.
        # Origin 을 그대로 echo(=* 대신) + Allow-Private-Network 로 loopback 접근 승인.
        origin = self.headers.get("Origin", "*")
        self.send_header("Access-Control-Allow-Origin", origin)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("Access-Control-Max-Age", "600")
        self.send_header("Vary", "Origin")

    def _send(self, code: int, obj: dict):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self._cors()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        n = int(self.headers.get("Content-Length", 0) or 0)
        if not n:
            return {}
        try:
            return json.loads(self.rfile.read(n))
        except json.JSONDecodeError:
            return {}

    def do_OPTIONS(self):
        # PNA 프리플라이트: Access-Control-Request-Private-Network: true 에 응답
        self._rlog("(CORS/PNA 프리플라이트)")
        self.send_response(204)
        self._cors()
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        self._rlog()
        if self.path == "/status":
            tok, note = get_valid_token()
            self._send(200, {"connected": bool(tok), "message": note, "busy": _busy})
        elif self.path == "/need-recaptcha":
            # 확장 bridge.js(ISOLATED) 가 1.5s 마다 폴링
            global _poll_count, _last_poll_log
            _poll_count += 1
            t = time.time()
            if t - _last_poll_log > 3:  # 3초마다 heartbeat 한 줄
                _last_poll_log = t
                dlog(f"[poll] /need-recaptcha 누적 {_poll_count}회 (bridge가 데몬에 닿는중)")
            with _state_lock:
                self._send(200, {"needed": _need, "action": _action})
        elif self.path == "/ping":
            dlog("[ping] 확장 SW 로드 확인 — SW→localhost 네트워킹 OK")
            self._send(200, {"ok": True})
        elif self.path == "/wait-recaptcha":
            # 확장 SW long-poll: 클라이언트가 reCAPTCHA를 필요로 할 때까지 ~25s 블록
            global _wait_count, _last_wait_log
            _wait_count += 1
            t = time.time()
            if t - _last_wait_log > 15:
                _last_wait_log = t
                dlog(f"[wait] SW long-poll 누적 {_wait_count}회 (SW가 데몬에 닿는중)")
            signaled = _need_event.wait(25)
            if signaled and _need:
                _need_event.clear()      # claim — 중복 서빙 방지
                dlog(f"[wait] reCAPTCHA 필요 → SW에 전달 (action={_action})")
                self._send(200, {"needed": True, "action": _action})
            else:
                self._send(200, {"needed": False})
        elif self.path == "/token":
            # flow_client 가 access token + projectId 를 얻는 곳
            tok, note = get_valid_token()
            data = read_token()
            if tok == "sapisid":
                self._send(200, {"authMode": "sapisid", "sapisid": data["sapisid"], "cookies": data["cookies"],
                                 "authuser": data.get("authuser", "0"), "projectId": data.get("projectId"),
                                 "note": note})
                return
            if tok:
                # sessionCookie: 비디오 다운로드(labs.google tRPC redirect)가 쿠키 인증이라 함께 노출(localhost 전용)
                self._send(200, {"accessToken": tok, "projectId": data.get("projectId"),
                                 "sessionCookie": data.get("sessionCookie"), "note": note})
            else:
                self._send(425, {"error": note})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        global _result
        self._rlog()
        if self.path == "/auth":
            # 확장이 로그인 토큰+쿠키를 넘김
            body = self._read_json()
            if body.get("authMode") == "sapisid":
                # ★2026-09-18 새 Flow(flow.google.com, boq 앱) — OAuth 토큰 없이
                #   구글 계정 쿠키(SAPISID)로 SAPISIDHASH 인증. 확장이 google.com 쿠키를 넘긴다.
                sap = body.get("sapisid") or ""
                cookies = body.get("cookies") or ""
                n_cookies = cookies.count("=")
                dlog(f"[auth] sapisid 모드 수신: SAPISID 길이={len(sap)} 쿠키 {n_cookies}개 authuser={body.get('authuser', 0)}")
                if not sap or n_cookies < 3:
                    self._send(400, {"error": "google.com 쿠키(SAPISID)를 못 읽음 — 이 프로필에서 구글에 로그인돼 있는지, 확장에 google.com 권한이 있는지 확인"})
                    return
                save_token({
                    "authMode": "sapisid",
                    "sapisid": sap,
                    "cookies": cookies,
                    "authuser": str(body.get("authuser", 0)),
                    "savedAt": now_ms(),
                    "projectId": read_token().get("projectId") or body.get("projectId"),
                })
                dlog("[auth] ✓ 저장 완료 — Connected (sapisid)")
                self._send(200, {"ok": True, "message": "Connected (sapisid)"})
                return
            tok = body.get("accessToken", "")
            dlog(f"[auth] 수신: 토큰 접두={tok[:4]!r} 길이={len(tok)} "
                 f"쿠키={'있음' if body.get('sessionCookie') else '없음'}")
            if not tok.startswith("ya29"):
                dlog("[auth] 거절 — ya29 로 시작하지 않음")
                self._send(400, {"error": "invalid access token"})
                return
            ok, why = verify_token(tok)
            dlog(f"[auth] Google 검증: {why}")
            if not ok:
                self._send(400, {"error": f"토큰이 무효({why}) — labs.google/fx 에 다시 로그인한 뒤 Reconnect"})
                return
            save_token({
                "accessToken": tok,
                "sessionCookie": body.get("sessionCookie"),
                "expiresAt": now_ms() + 3_600_000,
                "projectId": read_token().get("projectId") or body.get("projectId"),
            })
            dlog("[auth] ✓ 저장 완료 — Connected")
            self._send(200, {"ok": True, "message": "Connected"})
        elif self.path == "/recaptcha-token":
            # 확장이 실행한 reCAPTCHA 결과
            body = self._read_json()
            with _state_lock:
                if body.get("error"):
                    _result = {"error": body["error"]}
                elif body.get("token"):
                    _result = {"token": body["token"]}
                else:
                    _result = {"error": "empty recaptcha response"}
                _result_ready.set()
            self._send(200, {"ok": True})
        elif self.path == "/get-recaptcha":
            # flow_client 가 생성 직전 호출(블로킹). body {"action": "VIDEO_GENERATION"} 로 액션 지정 가능
            body = self._read_json()
            self._send(200, request_recaptcha(body.get("action") or RECAPTCHA_ACTION))
        elif self.path == "/acquire":
            # 멀티계정 레인 임대: 안 바쁘면 잡고 ok, 바쁘면 거절(단 오래된 임대는 스틸)
            global _busy, _busy_since
            with _lease_lock:
                now = time.time()
                if _busy and (now - _busy_since) < LEASE_TIMEOUT:
                    self._send(200, {"ok": False})
                else:
                    _busy = True
                    _busy_since = now
                    self._send(200, {"ok": True})
        elif self.path == "/release":
            with _lease_lock:
                _busy = False
            self._send(200, {"ok": True})
        elif self.path == "/set-project":
            # projectId 저장(최초 1회 편의)
            body = self._read_json()
            pid = body.get("projectId")
            if pid:
                data = read_token()
                data["projectId"] = pid
                save_token(data)
                self._send(200, {"ok": True, "projectId": pid})
            else:
                self._send(400, {"error": "projectId 필요"})
        else:
            self._send(404, {"error": "not found"})


def main() -> int:
    global TOKEN_FILE
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=3847)
    ap.add_argument("--host", default="127.0.0.1")
    args = ap.parse_args()

    # 멀티계정: 데몬(=레인/계정)마다 토큰 파일 분리. 레거시 token.json은 '주 레인' 3847에만
    # 1회 마이그레이션(그 외 포트로 복사하면 여러 레인이 같은 계정을 보게 됨).
    TOKEN_FILE = TOKEN_DIR / f"token_{args.port}.json"
    legacy = TOKEN_DIR / "token.json"
    if args.port == 3847 and not TOKEN_FILE.exists() and legacy.exists():
        try:
            TOKEN_DIR.mkdir(parents=True, exist_ok=True)
            TOKEN_FILE.write_text(legacy.read_text())
        except OSError:
            pass

    try:
        srv = ThreadingHTTPServer((args.host, args.port), Handler)
    except OSError as e:
        print(f"포트 {args.port} 사용 불가 (이미 데몬이 떠 있을 수 있음): {e}", file=sys.stderr)
        return 1

    tok, note = get_valid_token()
    print(f"Flow 토큰 브리지(레인) 시작 → http://{args.host}:{args.port}  토큰파일={TOKEN_FILE.name}")
    print(f"  토큰 상태: {'연결됨' if tok else '미연결'} ({note})")
    print(f"  이 레인의 Chrome 프로필에서: 확장 팝업 포트를 {args.port} 로 설정 → Flow 로그인 → Connect")
    print(f"  중지: Ctrl-C")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n종료")
    return 0


if __name__ == "__main__":
    sys.exit(main())
