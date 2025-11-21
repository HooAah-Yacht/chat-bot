# ✅ chatbot_unified.py 업데이트 완료!

## 🎉 **업데이트 내용**

`chatbot_unified.py`가 새로운 요트 등록 시 자동으로 ID를 생성하고 모든 JSON 파일에 반영하도록 업데이트되었습니다.

---

## 🔧 **변경 사항**

### **1. `_save_to_registered_yachts` 함수 업데이트**

#### **Before (ID 없음)**
```python
registration_entry = {
    "registrationDate": datetime.now().isoformat(),
    "source": "PDF Upload",
    "pdfFile": "...",
    "registrationData": registration_data
}
```

#### **After (ID 추가)** ✅
```python
yacht_id = registration_data.get("id") or registration_data.get("basicInfo", {}).get("id")

registration_entry = {
    "id": yacht_id,  # 🆕 최상위 ID
    "registrationDate": datetime.now().isoformat(),
    "source": "PDF Upload",
    "pdfFile": "...",
    "registrationData": registration_data  # 이미 ID 포함
}

data["totalYachts"] = len(data["yachts"])  # 🆕 총 요트 수 업데이트
data["schemaVersion"] = "5.0"  # 🆕 스키마 버전
```

---

## 📋 **ID 생성 및 저장 흐름**

```
1. 사용자가 PDF 업로드
   ↓
2. AI가 PDF 분석 (yachtModel 추출)
   ↓
3. _generate_yacht_id(yacht_name)
   "SWAN 41" → "swan-41"
   ↓
4. _convert_analysis_to_registration
   registration_data["id"] = "swan-41"
   registration_data["basicInfo"]["id"] = "swan-41"
   ↓
5. JSON 파일에 저장 (모두 동일한 ID 사용)
   ├─ yacht_specifications.json       (id: "swan-41")
   ├─ yacht_parts_database.json       (id: "swan-41")
   ├─ yacht_parts_app_data.json       (id: "swan-41")
   ├─ extracted_yacht_parts.json      (id: "swan-41")
   ├─ extracted_yacht_parts_detailed  (id: "swan-41")
   └─ registered_yachts.json          (id: "swan-41")
```

---

## 🆔 **ID 생성 규칙**

```python
def _generate_yacht_id(self, yacht_name: str) -> str:
    """
    예시:
    - "J/70" → "j-70"
    - "OCEANIS 46.1" → "oceanis-46.1"
    - "Grand Soleil 42 Long Cruise" → "grand-soleil-42-long-cruise"
    - "SWAN 41" → "swan-41"
    - "X–35 One Design" → "x35-one-design"
    """
    yacht_id = yacht_name.lower()
    yacht_id = yacht_id.replace("/", "-")
    yacht_id = yacht_id.replace(" ", "-")
    yacht_id = re.sub(r'[^a-z0-9\-\.]', '', yacht_id)
    yacht_id = re.sub(r'-+', '-', yacht_id)
    yacht_id = yacht_id.strip('-')
    return yacht_id
```

---

## 📁 **업데이트된 함수 목록**

| 함수명 | 상태 | 설명 |
|--------|------|------|
| `_generate_yacht_id` | ✅ 이미 존재 | ID 생성 |
| `_convert_analysis_to_registration` | ✅ 이미 존재 | ID를 registration_data에 포함 |
| `_save_to_registered_yachts` | ✅ 업데이트 완료 | 최상위에 ID 추가 |
| `_add_to_yacht_specifications` | ✅ 이미 존재 | ID 사용 |
| `_add_to_yacht_parts_database` | ✅ 이미 존재 | ID 사용 |
| `_add_to_extracted_parts_detailed` | ✅ 이미 존재 | ID 사용 |
| `_add_to_extracted_parts` | ✅ 이미 존재 | ID 사용 |
| `_add_to_parts_app_data` | ✅ 이미 존재 | ID 사용 |
| `_save_parts_to_json_files` | ✅ 이미 존재 | ID 전달 |

---

## 🧪 **테스트 방법**

