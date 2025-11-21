# 🗂️ 7개 JSON 파일 역할 설명

HooAah Yacht 챗봇 시스템에서 사용하는 7개 JSON 파일의 역할과 사용 목적을 설명합니다.

---

## 📊 **파일 개요**

| # | 파일명 | 역할 | 데이터 출처 | 주 사용처 |
|---|--------|------|------------|----------|
| 1 | `yacht_specifications.json` | 🏭 마스터 데이터 | AI 분석 | 챗봇 조회 |
| 2 | `yacht_parts_database.json` | 📦 부품 상세 DB | AI 분석 | 챗봇 조회 |
| 3 | `yacht_parts_app_data.json` | 📱 앱 최적화 데이터 | AI 분석 | 모바일 앱 |
| 4 | `extracted_yacht_parts.json` | 🔍 원본 추출 데이터 | AI 원본 | 디버깅/검증 |
| 5 | `extracted_yacht_parts_detailed.json` | 📋 상세 추출 데이터 | AI 원본 | 디버깅/검증 |
| 6 | `registered_yachts.json` | 👤 사용자 등록 데이터 | 사용자 업로드 | 개인화 |
| 7 | `yacht_manual_resources.json` | 🔗 매뉴얼 리소스 | AI 분석 | 다운로드 링크 |

---

## 1️⃣ **`yacht_specifications.json`** - 마스터 데이터

### **역할**
- 기존 20종 요트의 **핵심 스펙** 저장
- 챗봇이 가장 먼저 참조하는 **메인 데이터베이스**

### **데이터 구조**
```json
{
  "schemaVersion": "5.0",
  "totalYachts": 20,
  "yachts": [
    {
      "id": "j-70",
      "name": "J/70",
      "manufacturer": "C&C Fiberglass Components",
      "yachtSpecs": {
        "standard": {
          "dimensions": { "LOA": "7.08m", "Beam": "2.21m", ... },
          "engine": { "power": "6HP", ... },
          "sailArea": { "mainsail": "15.3m²", ... }
        }
      },
      "detailedDimensions": { ... },
      "exterior": { ... },
      "parts": [ ... ]
    }
  ]
}
```

### **사용 예시**
```javascript
// 사용자: "J/70 스펙 알려줘"
→ yacht_specifications.json에서 "j-70" 검색
→ 치수, 엔진, 돛 면적 정보 반환
```

### **특징**
- ✅ **완전한 Schema 5.0 구조**
- ✅ 모든 요트에 `id` 필드 포함
- ✅ AI가 PDF에서 추출한 **정제된 데이터**
- ✅ 챗봇 응답의 **1차 데이터 소스**

---

## 2️⃣ **`yacht_parts_database.json`** - 부품 상세 데이터베이스

### **역할**
- 각 요트의 **부품 목록** 저장
- 부품별 **상세 정보** 제공

### **데이터 구조**
```json
{
  "schemaVersion": "5.0",
  "totalYachts": 20,
  "yachts": [
    {
      "id": "j-70",
      "name": "J/70",
      "manufacturer": "C&C Fiberglass Components",
      "totalParts": 27,
      "parts": [
        {
          "id": "part-structure-hull-01",
          "name": "Hull",
          "category": "Structure",
          "specifications": {
            "material": "Fiberglass",
            "manufacturer": "C&C Fiberglass"
          },
          "maintenanceDetails": {
            "interval": "12 months",
            "method": "Visual inspection"
          }
        }
      ]
    }
  ]
}
```

### **사용 예시**
```javascript
// 사용자: "J/70 엔진 부품 알려줘"
→ yacht_parts_database.json에서 "j-70" 검색
→ category: "Engine"인 부품 필터링
→ 부품 목록 반환
```

### **특징**
- ✅ **부품별 ID** (`part-structure-hull-01`)
- ✅ **카테고리 분류** (Structure, Engine, Rigging, ...)
- ✅ **정비 정보** 포함 (interval, method)
- ✅ 챗봇이 부품 관련 질문 시 사용

---

