# 🔔 FCM 알림 기능 구현 가이드 (백엔드팀용)

> **작성일**: 2025-11-25  
> **작성자**: AI Chatbot Team  
> **대상**: 백엔드 개발팀 (Spring Boot)

---

## 📊 **현재 상황 요약**

### ✅ **완료된 작업**
- ✅ 캘린더 API 구현 완료 (`/api/calendars`)
- ✅ Part 엔티티에 `interval`, `latestMaintenanceDate` 필드 있음
- ✅ Flutter 프론트엔드에서 FCM 토큰 발급 가능

### 🚧 **구현 필요한 작업**
- ⚠️ User 엔티티에 `fcmToken` 컬럼 추가
- ⚠️ FCM 알림 전송 서비스 구현
- ⚠️ 스케줄러로 정비 일정 알림 (1주일 전, 1일 전)
- ⚠️ 요트 참조인 알림 (친구 초대 시)

---

## 🎯 **1. User 엔티티 수정**

### **현재 User 엔티티**

```java
@Entity
@Table(name = "user")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column
    private String email;
    
    @Column
    private String password;
    
    @Column
    private String name;
    
    @Column(name = "social_id")
    private String socialId;
}
```

### **수정 후 (fcmToken 추가)** ⭐

```java
@Entity
@Table(name = "user")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column
    private String email;
    
    @Column
    private String password;
    
    @Column
    private String name;
    
    @Column(name = "social_id")
    private String socialId;
    
    // 🆕 FCM 토큰 추가
    @Column(name = "fcm_token", length = 500)
    private String fcmToken;
    
    // Getter/Setter
    public void updateFcmToken(String fcmToken) {
        this.fcmToken = fcmToken;
    }
}
```

### **SQL Migration**

```sql
-- V5__add_fcm_token_to_user.sql
ALTER TABLE user 
ADD COLUMN fcm_token VARCHAR(500) NULL 
COMMENT 'Firebase Cloud Messaging 토큰';
```

---

## 🔧 **2. FCM 토큰 등록 API**

### **API 스펙**

```
PUT /api/user/fcm-token
Content-Type: application/json
Authorization: Bearer {JWT_TOKEN}

Request Body:
{
  "fcmToken": "fV3X5g9...[FCM 토큰 문자열]..."
}

Response (200 OK):
{
  "statusCode": 200,
  "message": "success",
  "data": {
    "userId": 1,
    "fcmToken": "fV3X5g9...",
    "updatedAt": "2025-11-25T14:30:00Z"
  }
}
```

### **Controller 구현**

```java
@RestController
@RequiredArgsConstructor
@RequestMapping("/api/user")
public class UserController {
    
    private final UserService userService;
    
    @PutMapping("/fcm-token")
    public ResponseEntity<SuccessResponse> updateFcmToken(
        @RequestBody FcmTokenRequest request,
        @AuthenticationPrincipal Long userId
    ) {
        userService.updateFcmToken(userId, request.getFcmToken());
        return ResponseEntity.ok(
            new SuccessResponse(HttpStatus.OK, "success", null)
        );
    }
}
```

### **DTO**

```java
@Getter
@NoArgsConstructor
public class FcmTokenRequest {
    @NotEmpty(message = "FCM 토큰은 필수입니다")
    private String fcmToken;
}
```

### **Service**

```java
@Service
@RequiredArgsConstructor
public class UserService {
    
    private final UserRepository userRepository;
    
    @Transactional
    public void updateFcmToken(Long userId, String fcmToken) {
        User user = userRepository.findById(userId)
            .orElseThrow(() -> new CustomException(ErrorCode.USER_NOT_FOUND));
        
        user.updateFcmToken(fcmToken);
        // JPA dirty checking으로 자동 업데이트
    }
}
```

---

## 📱 **3. FCM 알림 전송 서비스 구현**

### **의존성 추가 (build.gradle)**

```gradle
dependencies {
    // Firebase Admin SDK
    implementation 'com.google.firebase:firebase-admin:9.2.0'
}
```

### **Firebase 초기화 (Application.java)**

```java
@SpringBootApplication
public class YachtApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(YachtApplication.class, args);
    }
    
    @PostConstruct
    public void initializeFirebase() throws IOException {
        if (FirebaseApp.getApps().isEmpty()) {
            FirebaseOptions options = FirebaseOptions.builder()
                .setCredentials(GoogleCredentials.fromStream(
                    new ClassPathResource("firebase-service-account.json")
                        .getInputStream()
                ))
                .build();
            
            FirebaseApp.initializeApp(options);
        }
    }
}
```

