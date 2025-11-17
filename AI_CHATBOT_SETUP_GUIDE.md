# 🤖 HooAah Yacht AI Chatbot 설정 가이드

Gemini API 기반 대화형 AI 챗봇 설정 및 사용 방법

---

## 📋 목차

1. [사전 준비](#사전-준비)
2. [Gemini API 키 발급](#gemini-api-키-발급)
3. [Python 챗봇 설정](#python-챗봇-설정)
4. [API 서버 실행](#api-서버-실행)
5. [Flutter 앱 통합](#flutter-앱-통합)
6. [사용 예시](#사용-예시)
7. [문제 해결](#문제-해결)

---

## 🔧 사전 준비

### 필수 요구사항

- **Python 3.8 이상**
- **pip** (Python 패키지 관리자)
- **Gemini API 키** (Google AI Studio에서 발급)
- **Flutter 3.0 이상** (앱 통합 시)

### Python 패키지 설치

```bash
# 1. chat-bot 디렉토리로 이동
cd chat-bot

# 2. 필수 패키지 설치
pip install google-generativeai flask flask-cors

# 또는 requirements.txt 사용
pip install -r requirements.txt
```

### requirements.txt 생성

```txt
google-generativeai>=0.3.0
flask>=2.3.0
flask-cors>=4.0.0
```

---

## 🔑 Gemini API 키 발급

### 1. Google AI Studio 접속

https://makersuite.google.com/app/apikey

### 2. API 키 생성

1. **"Create API Key"** 클릭
2. 프로젝트 선택 또는 새로 생성
3. API 키 복사

### 3. 환경변수 설정

#### Windows (PowerShell)
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
```

#### Windows (CMD)
```cmd
set GEMINI_API_KEY=your-api-key-here
```

#### Mac/Linux
```bash
export GEMINI_API_KEY="your-api-key-here"
```

#### 영구 설정 (Windows)
```powershell
# 시스템 환경변수에 추가
[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', 'your-api-key-here', 'User')
```

#### 영구 설정 (Mac/Linux)
```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

---

## 💬 Python 챗봇 설정

### 1. 터미널 대화형 모드

```bash
# 챗봇 실행
python chatbot_gemini.py

# API 키 입력 (환경변수 미설정 시)
🔑 Gemini API 키를 입력하세요: your-api-key-here
```

### 2. 사용 예시

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

### 3. 명령어

- `/clear` - 대화 기록 초기화
- `/save` - 대화 기록 저장
- `/history` - 대화 기록 보기
- `/quit` 또는 `/exit` - 종료

---

## 🌐 API 서버 실행

### 1. 서버 시작

```bash
# API 서버 실행
python chatbot_api.py
```

**출력:**
```
============================================================
🛥️  HooAah Yacht AI Chatbot API Server
============================================================

🚀 서버 시작: http://localhost:5000
📡 API 문서: http://localhost:5000
```

### 2. API 엔드포인트

#### 채팅 메시지 전송
```http
POST http://localhost:5000/api/chat
Content-Type: application/json

{
  "message": "Farr 40 크기 알려줘",
  "session_id": "optional-session-id"
}
```

**응답:**
```json
{
  "success": true,
  "response": "Farr 40의 크기 정보입니다! ⛵\n\n📏 주요 치수:\n- 전장(LOA): 12.19m...",
  "session_id": "abc-123-def-456",
  "timestamp": "2024-11-17T10:30:00"
}
```

#### 대화 기록 조회
```http
GET http://localhost:5000/api/chat/history?session_id=abc-123-def-456
```

#### 대화 기록 초기화
```http
POST http://localhost:5000/api/chat/clear
Content-Type: application/json

{
  "session_id": "abc-123-def-456"
}
```

#### 요트 목록 조회
```http
GET http://localhost:5000/api/yachts
```

#### 요트 상세 정보
```http
GET http://localhost:5000/api/yacht/farr-40
```

### 3. cURL 테스트

```bash
# 채팅 메시지 전송
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Farr 40 크기 알려줘"}'

# 요트 목록 조회
curl http://localhost:5000/api/yachts

# 서버 상태 확인
curl http://localhost:5000/api/health
```

---

## 📱 Flutter 앱 통합

### 1. 파일 복사

```bash
# Flutter 프로젝트 디렉토리로 이동
cd ../frontend

# 서비스 파일 복사
cp ../chat-bot/flutter_integration.dart lib/services/yacht_ai_service.dart

# 화면 파일 복사
cp ../chat-bot/flutter_chat_screen.dart lib/screens/yacht_ai_chat_screen.dart
```

### 2. pubspec.yaml 수정

```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0  # HTTP 요청용
```

```bash
flutter pub get
```

### 3. 서버 URL 설정

`lib/services/yacht_ai_service.dart` 파일에서:

```dart
final YachtAIChatService _chatService = YachtAIChatService(
  baseUrl: 'http://your-server-ip:5000', // 실제 서버 IP로 변경
);
```

**로컬 테스트 시:**
- Android 에뮬레이터: `http://10.0.2.2:5000`
- iOS 시뮬레이터: `http://localhost:5000`
- 실제 기기: `http://192.168.x.x:5000` (컴퓨터 IP)

### 4. 화면 추가

`lib/main.dart` 또는 네비게이션 파일에서:

```dart
import 'screens/yacht_ai_chat_screen.dart';

// AI 버튼 클릭 시
Navigator.push(
  context,
  MaterialPageRoute(
    builder: (context) => const YachtAIChatScreen(),
  ),
);
```

### 5. 하단 네비게이션 바 연결

피그마 디자인의 AI 버튼에 연결:

```dart
BottomNavigationBar(
  items: const [
    BottomNavigationBarItem(icon: Icon(Icons.home), label: '홈'),
    BottomNavigationBarItem(icon: Icon(Icons.sailing), label: '요트'),
    BottomNavigationBarItem(icon: Icon(Icons.smart_toy), label: 'AI'), // AI 버튼
    BottomNavigationBarItem(icon: Icon(Icons.calendar_today), label: '달력'),
    BottomNavigationBarItem(icon: Icon(Icons.settings), label: '설정'),
  ],
  currentIndex: _selectedIndex,
  onTap: (index) {
    if (index == 2) { // AI 버튼
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => const YachtAIChatScreen(),
        ),
      );
    } else {
      setState(() => _selectedIndex = index);
    }
  },
)
```

---

## 🎯 사용 예시

### 질문 예시

#### 크기/스펙 질문
- "Farr 40 크기 알려줘"
- "Laser 길이는 얼마야?"
- "Beneteau Oceanis 46.1 스펙 알려줘"

#### 비교 질문
- "Farr 40과 J24 중 뭐가 더 빨라?"
- "레이싱 요트 중에서 가장 큰 건 뭐야?"
- "초보자에게 어떤 요트가 좋아?"

#### 추천 질문
- "레이싱에 좋은 요트 추천해줘"
- "가족과 크루징하기 좋은 요트는?"
- "10명이 탈 수 있는 요트 있어?"

#### 정비/관리 질문
- "Farr 40 정비 주기는?"
- "윈치 관리는 어떻게 해?"
- "세일 점검은 언제 해야 해?"

#### 부품 질문
- "Farr 40에 어떤 부품이 있어?"
- "메인세일 교체 시기는?"
- "리깅 점검 항목 알려줘"

---

## 🔍 문제 해결

### API 키 오류

**문제:**
```
ValueError: GEMINI_API_KEY가 설정되지 않았습니다.
```

**해결:**
1. API 키가 올바른지 확인
2. 환경변수가 설정되었는지 확인
3. 터미널 재시작 후 다시 시도

### 서버 연결 오류 (Flutter)

**문제:**
```
메시지 전송 실패: SocketException: Failed to connect
```

**해결:**
1. API 서버가 실행 중인지 확인
2. 서버 URL이 올바른지 확인
3. 방화벽 설정 확인
4. Android: `http://10.0.2.2:5000` 사용
5. iOS: `http://localhost:5000` 사용

### CORS 오류

**문제:**
```
Access to XMLHttpRequest has been blocked by CORS policy
```

**해결:**
`chatbot_api.py`에서 CORS 설정 확인:
```python
from flask_cors import CORS
CORS(app)  # 이미 설정되어 있음
```

### 응답 속도 느림

**해결:**
1. 프롬프트 길이 줄이기
2. 대화 히스토리 제한 (현재 10개)
3. Gemini Pro 대신 Gemini Pro Vision 사용 고려

### JSON 파일 없음

**문제:**
```
⚠️ yacht_specifications.json 파일을 찾을 수 없습니다.
```

**해결:**
1. `data/` 디렉토리가 있는지 확인
2. JSON 파일이 올바른 위치에 있는지 확인
3. 파일 경로 확인

---

## 🚀 배포 (Production)

### 서버 배포

#### 1. Heroku 배포

```bash
# Procfile 생성
echo "web: python chatbot_api.py" > Procfile

# requirements.txt 확인
pip freeze > requirements.txt

# Heroku 배포
heroku create hooaah-yacht-ai
heroku config:set GEMINI_API_KEY=your-api-key
git push heroku main
```

#### 2. AWS EC2 배포

```bash
# EC2 인스턴스에서
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt

# 환경변수 설정
export GEMINI_API_KEY=your-api-key

# 백그라운드 실행
nohup python3 chatbot_api.py &
```

#### 3. Docker 배포

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV GEMINI_API_KEY=""
EXPOSE 5000

CMD ["python", "chatbot_api.py"]
```

```bash
docker build -t hooaah-yacht-ai .
docker run -p 5000:5000 -e GEMINI_API_KEY=your-key hooaah-yacht-ai
```

### Flutter 앱 배포

```dart
// production 서버 URL로 변경
final YachtAIChatService _chatService = YachtAIChatService(
  baseUrl: 'https://your-production-server.com',
);
```

---

## 📊 성능 최적화

### 1. 응답 속도 개선

```python
# chatbot_gemini.py에서
# 대화 히스토리 제한 줄이기
recent_history = self.chat_history[-5:]  # 10 → 5

# 프롬프트 길이 줄이기
{json.dumps(self.yacht_data, ensure_ascii=False, indent=2)[:3000]}  # 5000 → 3000
```

### 2. 캐싱 추가

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_yacht_info(yacht_id: str):
    # 자주 조회되는 요트 정보 캐싱
    pass
```

### 3. 비동기 처리 (Flutter)

```dart
// 응답을 기다리는 동안 UI 블로킹 방지
Future<void> _sendMessage() async {
  // ... existing code ...
  
  // 비동기로 처리
  unawaited(_chatService.sendMessage(text).then((response) {
    setState(() {
      _messages.add(response);
      _isLoading = false;
    });
  }));
}
```

---

## 📚 추가 리소스

- **Gemini API 문서**: https://ai.google.dev/docs
- **Flask 문서**: https://flask.palletsprojects.com/
- **Flutter HTTP 패키지**: https://pub.dev/packages/http

---

## 🆘 지원

문제가 발생하면 GitHub Issues에 등록해주세요:
https://github.com/HooAah-Yacht/chat-bot/issues

---

**Made with ⛵ by HooAah-Yacht Team**