## 3️⃣ **`yacht_parts_app_data.json`** - 모바일 앱 최적화 데이터

### **역할**
- 모바일 앱(iOS/Android)에서 사용하기 위한 **경량화 데이터**
- `yacht_parts_database.json`의 **간소화 버전**

### **데이터 구조**
```json
{
  "schemaVersion": "5.0",
  "totalYachts": 20,
  "yachts": [
    {
      "id": "j-70",
      "name": "J/70",
      "manufacturer": "C&C Fiberglass Components",
      "parts": [
        {
          "id": "part-structure-hull-01",
          "name": "Hull",
          "category": "Structure",
          "manufacturer": "C&C Fiberglass",
          "interval": 12  // ← 정비 주기 (개월)
        }
      ]
    }
  ]
}
```

### **차이점**
| 항목 | `yacht_parts_database.json` | `yacht_parts_app_data.json` |
|------|----------------------------|----------------------------|
| 크기 | 큼 (8,547줄) | 작음 (4,606줄) |
| 상세도 | 매우 상세 | 필수 정보만 |
| 용도 | 챗봇 조회 | 모바일 앱 UI |
| 정비 정보 | 전체 구조 | `interval` 필드만 |

### **사용 예시**
```dart
// Flutter 앱에서 사용
final yacht = await YachtService.getYacht('j-70');
final parts = yacht['parts'];

// UI에 표시
ListView.builder(
  itemCount: parts.length,
  itemBuilder: (context, index) {
    return ListTile(
      title: Text(parts[index]['name']),
      subtitle: Text('정비 주기: ${parts[index]['interval']}개월'),
    );
  },
);
```

### **특징**
- ✅ **모바일 최적화** (파일 크기 50% 감소)
- ✅ **빠른 로딩**
- ✅ **interval 값이 정확** (`null`이 아닌 실제 값)
- ✅ 앱 배포 시 포함

---

## 4️⃣ **`extracted_yacht_parts.json`** - 원본 추출 데이터

### **역할**
- AI가 PDF에서 **처음 추출한 원본 데이터**
- 정제되지 않은 **raw 데이터**

### **데이터 구조**
```json
{
  "yachts": [
    {
      "yacht": "Beneteau Oceanis 46",
      "rigging": [
        {
          "description": "Air draft - Empty vessel: Classical mast ... 20,31m",
          "context": "Air draft - Empty vessel: Classical mast ...",
          "specifications": ["20"]
        }
      ]
    }
  ]
}
```

### **특징**
- ❌ **정제되지 않음** (PDF 원문 그대로)
- ❌ **구조화되지 않음**
- ✅ **디버깅 용도**
- ✅ AI 추출 정확도 검증

### **사용 예시**
```python
# 개발자가 AI 추출 결과 확인
if extracted_data != expected_data:
    print("AI 추출 오류 발견!")
    print(f"원본: {extracted_yacht_parts.json}")
    print(f"정제본: {yacht_specifications.json}")
```

### **일반 사용자에게는 필요 없음** ⚠️

---

## 5️⃣ **`extracted_yacht_parts_detailed.json`** - 상세 추출 데이터

### **역할**
- `extracted_yacht_parts.json`보다 **더 상세한 원본 데이터**
- 부품별 **세부 설명** 포함

### **데이터 구조**
```json
{
  "yachts": [
    {
      "id": "oceanis-46.1",
      "yacht": "OCEANIS 46.1",
      "parts": [
        {
          "name": "Hull Construction Material",
          "category": "Hull",
          "description": "Single skin laminated fibreglass / GRP",
          "specifications": {
            "material": "GRP",
            "implementation": "Wet laid fiber"
          },
          "raw_text": "Hull: Single skin laminated fibreglass..."
        }
      ]
    }
  ]
}
```

### **차이점**
| 항목 | `extracted_yacht_parts.json` | `extracted_yacht_parts_detailed.json` |
|------|----------------------------|-------------------------------------|
| 크기 | 36,244줄 | 33,112줄 |
| 구조 | 단순 리스트 | 부품별 분류 |
| 용도 | 디버깅 | 상세 디버깅 |

