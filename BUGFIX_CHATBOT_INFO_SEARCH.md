# 🔧 Chatbot 정보 검색 오류 수정

## 🐛 문제점

사용자가 특정 부품/엔진 정보를 질문했을 때 **"등록된 정보가 없습니다"**라고 잘못 응답하는 문제 발생

### 재현 방법:
```
👤 You: 요트 dehler38 엔진에 알고 싶어.
🤖 AI: 등록된 엔진 정보가 없습니다.  ❌

👤 You: j/24 엔진에 알고 싶어
🤖 AI: 등록된 엔진 정보가 없습니다.  ❌
```

---

## 🔍 원인 분석

### Schema 5.0 JSON 구조:
```json
{
  "yachts": [
    {
      "name": "OCEANIS 46.1",
      "yachtSpecs": {
        "standard": {
          "dimensions": {
            "LOA": "14.60m",
            "Beam": "4.50m"
          },
          "engine": {
            "type": null,
            "power": "59Kw"
          },
          "sailArea": {
            "mainsail": "53.75m²"
          }
        },
        "additional": {
          "nominalMaximumPropulsionPower": "1 x 59Kw"
        }
      },
      "detailedDimensions": {
        "LOA": "14.60m",
        "hullLength": "13.65m"
      }
    }
  ]
}
```

### 기존 코드 (잘못된 경로):
```python
# ❌ 잘못된 코드
def _format_yacht_engine_info(self, yacht: Dict):
    engine = yacht.get('engine', {})  # ← 직접 'engine' 키로 검색
    # → 찾을 수 없음! (실제 경로: yachtSpecs.standard.engine)
```

---

## ✅ 수정 내용

### 1. **엔진 정보 수정** (`_format_yacht_engine_info`)

**수정 전:**
```python
engine = yacht.get('engine', {})
```

**수정 후:**
```python
# Schema 5.0 경로: yachtSpecs.standard.engine
yacht_specs = yacht.get('yachtSpecs', {})
standard_specs = yacht_specs.get('standard', {})
engine = standard_specs.get('engine', {})

# 추가 정보도 확인 (additional에 엔진 정보가 있을 수 있음)
additional_specs = yacht_specs.get('additional', {})

engine_type = engine.get('type') or additional_specs.get('engineType')
engine_power = engine.get('power') or additional_specs.get('nominalMaximumPropulsionPower')
engine_model = engine.get('model')
```

---

### 2. **치수 정보 수정** (`_format_specific_dimension`, `_format_yacht_dimensions`)

**수정 전:**
```python
dim = yacht.get('dimensions', {})
```

**수정 후:**
```python
# Schema 5.0 경로: yachtSpecs.standard.dimensions + detailedDimensions
yacht_specs = yacht.get('yachtSpecs', {})
standard_specs = yacht_specs.get('standard', {})
dim = standard_specs.get('dimensions', {})

# 더 상세한 정보는 detailedDimensions에 있음
detailed_dim = yacht.get('detailedDimensions', {})

# 둘 다 확인
loa = dim.get('LOA') or detailed_dim.get('LOA')
```

---

### 3. **돛 면적 정보 수정** (`_format_yacht_sail_area`)

**수정 전:**
```python
sail_area = yacht.get('sailArea', {})
```

**수정 후:**
```python
# Schema 5.0 경로: yachtSpecs.standard.sailArea
yacht_specs = yacht.get('yachtSpecs', {})
standard_specs = yacht_specs.get('standard', {})
sail_area = standard_specs.get('sailArea', {})

# sailInventory도 확인
sail_inventory = yacht.get('sailInventory', {})
```

---

## 📊 수정 결과

### 수정 후 예상 응답:

```
👤 You: oceanis 46.1 엔진 알려줘
🤖 AI: 🔧 **OCEANIS 46.1 엔진 정보**

**출력**: 59Kw
**권장 엔진 중량**: 2 x 229kg

💡 더 자세한 정보를 원하시면 'OCEANIS 46.1 분석해줘'라고 물어보세요.
```

```
👤 You: oceanis 46.1 크기 알려줘
🤖 AI: 📏 **OCEANIS 46.1 크기 정보**

**기본 치수**
- LOA (전장): 14.60m
- LWL (수선장): 13.65m
- Beam (폭): 4.50m
- Draft (흘수): 1.87m / 2.47m / 2.68m
- Displacement (배수량): 11278kg
- Mast Height (마스트 높이): 20.31m
```

---

## 🔑 핵심 변경사항

### 수정된 함수:
1. ✅ `_format_yacht_engine_info()` - 엔진 정보 검색 경로 수정
2. ✅ `_format_specific_dimension()` - 특정 치수 검색 경로 수정
3. ✅ `_format_yacht_dimensions()` - 전체 치수 검색 경로 수정
4. ✅ `_format_yacht_sail_area()` - 돛 면적 검색 경로 수정

### 검색 경로 업데이트:
| 정보 | 기존 경로 | 새로운 경로 (Schema 5.0) |
|------|-----------|-------------------------|
| 엔진 | `yacht.engine` | `yacht.yachtSpecs.standard.engine` + `additional` |
| 치수 | `yacht.dimensions` | `yacht.yachtSpecs.standard.dimensions` + `detailedDimensions` |
| 돛 | `yacht.sailArea` | `yacht.yachtSpecs.standard.sailArea` + `sailInventory` |

---

## 🧪 테스트 방법

```bash
cd chat-bot
python chatbot_unified.py
```

**테스트 쿼리:**
```
👤 요트 dehler38 엔진 알려줘
👤 j/70 크기 알려줘
👤 oceanis 46.1 돛 면적 알려줘
👤 farr 40 displacement 알려줘
```

---

## ✅ 완료!

이제 사용자가 엔진, 치수, 돛 면적 등을 질문하면 **Schema 5.0 JSON 구조에서 정확하게 정보를 검색**하여 응답합니다! 🎉

**수정 파일:**
- `chat-bot/chatbot_unified.py` (4개 함수 수정)

