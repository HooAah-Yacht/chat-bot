# 📄 요트 문서 분석기 사용 가이드

Gemini API를 사용한 요트 문서 자동 분석 시스템

---

## ✅ 구현 완료 사항

### 1. **문서 분석기 구현**
- `yacht_document_analyzer.py`: Gemini API 기반 PDF 문서 분석
- 텍스트 추출 방식 (PyPDF2/pdfplumber)
- 파일 업로드 방식 (gemini-1.5-pro, fallback)

### 2. **분석 기능**
- 문서 기본 정보 추출 (제목, 모델, 제조사, 문서 유형)
- 요트 스펙 정보 추출 (치수, 엔진, 돛 면적 등)
- 부품 정보 추출 (부품명, 제조사, 모델, 정비 주기)
- 정비 정보 추출
- 문서 형식 평가 (분석 가능 여부)

### 3. **Gemini API 키 설정**
- API 키: `AIzaSyBhPZDNBTEqYu8ahBIVpK2B1h_CAKgo7JI`
- 코드에 하드코딩됨 (테스트용)

---

## 🚀 사용 방법

### 1. 패키지 설치

```bash
cd chat-bot
pip install google-generativeai PyPDF2 pdfplumber
```

### 2. 테스트 실행 (소수 파일)

```bash
python test_document_analyzer.py
```

### 3. 전체 파일 분석

```bash
python yacht_document_analyzer.py
```

---

## 📊 분석 결과

### 출력 파일

1. **`test_analysis_results.json`** (테스트용)
   - 소수 PDF 파일 분석 결과
   - JSON 형식

2. **`document_analysis_results.json`** (전체 분석)
   - 모든 PDF 파일 분석 결과
   - JSON 형식

3. **`document_analysis_report.md`** (요약 보고서)
   - 분석 가능/불가능 문서 분류
   - 상세 분석 결과
   - 마크다운 형식

---

## 📋 분석 가능한 문서 형식

### ✅ 분석 가능
- 텍스트 기반 PDF (선택 가능한 텍스트)
- 구조화된 매뉴얼
- 부품 목록 문서
- 기술 사양서

### ❌ 분석 불가능
- 스캔된 이미지 PDF (OCR 필요)
- 손상된 PDF
- 암호화된 PDF
- 텍스트가 없는 이미지만 있는 PDF

---

## 🔍 분석 결과 예시

```json
{
  "documentInfo": {
    "title": "J/70 User Manual",
    "yachtModel": "J/70",
    "manufacturer": "J/Boats",
    "documentType": "User Manual"
  },
  "yachtSpecs": {
    "dimensions": {
      "loa": 6.93,
      "beam": 2.28,
      "draft": 1.45
    },
    "engine": {
      "type": "Outboard",
      "power": "6 HP"
    }
  },
  "parts": [
    {
      "name": "Mainsail",
      "manufacturer": "North Sails",
      "model": "J/70 Mainsail",
      "interval": 12,
      "category": "Sails"
    }
  ],
  "analysisResult": {
    "canExtractText": true,
    "canAnalyze": true,
    "reason": ""
  }
}
```

---

## 📝 다음 단계

1. **패키지 설치 후 테스트 실행**
2. **결과 확인**: `test_analysis_results.json` 또는 `document_analysis_results.json`
3. **보고서 확인**: `document_analysis_report.md`
4. **Notion/카톡에 결과 공유**

---

## ⚠️ 주의사항

1. **API 키 보안**: 프로덕션에서는 환경변수 사용
2. **파일 크기**: 큰 PDF는 텍스트가 잘릴 수 있음 (30,000자 제한)
3. **API 제한**: Gemini API 사용량 제한 확인 필요
4. **비용**: API 호출 시 비용 발생 가능

---

## 🛠️ 문제 해결

### 패키지 설치 오류
```bash
pip install --upgrade pip
pip install google-generativeai PyPDF2 pdfplumber
```

### 텍스트 추출 실패
- PDF가 스캔된 이미지인지 확인
- OCR 라이브러리 (Tesseract) 추가 고려

### API 오류
- API 키 확인
- API 사용량 제한 확인
- 네트워크 연결 확인

---

**작성일**: 2025-01-19  
**API 키**: AIzaSyBhPZDNBTEqYu8ahBIVpK2B1h_CAKgo7JI (테스트용)

