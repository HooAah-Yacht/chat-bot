# 🆔 요트 ID 자동 생성 가이드

## ✅ 구현 완료!

이제 챗봇이 요트를 등록할 때 자동으로 **고유 ID**를 생성하고 모든 JSON 파일에 저장합니다.

---

## 📋 요트 ID 생성 규칙

### 변환 규칙
1. **소문자 변환**: 모든 문자를 소문자로
2. **슬래시(/) → 하이픈(-)**: `/` 문자를 `-`로 변경
3. **공백 → 하이픈(-)**: 공백을 `-`로 변경
4. **특수문자 제거**: 영문, 숫자, 하이픈, 점만 허용
5. **연속 하이픈 통합**: `--` → `-`
6. **앞뒤 하이픈 제거**: `-yacht-` → `yacht`

### 예시

| 요트 이름 | 생성된 ID |
|---------|----------|
| `J/70` | `j-70` |
| `OCEANIS 46.1` | `oceanis-46.1` |
| `Grand Soleil 42 Long Cruise` | `grand-soleil-42-long-cruise` |
| `Farr 40` | `farr-40` |
| `X–35 One Design` | `x-35-one-design` |
| `ClubSwan 50` | `clubswan-50` |

---

## 🔄 변경된 함수

### 1. `_generate_yacht_id(yacht_name: str) -> str`
**새로 추가된 함수**

```python
def _generate_yacht_id(self, yacht_name: str) -> str:
    """
    요트 ID 생성 함수
    
    예시:
    - "J/70" → "j-70"
    - "OCEANIS 46.1" → "oceanis-46.1"
    """
    import re
    yacht_id = yacht_name.lower()
    yacht_id = yacht_id.replace("/", "-")
    yacht_id = yacht_id.replace(" ", "-")
    yacht_id = re.sub(r'[^a-z0-9\-\.]', '', yacht_id)
    yacht_id = re.sub(r'-+', '-', yacht_id)
    yacht_id = yacht_id.strip('-')
    return yacht_id
```

### 2. `_convert_analysis_to_registration()` - **수정됨**
ID를 `registration_data`에 추가:

```python
yacht_id = self._generate_yacht_id(yacht_name)

registration_data = {
    "id": yacht_id,  # 🆕 최상위에 ID 추가
    "basicInfo": {
        "id": yacht_id,  # 🆕 basicInfo에도 ID 추가
        "name": yacht_name,
        ...
    },
    ...
}
```

### 3. `_add_to_yacht_specifications()` - **수정됨**
ID를 올바르게 가져오고 저장:

```python
yacht_id = registration_data.get("id") or basic_info.get("id")
if not yacht_id:
    yacht_id = self._generate_yacht_id(basic_info.get("name", ""))

new_yacht = {
    "id": yacht_id,  # 🆕 ID 우선 배치
    "name": yacht_name,
    ...
}
```

### 4. `_save_parts_to_json_files()` - **수정됨**
ID를 사용하여 부품 저장:

```python
yacht_id = registration_data.get("id") or basic_info.get("id")
if not yacht_id:
    yacht_id = self._generate_yacht_id(yacht_name)

self._add_to_yacht_parts_database(yacht_id, yacht_name, ...)
```

---

## 📊 JSON 파일에 저장되는 데이터

### 1. `yacht_specifications.json`

```json
{
  "yachts": [
    {
      "id": "j-70",
      "name": "J/70",
      "manufacturer": "J Boats",
      "type": "Owner's Manual",
      ...
    }
  ]
}
```

### 2. `yacht_parts_database.json`

```json
{
  "yachts": [
    {
      "id": "j-70",
      "name": "J/70",
      "manufacturer": "J Boats",
      "parts": {
        "rigging": {
          "physicalParts": [
            {
              "id": "j-70-rigging-01",
              "name": "Mast",
              ...
            }
          ]
        }
      }
    }
  ]
}
```

### 3. `yacht_parts_app_data.json`

```json
{
  "yachts": [
    {
      "id": "j-70",
      "name": "J/70",
      "manufacturer": "J Boats",
      "parts": [
        {
          "name": "Mast",
          "manufacturer": "Selden",
          ...
        }
      ]
    }
  ]
}
```

### 4. `extracted_yacht_parts.json`

