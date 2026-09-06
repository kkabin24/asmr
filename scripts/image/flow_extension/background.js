/**
 * Flow Proxy — Background Service Worker.
 *
 * WHY SW (not content script): content script fetch가 labs.google 오리진으로 나가면
 * Chrome의 Local Network Access(loopback) 정책이 localhost 데몬 접근을 차단한다
 * ("blocked by CORS policy: ... loopback address space"). SW의 fetch는 확장 오리진
 * (chrome-extension://)이라 host_permissions(http://localhost/*)로 loopback에 붙을 수 있다.
 *
 * 동작: 데몬 /wait-recaptcha 를 long-poll → reCAPTCHA 필요 시 chrome.scripting.executeScript
 * 로 Flow 탭 MAIN world에서 grecaptcha.enterprise.execute 실행 → 토큰을 /recaptcha-token 로 반환.
 * 탭이 포커스가 아니어도 executeScript는 실행된다.
 */
const SITE_KEY = '6LdsFiUsAAAAAIjVDZcuLhaHiDn5nnHVXVRQGeMV';
let looping = false;

// 레인 포트: 프로필(계정)마다 다른 데몬 포트. popup에서 chrome.storage.local.flowPort로 저장.
let FLOW_PORT = 3847;
function proxy() { return `http://localhost:${FLOW_PORT}`; }
async function loadPort() {
  try {
    const { flowPort } = await chrome.storage.local.get('flowPort');
    if (flowPort) FLOW_PORT = flowPort;
  } catch {}
}
chrome.storage.onChanged.addListener((changes, area) => {
  if (area === 'local' && changes.flowPort) FLOW_PORT = changes.flowPort.newValue || 3847;
});

// ★2026-09-06: Flow 가 flow.google.com 으로 이전했다. labs.google 만 보면
// 탭이 열려 있어도 0개로 나와 reCAPTCHA 를 못 돌린다. 두 도메인을 모두 본다.
const FLOW_TAB_URLS = ['https://flow.google.com/*', 'https://labs.google/*'];

async function flowTabId() {
  const tabs = await chrome.tabs.query({ url: FLOW_TAB_URLS });
  return tabs.length ? tabs[0].id : null;
}

async function runRecaptcha(action) {
  const tabId = await flowTabId();
  if (tabId == null) return { error: 'Flow 탭이 열려 있지 않음 (flow.google.com 또는 labs.google)' };
  try {
    const [res] = await chrome.scripting.executeScript({
      target: { tabId },
      world: 'MAIN',
      func: async (siteKey, act) => {
        if (typeof grecaptcha === 'undefined' || !grecaptcha.enterprise) {
          return { error: 'grecaptcha.enterprise 미로드 (Flow 페이지가 완전히 로드됐는지 확인)' };
        }
        try { return { token: await grecaptcha.enterprise.execute(siteKey, { action: act }) }; }
        catch (e) { return { error: String((e && e.message) || e) }; }
      },
      args: [SITE_KEY, action || 'IMAGE_GENERATION'],
    });
    return (res && res.result) || { error: 'executeScript 결과 없음' };
  } catch (e) {
    return { error: 'executeScript 실패: ' + String((e && e.message) || e) };
  }
}

async function loop() {
  if (looping) return;
  looping = true;
  await loadPort();
  // 로드 확인용 ping (SW→localhost 네트워킹 검증)
  try { await fetch(`${proxy()}/ping`, { signal: AbortSignal.timeout(1500) }); } catch {}
  try {
    while (true) {
      let data;
      try {
        const r = await fetch(`${proxy()}/wait-recaptcha`, { signal: AbortSignal.timeout(30000) });
        data = await r.json();
      } catch {
        await new Promise((r) => setTimeout(r, 2000));   // 데몬 미실행/타임아웃 → 재시도
        continue;
      }
      if (!data.needed) continue;
      const result = await runRecaptcha(data.action);
      try {
        await fetch(`${proxy()}/recaptcha-token`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(result.token ? { token: result.token } : { error: result.error || 'no token' }),
        });
      } catch {}
    }
  } finally {
    looping = false;
  }
}

// 여러 진입점 — SW가 잠들었다 깨어나도 루프 재개
chrome.runtime.onStartup.addListener(loop);
chrome.runtime.onInstalled.addListener(loop);
chrome.alarms.create('keepalive', { periodInMinutes: 0.5 });   // 30s마다 SW 부활 → loop() 재개
chrome.alarms.onAlarm.addListener(loop);
loop();
