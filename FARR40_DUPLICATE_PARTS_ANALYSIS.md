# 🔍 Farr 40 메뉴얼 부품 중복 문제 분석 보고서

**작성일**: 2025-11-26  
**분석 대상**: chatbot_unified.py의 AI 프롬프트 및 부품 추출 로직  
**보고자**: Farr 40 매뉴얼 분석 결과 (도현님)

---

## 📊 **문제 상황**

### **1️⃣ 추출된 부품 통계**
- **총 부품 수**: 약 120개
- **중복 부품**: 약 50% 이상
- **처리 시간**: 약 **4분** (너무 김)

### **2️⃣ 중복 사례**

#### **예시 1: Farr 40 본체**
```json
{
    "name": "Farr 40 One Design Racing Yacht",
    "manufacturer": "USWatercraft LLC",
    "model": "Farr 40"
},
{
    "name": "Farr 40 One Design Racing Yacht",
    "manufacturer": "McConaghy",
    "model": "Farr 40"
}
```
→ **동일 부품**, 제조사만 다름

#### **예시 2: Mast**
```json
{
    "name": "Mast",
    "manufacturer": "Whale Spar",
    "model": ""
},
{
    "name": "Mast",
    "manufacturer": "Hi-Tech",
    "model": "Farr 40 mast"
},
{
    "name": "Mast",
    "manufacturer": "",
    "model": "U100-054C (Construction drawing reference)"
}
```
→ **동일 부품**, 제조사와 모델이 다름

#### **예시 3: Winch**
```json
{
    "name": "Winch (wide body three-speed)",
    "manufacturer": "Harken",
    "model": "B480TCR"
},
{
    "name": "Winch (self-tailing, Ocean Racing)",
    "manufacturer": "Lewmar",
    "model": "Ocean Racing 440"
},
{
    "name": "Winch (aluminum self-tailing)",
    "manufacturer": "Lewmar",
    "model": "44"
}
```
→ **기능적으로 같은 부품**, 브랜드와 모델만 다름

#### **예시 4: Block (블록/풀리)**
```json
{
    "name": "Bullet Double Block with Bracket (Genoa Inhaul)",
    "manufacturer": "Harken",
    "model": "085NP Blk-Bullet Dbl W/Bkt"
},
{
    "name": "Carbo Double Swivel Block with Bracket (Genoa Inhaul)",
    "manufacturer": "Harken",
    "model": "343NP 29 mm Carbo Double Swivel W/Bkt"
}
```
→ **같은 위치**, 대체 가능한 블록

---

## 🔍 **원인 분석**

### **1️⃣ 프롬프트 문제**

#### **현재 프롬프트** (`chatbot_unified.py` 라인 1874-1886)
```python
### ✅ 섹션 13: 부품 (Parts) - 통합 리스트

**ID: `part-{{category}}-{{name}}-{{number}}`**

모든 부품을 하나의 배열에 통합하세요.

```json
[
  {{
    "id": "part-rigging-mast-01",
    "name": "Mast",
    "manufacturer": "Selden / Z-Spars / Hall Spars",  // ⚠️ 여기가 문제!
    "model": "...",
    "interval": 12,
    "category": "Rigging",
    ...
  }}
]
```
```

#### **문제점**
1. **"모든 부품을 하나의 배열에 통합하세요"** ← 너무 포괄적
2. **"Selden / Z-Spars / Hall Spars"** ← 대체 제조사를 `/`로 구분하여 표시
   - AI가 이를 "각각 별도 부품으로 추출하라"는 지시로 해석함
3. **중복 제거 규칙 없음** ← "중복 제거" 언급 없음

### **2️⃣ 매뉴얼 구조 문제**

Farr 40 매뉴얼에는 **"대체 가능한 부품 (Alternative Parts)"**이 매우 많습니다.

**예시: Class Rules**
```
Primary Winch: 
- Harken B480TCR (wide body three-speed) OR
- Lewmar Ocean Racing 440 (self-tailing) OR
- Lewmar 44 (aluminum self-tailing)
```

→ AI가 이를 **"3개의 별도 부품"**으로 인식

