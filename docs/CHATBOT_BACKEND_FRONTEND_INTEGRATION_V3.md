# 🔗 챗봇 ↔ 백엔드 ↔ 프론트엔드 연동 가이드 (최신판)

> **작성일**: 2025-11-25  
> **버전**: 3.0  
> **최종 업데이트**: 캘린더 API, FCM 알림, latestMaintenanceDate 필드 추가 반영

---

## 📊 **전체 시스템 아키텍처**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Flutter Frontend (Mobile App)                 │
│  - 요트 등록, 부품 관리, 캘린더, 알림, AI 채팅                   │
└──────────────┬─────────────────────────────────┬─────────────────┘
               │                                 │
        REST API (8080)                   REST API (5000/5001)
               │                                 │
               ↓                                 ↓
┌──────────────────────────────┐   ┌────────────────────────────┐
│  Spring Boot Backend         │   │  Python Flask AI API       │
│  - 사용자 인증 (JWT)          │←→│  - PDF 분석 (OpenAI GPT-4) │
│  - 요트/부품 CRUD             │   │  - 요트 매뉴얼 분석        │
│  - 캘린더 관리 ✨ NEW         │   │  - 부품 추출               │
│  - FCM 알림 전송 ✨ NEW       │   │  - 정비 정보 분석          │
└──────────────┬───────────────┘   └────────────────────────────┘
               │
               ↓
