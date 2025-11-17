# 새로운 요트 등록 기능 구현 요약

## 📋 개요

20종의 기본 요트가 아닌 **사용자 정의 요트**를 등록할 수 있는 완전한 시스템을 구현했습니다.

---

## 🎯 구현된 기능

### 1. 요트 기본 정보 확장
- 제조사 (manufacturer)
- 타입 (type) - Racing, Cruiser, Cruiser Racer 등
- 제조년도 (year)
- 설계자 (designer)
- 매뉴얼 경로 (manual)
- 별명 (nickName)

### 2. 요트 상세 스펙 관리
- **치수 (Dimensions)**: LOA, LWL, Beam, Draft, Displacement, Mast Height
- **돛 면적 (Sail Area)**: Main, Jib, Spinnaker, Total
- **엔진 (Engine)**: Type, Power, Model
- **선체 (Hull)**: Hull Material, Deck Material, Keel Type
- **수용 시설 (Accommodations)**: Berths, Cabins, Heads
- **용량 (Capacity)**: Fuel, Water
- **성능 (Performance)**: Max Speed, Cruising Speed
- **추가 정보**: CE Certification, Description, Features

### 3. 이중 저장 시스템
- **데이터베이스**: 관계형 DB에 정규화된 형태로 저장
- **JSON 파일**: `yacht_specifications.json`에 20종 요트와 동일한 형식으로 저장

---

## 🗂️ 생성된 파일들

### 엔티티 (Entity)
```
backend/src/main/java/HooYah/Yacht/yacht/domain/
├── Yacht.java                    ✅ 확장 (manufacturer, type 등 추가)
└── YachtSpecification.java       ✨ 신규 (상세 스펙 저장)
```

### DTO (Data Transfer Object)
```
backend/src/main/java/HooYah/Yacht/yacht/dto/request/
└── CreateYachtWithSpecsDto.java  ✨ 신규 (요트 + 스펙 등록)
    ├── YachtBasicInfo
    ├── YachtSpecificationInfo
    ├── DimensionsDto
    ├── SailAreaDto
    ├── EngineDto
    ├── HullDto
    ├── AccommodationsDto
    ├── CapacityDto
    └── PerformanceDto
```

### Repository
```
backend/src/main/java/HooYah/Yacht/yacht/repository/
├── YachtRepository.java                  ✅ 기존
└── YachtSpecificationRepository.java     ✨ 신규
```

### Service
```
backend/src/main/java/HooYah/Yacht/yacht/service/
├── YachtService.java                     ✅ 기존
└── YachtSpecificationService.java        ✨ 신규
```

### Controller
```
backend/src/main/java/HooYah/Yacht/yacht/controller/
└── YachtController.java                  ✅ 확장 (2개 API 추가)
```

### 문서
```
backend/docs/
├── API_NEW_YACHT_REGISTRATION.md         ✨ 신규 (API 가이드)
└── NEW_YACHT_REGISTRATION_SUMMARY.md     ✨ 신규 (구현 요약)
```

---

## 🔌 API 엔드포인트

### 1. 새로운 요트 등록
```
POST /api/yacht/with-specs
```
- **기능**: 요트 기본 정보 + 상세 스펙 등록
- **저장**: DB + JSON 파일
- **응답**: 생성된 요트 ID

### 2. 요트 상세 스펙 조회
```
GET /api/yacht/{yachtId}/specifications
```
- **기능**: 특정 요트의 상세 스펙 조회
- **권한**: 해당 요트에 접근 권한이 있는 사용자만

---

## 💾 데이터베이스 스키마

### yacht 테이블 (확장)
```sql
CREATE TABLE yacht (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    nick_name VARCHAR(255),
    manufacturer VARCHAR(255),
    type VARCHAR(255),
    production_year VARCHAR(50),
    designer VARCHAR(255),
    manual_path VARCHAR(500)
);
```

### yacht_specification 테이블 (신규)
```sql
CREATE TABLE yacht_specification (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    yacht_id BIGINT NOT NULL,
    
    -- Dimensions
    loa DOUBLE,
    lwl DOUBLE,
    beam DOUBLE,
    draft DOUBLE,
    displacement DOUBLE,
    mast_height DOUBLE,
    
    -- Sail Area
    main_sail_area DOUBLE,
    jib_sail_area DOUBLE,
    spinnaker_sail_area DOUBLE,
    total_sail_area DOUBLE,
    
    -- Engine
    engine_type VARCHAR(100),
    engine_power VARCHAR(100),
    engine_model VARCHAR(100),
    
    -- Hull
    hull_material VARCHAR(100),
    deck_material VARCHAR(100),
    keel_type VARCHAR(100),
    
    -- Accommodations
    berths INT,
    cabins INT,
    heads INT,
    
    -- Capacity
    fuel_capacity DOUBLE,
    water_capacity DOUBLE,
    
    -- Performance
    max_speed DOUBLE,
    cruising_speed DOUBLE,
    
    -- Additional
    ce_certification VARCHAR(50),
    description TEXT(2000),
    features TEXT(2000),
    
    FOREIGN KEY (yacht_id) REFERENCES yacht(id)
);
```

---

## 📝 사용 예제

### 최소 요청 (이름만)
```json
{
  "basicInfo": {
    "name": "My Yacht"
  }
}
```

