/**
 * Flow Proxy Auth - Chrome Extension
 * Connects Google Flow to CLI scripts for image generation
 */

const FLOW_URL = 'https://flow.google.com/';
// ★2026-09-06: Flow 가 flow.google.com 으로 이전. 탭 조회는 두 도메인을 모두 본다.
const FLOW_TAB_URLS = ['https://flow.google.com/*', 'https://labs.google/*'];
const isFlowTab = (u) => !!u && (u.includes('flow.google.com') || u.includes('labs.google'));
const AUTH_SESSION_URL = 'https://labs.google/fx/api/auth/session';
const SESSION_COOKIE_NAME = '__Secure-next-auth.session-token';

// 레인 포트: 프로필(계정)마다 다른 데몬 포트. chrome.storage.local에 저장.
let FLOW_PORT = 3847;
function proxyUrl() { return `http://localhost:${FLOW_PORT}`; }

async function loadPort() {
  const { flowPort } = await chrome.storage.local.get('flowPort');
  if (flowPort) FLOW_PORT = flowPort;
  const el = document.getElementById('portInput');
  if (el) el.value = FLOW_PORT;
}
async function savePort(p) {
  FLOW_PORT = p;
  await chrome.storage.local.set({ flowPort: p });
}

const statusEl = document.getElementById('status');
const statusTextEl = document.getElementById('statusText');
const infoEl = document.getElementById('info');
const connectBtn = document.getElementById('connectBtn');
const openFlowBtn = document.getElementById('openFlowBtn');
const errorEl = document.getElementById('error');

function showError(message) {
  errorEl.textContent = message;
  errorEl.style.display = 'block';
}

function hideError() {
  errorEl.style.display = 'none';
}

function updateStatus(connected, message) {
  statusEl.className = `status ${connected ? 'connected' : 'disconnected'}`;
  statusTextEl.textContent = message;
}

function setLoading(loading) {
  if (loading) {
    statusEl.className = 'status loading';
    statusTextEl.textContent = 'Connecting...';
    connectBtn.disabled = true;
    connectBtn.textContent = 'Connecting...';
  } else {
    connectBtn.disabled = false;
    connectBtn.textContent = 'Connect';
  }
}

async function checkSessionStatus() {
  try {
    const res = await fetch(AUTH_SESSION_URL, { credentials: 'include' });
    if (!res.ok) return null;
    const data = await res.json();
    return data.access_token || data.accessToken || null;
  } catch {
    return null;
  }
}

/**
 * Get access token via content script injection.
 * executeScript with async func returns a Promise-wrapped value,
 * so we must use the proper callback pattern.
 */
async function getTokenFromTab(tabId) {
  const results = await chrome.scripting.executeScript({
    target: { tabId },
    func: async () => {
      try {
        const res = await fetch('https://labs.google/fx/api/auth/session');
        if (!res.ok) return null;
        const data = await res.json();
        return data.access_token || data.accessToken || null;
      } catch {
        return null;
      }
    }
  });

  if (results && results[0] && results[0].result) {
    return results[0].result;
  }
  return null;
}

/**
 * ★2026-09-18 새 Flow(flow.google.com, boq 앱) 인증 — 구글 계정 쿠키.
 * 새 앱은 OAuth 토큰을 쓰지 않고 SAPISID 쿠키로 SAPISIDHASH 를 만든다.
 * 이 프로필의 google.com 쿠키를 모아 데몬에 넘기면, 클라이언트가 요청마다 해시를 계산한다.
 * 구글 로그인 쿠키 전체가 로컬 데몬(~/.flow-proxy)에 저장된다 — 본인 PC·버너 계정 전제.
 */
/**
 * ★2026-09-18 새 Flow 의 페이지 토큰 — 로그인된 flow.google.com 탭의 WIZ_global_data 에서
 * at(SNlM0e, XSRF) / f.sid(FdrFJe) / bl(cfb2h) 를 읽는다. batchexecute 호출에 셋 다 필요하다.
 */
async function getWizFromFlowTab() {
  const tabs = await chrome.tabs.query({ url: 'https://flow.google.com/*' });
  if (!tabs.length) return { error: 'flow.google.com 탭이 열려 있지 않음 — Open Flow 로 열고 로그인 후 다시 Connect' };
  try {
    const [res] = await chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      world: 'MAIN',
      func: () => {
        const w = (window.WIZ_global_data || {});
        return { at: w.SNlM0e || null, fsid: w.FdrFJe || null, bl: w.cfb2h || null };
      },
    });
    const wiz = (res && res.result) || {};
    if (!wiz.at) return { error: 'Flow 탭에서 로그인 토큰(at)을 못 읽음 — 그 탭에서 구글 로그인 상태인지 확인 후 새로고침' };
    return { wiz };
  } catch (e) {
    return { error: 'Flow 탭 접근 실패: ' + String((e && e.message) || e) };
  }
}