### **특징**
- ✅ **원본 텍스트 보존** (`raw_text`)
- ✅ **AI 추출 검증용**
- ✅ **개발/디버깅 전용**

### **일반 사용자에게는 필요 없음** ⚠️

---

## 6️⃣ **`registered_yachts.json`** - 사용자 등록 데이터

### **역할**
- 사용자가 **직접 업로드한 요트** 저장
- 기존 20종에 없는 **커스텀 요트** 관리

### **데이터 구조**
```json
{
  "schemaVersion": "5.0",
  "description": "사용자가 등록한 요트 목록",
  "totalYachts": 1,
  "yachts": [
    {
      "id": "swan-41",
      "registrationDate": "2025-11-21T19:18:40",
      "source": "PDF Upload",
      "pdfFile": "2020_03_31_11_03_39-48 owners manual.pdf",
      "registrationData": {
        "id": "swan-41",
        "basicInfo": {
          "name": "SWAN 41",
          "manufacturer": "Nautor",
          "type": "Owner's Manual"
        },
        "specifications": { ... },
        "parts": [ ... ]
      },
      "analysisResult": {
        "documentInfo": { ... },
        "partsCount": 23,
        "analysisStatus": "success"
      }
    }
  ]
}
```

### **사용 예시**
```javascript
// 사용자가 새 요트 등록
POST /api/yacht/register
{
  "pdf_file": "my_custom_yacht.pdf"
}

→ AI가 PDF 분석
→ registered_yachts.json에 저장
→ 이후 챗봇이 해당 요트 정보 제공 가능
```

### **특징**
- ✅ **사용자별 데이터** (개인화)
- ✅ **등록 날짜 추적**
- ✅ **분석 결과 저장**
- ✅ 기존 20종과 **별도 관리**

### **업데이트 방식**
```
기존 20종: batch_update_yachts_json.py (수동)
사용자 등록: chatbot_unified.py (자동)
```

---

## 7️⃣ **`yacht_manual_resources.json`** - 매뉴얼 리소스

### **역할**
- 요트 **매뉴얼 다운로드 링크** 제공
- PDF 파일 정보 관리

### **데이터 구조**
```json
{
  "schemaVersion": "5.0",
  "totalResources": 19,
  "resources": [
    {
      "yachtModel": "J/70",
      "manufacturer": "C&C Fiberglass Components",
      "manualPDF": "j70-user-manual.pdf",
      "documentType": "Owner's Manual",
      "canAnalyze": true
    }
  ],
  "yachts": [
    {
      "id": "j-70",
      "name": "J/70",
      "manufacturer": "C&C Fiberglass Components",
      "manualPDF": "j70-user-manual.pdf",
      "officialWebsite": "https://jboats.com",
      "downloadLinks": [
        {
          "type": "official",
          "url": "https://jboats.com/j70-manual.pdf"
        }
      ]
    }
  ]
}
```

### **사용 예시**
```javascript
// 사용자: "J/70 매뉴얼 어디서 받아?"
→ yacht_manual_resources.json에서 "j-70" 검색
→ downloadLinks 반환
→ "공식 웹사이트에서 다운로드 가능합니다: https://jboats.com/j70-manual.pdf"
```