### **FCM 알림 전송 서비스**

```java
@Service
@Slf4j
public class FcmService {
    
    /**
     * FCM 알림 전송
     * 
     * @param fcmToken 수신자의 FCM 토큰
     * @param title 알림 제목
     * @param body 알림 내용
     * @return 전송 성공 여부
     */
    public boolean sendNotification(String fcmToken, String title, String body) {
        if (fcmToken == null || fcmToken.isEmpty()) {
            log.warn("FCM 토큰이 없습니다.");
            return false;
        }
        
        try {
            Message message = Message.builder()
                .setToken(fcmToken)
                .setNotification(Notification.builder()
                    .setTitle(title)
                    .setBody(body)
                    .build())
                .setAndroidConfig(AndroidConfig.builder()
                    .setPriority(AndroidConfig.Priority.HIGH)
                    .build())
                .setApnsConfig(ApnsConfig.builder()
                    .setAps(Aps.builder()
                        .setSound("default")
                        .build())
                    .build())
                .build();
            
            String response = FirebaseMessaging.getInstance().send(message);
            log.info("FCM 알림 전송 성공: {}", response);
            return true;
            
        } catch (FirebaseMessagingException e) {
            log.error("FCM 알림 전송 실패: {}", e.getMessage());
            
            // 토큰 만료 시 DB에서 제거
            if (e.getErrorCode().equals("INVALID_ARGUMENT") || 
                e.getErrorCode().equals("REGISTRATION_TOKEN_NOT_REGISTERED")) {
                log.warn("FCM 토큰 만료됨. 토큰: {}", fcmToken);
                // TODO: DB에서 토큰 제거 로직
            }
            
            return false;
        }
    }
    
    /**
     * 여러 사용자에게 알림 전송
     */
    public void sendMultipleNotifications(
        List<String> fcmTokens, 
        String title, 
        String body
    ) {
        fcmTokens.stream()
            .filter(token -> token != null && !token.isEmpty())
            .forEach(token -> sendNotification(token, title, body));
    }
}
```

---

## ⏰ **4. 정비 일정 알림 스케줄러**

### **요구사항 (프론트엔드팀 요청)**

> - **알림 발송 시간**: 매일 오전 9시
> - **알림 대상**:
>   - 정비 예정일 **1주일 전** (7일 전)
>   - 정비 예정일 **1일 전**
>   - 정비 예정일 **당일**
> - **알림 내용**: "다가오는 정비 일정이 있습니다. 확인해주세요."
> - **백엔드 담당**: 권희님 (이권희)

### **스케줄러 구현**

```java
@Component
@RequiredArgsConstructor
@Slf4j
public class MaintenanceNotificationScheduler {
    
    private final CalendarEventRepository calendarRepository;
    private final PartRepository partRepository;
    private final YachtUserRepository yachtUserRepository;
    private final UserRepository userRepository;
    private final FcmService fcmService;
    
    /**
     * 매일 오전 9시에 정비 알림 전송
     */
    @Scheduled(cron = "0 0 9 * * *", zone = "Asia/Seoul")
    public void sendMaintenanceReminders() {
        log.info("정비 알림 스케줄러 시작");
        
        LocalDate today = LocalDate.now();
        LocalDate oneWeekLater = today.plusDays(7);
        LocalDate oneDayLater = today.plusDays(1);
        
        // 1주일 후 정비 일정 조회
        List<CalendarEvent> weekBeforeEvents = calendarRepository
            .findByStartDateBetween(oneWeekLater, oneWeekLater.plusDays(1));
        
        // 1일 후 정비 일정 조회
        List<CalendarEvent> dayBeforeEvents = calendarRepository
            .findByStartDateBetween(oneDayLater, oneDayLater.plusDays(1));
        
        // 당일 정비 일정 조회
        List<CalendarEvent> todayEvents = calendarRepository
            .findByStartDateBetween(today, today.plusDays(1));
        
        // 1주일 전 알림
        weekBeforeEvents.forEach(event -> 
            sendMaintenanceNotification(event, "1주일"));
        
        // 1일 전 알림
        dayBeforeEvents.forEach(event -> 
            sendMaintenanceNotification(event, "1일"));
        
        // 당일 알림
        todayEvents.forEach(event -> 
            sendMaintenanceNotification(event, "오늘"));
        
        log.info("정비 알림 스케줄러 종료: 1주일 전 {}건, 1일 전 {}건, 당일 {}건", 
            weekBeforeEvents.size(), dayBeforeEvents.size(), todayEvents.size());
    }
    
    /**
     * 정비 알림 전송
     */
    private void sendMaintenanceNotification(
        CalendarEvent calendarEvent, 
        String timeRemaining
    ) {
        try {
            // 부품 정보 조회
            Part part = calendarEvent.getPart();
            Yacht yacht = part.getYacht();
            
            // 해당 요트의 모든 사용자 조회
            List<YachtUser> yachtUsers = yachtUserRepository
                .findByYachtId(yacht.getId());
            
            // 알림 제목 & 내용
            String title = "HooAah";
            String body = String.format(
                "⚠️ 정비 일정 알림\n\n" +
                "요트: %s\n" +
                "부품: %s\n" +
                "정비 예정일: %s (%s 후)\n\n" +
                "앱에서 확인해주세요!",
                yacht.getName(),
                part.getName(),
                calendarEvent.getStartDate(),
                timeRemaining
            );
            
            // 각 사용자에게 알림 전송
            yachtUsers.forEach(yachtUser -> {
                User user = userRepository.findById(yachtUser.getUserId())
                    .orElse(null);
                
                if (user != null && user.getFcmToken() != null) {
                    boolean success = fcmService.sendNotification(
                        user.getFcmToken(), 
                        title, 
                        body
                    );
                    
                    if (!success) {
                        log.warn("알림 전송 실패: userId={}", user.getId());
                    }
                }
            });
            
        } catch (Exception e) {
            log.error("정비 알림 전송 중 오류: {}", e.getMessage());
        }
    }
}
```

