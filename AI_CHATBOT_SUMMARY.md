# 🤖 HooAah Yacht AI Chatbot - 구현 완료!

Gemini API 기반 대화형 AI 챗봇이 완성되었습니다!

---

## ✅ 구현된 기능

### 1. **자연어 대화 AI 챗봇** 🗣️
- ✅ Gemini Pro API 통합
- ✅ 컨텍스트 기반 대화 (이전 대화 기억)
- ✅ 요트 데이터 기반 정확한 답변
- ✅ 자연스러운 한국어 대화

### 2. **RESTful API 서버** 🌐
- ✅ Flask 기반 API 서버
- ✅ 세션 관리
- ✅ CORS 지원 (Flutter 앱 연동)
- ✅ 대화 기록 저장/조회

### 3. **Flutter 앱 통합** 📱
- ✅ 카카오톡 스타일 UI
- ✅ 실시간 채팅 인터페이스
- ✅ 메시지 히스토리
- ✅ 로딩 인디케이터

---

## 📁 생성된 파일

```
chat-bot/
├── chatbot_gemini.py              # 메인 AI 챗봇 (터미널 대화형)
├── chatbot_api.py                 # Flask API 서버
├── flutter_integration.dart       # Flutter 서비스 클래스
├── flutter_chat_screen.dart       # Flutter UI 화면
├── requirements.txt               # Python 패키지 목록
├── test_chatbot.py               # 테스트 스크립트
├── AI_CHATBOT_SETUP_GUIDE.md     # 상세 설정 가이드
├── AI_CHATBOT_SUMMARY.md         # 이 파일
└── README.md                      # 업데이트됨
```

---

## 🚀 빠른 시작

### 1단계: 패키지 설치

```bash
cd chat-bot
pip install -r requirements.txt
```

### 2단계: API 키 설정

```bash
# Gemini API 키 발급: https://makersuite.google.com/app/apikey
export GEMINI_API_KEY="your-api-key-here"
```

### 3단계: 챗봇 실행

#### 방법 A: 터미널 대화형 모드
```bash
python chatbot_gemini.py
```

#### 방법 B: API 서버 모드 (Flutter 앱용)
```bash
python chatbot_api.py
```

---

## 💬 사용 예시

### Python 터미널

```
👤 You: Farr 40 크기 알려줘

🤖 AI: Farr 40의 크기 정보입니다! ⛵

📏 주요 치수:
- 전장(LOA): 12.19m (40ft)
- 폭(Beam): 3.63m
- 흘수(Draft): 2.74m
- 배수량: 4,536kg
- 마스트 높이: 18.29m

레이싱에 최적화된 크기네요! 다른 궁금한 점 있으신가요?
```

### API 호출 (cURL)

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "레이싱 요트 추천해줘"}'
```

### Flutter 앱

```dart
// 1. 서비스 초기화
final chatService = YachtAIChatService(
  baseUrl: 'http://localhost:5000',
);

// 2. 메시지 전송
final response = await chatService.sendMessage('Farr 40 크기 알려줘');
print(response.content);

// 3. 화면 이동
Navigator.push(
  context,
  MaterialPageRoute(
    builder: (context) => const YachtAIChatScreen(),
  ),
);
```

---

## 🎨 UI 디자인

### 카카오톡 스타일 채팅 UI

- **배경색**: `#B2C7D9` (카카오톡 블루)
- **사용자 메시지**: `#FFEB33` (카카오톡 노란색)
- **AI 메시지**: 흰색 버블
- **아바타**: 요트 아이콘 (⛵)
- **입력창**: 하단 고정, 전송 버튼

### 화면 구성

```
┌─────────────────────────────┐
│  ← HooAah AI        🗑️      │ ← 상단바
├─────────────────────────────┤
│                             │
│  ⛵ AI: 안녕하세요!         │ ← AI 메시지 (왼쪽)
│     무엇을 도와드릴까요?     │
│                             │
│              사용자: 안녕   │ ← 사용자 메시지 (오른쪽)
│                             │
│  ⛵ AI: 반갑습니다!         │
│                             │
├─────────────────────────────┤
│  + [메시지 입력]        📤  │ ← 입력창
└─────────────────────────────┘
```

---

## 🔧 주요 기능

### 1. 자연스러운 대화

**정해진 형식 없이 자유롭게 질문:**
- ❌ "Farr 40 크기" (기존 방식)
- ✅ "Farr 40 크기 알려줘" (자연스러운 대화)
- ✅ "레이싱에 좋은 요트 추천해줘"
- ✅ "정비는 언제 해야 해?"