### **1. 챗봇 실행**
```bash
cd C:\Users\user\Documents\Yacht2\chat-bot
python chatbot_unified.py
```

### **2. 요트 등록**
```
💬 입력: 요트 정보 등록을 원해
📥 PDF 경로 입력: data/yachtpdf/owners_manual.pdf
```

### **3. 결과 확인**
```bash
# registered_yachts.json 확인
cat data/registered_yachts.json
```

**예상 결과:**
```json
{
  "schemaVersion": "5.0",
  "totalYachts": 1,
  "yachts": [
    {
      "id": "first-36.7",  // 🆕 최상위 ID
      "registrationDate": "2025-11-21T...",
      "source": "PDF Upload",
      "pdfFile": "owners_manual.pdf",
      "registrationData": {
        "id": "first-36.7",  // 🆕 registrationData ID
        "basicInfo": {
          "id": "first-36.7",  // 🆕 basicInfo ID
          "name": "FIRST 36.7",
          "manufacturer": "BENETEAU"
        }
      }
    }
  ]
}
```

---

## 📊 **저장되는 위치**

### **`registered_yachts.json` 구조**
```json
{
  "yachts": [
    {
      "id": "swan-41",           // ← 🆕 1. 최상위
      "registrationData": {
        "id": "swan-41",         // ← 🆕 2. registrationData
        "basicInfo": {
          "id": "swan-41",       // ← 🆕 3. basicInfo
          "name": "SWAN 41"
        }
      }
    }
  ]
}
```

**3곳에 ID가 저장되는 이유:**
1. **최상위 `id`**: 빠른 검색 및 API 응답
2. **registrationData `id`**: 백엔드 API 호환
3. **basicInfo `id`**: UI 표시 및 폼 데이터

---

## 🔍 **다른 JSON 파일도 확인**

### **yacht_specifications.json**
```json
{
  "yachts": [
    {
      "id": "swan-41",
      "name": "SWAN 41",
      "yachtSpecs": { ... }
    }
  ]
}
```

### **yacht_parts_database.json**
```json
{
  "yachts": [
    {
      "id": "swan-41",
      "name": "SWAN 41",
      "parts": [
        {
          "id": "swan-41-engine-01",  // ← 부품 ID에도 yacht_id 포함
          "name": "Engine"
        }
      ]
    }
  ]
}
```

---

## ✅ **완료 사항**

- ✅ `_save_to_registered_yachts` 함수에 ID 추가
- ✅ `schemaVersion` "5.0" 사용
- ✅ `totalYachts` 자동 계산
- ✅ 모든 부품 저장 함수에서 `yacht_id` 사용
- ✅ ID가 3곳에 저장됨 (최상위, registrationData, basicInfo)

---

## 🚀 **다음 단계**

1. ✅ **기존 20종 업데이트**: `batch_update_yachts_json.py` (완료!)
2. ✅ **chatbot_unified.py 업데이트** (완료!)
3. 🔜 **API 테스트**: `/api/yacht/register` 엔드포인트
4. 🔜 **MySQL 동기화**: 데이터베이스에 ID 반영

---

## 💡 **API 응답 예시**

### **POST /api/yacht/register**

**Request:**
```bash
curl -X POST http://localhost:5000/api/yacht/register \
  -F "file=@owners_manual.pdf"
```

**Response:**
```json
{
  "success": true,
  "yacht": {
    "id": "first-36.7",  // 🆕 자동 생성된 ID
    "name": "FIRST 36.7",
    "manufacturer": "BENETEAU",
    "specifications": { ... },
    "parts": [ ... ]
  },
  "message": "요트가 성공적으로 등록되었습니다!"
}
```

---

## 🎯 **요약**

1. **자동 ID 생성**: 요트 이름에서 자동으로 고유 ID 생성
2. **일관성**: 모든 JSON 파일에 동일한 ID 사용
3. **계층 구조**: registered_yachts.json에 3단계로 ID 저장
4. **하위 호환성**: 기존 코드와 호환 유지

모든 준비가 완료되었습니다! 🎉