### **Repository 추가 메서드**

```java
public interface CalendarEventRepository extends JpaRepository<CalendarEvent, Long> {
    
    /**
     * 특정 날짜 범위의 일정 조회
     */
    @Query("SELECT c FROM CalendarEvent c " +
           "WHERE c.startDate >= :startDate AND c.startDate < :endDate")
    List<CalendarEvent> findByStartDateBetween(
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate
    );
}
```

---

## 👥 **5. 참조인 초대 알림**

### **요구사항**

> 친구를 요트에 초대하면 해당 친구에게 알림 전송

### **초대 알림 구현**

```java
@Service
@RequiredArgsConstructor
public class YachtService {
    
    private final YachtUserRepository yachtUserRepository;
    private final UserRepository userRepository;
    private final FcmService fcmService;
    
    /**
     * 요트에 사용자 초대
     */
    @Transactional
    public void inviteUserToYacht(Long yachtId, Long invitedUserId, Long inviterId) {
        // 초대 로직 (기존 코드)
        YachtUser yachtUser = YachtUser.builder()
            .yachtId(yachtId)
            .userId(invitedUserId)
            .role("MEMBER")
            .build();
        
        yachtUserRepository.save(yachtUser);
        
        // 🆕 FCM 알림 전송
        User invitedUser = userRepository.findById(invitedUserId)
            .orElseThrow(() -> new CustomException(ErrorCode.USER_NOT_FOUND));
        
        User inviter = userRepository.findById(inviterId)
            .orElseThrow(() -> new CustomException(ErrorCode.USER_NOT_FOUND));
        
        Yacht yacht = yachtRepository.findById(yachtId)
            .orElseThrow(() -> new CustomException(ErrorCode.YACHT_NOT_FOUND));
        
        // 알림 내용
        String title = "HooAah";
        String body = String.format(
            "🎉 요트 초대 알림\n\n" +
            "%s님이 요트 '%s'에 참조인으로 초대했습니다!\n\n" +
            "앱에서 확인해주세요.",
            inviter.getName(),
            yacht.getName()
        );
        
        if (invitedUser.getFcmToken() != null) {
            fcmService.sendNotification(
                invitedUser.getFcmToken(), 
                title, 
                body
            );
        }
    }
}
```

---

## 🔧 **6. Part의 lastRepair 값 업데이트 API** ⭐ NEW

### **요구사항 (프론트엔드팀 지적)**

> **희성님**: "해당 part에 대한 last repair값을 변경해주는 api가 없긴하네요. 그래서 부품이랑 캘린더가 전체적으로 흐름 연결이 안됐던거같습니다"
>
> **권희님**: "repair값을 수정하면 같이 수정되게 하겠습니다"

