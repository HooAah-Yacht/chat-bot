(function(){
  const chatEl = document.getElementById('chat');
  const form = document.getElementById('chatForm');
  const input = document.getElementById('messageInput');
  const flaskHostInput = document.getElementById('flaskHost');
  const saveEnvBtn = document.getElementById('saveEnv');
  const previewBtn = document.getElementById('previewParts');
  const pdfPathInput = document.getElementById('pdfPath');
  const registerBtn = document.getElementById('registerSelected');
  const selectedPartsInput = document.getElementById('selectedParts');

  let baseApi = '/api'; // proxied by Node server

  const addMsg = (role, text, isLoading = false) => {
    const msgDiv = document.createElement('div');
    msgDiv.className = `msg ${role}${isLoading ? ' loading' : ''}`;
    if (isLoading) msgDiv.id = 'loading-msg';
    
    // 메시지 래퍼 (프로필 + 말풍선)
    const wrapper = document.createElement('div');
    wrapper.className = 'msg-wrapper';
    
    // 프로필 아이콘
    const profile = document.createElement('div');
    profile.className = 'profile';
    profile.textContent = role === 'user' ? '👤' : '🤖';
    
    // 말풍선 + 메타 컨테이너
    const bubbleContainer = document.createElement('div');
    bubbleContainer.style.display = 'flex';
    bubbleContainer.style.flexDirection = 'column';
    bubbleContainer.style.maxWidth = 'calc(100% - 44px)';
    
    // 말풍선
    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    
    const content = document.createElement('div');
    content.className = 'content';
    content.textContent = text;
    
    bubble.appendChild(content);
    bubbleContainer.appendChild(bubble);
    
    // 메타 정보 (시간)
    if (!isLoading) {
      const meta = document.createElement('div');
      meta.className = 'msg-meta';
      const time = new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit', hour12: true });
      meta.textContent = time;
      bubbleContainer.appendChild(meta);
    }
    
    wrapper.appendChild(profile);
    wrapper.appendChild(bubbleContainer);
    msgDiv.appendChild(wrapper);
    
    chatEl.appendChild(msgDiv);
    chatEl.scrollTop = chatEl.scrollHeight;
    return msgDiv;
  };

  const removeLoadingMsg = () => {
    const loadingEl = document.getElementById('loading-msg');
    if (loadingEl) loadingEl.remove();
  };

  const setFlaskHost = () => {
    const host = flaskHostInput.value.trim();
    if (!host) return;
    // Allow switching proxy target by using full URLs instead of proxied path
    // If full URL, we will call it directly (CORS allowed by server.js)
    if (host.startsWith('http://') || host.startsWith('https://')) {
      baseApi = host.endsWith('/') ? host.slice(0, -1) : host;
    }
    addMsg('ai', `Flask 대상 설정: ${baseApi}`);
  };

  saveEnvBtn.addEventListener('click', setFlaskHost);

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = input.value.trim();
    if (!message) return;
    addMsg('user', message);
    input.value = '';

    // 로딩 메시지 표시
    addMsg('ai', '⏳ 잠시만 기다려 주세요... AI가 분석 중입니다.', true);

    try {
      const res = await fetch(`${baseApi}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });
      
      removeLoadingMsg(); // 로딩 메시지 제거
      
      const data = await res.json();
      let text = '';
      if (data && typeof data === 'object') {
        // handle both {response: "..."} and {response: {response: "..."}}
        if (data.response && typeof data.response === 'string') {
          text = data.response;
        } else if (data.response && data.response.response) {
          text = data.response.response;
        } else if (data.message && typeof data.message === 'string') {
          text = data.message;
        } else {
          text = JSON.stringify(data);
        }
      } else {
        text = String(data);
      }
      addMsg('ai', text);
    } catch (err) {
      removeLoadingMsg(); // 에러 시에도 로딩 메시지 제거
      addMsg('ai', `❌ 에러: ${err.message}\n\n💡 Flask 서버가 실행 중인지 확인하세요:\npython chatbot_unified.py --mode api`);
    }
  });

  previewBtn.addEventListener('click', async () => {
    const pdfPath = pdfPathInput.value.trim();
    addMsg('user', `부품 미리보기 요청${pdfPath ? ` (pdf=${pdfPath})` : ''}`);
    addMsg('ai', '⏳ PDF 분석 중...', true);
    
    try {
      const url = `${baseApi}/api/yacht/preview-parts`;
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pdfPath: pdfPath || undefined })
      });
      removeLoadingMsg();
      const data = await res.json();
      addMsg('ai', JSON.stringify(data, null, 2));
    } catch (err) {
      removeLoadingMsg();
      addMsg('ai', `❌ 에러: ${err.message}`);
    }
  });

  registerBtn.addEventListener('click', async () => {
    let parts = [];
    try {
      parts = JSON.parse(selectedPartsInput.value.trim() || '[]');
    } catch (e) {
      addMsg('ai', '❌ 선택 부품 입력은 JSON 배열 형식이어야 합니다.\n예: ["엔진", "펌프"]');
      return;
    }
    addMsg('user', `선택 부품 등록 요청: ${JSON.stringify(parts)}`);
    addMsg('ai', '⏳ 부품 등록 중...', true);
    
    try {
      const url = `${baseApi}/api/yacht/register-selected`;
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ parts })
      });
      removeLoadingMsg();
      const data = await res.json();
      addMsg('ai', JSON.stringify(data, null, 2));
    } catch (err) {
      removeLoadingMsg();
      addMsg('ai', `❌ 에러: ${err.message}`);
    }
  });

  // Initial env info
  addMsg('ai', '웹 UI 준비 완료. Flask 대상은 상단에서 변경하세요.');
})();
