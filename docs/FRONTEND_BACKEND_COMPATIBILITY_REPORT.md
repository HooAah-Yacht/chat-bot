# Frontend-Backend 호환성 분석 보고서

## 📅 분석 일시

2024-11-12

## 🔍 분석 개요

프론트엔드(Flutter)와 백엔드(Spring Boot) 간의 API 호환성 및 데이터 구조 일치 여부를 분석합니다.

---

## ✅ 호환성 검증 결과

### 1. **Auth API (인증 관련)** ✅ 완벽 호환

#### 프론트엔드 요청

| 엔드포인트                               | 메서드 | 요청 데이터               | 응답 데이터                         |
| ---------------------------------------- | ------ | ------------------------- | ----------------------------------- |
| `/public/user/login`                     | POST   | `{email, password}`       | `{token}`                           |
| `/public/user/email-check?email={email}` | GET    | Query Parameter           | `{message: "exist" \| "not exist"}` |
| `/public/user/register`                  | POST   | `{name, email, password}` | `{}`                                |

#### 백엔드 API

```java
@PostMapping("/public/user/login")
public ResponseEntity login(@RequestBody @Valid LoginDto dto) {
    // email, password 필드 필요
    return ResponseEntity.ok(Map.of("token", token));
}

@GetMapping("/public/user/email-check")
public ResponseEntity emailCheck(@RequestParam("email") String email) {
    // message: "exist" or "not exist"
}

@PostMapping("/public/user/register")
public ResponseEntity register(@RequestBody @Valid RegisterDto dto) {
    // name, email, password 필드 필요
}
```

**✅ 결과**: **완벽하게 호환됨**

---

### 2. **Yacht & Part API (요트 및 부품 관리)** ⚠️ 부분 호환

#### 프론트엔드 요트 등록 Payload

**프론트엔드** (`create2_yacht_screen.dart` 78-93번 라인):

```dart
final payload = {
  'yachtName': 'Farr 40',            // 요트 종류
  'yachtAlias': '내 요트',           // 요트 별칭
  'parts': [
    {
      'name': 'Impeller',                      // 부품명
      'manufacturer': 'Yamaha',                // 제조사
      'model': '6CE-44352-00',                 // 모델명
      'latestMaintenanceDate': '2024-03-02',   // 최근 정비일 (ISO8601)
      'interval': 12,                          // 정비 주기 (개월)
    }
  ]
};
```

#### 백엔드 API

**Yacht Controller**:

```java
// ❌ 현재 백엔드에 요트 생성 + 부품 동시 등록 API 없음
// 백엔드에는 다음 API들이 있음:
POST /api/yacht        // 요트 생성 (YachtController - feat/yachthappy에 있음)
POST /api/part         // 부품 추가
```

**Part DTO** (`AddPartDto.java`):

```java
public class AddPartDto {
    private Long yachtId;      // 요트 ID (외래키)
    private String name;       // 부품명
    private String manufacturer; // 제조사
    private String model;      // 모델명
    private Long interval;     // 정비 주기 (Long 타입)
    // ❌ latestMaintenanceDate 필드 없음
}
```

**Yacht DTO** (`CreateYachtDto.java` - 확인 필요):

```java
// 아마도 이런 구조일 것으로 예상:
public class CreateYachtDto {
    private String name;
    private String alias;
    // parts 필드는 없을 것으로 예상
}
```

---

## ⚠️ 발견된 문제점

### 문제 1: **요트 등록 API 불일치**

**프론트엔드 기대 동작**:

```
POST /api/yacht/register (추정)
{
  "yachtName": "Farr 40",
  "yachtAlias": "내 요트",
  "parts": [...]
}
→ 요트와 부품을 한 번에 등록
```

**백엔드 현재 구조**:

```
1. POST /api/yacht          // 요트만 생성
2. POST /api/part (여러 번) // 각 부품마다 별도 요청
```

**📌 해결 방안**:

#### 옵션 A: 백엔드에 통합 API 추가 (권장)

