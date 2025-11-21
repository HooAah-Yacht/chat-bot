# 🔍 Frontend & Backend SQL 사용 현황 및 AI 연동 가이드

## 📊 현재 시스템 분석

### ✅ **Backend: MySQL 사용 중**

#### 1. **MySQL 연결 설정** (`backend/src/main/resources/application.yml`)

```yaml
spring:
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver      # ✅ MySQL 드라이버
    url: jdbc:mysql://${DB_URL}                       # ✅ MySQL JDBC URL
    username: ${DB_USERNAME}                          # 환경변수
    password: ${DB_PASSWORD}                          # 환경변수
    hikari:
      maximum-pool-size: 3                            # 커넥션 풀
  jpa:
    hibernate:
      ddl-auto: update                                # 자동 테이블 생성/업데이트
```

#### 2. **MySQL 의존성** (`backend/build.gradle`)

```gradle
dependencies {
    // MySQL Connector
    runtimeOnly 'com.mysql:mysql-connector-j'         # ✅ MySQL 8.0+
    
    // JPA (Hibernate)
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
}
```

#### 3. **환경변수 설정 필요**

Backend는 다음 환경변수를 사용:
```bash
DB_URL=localhost:3306/yacht_db
DB_USERNAME=root
DB_PASSWORD=your_password
SECRET_KEY=your_jwt_secret_key
```

---

### ✅ **Frontend: Backend API 호출** (Flutter)

#### 1. **Backend 연결** (`frontend/lib/services/auth_service.dart`)

```dart
static String get baseUrl {
  if (Platform.isAndroid) {
    return 'http://10.0.2.2:8080';      // Android 에뮬레이터
  } else if (Platform.isIOS) {
    return 'http://localhost:8080';     // iOS 시뮬레이터
  }
  return 'http://localhost:8080';       // 기본값
}
```

**Frontend는 SQL을 직접 사용하지 않음**
- REST API로 Backend와 통신
- Backend가 MySQL 쿼리 실행
- JSON 형식으로 데이터 송수신

---

### ✅ **AI Chatbot: 현재 JSON 파일 사용** (Python)

#### 현재 상태:
```python
# chat-bot/chatbot_unified.py
# ❌ MySQL 연결 없음
# ✅ JSON 파일만 읽음

yacht_specs = json.load(open('data/yacht_specifications.json'))
```

---

## 🎯 **결론: 모두 MySQL 사용 (또는 MySQL 호환)**

| 컴포넌트 | 데이터베이스 | 연결 방법 | 상태 |
|----------|--------------|-----------|------|
| **Backend** | ✅ MySQL | JDBC (Spring Data JPA) | 연결됨 |
| **Frontend** | - | REST API → Backend | 간접 연결 |
| **AI Chatbot** | ❌ 없음 | JSON 파일 | 연결 안 됨 |

---

## 🚀 AI Chatbot을 MySQL에 연결하는 방법

### 📋 **전체 구조**

```
┌─────────────────────────────────────┐
│   Frontend (Flutter)                │
│   - iOS/Android 앱                  │
│   - HTTP 요청만 사용                │
└─────────────────────────────────────┘
              ↕️ REST API
┌─────────────────────────────────────┐
│   Backend (Spring Boot)             │
│   - Port: 8080                      │
│   - JDBC → MySQL                    │
└─────────────────────────────────────┘
              ↕️ JDBC
┌─────────────────────────────────────┐
│   MySQL Database (yacht_db)         │  ← 중앙 데이터 저장소
│   - yacht 테이블                    │
│   - user 테이블                     │
│   - part 테이블                     │
└─────────────────────────────────────┘
              ↕️ PyMySQL ✨ (새로 추가)
┌─────────────────────────────────────┐
│   AI Chatbot (Python)               │
│   - yacht_db_connector.py           │
│   - chatbot_unified.py              │
└─────────────────────────────────────┘
```

---

## ✅ **단계별 설정 가이드**

### 1️⃣ **MySQL 데이터베이스 확인**

#### Backend가 사용 중인 DB 정보 확인:

1. **환경변수 파일 찾기**
   ```bash
   # Backend 폴더에서 .env 파일 확인
   cd backend
   cat .env
   ```

2. **만약 .env 파일이 없다면 생성**
   ```bash
   # backend/.env
   DB_URL=localhost:3306/yacht_db
   DB_USERNAME=root
   DB_PASSWORD=your_password_here
   SECRET_KEY=your_jwt_secret_key_here
   ```

3. **MySQL 접속 테스트**
   ```bash
   # Windows (HeidiSQL, MySQL Workbench)
   # 또는 명령어로 직접:
   mysql -u root -p
   
   # 데이터베이스 확인
   SHOW DATABASES;
   USE yacht_db;
   SHOW TABLES;
   ```