### **문제점**

현재 **정비 후기 작성** 시 `Repair` 테이블에만 기록되고, 해당 부품(`Part`)의 `latestMaintenanceDate` 필드가 자동으로 업데이트되지 않습니다.

### **해결 방법**

정비 후기 작성 시 **Part 엔티티의 latestMaintenanceDate도 자동 업데이트**

---

### **API 스펙 (신규)**

#### **정비 후기 작성 + Part 업데이트**

```
POST /api/repair
Content-Type: application/json
Authorization: Bearer {JWT_TOKEN}

Request Body:
{
  "partId": 123,
  "repairDate": "2025-11-25",
  "content": "메인 할야드 정비 완료. 이상 없음.",
  "cost": 50000
}

Response (201 Created):
{
  "statusCode": 201,
  "message": "success",
  "data": {
    "id": 789,
    "partId": 123,
    "repairDate": "2025-11-25",
    "content": "메인 할야드 정비 완료. 이상 없음.",
    "cost": 50000,
    "updatedPart": {
      "id": 123,
      "latestMaintenanceDate": "2025-11-25"  // ✨ 자동 업데이트됨!
    }
  }
}
```

---

### **Service 구현**

```java
@Service
@RequiredArgsConstructor
public class RepairService {
    
    private final RepairRepository repairRepository;
    private final PartRepository partRepository;
    
    /**
     * 정비 후기 작성 + Part의 latestMaintenanceDate 자동 업데이트
     */
    @Transactional
    public RepairDto createRepair(RequestRepairDto request) {
        // 1. Repair 엔티티 생성
        Part part = partRepository.findById(request.getPartId())
            .orElseThrow(() -> new CustomException(ErrorCode.PART_NOT_FOUND));
        
        Repair repair = Repair.builder()
            .part(part)
            .repairDate(request.getRepairDate())
            .content(request.getContent())
            .cost(request.getCost())
            .build();
        
        repairRepository.save(repair);
        
        // 2. ✨ Part의 latestMaintenanceDate 자동 업데이트
        part.update(
            null,  // name
            null,  // manufacturer
            null,  // model
            null,  // interval
            request.getRepairDate()  // ✨ latestMaintenanceDate 업데이트!
        );
        
        log.info("정비 후기 작성 완료 + Part 업데이트: partId={}, date={}", 
            request.getPartId(), request.getRepairDate());
        
        return RepairDto.from(repair);
    }
}
```

---

### **Part 엔티티 update 메서드 (이미 구현됨)**

```java
@Entity
public class Part {
    // ... fields ...
    
    /**
     * 부품 정보 업데이트
     * null인 값은 업데이트하지 않음
     */
    public void update(String name, String manufacturer, String model, 
                      Integer interval, LocalDate latestMaintenanceDate) {
        if (name != null)
            this.name = name;
        if (manufacturer != null)
            this.manufacturer = manufacturer;
        if (model != null)
            this.model = model;
        if (interval != null)
            this.interval = interval;
        if (latestMaintenanceDate != null)
            this.latestMaintenanceDate = latestMaintenanceDate;  // ✨ 여기서 업데이트!
    }
}
```

---

### **전체 플로우**

```
1. 사용자가 정비 완료 후 "정비 후기 작성" 버튼 클릭

2. Flutter → POST /api/repair (포트 8080)
   {
     "partId": 123,
     "repairDate": "2025-11-25",
     "content": "메인 할야드 정비 완료",
     "cost": 50000
   }

3. Backend RepairService
   └─ Repair 엔티티 생성 (정비 후기 저장)
   └─ Part.update() 호출 → latestMaintenanceDate 업데이트 ✨
   └─ JPA dirty checking으로 자동 커밋

4. Backend → Response
   {
     "data": {
       "id": 789,
       "updatedPart": {
         "id": 123,
         "latestMaintenanceDate": "2025-11-25"
       }
     }
   }

5. Flutter
   └─ Part의 latestMaintenanceDate 업데이트
   └─ 다음 정비 일정 자동 계산 (interval 기반)
```

---

### **추가 개선 사항 (선택)**

정비 후기 작성 시 **다음 정비 일정도 자동으로 생성**할 수 있습니다:

```java
@Transactional
public RepairDto createRepair(RequestRepairDto request) {
    // ... 기존 코드 ...
    
    // ✨ 다음 정비 일정 자동 생성 (interval이 있을 때만)
    if (part.getInterval() != null && part.getInterval() > 0) {
        LocalDate nextMaintenanceDate = request.getRepairDate()
            .plusMonths(part.getInterval());
        
        // 기존 캘린더 일정 확인
        List<CalendarEvent> existingEvents = calendarRepository
            .findByPartId(part.getId());
        
        if (!existingEvents.isEmpty()) {
            // 기존 일정 수정
            CalendarEvent event = existingEvents.get(0);
            event.update(nextMaintenanceDate, nextMaintenanceDate, 
                "자동 생성: 다음 정비 예정일");
        } else {
            // 새 일정 생성
            CalendarEvent newEvent = CalendarEvent.builder()
                .part(part)
                .startDate(nextMaintenanceDate)
                .endDate(nextMaintenanceDate)
                .content("자동 생성: 다음 정비 예정일")
                .build();
            calendarRepository.save(newEvent);
        }
        
        log.info("다음 정비 일정 자동 생성: {}", nextMaintenanceDate);
    }
    
    return RepairDto.from(repair);
}
```

---

## 🧪 **7. FCM 알림 테스트** (기존과 동일)

### **Postman으로 FCM 토큰 등록**

```bash
PUT http://localhost:8080/api/user/fcm-token
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

{
  "fcmToken": "fV3X5g9hR8y:APA91bH..."
}
```

### **스케줄러 테스트 (수동 실행)**

```java
@RestController
@RequestMapping("/api/test")
@RequiredArgsConstructor
public class TestController {
    
    private final MaintenanceNotificationScheduler scheduler;
    
    /**
     * 스케줄러 수동 실행 (테스트용)
     */
    @PostMapping("/trigger-scheduler")
    public ResponseEntity<?> triggerScheduler() {
        scheduler.sendMaintenanceReminders();
        return ResponseEntity.ok("스케줄러 실행 완료");
    }
}
```

### **단일 알림 테스트 API**

```java
@RestController
@RequestMapping("/api/test")
@RequiredArgsConstructor
public class TestController {
    
    private final FcmService fcmService;
    
    @PostMapping("/send-test-notification")
    public ResponseEntity<?> sendTestNotification(
        @RequestParam String fcmToken
    ) {
        boolean success = fcmService.sendNotification(
            fcmToken,
            "HooAah",
            "테스트 알림입니다. FCM 연동이 정상적으로 작동합니다!"
        );
        
        return ResponseEntity.ok(Map.of(
            "success", success,
            "message", success ? "알림 전송 성공" : "알림 전송 실패"
        ));
    }
}
```

---

## 📋 **7. 체크리스트**

### **백엔드 개발 체크리스트**

- [ ] User 엔티티에 `fcmToken` 컬럼 추가
- [ ] SQL Migration 스크립트 작성
- [ ] `PUT /api/user/fcm-token` API 구현
- [ ] Firebase Admin SDK 의존성 추가
- [ ] `firebase-service-account.json` 파일 추가 (`.gitignore`에 등록!)
- [ ] `FcmService` 구현
- [ ] `MaintenanceNotificationScheduler` 구현
- [ ] `CalendarEventRepository.findByStartDateBetween()` 구현
- [ ] 요트 초대 시 알림 전송 로직 추가
- [ ] 테스트 API 작성 (수동 스케줄러 실행)
- [ ] 프론트엔드팀과 연동 테스트

### **프론트엔드 협업 필요 사항**

- [ ] Flutter 앱 시작 시 FCM 토큰 발급 → `PUT /api/user/fcm-token` 호출
- [ ] 토큰 만료 시 자동 갱신 로직
- [ ] 알림 수신 시 적절한 화면으로 라우팅

---

## 🚀 **8. 배포 시 주의사항**

### **Firebase 설정 파일 보안**

```bash
# .gitignore에 추가 필수!
src/main/resources/firebase-service-account.json
```

### **환경 변수로 관리 (권장)**

```yaml
# application.yml
firebase:
  service-account-path: ${FIREBASE_SERVICE_ACCOUNT_PATH:/etc/secrets/firebase-service-account.json}
```

### **스케줄러 타임존 확인**

```java
@Scheduled(cron = "0 0 9 * * *", zone = "Asia/Seoul")
```

---

## 📞 **문의사항**

FCM 알림 구현 관련 문의사항은 AI Chatbot Team 또는 프론트엔드팀(희성님)에게 연락 바랍니다.

---

**작성 완료일**: 2025-11-25  
**최종 업데이트**: 2025-11-25