### **특징**
- ✅ **매뉴얼 메타데이터**
- ✅ **다운로드 링크 관리**
- ✅ **문서 타입 분류** (Owner's Manual, Class Rules, ...)
- ✅ 향후 확장 가능

---

## 📊 **파일 간 관계도**

```
┌─────────────────────────────────────────────────────────────┐
│                    사용자 PDF 업로드                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    ┌───────────────┐
                    │ chatbot_unified.py │
                    │   (AI 분석)     │
                    └───────────────┘
                            ↓
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ 원본 추출 데이터 │  │  정제된 데이터  │  │   리소스 정보  │
├──────────────┤  ├──────────────┤  ├──────────────┤
│extracted_    │  │yacht_        │  │yacht_manual_ │
│yacht_parts   │  │specifications│  │resources.json│
│.json         │  │.json         │  │              │
│              │  │              │  │              │
│extracted_    │  │yacht_parts_  │  │              │
│yacht_parts_  │  │database.json │  │              │
│detailed.json │  │              │  │              │
│              │  │yacht_parts_  │  │              │
│(디버깅 전용)   │  │app_data.json │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
                            ↓
                    ┌───────────────┐
                    │registered_    │
                    │yachts.json    │
                    │(사용자 등록 전용)│
                    └───────────────┘
```

---

## 🎯 **각 파일을 언제 사용하나요?**

### **일반 사용자 (챗봇 대화)**
```
사용: ✅ yacht_specifications.json
     ✅ yacht_parts_database.json
     ✅ yacht_parts_app_data.json
     ✅ yacht_manual_resources.json
     ✅ registered_yachts.json
무시: ❌ extracted_yacht_parts.json
     ❌ extracted_yacht_parts_detailed.json
```

### **모바일 앱 개발자**
```
사용: ✅ yacht_parts_app_data.json  (주로 사용)
     ✅ yacht_specifications.json
     ✅ yacht_manual_resources.json
```

### **백엔드 개발자**
```
사용: ✅ yacht_specifications.json
     ✅ yacht_parts_database.json
     ✅ registered_yachts.json
```

### **AI/데이터 과학자**
```
사용: ✅ extracted_yacht_parts.json       (원본 데이터)
     ✅ extracted_yacht_parts_detailed.json (상세 데이터)
     ✅ yacht_specifications.json          (정제 데이터)
목적: AI 추출 정확도 개선
```

---

## 💡 **파일 크기 비교**

| 파일 | 줄 수 | 크기 | 용도 |
|------|-------|------|------|
| `yacht_specifications.json` | 11,414 | ⭐⭐⭐ | 메인 |
| `yacht_parts_database.json` | 8,547 | ⭐⭐⭐ | 부품 DB |
| `yacht_parts_app_data.json` | 4,606 | ⭐⭐ | 앱 전용 |
| `extracted_yacht_parts.json` | 36,244 | ⭐⭐⭐⭐⭐ | 디버깅 |
| `extracted_yacht_parts_detailed.json` | 33,112 | ⭐⭐⭐⭐⭐ | 디버깅 |
| `registered_yachts.json` | 223 | ⭐ | 사용자 |
| `yacht_manual_resources.json` | 340 | ⭐ | 리소스 |

---

## 🔧 **파일 관리 가이드**

### **자동 업데이트 파일**
```
✅ registered_yachts.json
   → chatbot_unified.py가 자동 관리
   → 사용자가 PDF 업로드 시 자동 추가
```

### **수동 업데이트 파일**
```
✅ yacht_specifications.json
✅ yacht_parts_database.json
✅ yacht_parts_app_data.json
✅ yacht_manual_resources.json
   → batch_update_yachts_json.py로 일괄 업데이트
```

### **읽기 전용 파일**
```
⚠️ extracted_yacht_parts.json
⚠️ extracted_yacht_parts_detailed.json
   → AI가 생성한 원본 데이터
   → 절대 수동으로 수정하지 말 것
```

---

## 🚀 **요약**

| 파일 | 핵심 역할 | 주 사용자 |
|------|----------|----------|
| `yacht_specifications.json` | 📊 마스터 데이터 | 모두 |
| `yacht_parts_database.json` | 🔧 부품 상세 정보 | 챗봇 |
| `yacht_parts_app_data.json` | 📱 모바일 최적화 | 앱 개발자 |
| `extracted_yacht_parts.json` | 🐛 원본 디버깅 | AI 엔지니어 |
| `extracted_yacht_parts_detailed.json` | 🔍 상세 디버깅 | AI 엔지니어 |
| `registered_yachts.json` | 👤 사용자 데이터 | 최종 사용자 |
| `yacht_manual_resources.json` | 🔗 매뉴얼 링크 | 모두 |

**핵심 포인트**: 일반 사용자는 처음 5개 파일만 신경 쓰면 됩니다! 나머지 2개는 개발/디버깅 전용입니다.