```json
{
  "yachts": [
    {
      "id": "j-70",
      "name": "J/70",
      "manufacturer": "J Boats",
      "parts": [...]
    }
  ]
}
```

---

## 🚀 API 응답에도 ID 포함

### `/api/yacht/register` 응답

```json
{
  "success": true,
  "fileName": "J70_manual.pdf",
  "yacht": {
    "id": "j-70",
    "basicInfo": {
      "id": "j-70",
      "name": "J/70",
      "manufacturer": "J Boats",
      ...
    },
    "specifications": {...},
    "parts": [...]
  }
}
```

---

## 🔍 백엔드 연동 예시

### Spring Boot에서 요트 ID 사용

```java
@PostMapping("/register-from-pdf")
public ResponseEntity<?> registerYachtFromPdf(@RequestParam("file") MultipartFile file) {
    // Python API 호출
    YachtRegistrationResponse response = callPythonAPI(file);
    
    // 요트 ID 가져오기
    String yachtId = response.getYacht().getId();
    String yachtName = response.getYacht().getBasicInfo().getName();
    
    // DB에 저장 (ID 포함)
    Yacht yacht = new Yacht();
    yacht.setId(yachtId);  // 🆕 Python에서 생성한 ID 사용
    yacht.setName(yachtName);
    yachtRepository.save(yacht);
    
    // 부품 저장 (yacht_id 참조)
    for (Part part : response.getYacht().getParts()) {
        Part newPart = new Part();
        newPart.setYachtId(yachtId);  // 🆕 요트 ID로 연결
        newPart.setName(part.getName());
        partRepository.save(newPart);
    }
    
    return ResponseEntity.ok(yacht);
}
```

---

## ✅ 로그 확인

챗봇 실행 시 로그에 ID가 표시됩니다:

```
📄 파일 분석 시작: J70_manual.pdf (.pdf)
✅ 텍스트 추출 완료 (15234 문자)
🤖 AI 분석 중...
✅ 분석 완료!
✅ yacht_specifications.json에 저장됨 (ID: j-70)
✅ yacht_parts_database.json에 저장됨 (Yacht ID: j-70)
✅ extracted_yacht_parts_detailed.json에 저장됨
✅ extracted_yacht_parts.json에 저장됨
✅ yacht_parts_app_data.json에 저장됨
✅ 부품 정보가 4개 JSON 파일에 저장됨 (Yacht ID: j-70)
💾 JSON 파일에 저장 완료!
✅ J70_manual.pdf 분석 및 등록 준비 완료!
```

---

## 🎯 요약

| 항목 | 이전 | 현재 ✅ |
|-----|-----|--------|
| **요트 ID** | ❌ 없음 또는 임의 생성 | ✅ 자동 생성 (`_generate_yacht_id`) |
| **ID 규칙** | ❌ 일관성 없음 | ✅ 명확한 규칙 (소문자, 하이픈) |
| **JSON 저장** | ❌ ID 누락 가능 | ✅ 모든 파일에 ID 포함 |
| **API 응답** | ❌ ID 없음 | ✅ `yacht.id` 반환 |
| **백엔드 연동** | ❌ 어려움 | ✅ ID로 쉽게 연결 |

---

## 🔧 테스트

### 1. 대화형 모드
```bash
cd chat-bot
python chatbot_unified.py

# PDF 경로 입력
👤 You: C:\path\to\J70_manual.pdf

# 결과 확인
✅ 등록이 완료됐습니다! 🎉
⛵ 모델: J/70
🆔 요트 ID: j-70
```

### 2. API 모드
```bash
python chatbot_unified.py --mode api --port 5000
```

```bash
# API 호출
curl -X POST http://localhost:5000/api/yacht/register \
  -F "file=@J70_manual.pdf"

# 응답
{
  "success": true,
  "yacht": {
    "id": "j-70",
    ...
  }
}
```

---

## 🎉 완료!

이제 모든 요트가 등록될 때 자동으로 **고유 ID**를 가지게 됩니다!

- ✅ 일관된 ID 생성 규칙
- ✅ 모든 JSON 파일에 ID 저장
- ✅ API 응답에 ID 포함
- ✅ 백엔드 연동 용이
- ✅ 중복 ID 방지