```java
@PostMapping("/api/yacht/register")
public ResponseEntity registerYachtWithParts(
    @RequestBody CreateYachtWithPartsDto dto,
    @AuthenticationPrincipal User user
) {
    // 요트 생성 + 부품 일괄 등록
    YachtDto yacht = yachtService.createYachtWithParts(dto, user);
    return ResponseEntity.ok(yacht);
}
```

**CreateYachtWithPartsDto.java**:

```java
public class CreateYachtWithPartsDto {
    private String yachtName;
    private String yachtAlias;
    private List<PartInfo> parts;

    @Data
    public static class PartInfo {
        private String name;
        private String manufacturer;
        private String model;
        private LocalDate latestMaintenanceDate;  // ← 추가 필요
        private Integer interval;  // Long → Integer
    }
}
```

#### 옵션 B: 프론트엔드를 2단계 요청으로 수정

```dart
// 1. 요트 생성
final yachtResponse = await http.post('/api/yacht', body: {
  'name': yachtName,
  'alias': yachtAlias,
});
final yachtId = yachtResponse['id'];

// 2. 부품 일괄 등록
for (var part in parts) {
  await http.post('/api/part', body: {
    'yachtId': yachtId,
    ...part,
  });
}
```

---

### 문제 2: **Part DTO 필드 불일치**

| 필드                    | 프론트엔드          | 백엔드 AddPartDto | 상태                |
| ----------------------- | ------------------- | ----------------- | ------------------- |
| `yachtId`               | ❌ 없음 (payload에) | ✅ 있음           | ⚠️ 백엔드 필요      |
| `name`                  | ✅ 있음             | ✅ 있음           | ✅ 일치             |
| `manufacturer`          | ✅ 있음             | ✅ 있음           | ✅ 일치             |
| `model`                 | ✅ 있음             | ✅ 있음           | ✅ 일치             |
| `latestMaintenanceDate` | ✅ 있음 (ISO8601)   | ❌ 없음           | ⚠️ 백엔드 추가 필요 |
| `interval`              | ✅ 있음 (int)       | ✅ 있음 (Long)    | ⚠️ 타입 차이        |

**📌 해결 방안**:

**AddPartDto.java 수정**:

```java
public class AddPartDto {
    private Long yachtId;
    private String name;
    private String manufacturer;
    private String model;
    private LocalDate latestMaintenanceDate;  // ← 추가
    private Integer interval;  // Long → Integer 변경
}
```

---

### 문제 3: **API 베이스 URL**

**프론트엔드** (`auth_service.dart` 8번 라인):

```dart
static const String baseUrl = 'http://localhost:8080';
```

**✅ 개발 환경에서는 정상 작동**

**⚠️ 프로덕션 배포 시 변경 필요**:

```dart
// 환경 변수 또는 설정 파일로 관리
static const String baseUrl = String.fromEnvironment(
  'API_BASE_URL',
  defaultValue: 'http://localhost:8080',
);
```

---

## 📊 데이터 모델 비교

### 프론트엔드 YachtPart 모델

```dart
class YachtPart {
  final String equipmentName;           // 부품명
  final String manufacturerName;        // 제조사
  final String modelName;               // 모델명
  final DateTime latestMaintenanceDate; // 최근 정비일
  final int maintenancePeriodInMonths;  // 정비 주기
}
```

### 백엔드 Part Entity (추정)

```java
@Entity
public class Part {
    @Id
    @GeneratedValue
    private Long id;

    @ManyToOne
    private Yacht yacht;  // 요트와의 관계

    private String name;
    private String manufacturer;
    private String model;
    private LocalDate latestMaintenanceDate;  // ← 추가 필요
    private Integer interval;

    // ... getters, setters
}
```

---

## 🔧 권장 수정 사항

### 백엔드 수정 (우선순위 높음)

#### 1. **AddPartDto.java 수정**

