# 📋 챗봇 파트 업데이트 요약 (2025-11-25)

> **업데이트 날짜**: 2025년 11월 25일  
> **작성자**: AI Chatbot Team  
> **기반**: 백엔드팀(권희님), 프론트엔드팀(희성님) 카카오톡 논의 내용 반영

---

## 🎯 **주요 업데이트 사항**

### **1️⃣ 부품 추출 시 `latestMaintenanceDate` 필드 추가**

#### **수정 파일:**
- `chatbot_unified.py` (라인 2539-2545)
- `yacht_manual_uploader.py` (라인 442-446)

#### **변경 내용:**
PDF 매뉴얼 분석 시 부품의 **최근 정비일** 정보도 추출하도록 개선

```python
# Before
part_list.append({
    "name": part.get("name", ""),
    "manufacturer": part.get("manufacturer", ""),
    "model": part.get("model", ""),
    "interval": part.get("interval")
})

# After
part_list.append({
    "name": part.get("name", ""),
    "manufacturer": part.get("manufacturer", ""),
    "model": part.get("model", ""),
    "interval": part.get("interval"),
    "latestMaintenanceDate": part.get("latestMaintenanceDate") or 
                            part.get("lastMaintenanceDate") or 
                            part.get("servicedOn") or None  # ✨ NEW
})
```

---

### **2️⃣ FCM 알림 연동 가이드 작성**

#### **신규 문서:**
- `docs/FCM_NOTIFICATION_BACKEND_GUIDE.md`

#### **주요 내용:**
- ✅ User 엔티티에 `fcmToken` 컬럼 추가 방법
- ✅ `PUT /api/user/fcm-token` API 구현 가이드
- ✅ Firebase Admin SDK 설정 방법
- ✅ FCM 알림 전송 서비스 (`FcmService`) 구현
- ✅ 정비 알림 스케줄러 구현
  - **매일 오전 9시 실행**
  - **1주일 전, 1일 전, 당일** 알림 전송
- ✅ 요트 참조인 초대 알림
- ✅ **정비 후기 작성 시 Part의 latestMaintenanceDate 자동 업데이트** ⭐ NEW

---

### **3️⃣ 챗봇-백엔드-프론트엔드 통합 연동 가이드**

#### **신규 문서:**
- `docs/CHATBOT_BACKEND_FRONTEND_INTEGRATION_V3.md`

#### **주요 내용:**
- ✅ 전체 시스템 아키텍처 다이어그램
- ✅ API 엔드포인트 전체 목록
  - Spring Boot (포트 8080)
  - Python Flask AI (포트 5000)
  - Python Manual Uploader (포트 5001)
- ✅ 데이터 구조 및 필드 매핑
  - Part 엔티티 (Backend/Frontend/AI Chatbot)
  - Calendar 엔티티
  - User 엔티티 (fcmToken 추가)
- ✅ 연동 플로우 4가지
  - 새 요트 등록 (PDF 업로드)
  - 기존 요트에 매뉴얼 추가
  - 캘린더 일정 등록 (케이스 A/B)
  - FCM 알림 (토큰 등록, 정비 알림, 초대 알림)
- ✅ 팀별 작업 체크리스트

---

### **4️⃣ 피그마 화면 기반 API 응답 형식 문서**

#### **신규 문서:**
- `docs/FIGMA_API_SPECIFICATION.md`

#### **주요 내용:**
- ✅ 피그마 화면 분석 결과
  - 요트 문서 등록 화면
  - 캘린더 일정 Dialog
  - FCM 알림 형식
- ✅ API 스펙 상세 정의
  - Request/Response 예시
  - 에러 케이스 처리
- ✅ Flutter 구현 코드 예시
  - 요트 문서 등록 화면
  - 캘린더 일정 Dialog 로직
  - FCM 알림 처리

---

## 📊 **백엔드팀-프론트엔드팀 논의 내용 반영**

### **논의 1: 캘린더 일정 확인 방식**

**질문 (권희님):**
> "이전 일정이 존재하는지 확인하는 방법을 다른 api로 만들어야 할 까요?  
> 아니면 create api 호출 후 400반환하면 update api 호출해주시나요?"

**답변 (희성님):**
> "api 만들지 않아도 되고 부품에 대한 일정이 있는건 type이 part일 때는 일정이 무조건 있기 때문에 등록하기 버튼을 눌렀을 때 저 dialog가 뜨게 됩니다"

**반영 사항:**
- ✅ 별도 API 불필요
- ✅ 프론트엔드에서 `GET /api/calendars?partId={id}` 호출 후 Dialog 표시

