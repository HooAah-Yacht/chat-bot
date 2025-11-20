# 📄 PDF 분석 결과 JSON 저장 정보

PDF로 등록한 요트 정보는 다음 JSON 파일에 저장됩니다.

---

## 📁 저장 위치

### 1. **`data/yacht_specifications.json`**
- **용도**: 기존 요트 스펙 데이터베이스에 새 요트 추가
- **형식**: 기존 20종 요트와 동일한 형식
- **내용**:
  - 요트 기본 정보 (id, name, manufacturer, type, manual)
  - 상세 스펙 (dimensions, sailArea, engine, hull 등)
- **업데이트**: 같은 ID가 있으면 업데이트, 없으면 추가

**예시:**
```json
{
  "id": "sun-odyssey-380",
  "name": "Sun Odyssey 380",
  "manufacturer": "JEANNEAU",
  "type": "Owner's Manual",
  "manual": "Sun Odyssey 380 Owners manual.pdf",
  "dimensions": {
    "loa": {
      "value": 11.4,
      "unit": "m",
      "display": "11.4m"
    },
    ...
  },
  ...
}
```

---

### 2. **`data/registered_yachts.json`** (새 파일)
- **용도**: PDF로 등록된 모든 요트의 전체 등록 정보 저장
- **형식**: 등록 메타데이터 + 원본 분석 결과
- **내용**:
  - 등록 일시
  - PDF 파일명
  - 등록 데이터 (registrationData)
  - 분석 결과 요약 (analysisResult)

**예시:**
```json
{
  "version": "1.0",
  "description": "PDF로 등록된 요트 목록",
  "lastUpdated": "2025-01-19",
  "yachts": [
    {
      "registrationDate": "2025-01-19T10:30:00",
      "source": "PDF Upload",
      "pdfFile": "Sun Odyssey 380 Owners manual.pdf",
      "registrationData": {
        "basicInfo": {...},
        "specifications": {...},
        "parts": [...]
      },
      "analysisResult": {
        "documentInfo": {...},
        "partsCount": 15,
        "analysisStatus": "success"
      }
    }
  ]
}
```

---

## 🔄 저장 프로세스

1. **PDF 분석 완료**
   ↓
2. **등록 데이터 변환**
   ↓
3. **`yacht_specifications.json`에 추가/업데이트**
   - 기존 요트와 동일한 형식으로 저장
   - 챗봇에서 바로 사용 가능
   ↓
4. **`registered_yachts.json`에 전체 정보 저장**
   - 등록 이력 보관
   - 원본 분석 결과 포함

---

## 📊 저장 확인

PDF 분석 후 다음 메시지가 출력됩니다:

```
💾 JSON 파일에 저장 완료!
✅ data/yacht_specifications.json에 저장됨
✅ data/registered_yachts.json에 저장됨
```

---

## 💡 사용 팁

### 등록 데이터 확인
```bash
# 챗봇에서
/register

# 또는 직접 파일 확인
cat data/yacht_specifications.json
cat data/registered_yachts.json
```

### 기존 요트 업데이트
- 같은 이름의 요트를 다시 등록하면 기존 데이터가 업데이트됩니다
- ID는 요트 이름 기반으로 자동 생성됩니다

---

**수정일**: 2025-01-19

