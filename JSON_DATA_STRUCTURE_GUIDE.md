# 📊 JSON 파일 데이터 구조 및 예시

## 목차
1. [yacht_specifications.json](#1-yacht_specificationsjson)
2. [registered_yachts.json](#2-registered_yachtsjson)
3. [yacht_manual_resources.json](#3-yacht_manual_resourcesjson)
4. [yacht_parts_app_data.json](#4-yacht_parts_app_datajson)
5. [yacht_parts_database.json](#5-yacht_parts_databasejson)

---

## 1. yacht_specifications.json

### 📝 용도
**20종 요트의 상세 사양 마스터 데이터**
- PDF 매뉴얼 자동 분석 결과
- 모든 요트의 기본 정보, 치수, 엔진, 세일, 외관, 부품 등 포함

### 📥 입력 데이터
```
PDF 파일: 14670061006300089_USER_MANUAL_OCEANIS_46.1.pdf
```

### 📤 출력 데이터 구조
```json
{
  "schemaVersion": "5.0",
  "lastUpdated": "2025-11-21",
  "totalYachts": 19,
  "yachts": [
    {
      "id": "oceanis-46.1",                    // 🆔 요트 고유 ID
      "name": "OCEANIS 46.1",                  // 📛 요트 이름
      "manufacturer": "BENETEAU",              // 🏭 제조사
      "type": "Owner's Manual",                // 📄 문서 타입
      "manualPDF": "14670061006300089_USER_MANUAL_OCEANIS_46.1.pdf",
      
      "yachtSpecs": {
        "standard": {
          "dimensions": {                      // 📏 치수
            "LOA": "14.60m",                   // 전체 길이
            "Beam": "4.50m",                   // 폭
            "Draft": "1.87m / 2.47m / 2.68m",  // 흘수 (Shallow/Deep/Very Deep)
            "Displacement": "11278kg"          // 배수량
          },
          "engine": {                          // 🚢 엔진
            "type": null,
            "power": "59Kw"
          },
          "sailArea": {                        // ⛵ 세일 면적
            "mainsail": "53.75m²",
            "genoa": "52.16m²",
            "spinnaker": "151.70 m²",
            "jib": "40.42m²"
          }
        }
      },
      
      "exterior": {                            // 🏗️ 외관 구조
        "hull": {
          "id": "ext-hull-01",                 // 🆔 부품 ID
          "name": "Hull",
          "category": "Structure",
          "manufacturer": "SPBI S.A",
          "specifications": {
            "material": "Single skin laminated fibreglass / GRP",
            "implementation": "Wet laid fiber"
          },
          "subComponents": [                   // 🔗 하위 부품 (계층 구조)
            {
              "id": "ext-hull-keel-shallow-01",
              "parentId": "ext-hull-01",       // 👆 상위 부품 ID
              "name": "Shallow Draught Keel",
              "specifications": {
                "draft": "1.87m"
              }
            }
          ]
        }
      },
      
      "parts": [                               // 🔧 주요 부품 목록
        {
          "id": "part-engine-cooling-01",
          "name": "Engine Cooling System",
          "category": "Engine",
          "maintenanceDetails": {
            "interval": "12 months",
            "description": "Check coolant level"
          }
        }
      ]
    }
  ]
}
```

### 🎯 주요 특징
- ✅ **ID 기반 식별**: 모든 요트와 부품에 고유 ID
- ✅ **계층 구조**: `parentId`로 부품 간 관계 표현
- ✅ **상세 사양**: `specifications` 객체에 모든 세부 정보
- ✅ **신뢰도 점수**: `_confidence` 필드로 데이터 신뢰도 표시

---

## 2. registered_yachts.json

### 📝 용도
**사용자가 챗봇으로 등록한 요트 목록**
- `chatbot_unified.py`에서 PDF 업로드 시 저장
- 요트 등록 이력 관리

### 📥 입력 데이터
```
사용자 입력: "요트 정보 등록을 원해"
PDF 업로드: 2020_03_31_11_03_39-48 owners manual.pdf
```

### 📤 출력 데이터 구조
```json
{
  "schemaVersion": "5.0",
  "lastUpdated": "2025-11-21",
  "totalYachts": 1,
  "yachts": [
    {
      "registrationDate": "2025-11-21T19:18:40.654969",  // 📅 등록 날짜
      "source": "PDF Upload",                            // 📥 등록 방법
      "pdfFile": "2020_03_31_11_03_39-48 owners manual.pdf",
      
      "registrationData": {
        "basicInfo": {                                   // 📋 기본 정보
          "name": "SWAN 41",
          "nickName": "SWAN 41",
          "manufacturer": "Nautor",
          "type": "Owner's Manual",
          "manual": "2020_03_31_11_03_39-48 owners manual.pdf"
        },
        
        "specifications": {                              // 📊 사양
          "dimensions": {
            "loa": null,                                 // ⚠️ 추출 실패 시 null
            "beam": null,
            "draft": null
          },
          "sailArea": {
            "mainSailArea": null,
            "jibSailArea": null
          },
          "engine": {
            "type": "",
            "power": "",
            "model": ""
          }
        },
        
        "parts": [                                       // 🔧 추출된 부품 목록
          {
            "name": "Engine Cooling Water Strainer",
            "manufacturer": "",
            "model": "",
            "interval": null
          },
          {
            "name": "Warning Light (Low Oil Pressure/High Coolant Temperature)",
            "manufacturer": "",
            "model": "",
            "interval": null
          },
          {
            "name": "Folding Propeller",
            "manufacturer": "",
            "model": "",
            "interval": null
          }
        ]
      },
      
      "analysisResult": {                                // ✅ 분석 결과
        "documentInfo": {
          "title": "OWNER MANUAL",
          "yachtModel": "SWAN 41",
          "manufacturer": "Nautor",
          "documentType": "Owner's Manual"
        },
        "partsCount": 23,                                // 📊 추출된 부품 개수
        "analysisStatus": "success"                      // ✅ 분석 상태
      }
    }
  ]
}
```

### 🎯 주요 특징
- ✅ **등록 이력**: 언제, 어떤 PDF로 등록했는지 추적
- ✅ **분석 결과**: AI가 추출한 정보의 신뢰도 확인
- ⚠️ **Null 허용**: 추출 실패 시 null로 저장

---

## 3. yacht_manual_resources.json

### 📝 용도
**요트 매뉴얼 다운로드 정보**
- 어떤 PDF 파일이 어떤 요트의 매뉴얼인지 관리
- 매뉴얼 검색 및 다운로드 안내

### 📥 입력 데이터
```
PDF 파일: 14670061006300089_USER_MANUAL_OCEANIS_46.1.pdf
자동 분석: AI가 매뉴얼 정보 추출
```

### 📤 출력 데이터 구조
```json
{
  "schemaVersion": "5.0",
  "lastUpdated": "2025-11-21T17:07:52.022761",
  "totalResources": 19,
  "resources": [
    {
      "yachtModel": "OCEANIS 46.1",           // 📛 요트 모델명
      "manufacturer": "BENETEAU",             // 🏭 제조사
      "manualPDF": "14670061006300089_USER_MANUAL_OCEANIS_46.1.pdf",  // 📄 파일명
      "documentType": "Owner's Manual",       // 📝 문서 종류
      "canAnalyze": true,                     // ✅ 분석 가능 여부
      "schemaVersion": "5.0",
      "updatedAt": "2025-11-21T17:07:52.022761"
    },
    {
      "yachtModel": "J/70",
      "manufacturer": "C&C Fiberglass Components, Inc.",
      "manualPDF": "j70-user-manual.pdf",
      "documentType": "Owner's Manual",
      "canAnalyze": true
    },
    {
      "yachtModel": "Laser",
      "manufacturer": "International Laser Class Association",
      "manualPDF": "Handbook_2109.pdf",
      "documentType": "Class Rules",          // 📜 클래스 규정
      "canAnalyze": true
    }
  ]
}
```

### 🎯 주요 특징
- ✅ **매뉴얼 카탈로그**: 모든 요트 매뉴얼 목록
- ✅ **문서 타입**: Owner's Manual, Class Rules, Brochure 등 구분
- ✅ **분석 가능 여부**: AI 분석이 가능한 문서인지 표시

---

## 4. yacht_parts_app_data.json

### 📝 용도
**모바일 앱용 간소화 부품 데이터**
- iOS/Android 앱에서 빠르게 로드
- 정비 주기 관리에 필요한 최소 정보만 포함

### 📥 입력 데이터
```
yacht_parts_database.json의 부품 데이터
→ 앱에 필요한 필드만 추출
```

### 📤 출력 데이터 구조
```json
{
  "schemaVersion": "5.0",
  "lastUpdated": "2025-11-21T17:07:52.024759",
  "totalYachts": 19,
  "yachts": [
    {
      "id": "oceanis-46.1",                   // 🆔 요트 ID
      "name": "OCEANIS 46.1",                 // 📛 요트 이름
      "manufacturer": "BENETEAU",             // 🏭 제조사
      "parts": [
        {
          "id": "part-hull-material-01",      // 🆔 부품 ID
          "name": "Hull Construction Material", // 📛 부품 이름
          "category": "Hull",                 // 🏷️ 카테고리
          "manufacturer": "",                 // 🏭 부품 제조사
          "interval": 12                      // ⏱️ 정비 주기 (개월)
        },
        {
          "id": "part-engine-01",
          "name": "Engine",
          "category": "Propulsion",
          "manufacturer": "",
          "interval": 12
        }
      ]
    }
  ]
}
```

### 🎯 주요 특징
- ✅ **경량화**: 앱 성능을 위해 최소 정보만 포함
- ✅ **정비 주기**: `interval` 필드로 정비 알림 기능 지원
- ✅ **빠른 로드**: 상세 사양 제외, 핵심 정보만

---

## 5. yacht_parts_database.json

### 📝 용도
**전체 부품 데이터베이스 (가장 상세한 버전)**
- 모든 요트의 모든 부품 정보
- 상세 사양(specifications) 포함

### 📥 입력 데이터
```
yacht_specifications.json의 parts 섹션
→ 상세 사양과 함께 추출
```

### 📤 출력 데이터 구조
```json
{
  "schemaVersion": "5.0",
  "lastUpdated": "2025-11-21T17:07:52.004757",
  "totalYachts": 19,
  "yachts": [
    {
      "id": "oceanis-46.1",
      "name": "OCEANIS 46.1",
      "manufacturer": "BENETEAU",
      "manualPDF": "14670061006300089_USER_MANUAL_OCEANIS_46.1.pdf",
      "schemaVersion": "5.0",
      "totalParts": 13,                       // 📊 총 부품 개수
      "parts": [
        {
          "id": "part-hull-material-01",
          "name": "Hull Construction Material",
          "category": "Hull",
          "specifications": {                 // 📋 상세 사양
            "material": "Single skin laminated fibreglass / GRP",
            "implementation": "Wet laid fiber"
          }
        },
        {
          "id": "part-engine-01",
          "name": "Engine",
          "category": "Propulsion",
          "specifications": {
            "maxPropulsionPower": "59Kw",
            "maxRecommendedEngineSizeWeight": "2 x 229kg",
            "_additional": {
              "chapterReference": "203"       // 📖 매뉴얼 참조 페이지
            }
          }
        },
        {
          "id": "part-rigging-mainsail-classical-01",
          "name": "Classical Mast Mainsail Luff",
          "category": "Rigging",
          "specifications": {
            "length": "16.82m",
            "partIdentifier": "P"             // 🏷️ 부품 식별자
          }
        }
      ]
    }
  ]
}
```

### 🎯 주요 특징
- ✅ **완전한 정보**: 모든 부품의 상세 사양 포함
- ✅ **매뉴얼 참조**: `chapterReference`로 매뉴얼 페이지 연결
- ✅ **부품 식별자**: `partIdentifier`로 리깅 부품 등 구분
- ✅ **추가 정보**: `_additional` 필드에 기타 메타데이터

---

## 📊 5개 파일 비교표

| 파일 | 용도 | 데이터 양 | 주요 정보 | 사용처 |
|------|------|-----------|-----------|--------|
| **yacht_specifications.json** | 🎯 마스터 데이터 | ⭐⭐⭐⭐⭐ 최대 | 모든 정보 (치수, 엔진, 세일, 외관, 부품) | 전체 요트 정보 조회 |
| **registered_yachts.json** | 📝 사용자 등록 | ⭐⭐ 소량 | 등록 이력, 분석 결과 | 사용자 요트 관리 |
| **yacht_manual_resources.json** | 📚 매뉴얼 목록 | ⭐ 최소 | 매뉴얼 파일명, 문서 타입 | 매뉴얼 검색/다운로드 |
| **yacht_parts_app_data.json** | 📱 앱용 간소화 | ⭐⭐⭐ 중간 | 부품명, 카테고리, 정비 주기 | 모바일 앱 |
| **yacht_parts_database.json** | 🔧 부품 상세 | ⭐⭐⭐⭐ 많음 | 부품 상세 사양, 매뉴얼 참조 | 부품 검색/상세 조회 |

---

## 🔄 데이터 흐름

```
1️⃣ PDF 업로드
   ↓
2️⃣ AI 분석 (chatbot_unified.py)
   ↓
3️⃣ yacht_specifications.json 생성
   ├── 요트 기본 정보 추출
   ├── 치수, 엔진, 세일 데이터 추출
   ├── 외관 구조 (hull, deck 등) 추출
   └── 부품 목록 추출
   ↓
4️⃣ 파생 파일 생성
   ├── yacht_manual_resources.json (매뉴얼 정보만)
   ├── yacht_parts_database.json (부품 상세)
   └── yacht_parts_app_data.json (앱용 간소화)
   ↓
5️⃣ registered_yachts.json (사용자 등록 시)
```

---

## ✅ 요약

각 JSON 파일의 역할:

1. **yacht_specifications.json**: 📚 **전체 백과사전** - 모든 정보 포함
2. **registered_yachts.json**: 📝 **사용자 일기** - 누가 언제 무엇을 등록했는지
3. **yacht_manual_resources.json**: 🗂️ **도서 목록** - 어떤 매뉴얼이 있는지
4. **yacht_parts_app_data.json**: 📱 **앱용 간단 메모** - 빠른 조회용
5. **yacht_parts_database.json**: 🔍 **부품 사전** - 부품 상세 정보

Notion에 올릴 때는 각 파일의 **용도에 맞게** 다른 뷰를 만드는 것을 추천합니다! 🎯