async function getGoogleCookieBundle() {
  const all = await chrome.cookies.getAll({ domain: 'google.com' });
  const byName = {};
  for (const c of all) {
    // 같은 이름이 여러 경로/도메인에 있으면 .google.com 루트 것을 우선
    if (!byName[c.name] || c.domain === '.google.com') byName[c.name] = c;
  }
  const sapisid = (byName['SAPISID'] || byName['__Secure-3PAPISID'] || byName['__Secure-1PAPISID'] || {}).value || null;
  const wanted = Object.values(byName).filter(c =>
    /^(SID|HSID|SSID|APISID|SAPISID|NID|SIDCC|__Secure-|__Host-)/.test(c.name));
  const cookies = wanted.map(c => `${c.name}=${c.value}`).join('; ');
  return { sapisid, cookies, count: wanted.length };
}

/**
 * Get session cookie for long-lived auto-refresh (~30 days)
 */
async function getSessionCookie() {
  const cookie = await chrome.cookies.get({
    url: 'https://labs.google',
    name: SESSION_COOKIE_NAME
  });
  return cookie ? cookie.value : null;
}

/**
 * Send token + session cookie to the local auth server
 */
async function sendAuthToProxy(accessToken, sessionCookie) {
  const response = await fetch(`${proxyUrl()}/auth`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ accessToken, sessionCookie })
  });

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.error || 'Failed to send token');
  }

  return response.json();
}

async function handleConnect() {
  hideError();
  setLoading(true);

  // Connect 시점에 입력칸 포트를 직접 반영(blur 누락 대비 — 엉뚱한 포트로 붙는 것 방지)
  try {
    const portEl = document.getElementById('portInput');
    if (portEl && portEl.value) await savePort(parseInt(portEl.value) || 3847);
  } catch {}

  try {
    // ★2026-09-18 1순위: 구글 쿠키(SAPISID) 인증 — 새 Flow 는 이것만 받는다.
    // 언패킹 확장은 매니페스트에 host 권한을 더해도 Chrome 이 조용히 보류하는 경우가 있다(실측: granted 에 없음).
    // 클릭(사용자 제스처) 시점에 명시적으로 요청하면 승인 창이 뜬다.
    const GOOGLE_ORIGINS = ['https://*.google.com/*', 'https://google.com/*'];
    let hasGoogle = await chrome.permissions.contains({ origins: GOOGLE_ORIGINS }).catch(() => false);
    if (!hasGoogle) {
      hasGoogle = await chrome.permissions.request({ origins: GOOGLE_ORIGINS }).catch(() => false);
      if (!hasGoogle) throw new Error('google.com 쿠키 접근 권한이 거부됨 — Connect 를 다시 누르고 "허용"을 선택하세요');
    }
    const bundle = await getGoogleCookieBundle();
    if (bundle.sapisid) {
      const w = await getWizFromFlowTab();
      if (w.error) throw new Error(w.error);
      const portOk = await fetch(`${proxyUrl()}/auth`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ authMode: 'sapisid', sapisid: bundle.sapisid, cookies: bundle.cookies, authuser: 0, wiz: w.wiz })
      }).then(async r => {
        const d = await r.json().catch(() => ({}));
        if (!r.ok) throw new Error(`데몬이 거절: ${d.error || r.status}`);
        return d;
      }, e => { throw new Error(`데몬(포트 ${FLOW_PORT})에 연결 실패 — flow_token_server.py 가 떠 있는지 확인 (${e.message})`); });
      updateStatus(true, 'Connected');
      infoEl.textContent = `구글 쿠키 + 페이지 토큰(at) 확보 · 쿠키 ${bundle.count}개 · reCAPTCHA: auto`;
      connectBtn.textContent = 'Reconnect';
      return;
    }

    // ── 아래는 옛 labs.google OAuth 경로 (SAPISID 를 못 읽었을 때만) ──
    // ★2026-09-06 재수정 — 탭 의존을 없앤다.
    // 종전 경로는 labs.google 탭을 찾아 그 안에서 세션을 fetch 했는데,
    // chrome.tabs.query 는 **같은 프로필의 탭만** 본다. 다른 프로필/창(또는 시크릿)에
    // Flow 를 띄워두면 탭이 눈앞에 있어도 0개로 나와 Connect 가 막혔다.
    // 그런데 팝업 자신이 host_permissions(https://labs.google/*) + 쿠키로
    // 세션을 직접 가져올 수 있다(init() 의 OAuth ✓ 가 그 증거다). 그걸 1순위로 쓴다.
    let accessToken = await checkSessionStatus();

    if (!accessToken) {
      // 폴백: 탭 컨텍스트에서 뽑기 (쿠키 파티셔닝 등으로 팝업 fetch 가 막힌 경우)
      let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      if (!tab || !isFlowTab(tab.url)) {
        const found = await chrome.tabs.query({ url: FLOW_TAB_URLS });
        tab = found[0] || null;
      }
      if (tab) accessToken = await getTokenFromTab(tab.id);
    }

    if (!accessToken) {
      const n = (await chrome.tabs.query({ url: FLOW_TAB_URLS })).length;
      throw new Error(
        `로그인 세션을 못 읽었습니다 (이 프로필에서 보이는 labs.google 탭 ${n}개). ` +
        `Flow 를 이 프로필 창에서 열고 구글 로그인 후 다시 시도하세요.`
      );
    }

    // Get session cookie for auto-refresh
    const sessionCookie = await getSessionCookie();

    // Send to local proxy server (must be running via generate.mjs)
    // ★2026-09-06 수정: 종전에는 모든 실패를 'CLI server not running' 으로 뭉갰다.
    // 데몬이 400(invalid access token) 을 돌려줘도 같은 문구가 떠서 원인을 못 봤다.
    try {
      await sendAuthToProxy(accessToken, sessionCookie);
    } catch (e) {
      const msg = (e && e.message) || String(e);
      if (/Failed to fetch|NetworkError|load failed/i.test(msg)) {
        throw new Error(`데몬(포트 ${FLOW_PORT})에 연결 실패 — flow_token_server.py 가 떠 있는지 확인`);
      }
      throw new Error(`데몬이 거절: ${msg}`);
    }

    updateStatus(true, 'Connected');
    infoEl.textContent = (sessionCookie ? 'Token auto-refreshes for ~30 days.' : 'Token valid for ~1 hour.') + '  reCAPTCHA: auto';
    connectBtn.textContent = 'Reconnect';

  } catch (error) {
    showError(error.message);
    updateStatus(false, 'Connection failed');
  } finally {
    setLoading(false);
  }
}