```java
package HooYah.Yacht.part.dto.request;

import java.time.LocalDate;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@NoArgsConstructor
@Getter
@Setter
public class AddPartDto {
    private Long yachtId;
    private String name;
    private String manufacturer;
    private String model;
    private LocalDate latestMaintenanceDate;  // ✨ 추가
    private Integer interval;  // Long → Integer
}
```

#### 2. **Part Entity 수정** (Repository/Domain에 추가)

```java
@Entity
public class Part {
    // ... 기존 필드

    @Column(name = "latest_maintenance_date")
    private LocalDate latestMaintenanceDate;  // ✨ 추가

    @Column(name = "maintenance_interval")
    private Integer interval;
}
```

#### 3. **통합 요트 등록 API 추가** (선택사항, 권장)

**CreateYachtWithPartsDto.java** (신규 생성):

```java
package HooYah.Yacht.yacht.dto.request;

import java.time.LocalDate;
import java.util.List;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@NoArgsConstructor
@Getter
@Setter
public class CreateYachtWithPartsDto {
    private String yachtName;
    private String yachtAlias;
    private List<PartInfo> parts;

    @Getter
    @Setter
    @NoArgsConstructor
    public static class PartInfo {
        private String name;
        private String manufacturer;
        private String model;
        private LocalDate latestMaintenanceDate;
        private Integer interval;
    }
}
```

**YachtController.java 메서드 추가**:

```java
@PostMapping("/api/yacht/register")
public ResponseEntity registerYachtWithParts(
    @RequestBody @Valid CreateYachtWithPartsDto dto,
    @AuthenticationPrincipal User user
) {
    // 1. 요트 생성
    Yacht yacht = yachtService.createYacht(dto.getYachtName(), dto.getYachtAlias(), user);

    // 2. 부품 일괄 등록
    for (CreateYachtWithPartsDto.PartInfo partInfo : dto.getParts()) {
        partService.addPart(yacht.getId(), partInfo, user);
    }

    return ResponseEntity.ok(new SuccessResponse(HttpStatus.OK, "success", null));
}
```

---

### 프론트엔드 수정 (우선순위 낮음)

#### 1. **API 서비스 파일 생성**

**`lib/services/yacht_service.dart`** (신규 생성):

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'auth_service.dart';

class YachtService {
  static const String baseUrl = AuthService.baseUrl;

  /// 요트 + 부품 일괄 등록
  static Future<Map<String, dynamic>> registerYachtWithParts({
    required String yachtName,
    required String yachtAlias,
    required List<Map<String, dynamic>> parts,
  }) async {
    try {
      final token = await AuthService.getToken();
      if (token == null) {
        return {'success': false, 'message': '로그인이 필요합니다.'};
      }

      final url = '$baseUrl/api/yacht/register';
      final response = await http.post(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
        body: jsonEncode({
          'yachtName': yachtName,
          'yachtAlias': yachtAlias,
          'parts': parts,
        }),
      );

      if (response.statusCode == 200) {
        return {'success': true};
      }

      return {
        'success': false,
        'message': '요트 등록에 실패했습니다. (${response.statusCode})',
      };
    } catch (e) {
      return {
        'success': false,
        'message': '네트워크 오류가 발생했습니다.',
      };
    }
  }
}
```

#### 2. **create2_yacht_screen.dart 수정**

```dart
import '../services/yacht_service.dart';

void _handleRegister() async {
  final parts = _parts
      .map((part) => {
            'name': part.equipmentName,
            'manufacturer': part.manufacturerName,
            'model': part.modelName,
            'latestMaintenanceDate': part.latestMaintenanceDate.toIso8601String().split('T')[0],
            'interval': part.maintenancePeriodInMonths,
          })
      .toList();

  final result = await YachtService.registerYachtWithParts(
    yachtName: widget.yachtName,
    yachtAlias: widget.yachtAlias,
    parts: parts,
  );

  if (!mounted) return;

  if (result['success']) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('요트가 성공적으로 등록되었습니다!')),
    );
    Navigator.of(context).popUntil((route) => route.isFirst);
  } else {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(result['message'] ?? '요트 등록에 실패했습니다.'),
        backgroundColor: Colors.red,
      ),
    );
  }
}
```

---

## 🧪 테스트 시나리오

### 1. **Auth API 테스트**

```bash
# 회원가입
curl -X POST http://localhost:8080/public/user/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "홍길동",
    "email": "test@example.com",
    "password": "password123"
  }'