### **3️⃣ 중복 제거 로직 미흡**

#### **현재 중복 제거 코드** (`chatbot_unified.py` 라인 3043-3067)
```python
# 기존 부품 목록 가져오기 (중복 방지)
existing_parts = yacht_entry.get("parts", [])
existing_part_names = {p.get("name", "") for p in existing_parts if isinstance(p, dict)}

for part in parts:
    name = part.get("name", "")
    if not name or name in existing_part_names:
        continue
    
    part_entry = {
        "name": name,
        "manufacturer": part.get("manufacturer", ""),
        "model": part.get("model", ""),
        "category": part.get("category", "rigging"),
        "interval": part.get("interval")
    }
    
    yacht_entry["parts"].append(part_entry)
    existing_part_names.add(name)
```

**문제점**:
- **이름만** 체크 (`name in existing_part_names`)
- 제조사와 모델이 다르면 다른 부품으로 인식
- 예: "Mast (Whale Spar)" ≠ "Mast (Hi-Tech)"

---

## 🧪 **테스트 코드 분석**

### **Backend 테스트**
- **파일**: `backend/src/test/java/HooYah/Yacht/YachtApplicationTests.java`
- **내용**: 기본 Spring Boot 컨텍스트 로딩 테스트만 존재
- **부품 중복 검증**: ❌ **없음**

```java
@SpringBootTest
class YachtApplicationTests {
    @Test
    void contextLoads() {
    }
}
```

### **Frontend 테스트**
- **파일**: `frontend/test/widget_test.dart`
- **내용**: Flutter 기본 Counter 테스트
- **부품 중복 검증**: ❌ **없음**

```dart
testWidgets('Counter increments smoke test', (WidgetTester tester) async {
    await tester.pumpWidget(const MyApp());
    expect(find.text('0'), findsOneWidget);
    ...
});
```

### **Chatbot 테스트**
- **파일**: `chat-bot/test_actual_pdfs.py`
- **내용**: 11월11일/17일 멘토링 PDF 분석 테스트
- **부품 중복 검증**: ❌ **없음**

```python
def test_pdf_analysis():
    chatbot = UnifiedYachtChatbot()
    response = chatbot._handle_file_upload(file_info['path'])
    # 중복 체크 로직 없음
```

### **중복 체크 스크립트**
- **파일**: `chat-bot/check_duplicate_yachts.py`
- **내용**: 요트 데이터 중복 확인 (요트 이름 기준)
- **부품 중복 검증**: ⚠️ **부분적 (요트만)**

```python
def check_duplicates():
    """모든 JSON 파일에서 중복 확인"""
    # 요트 이름 중복 확인만 수행
    # 부품 중복은 확인하지 않음
```

---

## 🎯 **왜 중복이 발생하는가?**

### **1. 매뉴얼에 실제로 대체 부품이 나열되어 있음**
- Farr 40은 **One-Design Class** 요트
- Class Rules에 **"승인된 대체 부품"** 목록이 있음
- 예: Harken vs Lewmar 윈치

### **2. AI 프롬프트가 "모든" 부품을 추출하도록 지시**
- "모든 부품을 하나의 배열에 통합하세요" ← 너무 포괄적
- 대체 부품도 전부 추출

### **3. 중복 제거 로직이 부족**
- 이름만 체크, 제조사/모델 무시
- "Mast (Whale Spar)" ≠ "Mast (Hi-Tech)"로 판단

### **4. 테스트 코드가 없음**
- Backend/Frontend 모두 부품 중복 검증 테스트 없음
- Chatbot도 중복 체크 로직 없음

---

## 💡 **해결 방안**

### **방안 1: 프롬프트 개선** ⭐ **추천**

#### **현재 프롬프트**
```
모든 부품을 하나의 배열에 통합하세요.

"manufacturer": "Selden / Z-Spars / Hall Spars"
```