---

### **논의 2: FCM 알림 발송 시간 및 대상**

**질문 (권희님):**
> "알림을 미리 생성해 두게 되는데 그럼 1주일 전, 1일 전은 어떡게 확인하나요?  
> scheduler를 사용하면 매일 0시에 모든 알림을 확인하고 알림을 발송하게 되는데 매일 0시에 사용자에게 알림을 발송해도 될까요?"

**답변 (희성님):**
> "오전 9시 정도로 생각을 했고 이 부분에 대해서 생각을 안그래도 해봤는데 schedule이나 cron?으로 데이터 확인 후 업데이트가 가능하지 않나요?"

**최종 결정 (권희님):**
> "매일 9시에 모든 알림을 확인하고 1주일전, 하루전, 당일에 push 알림을 발송하겠습니다"

**반영 사항:**
- ✅ 매일 오전 9시 스케줄러 실행 (`@Scheduled(cron = "0 0 9 * * *")`)
- ✅ 3가지 시점 알림:
  - 1주일 전 (7일 전)
  - 1일 전
  - **당일** ⭐ NEW

---

### **논의 3: Part의 lastRepair 값 업데이트** ⭐ **중요**

**지적 (희성님):**
> "여기서 현재 dialog만 뜨고 해당 part에 대한 last repair값을 변경해주는 api가 없긴하네요 그래서 부품이랑 캘린더가 전체적으로 흐름 연결이 안됐던거같습니다"

**답변 (권희님):**
> "repair값을 수정하면 같이 수정되겠습니다"

**반영 사항:**
- ✅ `POST /api/repair` 호출 시 자동으로 `Part.latestMaintenanceDate` 업데이트
- ✅ `RepairService.createRepair()` 메서드에서 `part.update()` 호출
- ✅ JPA dirty checking으로 자동 커밋

---

## 🔧 **백엔드팀 작업 체크리스트**

### **우선순위 HIGH**
- [ ] User 엔티티에 `fcmToken VARCHAR(500)` 컬럼 추가
- [ ] `PUT /api/user/fcm-token` API 구현
- [ ] **정비 후기 작성 시 Part.latestMaintenanceDate 자동 업데이트** ⭐
  - `RepairService.createRepair()` 수정

### **우선순위 MEDIUM**
- [ ] FCM 알림 전송 서비스 (`FcmService`) 구현
- [ ] Firebase Admin SDK 설정 (`firebase-service-account.json`)
- [ ] 정비 알림 스케줄러 구현
  - 매일 오전 9시 실행
  - 1주일 전, 1일 전, **당일** 알림
- [ ] 요트 초대 시 알림 전송 로직 추가

### **우선순위 LOW**
- [ ] 테스트 API 작성 (수동 스케줄러 실행)
- [ ] 프론트엔드팀과 FCM 연동 테스트

---

## 🎨 **프론트엔드팀 작업 체크리스트**

### **우선순위 HIGH**
- [ ] 캘린더 일정 Dialog 로직 구현
  - 일정 있음 → "변경하시겠습니까?" Dialog
  - 일정 없음 → 바로 생성
- [ ] FCM 토큰 등록
  - 앱 시작 시 → `PUT /api/user/fcm-token`

### **우선순위 MEDIUM**
- [ ] 요트 문서 등록 화면 구현
  - `POST http://localhost:5001/api/yacht/{yacht_id}/upload-manual`
- [ ] FCM 알림 수신 시 라우팅
  - 정비 알림 → 캘린더 화면
  - 초대 알림 → 요트 상세 화면

---

## 🤖 **AI 챗봇팀 작업 완료 사항**

### ✅ **완료**
- ✅ `latestMaintenanceDate` 필드 추출 기능 추가
  - `chatbot_unified.py` 수정
  - `yacht_manual_uploader.py` 수정
- ✅ FCM 알림 연동 가이드 작성
  - `docs/FCM_NOTIFICATION_BACKEND_GUIDE.md`
  - 당일 알림 추가
  - Part 자동 업데이트 로직 추가
- ✅ 챗봇-백엔드-프론트엔드 통합 가이드 작성
  - `docs/CHATBOT_BACKEND_FRONTEND_INTEGRATION_V3.md`
- ✅ 피그마 화면 기반 API 문서 작성
  - `docs/FIGMA_API_SPECIFICATION.md`

---

## 📞 **문의**

- **백엔드**: 권희님 (이권희)
- **프론트엔드**: 희성님 (정희성)
- **AI 챗봇**: AI Chatbot Team

---

**최종 업데이트**: 2025-11-25  
**버전**: 3.1

