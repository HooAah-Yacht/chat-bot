# Notion API 연동 가이드

## 📋 개요

이 가이드는 JSON 데이터를 Notion 데이터베이스와 동기화하는 방법을 설명합니다.

---

## 🔧 1단계: Notion Integration 생성

### 1. Notion Integration 페이지 접속
https://www.notion.so/my-integrations

### 2. New Integration 생성
- **이름**: `HooAah Yacht Chatbot`
- **Associated workspace**: 본인의 워크스페이스 선택
- **Type**: Internal integration
- **Capabilities**:
  - ✅ Read content
  - ✅ Update content
  - ✅ Insert content

### 3. Internal Integration Token 복사
- `secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxx` 형식의 토큰을 복사

---

## 📊 2단계: Notion 데이터베이스 생성

### 각 JSON 파일마다 데이터베이스 생성:

#### 1. `yacht_specifications` 데이터베이스

**Properties (속성):**
| 속성명 | 타입 | 설명 |
|--------|------|------|
| ID | Text | 요트 ID |
| Name | Title | 요트 이름 |
| Manufacturer | Text | 제조사 |
| Type | Select | 요트 유형 |
| LOA (m) | Number | 전체 길이 |
| Beam (m) | Number | 폭 |
| Draft (m) | Number | 흘수 |
| Displacement (kg) | Number | 배수량 |
| Main Sail (m²) | Number | 메인 세일 면적 |
| Jib Sail (m²) | Number | 집 세일 면적 |
| Spinnaker (m²) | Number | 스피네이커 면적 |
| Engine Type | Text | 엔진 타입 |
| Engine Power | Text | 엔진 출력 |
| Manual PDF | URL | 매뉴얼 PDF |
| Updated At | Date | 업데이트 날짜 |

#### 2. `yacht_parts_database` 데이터베이스

**Properties:**
| 속성명 | 타입 | 설명 |
|--------|------|------|
| Part ID | Text | 부품 ID |
| Part Name | Title | 부품 이름 |
| Yacht ID | Text | 요트 ID |
| Yacht Name | Text | 요트 이름 |
| Category | Select | 카테고리 |
| Manufacturer | Text | 제조사 |
| Model | Text | 모델명 |
| Maintenance Interval | Number | 정비 주기 (개월) |
| Specifications | Text | 상세 사양 |

#### 3. `yacht_parts_app_data` 데이터베이스

**Properties:**
| 속성명 | 타입 | 설명 |
|--------|------|------|
| Part ID | Text | 부품 ID |
| Part Name | Title | 부품 이름 |
| Yacht ID | Text | 요트 ID |
| Yacht Name | Text | 요트 이름 |
| Category | Multi-select | 카테고리 |
| Manufacturer | Text | 제조사 |
| Interval (months) | Number | 정비 주기 |

#### 4. `registered_yachts` 데이터베이스

**Properties:**
| 속성명 | 타입 | 설명 |
|--------|------|------|
| Registration Date | Date | 등록일 |
| Yacht Name | Title | 요트 이름 |
| Manufacturer | Text | 제조사 |
| Source | Select | 출처 |
| PDF File | Text | PDF 파일명 |
| Parts Count | Number | 부품 개수 |
| Status | Select | 상태 |

#### 5. `yacht_manual_resources` 데이터베이스

**Properties:**
| 속성명 | 타입 | 설명 |
|--------|------|------|
| Yacht Model | Title | 요트 모델 |
| Manufacturer | Text | 제조사 |
| Manual PDF | Files & media | 매뉴얼 PDF |
| Document Type | Select | 문서 타입 |
| Can Analyze | Checkbox | 분석 가능 여부 |
| Updated At | Date | 업데이트 날짜 |

---

## 🔗 3단계: 데이터베이스 연결

각 데이터베이스마다:

1. 데이터베이스 페이지 열기
2. 우측 상단 `⋯` 클릭
3. `Add connections` 선택
4. `HooAah Yacht Chatbot` Integration 선택

---

## 🆔 4단계: 데이터베이스 ID 가져오기

### 데이터베이스 ID 추출 방법:

1. Notion에서 데이터베이스 열기
2. URL 확인:
   ```
   https://www.notion.so/xxxxxxxxxxxxxxxxxxxxx?v=yyyyy
   ```
3. `xxxxxxxxxxxxxxxxxxxxx` 부분이 데이터베이스 ID

### 각 데이터베이스 ID 저장:
- `yacht_specifications`: `xxxxx`
- `yacht_parts_database`: `xxxxx`
- `yacht_parts_app_data`: `xxxxx`
- `registered_yachts`: `xxxxx`
- `yacht_manual_resources`: `xxxxx`

---

## ⚙️ 5단계: 환경변수 설정

### Windows (CMD):
```cmd
set NOTION_API_KEY=secret_xxxxxxxxxxxxx
set NOTION_DB_YACHT_SPECS=데이터베이스_ID_1
set NOTION_DB_PARTS=데이터베이스_ID_2
set NOTION_DB_PARTS_APP=데이터베이스_ID_3
set NOTION_DB_REGISTERED=데이터베이스_ID_4
set NOTION_DB_MANUALS=데이터베이스_ID_5
```

### 또는 `.env` 파일 생성:
```env
NOTION_API_KEY=secret_xxxxxxxxxxxxx
NOTION_DB_YACHT_SPECS=데이터베이스_ID_1
NOTION_DB_PARTS=데이터베이스_ID_2
NOTION_DB_PARTS_APP=데이터베이스_ID_3
NOTION_DB_REGISTERED=데이터베이스_ID_4
NOTION_DB_MANUALS=데이터베이스_ID_5
```

---

## 🚀 6단계: 스크립트 실행

### 패키지 설치:
```bash
cd chat-bot
pip install -r requirements.txt
```

### Notion 업데이트 실행:
```bash
python update_notion.py
```

### 대화형 설정 모드:
API Key와 데이터베이스 ID를 직접 입력하여 설정할 수 있습니다.

---

## 🔄 업데이트 방법

### 자동 업데이트:
JSON 파일이 변경될 때마다:
```bash
python update_notion.py
```

### 동작:
- **ID 매칭**: JSON의 ID와 Notion의 ID를 비교
- **존재하면 업데이트**: 기존 페이지 수정
- **없으면 생성**: 새 페이지 추가

---

## 📝 주의사항

1. **API Rate Limit**: Notion API는 요청 제한이 있습니다 (초당 3회)
2. **ID 필드**: ID 필드가 비어있으면 중복 생성될 수 있습니다
3. **Select 타입**: 새로운 옵션은 자동으로 추가되지만, 기존 옵션과 정확히 일치해야 합니다
4. **URL 필드**: 유효한 URL이 아니면 null로 저장됩니다

---

## ✅ 완료!

이제 JSON 파일과 Notion 데이터베이스가 동기화됩니다! 🎉

### 다음 단계:
- Notion에서 데이터 확인
- 필요시 View 커스터마이징
- 자동 업데이트 스케줄 설정

---

## 🆘 문제 해결

### "Invalid database_id" 오류
→ 데이터베이스 ID를 다시 확인하세요

### "Unauthorized" 오류
→ Integration이 데이터베이스에 연결되었는지 확인하세요

### "Property not found" 오류
→ 데이터베이스 속성 이름이 가이드와 일치하는지 확인하세요

---

**문의사항이 있으시면 팀에 연락주세요!**

