# 새로운 요트 등록 API 가이드

## 개요

20종의 기본 요트가 아닌 사용자 정의 요트를 등록하는 API입니다. 요트의 기본 정보와 상세 스펙을 모두 저장할 수 있습니다.

## API 엔드포인트

### 1. 새로운 요트 등록 (상세 스펙 포함)

**Endpoint:** `POST /api/yacht/with-specs`

**Authentication:** Required (JWT Token)

**Request Body:**

```json
{
  "basicInfo": {
    "name": "My Custom Yacht",
    "nickName": "Sea Breeze",
    "manufacturer": "Custom Yachts Inc.",
    "type": "Cruiser Racer",
    "year": "2024",
    "designer": "John Smith",
    "manual": "data/yachtpdf/my-custom-yacht-manual.pdf"
  },
  "specifications": {
    "dimensions": {
      "loa": 15.5,
      "lwl": 13.2,
      "beam": 4.5,
      "draft": 2.8,
      "displacement": 8500.0,
      "mastHeight": 22.0
    },
    "sailArea": {
      "mainSailArea": 65.0,
      "jibSailArea": 45.0,
      "spinnakerSailArea": 150.0,
      "totalSailArea": 110.0
    },
    "engine": {
      "type": "Inboard",
      "power": "40 HP",
      "model": "Yanmar 4JH40"
    },
    "hull": {
      "hullMaterial": "GRP",
      "deckMaterial": "GRP with teak deck",
      "keelType": "Fin keel with bulb"
    },
    "accommodations": {
      "berths": 6,
      "cabins": 3,
      "heads": 2
    },
    "capacity": {
      "fuelCapacity": 200.0,
      "waterCapacity": 400.0
    },
    "performance": {
      "maxSpeed": 9.5,
      "cruisingSpeed": 7.0
    },
    "ceCertification": "Category A",
    "description": "A comfortable cruiser-racer designed for long-distance sailing",
    "features": "GPS, Autopilot, Bow thruster, Solar panels"
  }
}
```

**Response (Success):**

```json
{
  "status": 200,
  "message": "Yacht created successfully",
  "data": {
    "yachtId": 123
  }
}
```

**Response (Error - Validation Failed):**

```json
{
  "status": 400,
  "message": "Validation failed",
  "errors": [
    {
      "field": "basicInfo.name",
      "message": "Name is required"
    }
  ]
}
```

---

### 2. 요트 상세 스펙 조회

**Endpoint:** `GET /api/yacht/{yachtId}/specifications`

**Authentication:** Required (JWT Token)

**Path Parameters:**
- `yachtId` (Long): 요트 ID

**Response (Success):**

```json
{
  "status": 200,
  "message": "success",
  "data": {
    "id": 1,
    "yacht": {
      "id": 123,
      "name": "My Custom Yacht"
    },
    "loa": 15.5,
    "lwl": 13.2,
    "beam": 4.5,
    "draft": 2.8,
    "displacement": 8500.0,
    "mastHeight": 22.0,
    "mainSailArea": 65.0,
    "jibSailArea": 45.0,
    "spinnakerSailArea": 150.0,
    "totalSailArea": 110.0,
    "engineType": "Inboard",
    "enginePower": "40 HP",
    "engineModel": "Yanmar 4JH40",
    "hullMaterial": "GRP",
    "deckMaterial": "GRP with teak deck",
    "keelType": "Fin keel with bulb",
    "berths": 6,
    "cabins": 3,
    "heads": 2,
    "fuelCapacity": 200.0,
    "waterCapacity": 400.0,
    "maxSpeed": 9.5,
    "cruisingSpeed": 7.0,
    "ceCertification": "Category A",
    "description": "A comfortable cruiser-racer designed for long-distance sailing",
    "features": "GPS, Autopilot, Bow thruster, Solar panels"
  }
}
```

---

## 필드 설명

### basicInfo (필수)

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| name | String | ✅ | 요트 이름 |
| nickName | String | ❌ | 요트 별명 |
| manufacturer | String | ❌ | 제조사 |
| type | String | ❌ | 요트 타입 (예: Racing, Cruiser, Cruiser Racer) |
| year | String | ❌ | 제조년도 |
| designer | String | ❌ | 설계자 |
| manual | String | ❌ | 매뉴얼 PDF 파일 경로 |

### specifications (선택)

모든 필드는 선택사항입니다.

#### dimensions (치수)
- `loa` (Double): Length Overall - 전장 (m)
- `lwl` (Double): Length Waterline - 수선장 (m)
- `beam` (Double): Beam - 폭 (m)
- `draft` (Double): Draft - 흘수 (m)
- `displacement` (Double): Displacement - 배수량 (kg)
- `mastHeight` (Double): Mast Height - 마스트 높이 (m)

#### sailArea (돛 면적)
- `mainSailArea` (Double): Main Sail Area - 메인세일 면적 (m²)
- `jibSailArea` (Double): Jib Sail Area - 집세일 면적 (m²)
- `spinnakerSailArea` (Double): Spinnaker Sail Area - 스피네이커 면적 (m²)
- `totalSailArea` (Double): Total Sail Area - 총 면적 (m²)