# 로그인
curl -X POST http://localhost:8080/public/user/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'

# 이메일 중복 확인
curl -X GET "http://localhost:8080/public/user/email-check?email=test@example.com"
```

### 2. **Yacht + Part API 테스트** (수정 후)

```bash
# 요트 + 부품 일괄 등록
curl -X POST http://localhost:8080/api/yacht/register \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "yachtName": "Farr 40",
    "yachtAlias": "내 요트",
    "parts": [
      {
        "name": "Impeller",
        "manufacturer": "Yamaha",
        "model": "6CE-44352-00",
        "latestMaintenanceDate": "2024-03-02",
        "interval": 12
      }
    ]
  }'
```

---

## 📝 체크리스트

### 백엔드 (Spring Boot)

- [ ] `AddPartDto.java`에 `latestMaintenanceDate` 필드 추가
- [ ] `Part` Entity에 `latestMaintenanceDate` 필드 추가
- [ ] `CreateYachtWithPartsDto.java` 생성
- [ ] `YachtController`에 `/api/yacht/register` 엔드포인트 추가
- [ ] `YachtService`에 `createYachtWithParts` 메서드 구현
- [ ] 데이터베이스 마이그레이션 (ALTER TABLE 추가)
- [ ] 통합 테스트 작성

### 프론트엔드 (Flutter)

- [ ] `lib/services/yacht_service.dart` 생성
- [ ] `create2_yacht_screen.dart` API 연동 수정
- [ ] 에러 핸들링 개선
- [ ] 로딩 상태 UI 추가
- [ ] API 베이스 URL 환경 변수화

---

## 🚀 배포 전 확인사항

### 환경 설정

- [ ] 프론트엔드 API URL 프로덕션으로 변경
- [ ] 백엔드 CORS 설정 확인
- [ ] JWT Secret Key 환경 변수 설정
- [ ] 데이터베이스 연결 정보 확인

### 보안

- [ ] HTTPS 적용
- [ ] JWT 토큰 만료 시간 설정
- [ ] 비밀번호 암호화 확인 (BCrypt)
- [ ] SQL Injection 방어 확인

---

## 📊 최종 판정

| 항목            | 상태         | 비고                                    |
| --------------- | ------------ | --------------------------------------- |
| **Auth API**    | ✅ 호환      | 로그인, 회원가입, 이메일 확인 모두 정상 |
| **Yacht API**   | ⚠️ 부분 호환 | 통합 등록 API 필요                      |
| **Part API**    | ⚠️ 부분 호환 | `latestMaintenanceDate` 필드 추가 필요  |
| **데이터 타입** | ⚠️ 주의      | `interval`: Long vs Integer             |
| **보안**        | ✅ 정상      | JWT 기반 인증 구현됨                    |

---

## 🎯 우선순위 작업 순서

### Phase 1: 즉시 수정 (필수)

1. ✅ `AddPartDto.java`에 `latestMaintenanceDate` 추가
2. ✅ `Part` Entity 필드 추가
3. ✅ 데이터베이스 스키마 업데이트

### Phase 2: API 통합 (권장)

4. ✅ `CreateYachtWithPartsDto` 생성
5. ✅ Yacht 통합 등록 API 구현
6. ✅ 프론트엔드 API 서비스 생성

### Phase 3: 테스트 & 배포

7. ✅ 통합 테스트 작성
8. ✅ E2E 테스트 수행
9. ✅ 프로덕션 배포

---

**작성자**: AI Assistant  
**분석 기준**: feat/yachthappy 브랜치 (백엔드), main 브랜치 (프론트엔드)  
**상태**: ⚠️ 수정 필요 (Auth는 정상, Yacht/Part API 개선 필요)