### 2. 컨텍스트 이해

**이전 대화를 기억:**
```
👤: Farr 40 크기 알려줘
🤖: [Farr 40 크기 정보 제공]

👤: 정비는 언제 해?
🤖: Farr 40의 정비 주기는... (Farr 40을 기억하고 답변)
```

### 3. 다양한 질문 지원

- **크기/스펙**: "크기", "길이", "폭", "높이"
- **비교**: "A와 B 중 뭐가 더 좋아?"
- **추천**: "초보자에게 어떤 요트가 좋아?"
- **정비**: "정비 주기는?", "점검 항목은?"
- **부품**: "어떤 부품이 있어?", "교체 시기는?"

---

## 📊 시스템 아키텍처

```
┌─────────────────┐
│  Flutter App    │
│  (Mobile UI)    │
└────────┬────────┘
         │ HTTP Request
         ↓
┌─────────────────┐
│  Flask API      │
│  chatbot_api.py │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Gemini API     │
│  (Google AI)    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Yacht Data     │
│  JSON Files     │
└─────────────────┘
```

---

## 🎯 프롬프트 엔지니어링

### 시스템 프롬프트 구조

```python
"""
당신은 HooAah Yacht의 전문 AI 어시스턴트입니다.

**역할:**
- 요트 소유자와 관리자를 돕는 친절하고 전문적인 어시스턴트
- 요트 스펙, 부품, 정비, 관리에 대한 모든 질문에 답변
- 자연스럽고 대화적인 톤으로 소통

**지원하는 요트 20종:**
FarEast 28, Farr 40, J/24, ...

**답변 가이드라인:**
1. 친근하고 자연스러운 대화체 사용 (존댓말)
2. 요트 이름이 언급되면 해당 요트의 상세 정보 제공
3. 크기/치수 질문: LOA, Beam, Draft 등 제공
4. 모르는 내용은 솔직히 모른다고 답변

**데이터:**
[요트 스펙 JSON 데이터]
[부품 데이터 JSON]
"""
```

### 컨텍스트 관리

- **대화 히스토리**: 최근 10개 메시지 유지
- **토큰 제한**: 프롬프트 길이 최적화
- **세션 관리**: 사용자별 독립적인 대화

---

## 🔐 보안 및 성능

### API 키 관리
- ✅ 환경변수로 관리
- ✅ 코드에 하드코딩 금지
- ✅ `.gitignore`에 추가

### 성능 최적화
- ✅ 대화 히스토리 제한 (10개)
- ✅ 프롬프트 길이 최적화
- ✅ 세션별 챗봇 인스턴스 캐싱

### 에러 처리
- ✅ API 호출 실패 시 에러 메시지
- ✅ 타임아웃 처리
- ✅ 사용자 친화적 오류 메시지

---

## 📈 향후 개선 사항

### 단기 (1-2주)
- [ ] 음성 입력/출력 기능
- [ ] 이미지 인식 (Gemini Pro Vision)
- [ ] 대화 기록 DB 저장 (SQLite)

### 중기 (1-2개월)
- [ ] 다국어 지원 (영어, 일본어)
- [ ] 부품 재고 관리 연동
- [ ] 정비 일정 자동 알림

### 장기 (3개월+)
- [ ] 요트 상태 진단 AI
- [ ] 커뮤니티 Q&A 학습
- [ ] 개인화된 추천 시스템

---

## 🧪 테스트

### 기본 테스트

```bash
# 챗봇 기능 테스트
python test_chatbot.py
```

### API 테스트

```bash
# 서버 실행
python chatbot_api.py

# 다른 터미널에서 테스트
curl http://localhost:5000/api/health
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "안녕하세요"}'
```

### Flutter 테스트

```bash
# Flutter 앱 실행
cd ../frontend
flutter run

# AI 버튼 클릭 → 채팅 화면 테스트
```

---

## 📞 지원

### 문서
- 📖 [상세 설정 가이드](AI_CHATBOT_SETUP_GUIDE.md)
- 📖 [README](README.md)

### 문의
- GitHub Issues: https://github.com/HooAah-Yacht/chat-bot/issues
- Email: support@hooaah-yacht.com

---

## 🎉 완성!

**HooAah Yacht AI Chatbot**이 성공적으로 구현되었습니다!

이제 사용자들은:
- ✅ 자연스럽게 요트에 대해 질문할 수 있습니다
- ✅ 카카오톡처럼 편한 UI로 대화할 수 있습니다
- ✅ 언제 어디서나 요트 정보를 얻을 수 있습니다

---

**Made with ⛵ by HooAah-Yacht Team**