┌──────────────────────────────┐
│  MySQL Database              │
│  - user, yacht, part         │
│  - calendar ✨ NEW            │
│  - repair                    │
└──────────────────────────────┘
```

---

## 🎯 **API 엔드포인트 전체 목록**

### **1️⃣ Spring Boot Backend (포트 8080)**

#### **인증 API**
- `POST /api/user/register` - 회원가입
- `POST /api/user/login` - 로그인
- `PUT /api/user/fcm-token` - FCM 토큰 등록 ✨ NEW

#### **요트 API**
- `GET /api/yacht` - 요트 목록 조회
- `GET /api/yacht/{id}` - 요트 상세 조회
- `POST /api/yacht` - 요트 생성
- `POST /api/yacht/with-parts` - 요트 + 부품 일괄 생성
- `PUT /api/yacht/{id}` - 요트 수정
- `DELETE /api/yacht/{id}` - 요트 삭제

#### **부품 API**
- `GET /api/parts?yachtId={id}` - 특정 요트의 부품 목록
- `POST /api/parts` - 부품 추가
- `PUT /api/parts/{id}` - 부품 수정
- `DELETE /api/parts/{id}` - 부품 삭제

#### **캘린더 API** ✨ NEW
- `GET /api/calendars` - 캘린더 목록 조회
- `GET /api/calendars?partId={id}` - 특정 부품의 일정 조회
- `GET /api/calendars/{id}` - 캘린더 상세 조회
- `POST /api/calendars` - 캘린더 이벤트 생성
- `PUT /api/calendars/{id}` - 캘린더 이벤트 수정
- `DELETE /api/calendars/{id}` - 캘린더 이벤트 삭제

#### **정비 후기 API**
- `POST /api/repair` - 정비 후기 작성 (**Part의 latestMaintenanceDate 자동 업데이트** ✨)
- `GET /api/repair/{id}` - 정비 후기 조회

---

### **2️⃣ Python Flask AI API (포트 5000)**

#### **AI 채팅 API**
- `POST /api/chat` - AI 챗봇 대화
- `POST /api/chat/upload` - PDF 업로드 + AI 분석

#### **요트 분석 API**
- `POST /api/yacht/register` - 요트 등록 (JSON 응답)
- `GET /api/yacht/analyze?yacht_name={name}` - 요트 이름으로 부품 조회
- `POST /api/yacht/analyze-pdf` - PDF 파일 분석 (백엔드 전용)

#### **요트 목록 API**
- `GET /api/yachts` - 요트 목록 조회
- `GET /api/yacht/{yacht_id}` - 특정 요트 정보 조회

---

### **3️⃣ Python Flask Manual Uploader (포트 5001)** ✨ NEW

> **기존 요트에 새 매뉴얼(부품) 추가 전용 API**

- `GET /api/yachts` - 요트 목록 조회
- `GET /api/yacht/{yacht_id}` - 특정 요트 정보 조회
- `POST /api/yacht/{yacht_id}/upload-manual` - 매뉴얼 업로드 (부품만 추가)
- `GET /api/yacht/{yacht_id}/parts` - 특정 요트의 부품 조회

---

## 📝 **데이터 구조 및 필드 매핑**

### **1. Part (부품) 엔티티**

#### **Backend (Spring Boot)**
```java
@Entity
public class Part {
    private Long id;
    private Yacht yacht;
    private String name;               // 필수
    private String manufacturer;       // 선택
    private String model;              // 선택
    private Integer interval;          // 정비 주기 (개월) - 선택 ✨
    private LocalDate latestMaintenanceDate;  // 최근 정비일 - 선택 ✨ NEW
}
```

#### **Frontend (Flutter)**
```dart
class Part {
  final int? id;
  final int yachtId;
  final String name;
  final String? manufacturer;
  final String? model;
  final int? interval;                      // 정비 주기 (개월)
  final String? latestMaintenanceDate;      // 최근 정비일 (ISO 8601) ✨ NEW
}
```

#### **AI Chatbot (Python)**
```python
{
    "name": "Main Halyard",
    "manufacturer": "Harken",
    "model": "H-40",
    "interval": 12,                           # 정비 주기 (개월)
    "latestMaintenanceDate": "2024-10-15"     # 최근 정비일 ✨ NEW
}
```

---

### **2. Calendar (캘린더) 엔티티** ✨ NEW

#### **Backend (Spring Boot)**
```java
@Entity
public class CalendarEvent {
    private Long id;
    private Part part;                    // 연관된 부품 (nullable)
    private LocalDate startDate;          // 시작 날짜
    private LocalDate endDate;            // 종료 날짜
    private String content;               // 일정 내용 (참조인 정보 등)
}
```

#### **API Request/Response**
```json
{
  "partId": 123,
  "startDate": "2025-10-01T15:00:00+09:00",
  "endDate": "2025-10-01T16:00:00+09:00",
  "content": "메인 할야드 정비 - 참조인: 김철수"
}
```

---

### **3. User (사용자) 엔티티**

#### **Backend (Spring Boot) - 기존**
```java
@Entity
public class User {
    private Long id;
    private String email;
    private String password;
    private String name;
    private String socialId;
}
```

#### **Backend (Spring Boot) - 수정 필요** ✨ NEW
```java
@Entity
public class User {
    private Long id;
    private String email;
    private String password;
    private String name;
    private String socialId;
    private String fcmToken;  // ✨ FCM 토큰 추가 필요!
}
```

---

## 🔄 **연동 플로우**

### **플로우 1: 새 요트 등록 (PDF 업로드)**

```
1. Flutter → POST /api/yacht/register (포트 5000) [PDF 파일]
   └─ Python AI가 PDF 분석 → GPT-4로 부품 추출
   └─ latestMaintenanceDate 필드도 추출 시도 ✨

2. Python AI → Response JSON
   {
     "basicInfo": { ... },
     "specifications": { ... },
     "parts": [
       {
         "name": "Main Halyard",
         "manufacturer": "Harken",
         "model": "H-40",
         "interval": 12,
         "latestMaintenanceDate": "2024-10-15"  ✨
       }
     ]
   }

3. Flutter → POST /api/yacht (포트 8080) [요트 기본 정보]
   └─ Backend가 Yacht 엔티티 생성

4. Flutter → POST /api/parts (포트 8080) [부품들]
   └─ Backend가 Part 엔티티들 생성
   └─ latestMaintenanceDate도 저장 ✨
```

---

### **플로우 2: 기존 요트에 매뉴얼 추가 (부품만 추가)** ✨ NEW

```
1. Flutter → GET /api/yachts (포트 5001)
   └─ 기존 요트 목록 조회

2. 사용자가 요트 선택 (예: Farr 40)

3. Flutter → POST /api/yacht/farr-40/upload-manual (포트 5001) [PDF 파일]
   └─ Python AI가 부품만 추출
   └─ 기존 요트 정보는 변경 안 함
   └─ 중복 부품 자동 필터링