#### 예상 결과:
```sql
mysql> SHOW TABLES;
+--------------------+
| Tables_in_yacht_db |
+--------------------+
| user               |
| yacht              |
| yacht_user         |
| part               |
| repair             |
| calendar           |
+--------------------+
```

---

### 2️⃣ **AI Chatbot MySQL 연결 설정**

#### A. **패키지 설치**

```bash
cd chat-bot
pip install pymysql
```

이미 `requirements.txt`에 추가되어 있습니다:
```
pymysql==1.1.0
```

#### B. **환경변수 설정** (`.env` 파일 생성)

```bash
# chat-bot/.env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=yacht_db

# Google Gemini API (기존)
GEMINI_API_KEY=your_gemini_key
```

#### C. **연결 테스트**

```bash
cd chat-bot
python yacht_db_connector.py
# → 선택: 1 (DB 연결 테스트)
```

**입력 예시:**
```
Host: localhost
Port: 3306
User: root
Password: [Backend .env의 DB_PASSWORD와 동일하게 입력]
Database: yacht_db
```

**성공 시:**
```
✅ MySQL 연결 성공!

📊 DB의 요트 목록:
   - Ocean Dream (ID: 1, 위치: 부산 마리나)
   - Sailing Paradise (ID: 2, 위치: 제주)
   ... 외 3개
```

---

### 3️⃣ **Backend의 yacht 테이블 구조 확인**

#### 현재 Backend Entity (`Yacht.java`):

```java
@Entity
@Table(name = "yacht")
public class Yacht {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;              // bigint AUTO_INCREMENT
    
    private String name;          // varchar(255)
    private String nickName;      // varchar(255)
    
    @OneToMany(mappedBy = "yacht")
    private List<YachtUser> yachtUser;
}
```

#### ⚠️ **문제: Backend의 yacht 테이블이 간소화됨**

귀하가 보여주신 MySQL 테이블:
```sql
CREATE TABLE `yacht` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `available` bit(1) DEFAULT NULL,        # Backend에 없음
  `capacity` int DEFAULT NULL,            # Backend에 없음
  `created_at` datetime(6) DEFAULT NULL,  # Backend에 없음
  `description` text,                     # Backend에 없음
  `location` varchar(255),                # Backend에 없음
  `name` varchar(255) NOT NULL,
  `price_per_hour` decimal(38,2),         # Backend에 없음
  `thumbnail_path` varchar(255),          # Backend에 없음
  `updated_at` datetime(6),               # Backend에 없음
  PRIMARY KEY (`id`)
)
```

**Backend의 테이블과 귀하의 테이블이 다릅니다!**

---

### 4️⃣ **해결 방안: Backend Entity 확장**

#### Option 1: Backend Entity에 필드 추가 (권장)

```java
// backend/src/main/java/HooYah/Yacht/yacht/domain/Yacht.java
@Entity
@Table(name = "yacht")
public class Yacht {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String name;
    private String nickName;
    
    // ✨ 새로 추가할 필드들
    private Boolean available;              // 예약 가능 여부
    private Integer capacity;               // 수용 인원
    
    @Column(columnDefinition = "TEXT")
    private String description;             // 설명 (AI 분석 결과)
    
    private String location;                // 위치
    private BigDecimal pricePerHour;        // 시간당 가격
    private String thumbnailPath;           // 썸네일 경로
    
    @CreatedDate
    private LocalDateTime createdAt;        // 생성일
    
    @LastModifiedDate
    private LocalDateTime updatedAt;        // 수정일
    
    @OneToMany(mappedBy = "yacht")
    private List<YachtUser> yachtUser;
}
```

#### Option 2: AI용 별도 테이블 생성

```sql
-- AI 분석 결과 전용 테이블
CREATE TABLE yacht_ai_data (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    yacht_id BIGINT,                        -- yacht.id 참조
    manufacturer VARCHAR(255),
    yacht_type VARCHAR(255),
    loa DECIMAL(10,2),                      -- Length Overall
    beam DECIMAL(10,2),
    draft DECIMAL(10,2),
    displacement INT,
    engine_type VARCHAR(255),
    engine_power VARCHAR(255),
    sail_area_main DECIMAL(10,2),
    sail_area_jib DECIMAL(10,2),
    manual_pdf VARCHAR(500),
    analyzed_at DATETIME,
    FOREIGN KEY (yacht_id) REFERENCES yacht(id)
);
```

---

### 5️⃣ **AI 분석 결과를 DB에 저장**

#### A. **JSON 데이터를 MySQL로 마이그레이션**

```bash
cd chat-bot
python yacht_db_connector.py
# → 선택: 2 (JSON → DB 동기화)
```

