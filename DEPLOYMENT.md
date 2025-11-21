# HooAah Yacht Chatbot - 배포 가이드

## 📦 배포 옵션

### 🐳 옵션 1: Docker 배포 (권장)

**장점:**
- ✅ Tesseract OCR 자동 포함
- ✅ 모든 의존성 자동 설치
- ✅ 어떤 서버에서든 동일하게 작동
- ✅ iOS/Android 앱에서 API 호출 가능

**실행:**
```bash
# chat-bot 디렉토리에서
docker-compose up -d
```

**앱 연동:**
```
API 엔드포인트: http://your-server-ip:5000/api/chat/upload
```

---

### 🖥️ 옵션 2: 직접 서버 배포

**Ubuntu/Debian 서버:**
```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-kor
pip install -r requirements.txt
python chatbot_unified.py --mode api --port 5000
```

---

### ☁️ 옵션 3: 외부 OCR API 사용

**스캔 PDF 1개**를 위해 복잡도를 높이지 않으려면:
- Google Cloud Vision API
- AWS Textract
- Azure Computer Vision

현재 **19개 PDF는 OCR 없이 완벽 작동** 중

---

## 📱 모바일 앱 통합

### Flutter 코드 예시:

```dart
// PDF 업로드
final response = await http.post(
  Uri.parse('$serverUrl/api/chat/upload'),
  body: FormData.fromMap({
    'file': await MultipartFile.fromFile(pdfFile.path),
    'session_id': userId,
  }),
);

final result = jsonDecode(response.body);
// result['response'] = 분석 결과
```

---

## 🎯 현재 상태

✅ **Python 패키지 설치 완료:**
- PyMuPDF (스캔 PDF → 이미지 변환)
- pytesseract (OCR 인터페이스)
- Pillow (이미지 처리)

⏳ **서버 배포 시:**
- Docker 사용 → Tesseract 자동 설치 ✅
- 직접 배포 → 서버에 Tesseract 설치 필요

✅ **19개 일반 PDF:** 지금도 완벽 작동 (OCR 불필요)