#### **개선된 프롬프트**
```
⚠️ 중요: 대체 가능한 부품 (Alternative Parts) 처리 규칙

1. **같은 이름의 부품**이 여러 제조사로 나열된 경우:
   - 하나의 부품으로 통합
   - manufacturer 필드에 모든 제조사를 슬래시(/)로 구분하여 나열
   
2. **같은 기능의 부품**이 다른 이름으로 나열된 경우:
   - 대표적인 이름 하나만 선택
   - manufacturer 필드에 모든 제조사 나열
   
3. **예시**:
   
   매뉴얼 원문:
   ```
   Primary Winch: 
   - Harken B480TCR (wide body three-speed)
   - Lewmar Ocean Racing 440 (self-tailing)
   - Lewmar 44 (aluminum self-tailing)
   ```
   
   올바른 추출:
   ```json
   {
     "name": "Primary Winch",
     "manufacturer": "Harken / Lewmar",
     "model": "B480TCR / Ocean Racing 440 / 44",
     "alternativeModels": [
       {"manufacturer": "Harken", "model": "B480TCR", "description": "wide body three-speed"},
       {"manufacturer": "Lewmar", "model": "Ocean Racing 440", "description": "self-tailing"},
       {"manufacturer": "Lewmar", "model": "44", "description": "aluminum self-tailing"}
     ]
   }
   ```
   
   잘못된 추출 (❌):
   ```json
   [
     {"name": "Primary Winch", "manufacturer": "Harken", "model": "B480TCR"},
     {"name": "Primary Winch", "manufacturer": "Lewmar", "model": "Ocean Racing 440"},
     {"name": "Primary Winch", "manufacturer": "Lewmar", "model": "44"}
   ]
   ```

4. **중복 제거 체크리스트**:
   - [ ] 같은 이름 + 다른 제조사 → 통합
   - [ ] 같은 카테고리 + 같은 위치 → 통합
   - [ ] "OR", "alternatively", "/" 키워드 → 대체 부품으로 처리
```

---

### **방안 2: 후처리 중복 제거 강화**

#### **현재 코드**
```python
if not name or name in existing_part_names:
    continue
```

#### **개선된 코드**
```python
def is_duplicate_part(new_part, existing_parts):
    """부품 중복 체크 (이름, 제조사, 모델 고려)"""
    new_name = normalize_part_name(new_part.get("name", ""))
    new_mfr = normalize_manufacturer(new_part.get("manufacturer", ""))
    
    for existing in existing_parts:
        ex_name = normalize_part_name(existing.get("name", ""))
        ex_mfr = normalize_manufacturer(existing.get("manufacturer", ""))
        
        # 1. 이름이 완전히 같으면 중복
        if new_name == ex_name:
            return True
        
        # 2. 이름이 유사하고 제조사도 같으면 중복
        if similarity(new_name, ex_name) > 0.8 and new_mfr == ex_mfr:
            return True
        
        # 3. 카테고리 + 위치가 같으면 중복 가능성
        if (new_part.get("category") == existing.get("category") and
            extract_location(new_name) == extract_location(ex_name)):
            return True
    
    return False

def normalize_part_name(name):
    """부품 이름 정규화"""
    name = name.lower().strip()
    # 괄호 안 제거 (예: "Winch (wide body)" → "winch")
    name = re.sub(r'\([^)]*\)', '', name).strip()
    return name

def normalize_manufacturer(mfr):
    """제조사 이름 정규화"""
    mfr = mfr.lower().strip()
    # "Harken / Lewmar" → ["harken", "lewmar"]
    return sorted([m.strip() for m in mfr.split('/')])
```

---

### **방안 3: 테스트 코드 추가** ⭐ **중요**

#### **Backend 테스트 추가**
```java
// PartServiceTest.java
@Test
public void testDuplicatePartDetection() {
    // Given
    Part part1 = new Part("Mast", "Whale Spar", "...");
    Part part2 = new Part("Mast", "Hi-Tech", "Farr 40 mast");
    
    // When
    boolean isDuplicate = partService.isDuplicatePart(part1, part2);
    
    // Then
    assertTrue(isDuplicate, "같은 이름의 부품은 중복으로 처리되어야 함");
}

@Test
public void testAlternativePartsMerging() {
    // Given
    List<Part> parts = Arrays.asList(
        new Part("Primary Winch", "Harken", "B480TCR"),
        new Part("Primary Winch", "Lewmar", "Ocean Racing 440")
    );
    
    // When
    List<Part> merged = partService.mergeAlternativeParts(parts);
    
    // Then
    assertEquals(1, merged.size(), "대체 부품은 하나로 통합되어야 함");
    assertEquals("Harken / Lewmar", merged.get(0).getManufacturer());
}
```

