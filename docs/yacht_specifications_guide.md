# 요트 스펙 데이터베이스 가이드

## 📁 파일 위치

- **메인 파일**: `backend/data/yacht_specifications.json`
- **부품 데이터베이스**: `backend/data/yacht_parts_database.json`

## 📊 포함된 데이터

### 요트 스펙 데이터베이스 (yacht_specifications.json)

**총 20종 세일링 요트의 완전한 스펙 정보**

#### 포함 정보:
1. **기본 정보**
   - 요트 이름 (name)
   - 제조사 (manufacturer)
   - 타입 (type): Racing, Cruiser, Cruiser/Racer, Dinghy
   - 디자이너 (designer)
   - 제조 연도 (year)

2. **치수 정보 (dimensions)**
   - LOA (Length Overall) - 전체 길이
   - LWL (Length Waterline) - 수선 길이
   - Beam - 폭
   - Draft - 흘수
   - Displacement - 배수량
   - Mast Height - 마스트 높이

3. **돛 면적 (sailArea)**
   - Main sail - 메인 세일
   - Jib/Genoa - 집/제노아
   - Spinnaker - 스피네이커
   - Total - 총 면적

4. **엔진 (engine)**
   - 타입 (type): Inboard/Outboard
   - 출력 (power): HP
   - 모델 (model)

5. **탱크 용량 (tanks)**
   - Fuel tank - 연료 탱크
   - Water tank - 물 탱크

6. **수용 인원 (accommodation)**
   - Cabins - 선실 수
   - Berths - 침대 수
   - Heads - 화장실 수
   - Crew - 승무원

## 📋 요트 목록 (20종)

### 레이싱 요트 (9개)
1. **FarEast 28** - One-Design Racing (8.53m)
2. **Farr 40** - One-Design Racing (12.19m)
3. **J/24** - One-Design Racing (7.32m)
4. **Swan 50** - One-Design Racing/Cruiser (16.10m)
5. **X-35** - One-Design Racing/Cruiser (10.60m)
6. **Melges 32** - One-Design Racing (9.75m)
7. **TP52** - Grand Prix Racing (15.85m)
8. **RS21** - One-Design Keelboat (6.40m)
9. **J/70** - One-Design Sportboat (6.91m)

### 크루저 (3개)
10. **Beneteau 473** - Cruiser/Racer (14.40m)
11. **Beneteau Oceanis 46** - Cruiser (14.60m)
12. **Hanse 458** - Cruiser (14.05m)

### 크루저/레이서 (7개)
13. **Beneteau First 36** - Performance Cruiser/Racer (11.35m)
14. **Jeanneau Sun Fast 3300** - Performance Cruiser/Racer (10.10m)
15. **Dehler 38** - Performance Cruiser (11.38m)
16. **X-Yachts XP 44** - Performance Racing/Cruiser (13.50m)
17. **Nautor Swan 48** - Performance Cruiser (14.90m)
18. **Grand Soleil 42 LC** - Performance Cruiser (12.99m)
19. **Solaris 44** - Performance Cruiser (13.40m)

### 딩기 (1개)
20. **Laser (ILCA)** - One-Design Dinghy (4.23m)

## 💡 사용 예시

### Python에서 불러오기
```python
import json

# 요트 스펙 불러오기
with open('backend/data/yacht_specifications.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 특정 요트 찾기
for yacht in data['yachts']:
    if yacht['id'] == 'fareast-28':
        print(f"Name: {yacht['name']}")
        print(f"LOA: {yacht['dimensions']['loa']['display']}")
        print(f"Displacement: {yacht['dimensions']['displacement']['display']}")
        print(f"Sail Area: {yacht['sailArea']['total']['display']}")
```

### JavaScript/TypeScript에서 사용
```typescript
import yachtSpecs from './backend/data/yacht_specifications.json';

// 모든 레이싱 요트 가져오기
const racingYachts = yachtSpecs.yachts.filter(
  yacht => yachtSpecs.categories.racing.includes(yacht.id)
);

// 특정 크기 범위의 요트 찾기
const mediumYachts = yachtSpecs.yachts.filter(
  yacht => yacht.dimensions.loa.value >= 10 && yacht.dimensions.loa.value <= 15
);
```

### Java/Spring Boot에서 사용
```java
@Service
public class YachtSpecificationService {
    
    @Value("classpath:data/yacht_specifications.json")
    private Resource yachtSpecsResource;
    
    public List<YachtSpecification> loadYachtSpecs() throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        JsonNode root = mapper.readTree(yachtSpecsResource.getInputStream());
        // Parse and return yacht specifications
    }
}
```

## 📈 통계

| 항목 | 값 |
|-----|-----|
| **총 요트 수** | 20개 |
| **레이싱 요트** | 9개 (45%) |
| **크루저** | 3개 (15%) |
| **크루저/레이서** | 7개 (35%) |
| **딩기** | 1개 (5%) |
| **평균 상세 스펙/요트** | 14.6개 |

## 🔧 관련 스크립트

### 1. extract_yacht_specifications.py
- PDF 매뉴얼에서 자동으로 스펙 추출
- pdfplumber 사용
- 기본 스펙 템플릿 생성

### 2. create_complete_yacht_specs.py
- 완전한 요트 스펙 데이터베이스 생성
- 수동으로 검증된 정확한 데이터
- 실행: `python scripts/create_complete_yacht_specs.py`

## 📝 데이터 구조

```json
{
  "version": "1.0",
  "description": "20종 세일링 요트 완전한 스펙 데이터베이스",
  "lastUpdated": "2024-11-13",
  "totalYachts": 20,
  "categories": {
    "racing": [...],
    "cruiser": [...],
    "cruiserRacer": [...],
    "dinghy": [...]
  },
  "yachts": [
    {
      "id": "fareast-28",
      "name": "FarEast 28",
      "manufacturer": "FarEast Yachts",
      "type": "One-Design Racing",
      "year": "1992-Present",
      "designer": "Tom Schnackenberg",
      "manual": "data/yachtpdf/...",
      "dimensions": { ... },
      "sailArea": { ... },
      "engine": { ... },
      "tanks": { ... },
      "accommodation": { ... }
    },
    ...
  ]
}
```

## 🔄 업데이트 방법

1. **스크립트 수정**: `backend/scripts/create_complete_yacht_specs.py`
2. **데이터 수정**: `YACHT_SPECIFICATIONS` 리스트 편집
3. **재생성**: `python scripts/create_complete_yacht_specs.py`
4. **커밋**: Git에 추가 및 커밋

## 📚 추가 정보

- 모든 측정값은 미터법(m, kg, l) 및 제곱미터(m²) 사용
- 각 필드에 `display` 값이 포함되어 UI 표시에 최적화
- PDF 매뉴얼 경로가 `manual` 필드에 포함됨
- 부품 데이터베이스(`yacht_parts_database.json`)와 연계 가능

## 🎯 다음 단계

1. Spring Boot Entity 클래스 생성
2. Repository 및 Service 구현
3. REST API 엔드포인트 개발
4. Frontend와 연동
5. 데이터베이스에 import

---

**Last Updated**: 2024-11-13  
**Version**: 1.0  
**Maintained by**: Yacht Management Team



