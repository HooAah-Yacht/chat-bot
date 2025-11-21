# 🔧 MySQL 연결 설정 완료 가이드

## ✅ 설정 정보 확인

### Backend 환경변수 (`.env`)

```env
SECRET_KEY=duwkclsrntkrnlrhtlvdjdydjswpWmaduwkclsrnrktodrlfRkdy
DB_URL=localhost:3306/HooYah
DB_USERNAME=root
DB_PASSWORD=root
```

### MySQL Workbench 커넥션 (Yacht01)

```
Connection Name: Yacht01
Hostname: localhost
Port: 3306
Username: root
Password: (저장 안 함)
```

---

## 🎯 AI Chatbot 설정

### 1️⃣ `.env` 파일 생성

**위치:** `chat-bot/.env`

**내용:**

```env
# MySQL 연결 정보 (Backend와 동일)
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=root
DB_NAME=HooYah

# Google Gemini API
GEMINI_API_KEY=AIzaSyDLp4vq9fqGVLm8Y3YJxNXxKqG0j_9fY8s
```

> ✅ **GEMINI_API_KEY 기억하고 있습니다!**

---

## 🔍 차이점 및 해결

### ❌ **데이터베이스 이름 불일치**

| 위치            | 데이터베이스 이름            |
| --------------- | ---------------------------- |
| Backend         | `HooYah`                     |
| MySQL Workbench | `yacht_db` (표시명: Yacht01) |

**→ 이것은 문제가 아닙니다!**

**설명:**

- MySQL Workbench의 "Connection Name" (Yacht01)은 **커넥션 저장 이름**일 뿐
- 실제 데이터베이스는 `HooYah`일 가능성이 높음
- Backend가 `HooYah`를 사용하므로, AI도 `HooYah` 사용

### ✅ **확인 방법**

MySQL Workbench에서:

```sql
-- 1. 연결 후 데이터베이스 목록 확인
SHOW DATABASES;

-- 2. HooYah 데이터베이스가 있는지 확인
USE HooYah;
SHOW TABLES;

-- 3. yacht 테이블 확인
SELECT * FROM yacht;
```

**예상 결과:**

```
Database: HooYah
Tables:
  - user
  - yacht
  - yacht_user
  - part
  - repair
  - calendar
```

---

## 🚀 AI Chatbot 연결 테스트

### 방법 1: 자동 테스트 스크립트

```bash
cd chat-bot
python test_mysql_connection.py
```

**동작:**

1. `.env` 파일 자동 읽기
2. MySQL 연결 테스트
3. `HooYah` 데이터베이스 확인
4. `yacht` 테이블 조회
5. 테이블 구조 확인

**예상 출력:**

```
🔍 MySQL 연결 테스트
================================================================================

📋 연결 정보:
   Host: localhost
   Port: 3306
   User: root
   Password: ****
   Database: HooYah

✅ MySQL 연결 성공!

📊 데이터베이스 테이블:
   ✅ user (5개 레코드)
   ✅ yacht (2개 레코드)
   ✅ yacht_user (3개 레코드)
   ✅ part (10개 레코드)

🚢 yacht 테이블 조회:
   총 2개 요트 발견
   - ID: 1, Name: Ocean Dream, NickName: Dream
   - ID: 2, Name: Sailing Paradise, NickName: Paradise
```

### 방법 2: 수동 테스트

```bash
cd chat-bot
python yacht_db_connector.py
# → 선택: 1 (DB 연결 테스트)
```

**입력값:**

```
Host: localhost
Port: 3306
User: root
Password: root
Database: HooYah
```

---

## ⚠️ 주의사항

### 1. **Backend의 yacht 테이블 구조**

Backend `Yacht.java` Entity:

```java
@Entity
@Table(name = "yacht")
public class Yacht {
    private Long id;
    private String name;
    private String nickName;
}
```

**문제:** AI가 저장하려는 필드가 없음

- `available`, `capacity`, `description`, `location`, `price_per_hour`, `thumbnail_path`, `created_at`, `updated_at`

**해결 방법:**

#### Option 1: Backend Entity 확장 (권장)

```java
@Entity
@Table(name = "yacht")
public class Yacht {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private String nickName;

    // ✨ AI가 사용할 필드 추가
    private Boolean available;
    private Integer capacity;

    @Column(columnDefinition = "TEXT")
    private String description;

    private String location;
    private BigDecimal pricePerHour;
    private String thumbnailPath;

    @CreatedDate
    private LocalDateTime createdAt;

    @LastModifiedDate
    private LocalDateTime updatedAt;
}
```

#### Option 2: AI 전용 테이블 생성

```sql
-- HooYah 데이터베이스에서 실행
CREATE TABLE yacht_ai_specs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    yacht_id BIGINT,
    manufacturer VARCHAR(255),
    loa DECIMAL(10,2),
    beam DECIMAL(10,2),
    draft DECIMAL(10,2),
    engine_power VARCHAR(255),
    manual_pdf VARCHAR(500),
    analyzed_at DATETIME,
    FOREIGN KEY (yacht_id) REFERENCES yacht(id)
);
```

---

## 📋 실행 순서

### 1. `.env` 파일 확인

```bash
cd chat-bot
cat .env
```

**내용이 이렇게 되어 있는지 확인:**

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=root
DB_NAME=HooYah
GEMINI_API_KEY=AIzaSyDLp4vq9fqGVLm8Y3YJxNXxKqG0j_9fY8s
```

### 2. 패키지 설치

```bash
pip install pymysql python-dotenv
```

### 3. 연결 테스트

```bash
python test_mysql_connection.py
```

### 4. JSON → DB 마이그레이션 (선택)

```bash
python yacht_db_connector.py
# → 선택: 2
```

**주의:** Backend Entity에 필드가 부족하면 오류 발생 가능!

---

## ✅ 요약

### 수정 필요 사항

❌ **커넥션 수정 불필요**

- Backend: `localhost:3306/HooYah`
- AI: `localhost:3306/HooYah` (동일)

❌ **URL 수정 불필요**

- 모두 `localhost:3306` 사용

✅ **AI `.env` 파일만 생성하면 됨**

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=root
DB_NAME=HooYah
GEMINI_API_KEY=AIzaSyDLp4vq9fqGVLm8Y3YJxNXxKqG0j_9fY8s
```

---

## 🎉 완료!

이제 다음 명령어로 테스트하세요:

```bash
cd chat-bot
python test_mysql_connection.py
```

문제가 발생하면 오류 메시지를 알려주세요! 🚀