4. Python AI → Response JSON
   {
     "yachtId": "farr-40",
     "addedParts": 5,
     "skippedParts": 2,
     "parts": [ ... ]
   }

5. Flutter → POST /api/parts (포트 8080) [새 부품들]
   └─ Backend가 Part 엔티티 추가
```

---

### **플로우 3: 캘린더 일정 등록** ✨ NEW

#### **케이스 A: 일정이 없을 때 (신규 생성)**

```
1. Flutter → GET /api/calendars?partId=123 (포트 8080)
   └─ Backend 응답: []  (빈 배열)

2. Flutter → Dialog 표시 (일정 입력 폼)

3. 사용자가 시작/종료 날짜 입력

4. Flutter → POST /api/calendars (포트 8080)
   {
     "partId": 123,
     "startDate": "2025-10-01T15:00:00+09:00",
     "endDate": "2025-10-01T16:00:00+09:00",
     "content": "참조인: 김철수"
   }

5. Backend → Calendar 엔티티 생성
```

#### **케이스 B: 일정이 이미 있을 때 (수정)** ⭐ 피그마 화면

```
1. Flutter → GET /api/calendars?partId=123 (포트 8080)
   └─ Backend 응답: [{ id: 456, ... }]

2. Flutter → Dialog 표시 ⭐
   "부품에 대한 일정이 이미 존재합니다. 일정을 변경하시겠습니까?"
   [취소] [변경]

3. 사용자가 "변경" 선택

4. Flutter → PUT /api/calendars/456 (포트 8080)
   {
     "startDate": "2025-10-15T15:00:00+09:00",
     "endDate": "2025-10-15T16:00:00+09:00",
     "content": "참조인: 이영희"
   }

5. Backend → Calendar 엔티티 수정
```

---

### **플로우 4: FCM 알림** ✨ NEW

#### **4-1. FCM 토큰 등록**

```
1. Flutter 앱 시작 → Firebase SDK가 FCM 토큰 발급
   └─ Token: "fV3X5g9hR8y:APA91bH..."

2. Flutter → PUT /api/user/fcm-token (포트 8080)
   {
     "fcmToken": "fV3X5g9hR8y:APA91bH..."
   }

3. Backend → User 엔티티의 fcmToken 필드 업데이트
```

#### **4-2. 정비 알림 (스케줄러)**

```
1. Backend 스케줄러 (매일 오전 9시 실행)
   └─ CalendarEvent 테이블 조회
   └─ 오늘로부터 1주일 후 & 1일 후 일정 필터링

2. 각 일정에 대해:
   └─ 해당 요트의 모든 사용자 조회 (YachtUser 테이블)
   └─ 각 사용자의 FCM 토큰으로 알림 전송

3. Firebase Cloud Messaging
   {
     "title": "HooAah",
     "body": "⚠️ 정비 일정 알림\n\n요트: Farr 40\n부품: Main Halyard\n정비 예정일: 2025-10-15 (1주일 후)"
   }

4. Flutter → FCM 알림 수신 → 알림 표시
```

#### **4-3. 참조인 초대 알림**

```
1. 사용자 A가 사용자 B를 요트에 초대
   └─ Flutter → POST /api/yacht/invite (포트 8080)

2. Backend → YachtUser 엔티티 생성
   └─ 사용자 B의 FCM 토큰 조회
   └─ FCM 알림 전송

3. Firebase Cloud Messaging
   {
     "title": "HooAah",
     "body": "🎉 김철수님이 요트 'Farr 40'에 참조인으로 초대했습니다!"
   }

