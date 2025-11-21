# -*- coding: utf-8 -*-
"""
서버 배포용 설정 스크립트 (Ubuntu/Debian)
Docker 없이 직접 서버에 배포할 때 사용
"""

import sys
import os

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

print("""
================================================================================
🚀 HooAah Yacht Chatbot 서버 배포 가이드
================================================================================

1. Ubuntu/Debian 서버에서 실행할 명령어:
   
   sudo apt-get update
   sudo apt-get install -y tesseract-ocr tesseract-ocr-kor tesseract-ocr-eng
   pip install -r requirements.txt

2. Docker 사용 (권장):
   
   docker-compose up -d

3. 서버 실행:
   
   python chatbot_unified.py --mode api --port 5000

4. 앱 연동:
   
   iOS/Android 앱에서 API 호출:
   POST http://your-server-ip:5000/api/chat
   POST http://your-server-ip:5000/api/chat/upload (PDF 업로드)

================================================================================
📱 모바일 앱 통합
================================================================================

Flutter 앱에서 사용:

```dart
// PDF 업로드 API 호출
final response = await http.post(
  Uri.parse('http://your-server:5000/api/chat/upload'),
  body: FormData.fromMap({
    'file': await MultipartFile.fromFile(pdfPath),
    'session_id': userId,
  }),
);
```

서버에 Tesseract가 설치되어 있으면:
✅ 일반 PDF (19개) 처리
✅ 스캔 PDF (1개) OCR 처리

================================================================================
""")

