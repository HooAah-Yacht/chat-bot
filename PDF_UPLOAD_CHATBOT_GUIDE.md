# 📄 요트 챗봇 PDF 업로드 기능 가이드

PDF 업로드 및 자동 분석 기능이 통합된 챗봇 사용 방법

---

## ✅ 구현 완료

### 1. **PDF 업로드 통합 챗봇**
- `chatbot_with_pdf_upload.py`: PDF 업로드 기능이 있는 챗봇
- 자동 PDF 분석 및 요트 등록 데이터 생성

### 2. **API 엔드포인트 추가**
- `POST /api/chat/upload-pdf`: PDF 파일 업로드 및 분석
- `GET /api/chat/registration-data`: 등록 데이터 조회

### 3. **테스트 스크립트**
- `test_chatbot_with_pdf.py`: 사용자 플로우 시뮬레이션

---

## 🚀 사용 플로우

### 1️⃣ 챗봇 실행

```bash
cd chat-bot
python chatbot_with_pdf_upload.py
```

또는 API 서버 실행:

```bash
python chatbot_api.py
```

### 2️⃣ 요트 문서 등록 안내

사용자가 챗봇에게:
```
"요트 등록하고 싶어요"
"PDF 업로드하고 싶어요"
"매뉴얼 등록"
```

챗봇 응답:
```
📄 요트 문서를 등록하세요!

요트 매뉴얼 PDF 파일을 업로드해주시면:
1. 📋 문서를 자동으로 분석합니다
2. ⛵ 요트 정보를 추출합니다
3. 🔧 부품 정보를 정리합니다
4. ✅ 데이터베이스에 등록합니다

PDF 파일을 업로드해주세요!
```

### 3️⃣ 사용자가 PDF 업로드

**터미널에서:**
```bash
# PDF 파일 경로 입력
👤 You: data/yachtpdf/j70-user-manual.pdf
```

**API에서:**
```bash
curl -X POST http://localhost:5000/api/chat/upload-pdf \
  -F "file=@data/yachtpdf/j70-user-manual.pdf" \
  -F "session_id=test-session"
```

### 4️⃣ 챗봇이 분석

```
📄 문서를 분석 중입니다...
잠시만 기다려주세요! ⏳

[분석 진행 중...]
```

### 5️⃣ 등록 완료

```
✅ 등록이 완료됐습니다! 🎉

**등록된 요트 정보:**
⛵ 모델: J/70
🏭 제조사: C&C Fiberglass Components, Inc.
📄 문서 유형: Owner Guide

**추출된 정보:**
📏 치수 정보: 추출됨
🔧 부품 정보: 15개 부품 추출됨
⚙️ 엔진 정보: 추출됨

요트가 성공적으로 등록되었습니다! 이제 부품 관리와 정비 일정을 설정할 수 있습니다.
```

---

## 📋 테스트 실행

### 자동 테스트

```bash
python test_chatbot_with_pdf.py
```

**출력:**
```
1️⃣ 챗봇 초기화 중...
✅ 챗봇이 실행 중입니다.

2️⃣ 요트 문서 등록 안내
🤖 AI: 📄 요트 문서를 등록하세요!...

3️⃣ 사용자가 요트 매뉴얼 PDF를 넣습니다
📄 PDF 파일: j70-user-manual.pdf

4️⃣ 챗봇이 분석합니다
🤖 AI: 📄 문서를 분석 중입니다...

5️⃣ 등록 완료 확인
✅ 등록 데이터가 준비되었습니다!
```

### 수동 테스트 (대화형)

```bash
python chatbot_with_pdf_upload.py
```

**대화 예시:**
```
👤 You: 요트 등록하고 싶어요
🤖 AI: 📄 요트 문서를 등록하세요!...

👤 You: data/yachtpdf/j70-user-manual.pdf
🤖 AI: 📄 문서를 분석 중입니다...
      ✅ 등록이 완료됐습니다! 🎉
```

---

## 🔌 API 사용법

### PDF 업로드

```bash
curl -X POST http://localhost:5000/api/chat/upload-pdf \
  -F "file=@path/to/yacht-manual.pdf" \
  -F "session_id=user-123"
```

**응답:**
```json
{
  "success": true,
  "response": "✅ 등록이 완료됐습니다! 🎉...",
  "session_id": "user-123",
  "registration_data": {
    "basicInfo": {
      "name": "J/70",
      "manufacturer": "...",
      ...
    },
    "specifications": {...},
    "parts": [...]
  },
  "timestamp": "2025-01-19T..."
}
```

### 등록 데이터 조회

```bash
curl http://localhost:5000/api/chat/registration-data?session_id=user-123
```

---

## 📊 등록 데이터 구조

```json
{
  "basicInfo": {
    "name": "J/70",
    "nickName": "J/70",
    "manufacturer": "C&C Fiberglass Components, Inc.",
    "type": "Owner Guide",
    "year": "",
    "designer": "",
    "manual": "j70-user-manual.pdf"
  },
  "specifications": {
    "dimensions": {
      "loa": 6.934,
      "beam": 2.249,
      "draft": 1.45,
      "displacement": 794.0,
      "mastHeight": 10.0
    },
    "sailArea": {...},
    "engine": {...},
    ...
  },
  "parts": [
    {
      "name": "Foredeck Hatch",
      "manufacturer": "Global BSI Inc.",
      "model": null,
      "interval": null
    },
    ...
  ]
}
```

---

## 🔗 백엔드 API 연동

등록 데이터를 백엔드 API로 전송:

```python
import requests

# 등록 데이터 가져오기
registration_data = chatbot.get_registration_data()

# 백엔드 API로 전송
response = requests.post(
    'http://backend-url/api/yacht/with-specs',
    json=registration_data,
    headers={
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json'
    }
)
```

---

## 📝 파일 구조

```
chat-bot/
├── chatbot_with_pdf_upload.py    # PDF 업로드 통합 챗봇
├── test_chatbot_with_pdf.py      # 테스트 스크립트
├── yacht_document_analyzer.py    # PDF 분석기
├── chatbot_api.py                 # API 서버 (업데이트됨)
└── uploads/                       # 업로드된 파일 저장 (자동 생성)
```

---

## ⚠️ 주의사항

1. **파일 크기**: 큰 PDF는 분석 시간이 오래 걸릴 수 있음
2. **세션 관리**: 세션 ID로 사용자별 챗봇 인스턴스 관리
3. **파일 저장**: 업로드된 파일은 `uploads/` 폴더에 저장됨
4. **정리**: 사용하지 않는 파일은 주기적으로 삭제 필요

---

## 🎯 다음 단계

1. ✅ PDF 업로드 기능 구현 완료
2. ⏳ 백엔드 API 연동 (등록 데이터 전송)
3. ⏳ Flutter 앱 통합 (파일 선택 및 업로드 UI)
4. ⏳ 진행 상황 표시 (로딩 인디케이터)

---

**작성일**: 2025-01-19