### 완전한 요청 (모든 스펙)
```json
{
  "basicInfo": {
    "name": "Beneteau Oceanis 51.1",
    "nickName": "Ocean Star",
    "manufacturer": "Beneteau",
    "type": "Cruiser",
    "year": "2024",
    "designer": "Berret-Racoupeau",
    "manual": "data/yachtpdf/oceanis-51-manual.pdf"
  },
  "specifications": {
    "dimensions": {
      "loa": 15.94,
      "lwl": 14.50,
      "beam": 4.80,
      "draft": 2.30,
      "displacement": 15400.0,
      "mastHeight": 23.50
    },
    "sailArea": {
      "mainSailArea": 75.0,
      "jibSailArea": 52.0,
      "spinnakerSailArea": 180.0,
      "totalSailArea": 127.0
    },
    "engine": {
      "type": "Inboard Diesel",
      "power": "80 HP",
      "model": "Yanmar 4JH80"
    },
    "hull": {
      "hullMaterial": "GRP",
      "deckMaterial": "GRP with teak deck",
      "keelType": "Deep draft fin keel"
    },
    "accommodations": {
      "berths": 10,
      "cabins": 5,
      "heads": 3
    },
    "capacity": {
      "fuelCapacity": 240.0,
      "waterCapacity": 730.0
    },
    "performance": {
      "maxSpeed": 10.0,
      "cruisingSpeed": 8.0
    },
    "ceCertification": "Category A",
    "description": "Luxury cruising yacht",
    "features": "Bow thruster, Generator, Autopilot"
  }
}
```

---

## 🔄 데이터 흐름

```
사용자 요청
    ↓
YachtController
    ↓
YachtSpecificationService
    ├─→ Yacht 엔티티 생성 & 저장
    ├─→ YachtUser 연결
    ├─→ YachtSpecification 엔티티 생성 & 저장
    └─→ yacht_specifications.json 파일 업데이트
    ↓
응답 (요트 ID)
```

---

## ✅ 주요 특징

### 1. 유연한 입력
- 필수 필드: `name`만
- 선택 필드: 나머지 모든 스펙은 선택사항
- 부분 입력 가능: 필요한 정보만 입력 가능

### 2. 이중 저장
- **DB**: 빠른 조회, 관계형 데이터 관리
- **JSON**: 챗봇 통합, 데이터 백업, 호환성

### 3. JSON 형식 호환
- 20종 기본 요트와 동일한 JSON 구조
- 챗봇이 자동으로 인식 가능
- 기존 시스템과 완벽 호환

### 4. 권한 관리
- 요트 등록 시 자동으로 사용자 연결
- 조회 시 권한 확인
- 다른 사용자 초대 기능 지원

---

## 🔐 보안

### 인증 (Authentication)
- JWT 토큰 기반 인증
- 모든 API 호출 시 필수

### 권한 (Authorization)
- 요트 소유자만 조회/수정 가능
- 초대된 사용자도 접근 가능

---

## 🧪 테스트 방법

### 1. Postman
```
POST http://localhost:8080/api/yacht/with-specs
Headers:
  - Content-Type: application/json
  - Authorization: Bearer YOUR_JWT_TOKEN
Body: (위의 예제 JSON 참조)
```

### 2. cURL
```bash
curl -X POST http://localhost:8080/api/yacht/with-specs \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d @request.json
```

### 3. Frontend 통합
```javascript
const response = await fetch('/api/yacht/with-specs', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify(yachtData)
});

const result = await response.json();
console.log('Created yacht ID:', result.data.yachtId);
```

---

## 📊 JSON 파일 예시

등록된 요트는 `yacht_specifications.json`에 다음과 같이 저장됩니다:

```json
{
  "version": "1.0",
  "totalYachts": 21,
  "yachts": [
    // ... 기존 20종 요트 ...
    {
      "id": "my-custom-yacht",
      "name": "My Custom Yacht",
      "manufacturer": "Custom Yachts Inc.",
      "type": "Cruiser Racer",
      "year": "2024",
      "designer": "John Smith",
      "manual": "data/yachtpdf/my-custom-yacht-manual.pdf",
      "dimensions": {
        "loa": {
          "value": 15.5,
          "unit": "m"
        },
        "beam": {
          "value": 4.5,
          "unit": "m"
        }
        // ... 기타 치수
      },
      "sailArea": {
        "main": {
          "value": 65.0,
          "unit": "m²"
        }
        // ... 기타 돛 면적
      }
      // ... 기타 스펙
    }
  ]
}
```

---

## 🎯 활용 사례

### 1. 개인 요트 등록
- 사용자가 자신의 요트 정보를 등록
- 상세 스펙을 기록하여 관리

### 2. 중고 요트 거래
- 판매자가 요트 정보 등록
- 구매자가 상세 스펙 확인

### 3. 요트 클럽 관리
- 클럽 소유 요트 등록
- 회원들과 정보 공유

### 4. 챗봇 통합
- 등록된 요트에 대해 챗봇이 질문 응답
- PDF 매뉴얼 자동 연결

---

## 🚀 향후 개선 사항

1. **이미지 업로드**
   - 요트 사진 등록
   - 다중 이미지 지원

2. **스펙 수정 API**
   - `PUT /api/yacht/{yachtId}/specifications`
   - 등록 후 스펙 수정 가능

3. **스펙 검증**
   - 현실적인 값 범위 체크
   - 단위 자동 변환

4. **검색 및 필터링**
   - 스펙 기반 요트 검색
   - 범위 필터링 (예: LOA 10-15m)

5. **비교 기능**
   - 여러 요트 스펙 비교
   - 그래프로 시각화

---

## 📚 참고 문서

- [API 상세 가이드](API_NEW_YACHT_REGISTRATION.md)
- [기존 요트 데이터 구조](yacht_specifications_guide.md)
- [Backend README](README.md)

---

## 💡 문의

구현 관련 질문이나 개선 사항이 있으면 이슈를 등록해주세요!