**동작:**
1. `yacht_specifications.json` 읽기
2. 각 요트를 MySQL `yacht` 테이블에 INSERT
3. AI 분석 정보를 `description` 필드에 저장

**예시 결과:**
```
📥 JSON 파일 읽는 중: data/yacht_specifications.json
📊 총 19개 요트 발견

✅ 요트 저장 완료! ID: 10, Name: OCEANIS 46.1
   Description: 제조사: BENETEAU | 전체 길이: 14.60m | 엔진: 59Kw

✅ 요트 저장 완료! ID: 11, Name: J/70
   Description: 제조사: C&C Fiberglass | 전체 길이: 6.86m

========================================
✅ 동기화 완료!
   - 성공: 19개
   - 스킵: 0개
========================================
```

#### B. **Python 코드로 직접 저장**

```python
from yacht_db_connector import YachtDatabaseConnector

# DB 연결
connector = YachtDatabaseConnector(
    host='localhost',
    user='root',
    password='your_password',
    database='yacht_db'
)
connector.connect()

# AI 분석 결과 저장
yacht_data = {
    "name": "OCEANIS 46.1",
    "manufacturer": "BENETEAU",
    "specifications": {
        "dimensions": {
            "loa": "14.60m",
            "beam": "4.50m"
        },
        "engine": {
            "power": "59Kw"
        }
    }
}

yacht_id = connector.save_yacht_from_ai(yacht_data)
print(f"요트 저장됨! ID: {yacht_id}")

connector.disconnect()
```

---

### 6️⃣ **AI Chatbot에서 DB 데이터 조회**

#### `chatbot_unified.py` 수정

```python
# 기존 (JSON 파일 읽기)
# with open('data/yacht_specifications.json', 'r') as f:
#     yacht_data = json.load(f)

# ✨ 새로운 방식 (DB에서 직접 조회)
from yacht_db_connector import YachtDatabaseConnector

connector = YachtDatabaseConnector(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', ''),
    database=os.getenv('DB_NAME', 'yacht_db')
)

connector.connect()
yachts = connector.get_all_yachts()  # DB에서 실시간 조회
connector.disconnect()

# AI에게 전달
yacht_info = "\n".join([f"- {y['name']} ({y.get('location', 'N/A')})" for y in yachts])
```

---

## 🎯 **최종 권장 구조**

### ✅ **단일 MySQL 데이터베이스 사용**

```
┌────────────────────────────────────────────────┐
│           MySQL (yacht_db)                     │
│                                                │
│  📊 Tables:                                    │
│  ├── yacht (기본 정보 + AI 분석 결과)         │
│  ├── user (사용자)                             │
│  ├── yacht_user (다대다 관계)                 │
│  ├── part (부품)                               │
│  ├── repair (정비 이력)                        │
│  └── calendar (일정)                           │
└────────────────────────────────────────────────┘
          ↕️ JDBC              ↕️ PyMySQL
┌─────────────────┐     ┌─────────────────────┐
│   Backend       │     │   AI Chatbot        │
│   (Spring Boot) │     │   (Python)          │
└─────────────────┘     └─────────────────────┘
          ↕️ REST API
┌─────────────────────────┐
│   Frontend (Flutter)    │
└─────────────────────────┘
```

---

## 📋 **체크리스트**

### ✅ 완료해야 할 작업:

- [ ] 1. Backend `.env` 파일 확인/생성 (DB 연결 정보)
- [ ] 2. MySQL 접속 테스트 (`yacht_db` 데이터베이스 확인)
- [ ] 3. Backend `Yacht.java` Entity 확장 (필요시)
- [ ] 4. AI Chatbot `.env` 파일 생성 (Backend와 동일한 DB 정보)
- [ ] 5. `pymysql` 패키지 설치
- [ ] 6. `yacht_db_connector.py` 연결 테스트
- [ ] 7. JSON → DB 마이그레이션 실행
- [ ] 8. `chatbot_unified.py`에서 DB 조회 코드 추가

---

## 🚀 **다음 단계**

### 1. Backend 환경변수 확인
```bash
cd backend
# .env 파일이 있는지 확인
ls -a
```

### 2. MySQL 접속 정보 공유
Backend의 `.env` 파일에 있는:
- `DB_URL`
- `DB_USERNAME`
- `DB_PASSWORD`

이 정보를 AI Chatbot의 `.env`에도 동일하게 설정

### 3. AI 연결 테스트
```bash
cd chat-bot
python yacht_db_connector.py
```

---

**이제 AI가 Backend와 동일한 MySQL을 사용하게 됩니다!** ✅

Backend `.env` 파일 내용을 알려주시면, AI Chatbot 설정을 완료해드리겠습니다! 🎯

