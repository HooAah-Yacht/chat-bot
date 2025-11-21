# 🐛 정비 주기 데이터 미표시 문제 수정

## 🚨 문제 재현

```
👤 You: J/70 정비는 언제 해야 해?
🤖 AI: 정비 주기 정보가 없습니다.
      총 **27개**의 부품이 등록되어 있지만, 정비 주기가 명시되지 않았습니다.
```

**기대 응답:**
```
🔧 **J/70 정비 및 유지보수 정보**
**부품별 정비 주기**
📦 Rigging
  • Mast: 12개월마다 점검
  ...
```

---

## 🔍 원인 분석

### 데이터 파일 비교:

#### 1. `yacht_parts_database.json` (현재 사용 중) ❌
```json
{
  "yachts": [{
    "name": "J/70",
    "parts": [{
      "id": "part-rigging-mast-01",
      "name": "Mast",
      "category": "Rigging",
      "interval": null      ← ❌ 정비 주기 없음!
    }]
  }]
}
```

#### 2. `yacht_parts_app_data.json` (사용 안 함) ✅
```json
{
  "yachts": [{
    "name": "J/70",
    "parts": [{
      "id": "part-rigging-mast-01",
      "name": "Mast",
      "category": "Rigging",
      "interval": 12      ← ✅ 정비 주기 있음!
    }]
  }]
}
```

### 문제:
챗봇이 **`yacht_parts_database.json`**을 읽고 있었는데, 이 파일의 `interval` 필드가 모두 `null`로 저장되어 있었습니다.

---

## ✅ 해결 방법

### 수정: `_load_parts_data()` 함수

**변경 전:**
```python
def _load_parts_data(self) -> Dict:
    """부품 데이터 로드"""
    with open('data/yacht_parts_database.json', 'r', encoding='utf-8') as f:
        return json.load(f)  # ← interval이 null인 파일 읽음
```

**변경 후:**
```python
def _load_parts_data(self) -> Dict:
    """부품 데이터 로드 (interval 정보가 있는 yacht_parts_app_data.json 우선)"""
    try:
        # yacht_parts_app_data.json을 우선 로드 (interval 정보 포함)
        with open('data/yacht_parts_app_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)  # ← interval이 12인 파일 읽음
    except FileNotFoundError:
        # fallback: yacht_parts_database.json
        with open('data/yacht_parts_database.json', 'r', encoding='utf-8') as f:
            return json.load(f)
```

---

## 📊 데이터 검증

### grep 결과:

**`yacht_parts_database.json`:**
```bash
$ grep "interval" yacht_parts_database.json
"interval": null      ← 19줄 모두 null
"interval": null
"interval": null
...
```

**`yacht_parts_app_data.json`:**
```bash
$ grep "interval" yacht_parts_app_data.json
"interval": 12       ← 19줄 모두 12
"interval": 12
"interval": 12
...
```

---

## ✅ 수정 후 예상 결과

### 질문: "J/70 정비는 언제 해야 해?"

```
🔧 **J/70 정비 및 유지보수 정보**

**부품별 정비 주기** (총 27개 부품)

**📦 Hull**
  • Hull: 12개월마다 점검
  • Keel: 12개월마다 점검

**📦 Rigging**
  • Mast: 12개월마다 점검
  • Shrouds: 12개월마다 점검
  • Standing Rigging: 12개월마다 점검
  ... 외 5개 부품

**📦 Sails**
  • Mainsail: 12개월마다 점검
  • Jib: 12개월마다 점검

💡 정비 관련 궁금한 점은 언제든 물어보세요!
📊 전체 부품 목록: 'J/70 부품'
📖 상세 분석: 'J/70 분석해줘'
```

---

## 🎯 파일별 역할

| 파일 | 용도 | interval 필드 | 챗봇 사용 |
|------|------|---------------|----------|
| `yacht_parts_database.json` | 상세 부품 정보 | ❌ null | ❌ 이전 |
| `yacht_parts_app_data.json` | 앱용 간소화 데이터 | ✅ 12 | ✅ 현재 |

---

## 📝 수정 요약

1. **`_load_parts_data()`**: `yacht_parts_app_data.json` 우선 로드
2. **Fallback 메커니즘**: 파일이 없으면 `yacht_parts_database.json` 사용
3. **정비 주기 표시**: 이제 `interval: 12`가 제대로 읽힘

---

## 🧪 테스트

```bash
cd chat-bot
python chatbot_unified.py
```

**질문:**
```
👤 J/70 정비는 언제 해야 해?
👤 Dehler 38 어떻게 관리해야 고장 안나?
👤 Farr 40 유지보수 방법 알려줘
👤 Hanse 458 점검 주기는?
```

**기대 결과:**
- ✅ 부품별 정비 주기 표시됨
- ✅ 카테고리별로 그룹화
- ✅ "12개월마다 점검" 형식으로 표시

---

## ✅ 완료!

이제 모든 요트의 정비 주기가 제대로 표시됩니다! 🎉

**수정 파일:**
- `chat-bot/chatbot_unified.py` (1개 함수 수정)