async function handleOpenFlow() {
  chrome.tabs.create({ url: FLOW_URL });
}

async function init() {
  await loadPort();
  const portEl = document.getElementById('portInput');
  if (portEl) {
    portEl.addEventListener('change', async () => {
      const p = parseInt(portEl.value) || 3847;
      await savePort(p);
      infoEl.textContent = `레인 포트 ${p} 저장됨. 이 프로필은 이 포트의 데몬에 붙습니다.`;
    });
  }
  // ★2026-09-18: 이 표시는 "구글 로그인 감지" 이지 데몬 연결 상태가 아니다. 연결은 Connect 를 눌러야 한다.
  let bundle = { sapisid: null, count: 0 };
  let cookieErr = '';
  try { bundle = await getGoogleCookieBundle(); } catch (e) { cookieErr = String((e && e.message) || e); }
  // 진단: 데몬 로그에 어떤 빌드가 떠 있고 쿠키를 몇 개 읽었는지 남긴다 (값은 보내지 않음)
  try {
    const perms = await chrome.permissions.getAll();
    fetch(`${proxyUrl()}/diag`, { method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ build: '3.1.0', sapisidFound: !!bundle.sapisid, cookieCount: bundle.count,
                             cookieErr, origins: perms.origins || [] }) }).catch(() => {});
  } catch {}
  if (bundle.sapisid) {
    updateStatus(false, `구글 로그인 감지 (쿠키 ${bundle.count}개) — Connect 를 누르세요`);
    infoEl.textContent = '새 Flow(flow.google.com)는 구글 쿠키로 인증합니다.';
  } else {
    updateStatus(false, '구글 로그인 없음');
    infoEl.textContent = '이 프로필에서 google.com 에 로그인한 뒤 Connect.';
  }

  connectBtn.disabled = false;
}

connectBtn.addEventListener('click', handleConnect);
openFlowBtn.addEventListener('click', handleOpenFlow);
document.getElementById('githubLink').addEventListener('click', (e) => {
  e.preventDefault();
  chrome.tabs.create({ url: 'https://github.com/liorium/flow-proxy' });
});

init();