4. Flutter (사용자 B) → FCM 알림 수신 → 알림 표시
```

---

## 🔧 **백엔드팀 작업 필요 사항**

### ✅ **완료된 작업**
- ✅ 캘린더 API 구현 (`/api/calendars`)
- ✅ Part 엔티티에 `interval` 필드 있음
- ✅ Part 엔티티에 `latestMaintenanceDate` 필드 있음

### ⚠️ **작업 필요**
- [ ] User 엔티티에 `fcmToken` 컬럼 추가
  ```sql
  ALTER TABLE user ADD COLUMN fcm_token VARCHAR(500) NULL;
  ```
- [ ] `PUT /api/user/fcm-token` API 구현
- [ ] FCM 알림 전송 서비스 구현 (`FcmService`)
- [ ] 정비 알림 스케줄러 구현 (`MaintenanceNotificationScheduler`)
  - 매일 오전 9시 실행
  - **1주일 전, 1일 전, 당일** 알림 전송
- [ ] 요트 초대 시 알림 전송 로직 추가
- [ ] **정비 후기 작성 시 Part의 latestMaintenanceDate 자동 업데이트** ⭐ NEW

> **📄 상세 가이드**: `docs/FCM_NOTIFICATION_BACKEND_GUIDE.md` 참고

---

## 🎨 **프론트엔드팀 작업 필요 사항**

### ✅ **완료된 작업**
- ✅ 요트 등록 화면
- ✅ 부품 관리 화면
- ✅ 캘린더 화면
- ✅ AI 채팅 화면

### ⚠️ **작업 필요**
- [ ] "요트 문서 등록" 화면 구현 (기존 요트에 매뉴얼 추가)
  - API: `POST http://localhost:5001/api/yacht/{yacht_id}/upload-manual`
- [ ] 캘린더 일정 Dialog에서 기존 일정 확인 로직
  - 일정 있음 → "변경하시겠습니까?" Dialog 표시
  - 일정 없음 → 바로 생성
- [ ] FCM 토큰 등록 로직
  - 앱 시작 시 → `PUT /api/user/fcm-token`
  - 토큰 갱신 시 → 자동 재등록
- [ ] FCM 알림 수신 시 라우팅
  - 정비 알림 → 캘린더 화면으로 이동
  - 초대 알림 → 요트 목록 화면으로 이동

---

## 🤖 **AI 챗봇팀 작업 사항**

### ✅ **완료된 작업**
- ✅ `latestMaintenanceDate` 필드 추출 추가
  - `chatbot_unified.py` 수정 완료
  - `yacht_manual_uploader.py` 수정 완료
- ✅ FCM 알림 연동 가이드 작성
  - `docs/FCM_NOTIFICATION_BACKEND_GUIDE.md`
- ✅ 챗봇-백엔드 연동 가이드 업데이트
  - 캘린더 API 반영
  - latestMaintenanceDate 필드 반영

### 🔄 **추가 개선 사항 (선택)**
- [ ] PDF에서 정비 날짜 추출 정확도 향상
  - "Last Service: 2024-10-15"
  - "Serviced on 15/10/2024"
  - "최근 정비일: 2024년 10월 15일"
- [ ] 부품 카테고리 자동 분류 개선

---

## 🧪 **통합 테스트 시나리오**

### **시나리오 1: 완전한 요트 등록 플로우**

```bash
# 1. 요트 등록 (AI PDF 분석)
curl -X POST http://localhost:5000/api/yacht/register \
  -F "file=@farr40_manual.pdf"

# 2. Backend에 요트 생성
curl -X POST http://localhost:8080/api/yacht \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {JWT_TOKEN}" \
  -d '{"yachtName": "Farr 40", "yachtAlias": "My Farr"}'

# 3. 부품 추가
curl -X POST http://localhost:8080/api/parts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {JWT_TOKEN}" \
  -d '{
    "yachtId": 1,
    "name": "Main Halyard",
    "manufacturer": "Harken",
    "model": "H-40",
    "interval": 12,
    "latestMaintenanceDate": "2024-10-15"
  }'

# 4. 캘린더 일정 생성
curl -X POST http://localhost:8080/api/calendars \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {JWT_TOKEN}" \
  -d '{
    "partId": 1,
    "startDate": "2025-10-15T09:00:00+09:00",
    "endDate": "2025-10-15T11:00:00+09:00",
    "content": "메인 할야드 정비 예정"
  }'
```

---

## 📞 **문의**

- **백엔드**: 권희님
- **프론트엔드**: 희성님
- **AI 챗봇**: AI Chatbot Team

---

**최종 업데이트**: 2025-11-25  
**버전**: 3.0

