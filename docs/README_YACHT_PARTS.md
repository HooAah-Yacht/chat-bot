# 요트 부품 데이터베이스 프로젝트

## 📋 프로젝트 개요

이 프로젝트는 다양한 요트 모델의 부품 정보를 체계적으로 관리하기 위한 JSON 데이터베이스 구조입니다.

## 📁 파일 구조

### 1. `yacht_parts_database.json`

- **목적**: 실제 요트 부품 데이터를 저장하는 메인 데이터베이스
- **구조**:
  - 20개 요트 모델의 기본 정보
  - 각 요트별 부품 카테고리 (hull, deck, rigging, sails, winches, blocks, engine, electrical, plumbing, navigation, interior 등)
  - 공통 부품 카테고리 목록
  - 주요 제조사 목록

### 2. `yacht_manual_resources.json`

- **목적**: 요트 매뉴얼을 찾을 수 있는 리소스 가이드
- **내용**:
  - 각 요트 제조사의 공식 웹사이트
  - 오너 포털 링크
  - 클래스 협회 정보
  - 하드웨어 제조사 카탈로그 링크

## 🚀 사용 방법

### Step 1: 매뉴얼 다운로드

1. `yacht_manual_resources.json` 파일을 열어 해당 요트의 웹사이트 확인
2. 제조사 웹사이트의 오너 포털에 등록
3. 요트 모델의 Owner's Manual 또는 Parts List 다운로드

**주요 제조사별 접근 방법:**

#### Beneteau / Jeanneau

- 웹사이트: https://www.beneteau.com/en/owners
- 요구사항: 보트 등록 또는 HIN (Hull Identification Number)

#### J/Boats (J/24, J/70)

- 클래스 협회 웹사이트에서 무료 제공
- J/24: https://www.j24class.org
- J/70: https://www.j70class.org

#### X-Yachts

- 웹사이트: https://www.x-yachts.com/owners
- 딜러 또는 오너 포털 통해 접근

#### Nautor's Swan

- 웹사이트: https://www.nautorswan.com/owners
- 등록 필요 (프리미엄 지원)

### Step 2: 부품 정보 추출

매뉴얼에서 다음 정보를 찾으세요:

```
✓ Part Number (부품 번호)
✓ Part Name (부품 이름)
✓ Category (카테고리)
✓ Manufacturer (제조사)
✓ Material (재질)
✓ Specifications (사양)
```

### Step 3: JSON 파일 업데이트

`yacht_parts_database.json`의 해당 요트 섹션에 정보 입력:

```json
{
  "partNumber": "WN-48ST",
  "name": "Primary Winch - Starboard",
  "category": "Deck Hardware",
  "type": "Two-Speed Self-Tailing",
  "manufacturer": "Harken",
  "model": "48.2ST",
  "price": 1250,
  "availability": "In Stock"
}
```

## 🔍 부품 카테고리 가이드

### 주요 카테고리:

1. **hull**: 선체 관련 (Hull, Keel, Rudder)
2. **deck**: 데크 하드웨어 (Hatches, Portlights, Chainplates)
3. **rigging**: 리깅 (Mast, Boom, Standing/Running Rigging)
4. **sails**: 세일 (Mainsail, Genoa, Spinnaker)
5. **winches**: 윈치 (Primary, Halyard, Sheet Winches)
6. **blocks**: 블록 및 트래블러
7. **engine**: 엔진 및 추진 시스템
8. **electrical**: 전기 시스템
9. **plumbing**: 배관 시스템
10. **navigation**: 항해 장비
11. **interior**: 내부 설비
12. **safety**: 안전 장비

## 📊 데이터 수집 팁

### 제조사 직접 접근이 어려운 경우:

1. **하드웨어 제조사 카탈로그 활용**

   - Harken: https://www.harken.com
   - Lewmar: https://www.lewmar.com
   - Ronstan: https://www.ronstan.com

2. **엔진 제조사**

   - Yanmar: 온라인 파츠 카탈로그 제공
   - Volvo Penta: EPC (Electronic Parts Catalog)

3. **전자장비**

   - Garmin, Raymarine, B&G: 제품별 매뉴얼 무료 다운로드

4. **세일메이커**
   - North Sails, Quantum Sails: 세일 사양 및 사이즈 가이드

### 추가 정보 소스:

- 요트 클래스 협회 (One-Design 클래스의 경우)
- 요트 오너 포럼 및 커뮤니티
- 이전 오너 또는 딜러
- 보트 서베이 문서
- 마리나 정비사

## 💡 실제 적용 예시

### 예시 1: J/70 부품 조사

```json
{
  "id": "j70",
  "name": "J/70",
  "parts": {
    "rigging": [
      {
        "partNumber": "J70-MAST-01",
        "name": "Mast",
        "category": "Rigging",
        "material": "Carbon Fiber",
        "manufacturer": "Selden",
        "model": "J70 Mast Section",
        "specifications": {
          "length": "9.14m",
          "weight": "42kg"
        }
      }
    ],
    "sails": [
      {
        "partNumber": "J70-MAIN-NS",
        "name": "Mainsail",
        "category": "Sails",
        "manufacturer": "North Sails",
        "material": "NPL Tour",
        "area": "21.9 sq m"
      }
    ]
  }
}
```

## 🔧 권장 작업 순서

1. **원디자인 클래스부터 시작** (정보가 공개되어 있음)

   - J/24, J/70
   - Laser
   - RS21
   - Melges 32

2. **대형 제조사 모델**

   - Beneteau 시리즈
   - Jeanneau 시리즈
   - X-Yachts 시리즈

3. **프리미엄 브랜드**
   - Nautor's Swan
   - Grand Soleil
   - Solaris

## 📞 도움이 필요한 경우

각 제조사의 고객 서비스에 연락:

- 보트의 HIN (Hull Identification Number) 준비
- 구매 시기 및 딜러 정보
- 오너 증명 서류

## ⚠️ 중요 사항

- **저작권**: 매뉴얼은 저작권으로 보호됩니다. 개인적 사용 목적으로만 활용하세요.
- **정확성**: 부품 정보는 연식과 옵션에 따라 다를 수 있습니다.
- **업데이트**: 제조사는 부품을 변경할 수 있으므로 최신 정보를 확인하세요.

## 📱 앱 개발 활용

이 데이터베이스는 다음과 같은 기능을 구현하는데 활용할 수 있습니다:

- 요트 모델별 부품 검색
- 부품 카탈로그 브라우징
- 유지보수 체크리스트
- 부품 교체 주기 관리
- 제조사별 부품 필터링
- 가격 비교 기능

## 🎯 다음 단계

1. ✅ JSON 구조 완성 (완료)
2. ⬜ 각 요트의 매뉴얼 수집
3. ⬜ 부품 정보 입력
4. ⬜ 이미지 및 다이어그램 추가
5. ⬜ API 또는 앱 개발
6. ⬜ 데이터베이스 연동

---

**작성일**: 2025년 11월 12일
**버전**: 1.0
**상태**: 데이터베이스 구조 완성, 데이터 수집 필요