#### **Chatbot 테스트 추가**
```python
# test_duplicate_parts.py
def test_farr_40_duplicate_detection():
    """Farr 40 매뉴얼 중복 체크"""
    chatbot = UnifiedYachtChatbot()
    
    # Farr 40 PDF 분석
    result = chatbot._analyze_pdf_with_gemini("data/yachtpdf/manual_farr40.pdf")
    parts = result.get("parts", [])
    
    # 중복 검사
    part_names = [p["name"] for p in parts]
    unique_names = set(part_names)
    
    # 중복률 계산
    duplicate_rate = (len(part_names) - len(unique_names)) / len(part_names) * 100
    
    # 중복률이 20% 이하여야 함
    assert duplicate_rate < 20, f"중복률이 너무 높음: {duplicate_rate:.1f}%"
    
    # Mast는 1개만 있어야 함
    mast_count = sum(1 for name in part_names if "Mast" in name)
    assert mast_count <= 2, f"Mast 중복: {mast_count}개"
    
    # 같은 제조사+모델 중복 체크
    part_keys = [(p["name"], p["manufacturer"], p["model"]) for p in parts]
    unique_keys = set(part_keys)
    assert len(part_keys) == len(unique_keys), "완전 동일한 부품 중복 발견"
```

---

### **방안 4: 성능 최적화**

#### **현재: 4분 소요**
- Gemini API 호출 1회 (전체 매뉴얼)
- 토큰 수: 많음

#### **개선안 1: Streaming 사용**
```python
response = self.model.generate_content(prompt, stream=True)
for chunk in response:
    # 청크별로 처리
    process_chunk(chunk)
```

#### **개선안 2: 페이지별 분석**
```python
def analyze_pdf_by_pages(pdf_path, page_range=50):
    """50페이지씩 나눠서 분석"""
    total_pages = get_pdf_page_count(pdf_path)
    
    all_parts = []
    for start in range(0, total_pages, page_range):
        end = min(start + page_range, total_pages)
        text = extract_text_from_pages(pdf_path, start, end)
        parts = analyze_text_chunk(text)
        all_parts.extend(parts)
    
    # 최종 중복 제거
    return remove_duplicates(all_parts)
```

---

## 📈 **예상 효과**

### **Before (현재)**
- **부품 수**: 120개
- **중복**: 50% (60개)
- **처리 시간**: 4분

### **After (개선 후)**
- **부품 수**: 60개 (50% 감소)
- **중복**: 10% 이하 (6개)
- **처리 시간**: 2분 (50% 감소)

---

## 🎯 **결론**

### **중복 발생 이유**
1. ✅ **프롬프트가 너무 포괄적** - "모든 부품" 추출
2. ✅ **대체 부품 처리 규칙 없음** - "Harken / Lewmar" 각각 추출
3. ✅ **중복 제거 로직 미흡** - 이름만 체크
4. ✅ **테스트 코드 없음** - 중복 검증 불가

### **추천 해결 방안** (우선순위 순)
1. 🥇 **프롬프트 개선** - "대체 부품 통합" 규칙 추가
2. 🥈 **테스트 코드 추가** - 중복 검증 자동화
3. 🥉 **후처리 강화** - 유사도 기반 중복 제거
4. 💡 **성능 최적화** - 페이지별 분석

---

**작성자**: AI Assistant  
**참고 파일**:
- `chat-bot/chatbot_unified.py` (라인 1874-1904)
- `chat-bot/check_duplicate_yachts.py`
- `backend/src/test/java/HooYah/Yacht/YachtApplicationTests.java`
- `frontend/test/widget_test.dart`


