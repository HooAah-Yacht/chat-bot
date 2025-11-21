# 🔗 AI ↔ MySQL DB 연동 가이드

## 📋 목차
1. [현재 문제점](#현재-문제점)
2. [해결 방안](#해결-방안)
3. [DB 연동 설정](#db-연동-설정)
4. [사용 방법](#사용-방법)
5. [데이터 흐름](#데이터-흐름)

---

## 🚨 현재 문제점

### ❌ AI와 DB가 분리되어 있음

```
현재 시스템:
┌─────────────────────────────┐
│   chat-bot/                 │  ← Python AI
│   ├── chatbot_unified.py    │  ← Google Gemini AI
│   └── data/                 │
│       ├── yacht_specs.json  │  ← 파일 기반 저장
│       └── registered.json   │
└─────────────────────────────┘
              ❌ 연결 안 됨
┌─────────────────────────────┐
│   backend/                  │  ← Spring Boot
│   ├── MySQL (yacht_db)      │  ← 실제 DB
│   ├── user 테이블           │
│   └── yacht 테이블          │
└─────────────────────────────┘
```

### 문제:
1. **데이터 불일치**: AI는 JSON 파일만 읽음, DB 데이터를 실시간으로 모름
2. **중복 저장**: 같은 요트 정보가 JSON과 DB에 따로 저장됨
3. **동기화 문제**: 사용자가 앱에서 등록한 요트를 AI가 모름

---

## ✅ 해결 방안

### 🔗 AI ↔ DB 직접 연결

```
개선된 시스템:
┌─────────────────────────────┐
│   chat-bot/                 │
│   ├── chatbot_unified.py    │  ← AI 챗봇
│   └── yacht_db_connector.py │  ← DB 연결 모듈 ✨
└─────────────────────────────┘
              ↕️ PyMySQL
┌─────────────────────────────┐
│   MySQL (yacht_db)          │
│   ├── user 테이블           │
│   └── yacht 테이블          │  ← 단일 데이터 소스 ✅
└─────────────────────────────┘
              ↕️ JDBC
┌─────────────────────────────┐
│   backend/                  │
│   └── Spring Boot           │
└─────────────────────────────┘
```

---

## 🔧 DB 연동 설정

### 1️⃣ 패키지 설치

```bash
cd chat-bot
pip install pymysql
```

이미 `requirements.txt`에 추가됨:
```
pymysql==1.1.0
```

### 2️⃣ MySQL 테이블 확인

귀하의 현재 테이블:
```sql
CREATE TABLE `yacht` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `available` bit(1) DEFAULT NULL,
  `capacity` int DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `description` text,
  `location` varchar(255),
  `name` varchar(255) NOT NULL,
  `price_per_hour` decimal(38,2),
  `thumbnail_path` varchar(255),
  `updated_at` datetime(6),
  PRIMARY KEY (`id`)
)
```

### 3️⃣ 환경 변수 설정

`.env` 파일 생성:
```env
# MySQL 연결 정보
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=yacht_db
```

---

## 📖 사용 방법

### 방법 1: DB 연결 테스트

```bash
python yacht_db_connector.py
# → 선택: 1 (DB 연결 테스트)
```

**결과:**
```
🧪 MySQL 연결 테스트
✅ MySQL 연결 성공!

📊 DB의 요트 목록:
   - Ocean Dream (ID: 1, 위치: 부산 마리나)
   - Sailing Paradise (ID: 2, 위치: 제주)
   ... 외 3개
```

### 방법 2: JSON → DB 동기화

```bash
python yacht_db_connector.py
# → 선택: 2 (JSON → DB 동기화)
```

**동작:**
- `yacht_specifications.json`의 19개 요트를 DB에 저장
- 이미 존재하는 요트는 스킵
- AI가 추출한 정보를 `description` 필드에 저장

**결과:**
```
📥 JSON 파일 읽는 중: data/yacht_specifications.json
📊 총 19개 요트 발견

✅ 요트 저장 완료! ID: 10, Name: OCEANIS 46.1
✅ 요트 저장 완료! ID: 11, Name: J/70
⏭️  스킵: Hanse 458 (이미 존재)

========================================
✅ 동기화 완료!
   - 성공: 17개
   - 스킵: 2개
========================================
```

### 방법 3: DB → JSON 내보내기

```bash
python yacht_db_connector.py
# → 선택: 3 (DB → JSON 내보내기)
```

**결과:**
- DB의 요트 데이터를 JSON 파일로 내보냄
- AI 백업용으로 사용 가능

---

## 🔄 데이터 흐름

### 시나리오 1: 사용자가 앱에서 요트 등록

```
1️⃣ 사용자 (앱)
   ↓ 요트 정보 입력
2️⃣ Backend (Spring Boot)
   ↓ MySQL INSERT
3️⃣ MySQL DB (yacht 테이블)
   ↓ PyMySQL 조회
4️⃣ AI Chatbot
   ✅ 실시간으로 새 요트 정보 확인 가능!
```

### 시나리오 2: AI가 PDF에서 요트 분석

```
1️⃣ 사용자가 PDF 업로드
   ↓
2️⃣ AI (chatbot_unified.py)
   ↓ Google Gemini 분석
3️⃣ 추출된 요트 정보
   ↓ yacht_db_connector.save_yacht_from_ai()
4️⃣ MySQL DB 저장
   ✅ 바로 앱에서 조회 가능!
```

---

## 🎯 AI가 DB에서 가져올 데이터

### 1. 모든 요트 조회
```python
from yacht_db_connector import YachtDatabaseConnector

connector = YachtDatabaseConnector(
    host='localhost',
    user='root',
    password='your_password',
    database='yacht_db'
)

connector.connect()
yachts = connector.get_all_yachts()

for yacht in yachts:
    print(f"{yacht['name']} - {yacht['location']}")
```

**결과:**
```json
[
  {
    "id": 1,
    "name": "Ocean Dream",
    "available": true,
    "capacity": 8,
    "location": "부산 마리나",
    "price_per_hour": 150000,
    "description": "제조사: Beneteau | 전체 길이: 14.60m | 엔진: 59Kw",
    "created_at": "2025-11-21 10:00:00"
  }
]
```

### 2. 특정 요트 검색
```python
yachts = connector.search_yachts_by_name("Ocean")
# → 이름에 "Ocean"이 포함된 요트 검색
```

### 3. AI 분석 결과 저장
```python
yacht_data = {
    "name": "OCEANIS 46.1",
    "manufacturer": "BENETEAU",
    "specifications": {
        "dimensions": {"loa": "14.60m", "beam": "4.50m"},
        "engine": {"power": "59Kw"}
    }
}

yacht_id = connector.save_yacht_from_ai(yacht_data)
# → DB에 저장, yacht_id 반환
```

---

## 💾 JSON vs DB 비교

| 항목 | JSON 파일 | MySQL DB |
|------|-----------|----------|
| **속도** | 빠름 | 중간 (쿼리 필요) |
| **동기화** | ❌ 수동 | ✅ 실시간 |
| **다중 접근** | ❌ 파일 잠김 | ✅ 동시 접근 |
| **백업** | ✅ 쉬움 | 중간 (덤프 필요) |
| **확장성** | ❌ 파일 크기 제한 | ✅ 무제한 |
| **앱 연동** | ❌ 불가 | ✅ 가능 |

---

## 🚀 권장 구조

### ✅ **최종 권장: DB를 단일 데이터 소스로 사용**

```
┌─────────────────────────────┐
│   사용자 (iOS/Android 앱)   │
└─────────────────────────────┘
              ↕️
┌─────────────────────────────┐
│   Backend (Spring Boot)     │
│   - REST API                │
└─────────────────────────────┘
              ↕️
┌─────────────────────────────┐
│   MySQL (yacht_db)          │  ← 단일 진실 공급원 ✨
│   - yacht 테이블            │
│   - user 테이블             │
└─────────────────────────────┘
              ↕️
┌─────────────────────────────┐
│   AI Chatbot (Python)       │
│   - yacht_db_connector.py   │
│   - chatbot_unified.py      │
└─────────────────────────────┘
```

### JSON 파일 역할 변경:
- ❌ **이전**: 메인 데이터 소스
- ✅ **이후**: 백업 & 캐시 용도

---

## ✅ 다음 단계

### 1. DB 연결 테스트
```bash
python yacht_db_connector.py
```

### 2. JSON 데이터를 DB로 마이그레이션
```bash
python yacht_db_connector.py
# → 선택: 2
```

### 3. `chatbot_unified.py` 수정
- JSON 파일 대신 `yacht_db_connector` 사용
- 실시간 DB 조회

### 4. Backend API 추가
- AI 분석 결과를 받는 엔드포인트 생성
- `POST /api/ai/analyze-yacht`

---

## 🎉 완료!

이제 AI가 DB에 직접 연결되어:
- ✅ 실시간으로 앱의 요트 정보 확인
- ✅ AI 분석 결과를 바로 DB에 저장
- ✅ 데이터 중복 없음
- ✅ 앱 ↔ AI 완전 동기화

---

**문의사항이 있으시면 팀에 연락주세요!**

