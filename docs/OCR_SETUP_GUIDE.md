# 📷 OCR 기능 설정 가이드

## 개요

OCR(광학 문자 인식) 기능을 사용하면 **스캔된 이미지 PDF**도 분석할 수 있습니다.

---

## 설치 방법

### 1. Tesseract OCR 설치

#### Windows
1. Tesseract 설치 파일 다운로드:
   - https://github.com/UB-Mannheim/tesseract/wiki
   - 또는 https://digi.bib.uni-mannheim.de/tesseract/
   
2. 설치 실행 (기본 경로: `C:\Program Files\Tesseract-OCR`)

3. 환경 변수 설정 (선택사항):
   - `PATH`에 `C:\Program Files\Tesseract-OCR` 추가
   - 또는 코드에서 직접 경로 지정

#### macOS
```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get install tesseract-ocr
```

### 2. Python 패키지 설치

```bash
pip install pytesseract pdf2image Pillow
```

**참고:** `pdf2image`는 `poppler`도 필요합니다.

#### Windows (poppler)
- https://github.com/oschwartz10612/poppler-windows/releases 에서 다운로드
- 압축 해제 후 `PATH`에 추가

#### macOS (poppler)
```bash
brew install poppler
```

#### Linux (poppler)
```bash
sudo apt-get install poppler-utils
```

---

## 사용 방법

### 자동 사용

OCR 기능이 설치되어 있으면 **자동으로 사용**됩니다:

1. 일반 텍스트 추출 시도 (PyPDF2, pdfplumber)
2. 텍스트 추출 실패 시 → OCR 자동 시도
3. OCR 성공 시 → 분석 진행

### 수동 설정 (Windows)

Windows에서 Tesseract 경로를 지정하려면:

```python
import pytesseract

# Tesseract 경로 설정
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

---

## 지원 언어

기본적으로 **영문(eng)**과 **한글(kor)**을 지원합니다.

추가 언어가 필요하면:
1. Tesseract 언어 데이터 다운로드
2. `lang='eng+kor+fra'` 형식으로 지정

---

## 성능 및 제한사항

### 장점
- ✅ 스캔된 이미지 PDF 분석 가능
- ✅ 오래된 매뉴얼도 처리 가능
- ✅ 자동으로 텍스트 추출 실패 시 OCR 시도

### 단점
- ⚠️ 처리 시간이 오래 걸림 (페이지당 5-10초)
- ⚠️ 정확도가 100%가 아닐 수 있음
- ⚠️ 복잡한 레이아웃은 인식 어려움
- ⚠️ 추가 의존성 필요 (Tesseract, poppler)

### 권장 사항
- 텍스트 기반 PDF는 일반 방법 사용 (빠름)
- 스캔된 PDF만 OCR 사용
- 고해상도 스캔(300 DPI 이상) 권장

---

## 테스트

OCR이 제대로 작동하는지 테스트:

```python
from chatbot_unified import UnifiedYachtChatbot

chatbot = UnifiedYachtChatbot()
# 스캔된 PDF 경로 입력
response = chatbot.chat("PDF 분석: path/to/scanned_manual.pdf")
```

---

## 문제 해결

### 오류: "TesseractNotFoundError"
- Tesseract가 설치되지 않았거나 PATH에 없음
- 해결: Tesseract 설치 및 PATH 설정

### 오류: "pdf2image.exceptions.PDFInfoNotInstalledError"
- poppler가 설치되지 않음
- 해결: poppler 설치

### OCR 정확도가 낮음
- 스캔 품질이 낮을 수 있음
- 해결: 고해상도 스캔(300 DPI 이상) 사용

---

## 참고 자료

- [Tesseract OCR 공식 문서](https://github.com/tesseract-ocr/tesseract)
- [pytesseract 문서](https://github.com/madmaze/pytesseract)
- [pdf2image 문서](https://github.com/Belval/pdf2image)