#### engine (엔진)
- `type` (String): Engine Type - 엔진 타입 (예: Inboard, Outboard)
- `power` (String): Engine Power - 엔진 출력 (예: "40 HP")
- `model` (String): Engine Model - 엔진 모델

#### hull (선체)
- `hullMaterial` (String): Hull Material - 선체 재질 (예: GRP, Carbon Fiber)
- `deckMaterial` (String): Deck Material - 데크 재질
- `keelType` (String): Keel Type - 킬 타입 (예: Fin, Bulb)

#### accommodations (수용 시설)
- `berths` (Integer): Number of Berths - 침대 수
- `cabins` (Integer): Number of Cabins - 객실 수
- `heads` (Integer): Number of Heads - 화장실 수

#### capacity (용량)
- `fuelCapacity` (Double): Fuel Capacity - 연료 탱크 용량 (liters)
- `waterCapacity` (Double): Water Capacity - 물 탱크 용량 (liters)

#### performance (성능)
- `maxSpeed` (Double): Max Speed - 최대 속도 (knots)
- `cruisingSpeed` (Double): Cruising Speed - 순항 속도 (knots)

#### 추가 정보
- `ceCertification` (String): CE Certification - CE 인증 (예: "Category A")
- `description` (String): Description - 설명 (최대 2000자)
- `features` (String): Features - 특징 (최대 2000자)

---

## 최소 요청 예제 (기본 정보만)

```json
{
  "basicInfo": {
    "name": "My Yacht"
  }
}
```

이 경우 요트의 이름만 등록되며, 다른 모든 정보는 null로 저장됩니다.

---

## 완전한 요청 예제

```json
{
  "basicInfo": {
    "name": "Beneteau Oceanis 51.1",
    "nickName": "Ocean Star",
    "manufacturer": "Beneteau",
    "type": "Cruiser",
    "year": "2024",
    "designer": "Berret-Racoupeau Yacht Design",
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
    "description": "The Oceanis 51.1 is a luxury cruising yacht with exceptional comfort and performance. Perfect for long-distance cruising with family or friends.",
    "features": "Bow thruster, Generator, Air conditioning, Heating, Full navigation system, Autopilot, Solar panels, Water maker"
  }
}
```

---

## 데이터 저장

요트 등록 시 다음 두 곳에 데이터가 저장됩니다:

1. **데이터베이스 (MySQL/PostgreSQL)**
   - `yacht` 테이블: 기본 정보
   - `yacht_specification` 테이블: 상세 스펙

2. **JSON 파일**
   - `backend/data/yacht_specifications.json`
   - 20종 기본 요트와 동일한 형식으로 저장
   - 챗봇 및 다른 시스템에서 활용 가능

---

## 주의사항

1. **인증 필수**: 모든 API 호출 시 JWT 토큰이 필요합니다.
2. **권한 확인**: 요트 조회 시 해당 사용자가 해당 요트에 대한 접근 권한이 있어야 합니다.
3. **필수 필드**: `basicInfo.name`은 반드시 입력해야 합니다.
4. **선택 필드**: `specifications`는 전체를 생략하거나, 필요한 부분만 입력할 수 있습니다.
5. **JSON 파일**: JSON 파일 저장 실패 시에도 데이터베이스에는 정상적으로 저장됩니다.

---

## cURL 예제

```bash
curl -X POST http://localhost:8080/api/yacht/with-specs \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "basicInfo": {
      "name": "My Custom Yacht",
      "manufacturer": "Custom Yachts Inc.",
      "type": "Cruiser Racer",
      "year": "2024"
    },
    "specifications": {
      "dimensions": {
        "loa": 15.5,
        "beam": 4.5,
        "draft": 2.8
      },
      "sailArea": {
        "mainSailArea": 65.0,
        "jibSailArea": 45.0
      }
    }
  }'
```

---

## Postman 테스트

1. **Headers 설정:**
   - `Content-Type`: `application/json`
   - `Authorization`: `Bearer YOUR_JWT_TOKEN`

2. **Body 설정:**
   - `raw` 선택
   - `JSON` 타입 선택
   - 위의 예제 JSON 입력

3. **Send** 클릭

---

## 에러 코드

| 상태 코드 | 설명 |
|----------|------|
| 200 | 성공 |
| 400 | 잘못된 요청 (Validation 실패) |
| 401 | 인증 실패 (JWT 토큰 없음 또는 만료) |
| 403 | 권한 없음 |
| 404 | 요트를 찾을 수 없음 |
| 500 | 서버 내부 오류 |

---

## 다음 단계

요트 등록 후:
1. 요트에 파트 추가: `POST /api/part`
2. 요트에 사용자 초대: `POST /api/yacht/invite`
3. 요트 정보 수정: `PUT /api/yacht`
4. 요트 상세 스펙 조회: `GET /api/yacht/{yachtId}/specifications`

