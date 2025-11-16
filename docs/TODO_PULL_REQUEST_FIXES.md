# 🎯 Pull Request 리뷰 및 수정 사항 종합

## 📋 현재 상황 분석

### ✅ 이미 완료된 작업
- [x] feat/part 브랜치에서 Part, Repair 모듈 통합 완료
- [x] feat/calendar 브랜치에서 Calendar 모듈 통합 완료  
- [x] Controller, Service, DTO 모두 추가 완료
- [x] 총 19개 파일 통합 (Staged 상태)

### ⚠️ 수정 필요 사항 (Frontend 호환성)
기존 `REQUIRED_CHANGES.md`와 `FRONTEND_BACKEND_COMPATIBILITY_REPORT.md`에서 파악된 문제점:

---

## 🔧 우선순위별 수정 사항

### 🔴 High Priority - 즉시 수정 필요

#### 1. Part Entity에 `latestMaintenanceDate` 필드 추가

**문제점**:
Frontend가 부품 등록 시 `latestMaintenanceDate`를 보내지만, Backend Entity에 해당 필드가 없음

**수정 위치**: `backend/src/main/java/HooYah/Yacht/part/domain/Part.java`

**수정 내용**:
```java
@Entity
public class Part {
    // 기존 필드들...
    
    @Column(name = "latest_maintenance_date")
    private LocalDate latestMaintenanceDate;  // ← 추가
    
    // getter, setter 추가
}
```

**관련 DTO 수정**:
- `AddPartDto.java` - latestMaintenanceDate 필드 추가
- `PartDto.java` - latestMaintenanceDate 필드 추가
- `UpdatePartDto.java` - latestMaintenanceDate 필드 추가

---

#### 2. Yacht Entity에 `alias` 필드 추가

**문제점**:
Frontend가 요트 등록 시 `yachtAlias` (사용자 지정 별명)를 보내지만, Backend Entity에 해당 필드가 없음

**수정 위치**: `backend/src/main/java/HooYah/Yacht/yacht/domain/Yacht.java`

**수정 내용**:
```java
@Entity
public class Yacht {
    @Column(name = "name")
    private String name;  // 공식 요트 이름 (예: "Farr 40")
    
    @Column(name = "alias")
    private String alias;  // 사용자 지정 별명 (예: "내 요트") ← 추가
    
    // getter, setter 추가
}
```

**관련 DTO 수정**:
- `CreateYachtDto.java` - `yachtAlias` 필드 추가
- `ResponseYachtDto.java` - `alias` 필드 추가
- `UpdateYachtDto.java` - `alias` 필드 추가

---

#### 3. Yacht 통합 등록 API 추가

**문제점**:
Frontend는 요트 생성 + 부품 등록을 한 번에 하는 API를 호출하지만, Backend에 해당 엔드포인트가 없음

**Frontend 요청**:
```dart
POST /api/yacht
{
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
}
```

**수정 위치**: `backend/src/main/java/HooYah/Yacht/yacht/controller/YachtController.java`

**추가 DTO 필요**:
```java
// CreateYachtWithPartsDto.java
public class CreateYachtWithPartsDto {
    private String yachtName;
    private String yachtAlias;
    private List<AddPartDto> parts;
}
```

**추가 Service 메서드**:
```java
// YachtService.java
@Transactional
public ResponseYachtDto createYachtWithParts(CreateYachtWithPartsDto dto, String username) {
    // 1. Yacht 생성
    // 2. Parts 생성
    // 3. 관계 설정
    // 4. 저장
}
```

---

### 🟡 Medium Priority - 단기 수정

#### 4. yacht_parts_database.json 데이터를 DB에 로드

**목적**: 앱에서 요트 선택 시 해당 요트의 기본 부품 정보를 불러올 수 있도록

**작업 내용**:
1. `YachtTemplate` Entity 생성 (요트 템플릿)
2. `PartTemplate` Entity 생성 (부품 템플릿)
3. JSON 데이터를 DB에 Import하는 스크립트 작성
4. API 엔드포인트 추가: `GET /api/yacht-templates/{yachtId}/parts`

**스크립트 위치**: `backend/scripts/import_yacht_parts_to_db.py`

---

#### 5. yacht_specifications.json 데이터를 DB에 로드

**목적**: 앱에서 요트 스펙 정보를 조회할 수 있도록

**작업 내용**:
1. `YachtSpecification` Entity 생성
2. JSON 데이터를 DB에 Import
3. API 엔드포인트 추가: `GET /api/specifications/{yachtId}`

---

#### 6. 디자인 시스템 적용 (후아_디자인.pdf)

**작업 내용**:
1. 디자인 PDF에서 색상 스키마 추출
2. Frontend `lib/theme/` 디렉토리에 테마 파일 생성
3. 컴포넌트 스타일 가이드 작성
4. 공통 위젯 라이브러리 구축

**우선 작업**:
- 색상 팔레트 정의
- Typography 설정
- 버튼/카드/입력 필드 공통 스타일

---

### 🟢 Low Priority - 장기 작업

#### 7. API 문서화 (Swagger/OpenAPI)

**작업 내용**:
```yaml
# application.yml
springdoc:
  api-docs:
    path: /api-docs
  swagger-ui:
    path: /swagger-ui.html
```

**추가 dependency** (`build.gradle`):
```gradle
implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:2.2.0'
```

---

#### 8. Schedule 모듈 구현

**현재 상태**: Domain, Repository만 존재
**필요 작업**: Controller, Service, DTO 구현

---

#### 9. 통합 테스트 작성

**작업 내용**:
- Unit Tests for Services
- Integration Tests for Controllers
- E2E Tests with Frontend

---

## 📝 구체적인 파일별 수정 계획

### 파일 1: `backend/src/main/java/HooYah/Yacht/part/domain/Part.java`

```java
// 추가할 내용:
import java.time.LocalDate;

@Column(name = "latest_maintenance_date")
private LocalDate latestMaintenanceDate;

public LocalDate getLatestMaintenanceDate() {
    return latestMaintenanceDate;
}

public void setLatestMaintenanceDate(LocalDate latestMaintenanceDate) {
    this.latestMaintenanceDate = latestMaintenanceDate;
}
```

---

### 파일 2: `backend/src/main/java/HooYah/Yacht/part/dto/request/AddPartDto.java`

```java
// 추가할 내용:
import java.time.LocalDate;

@JsonProperty("latestMaintenanceDate")
private LocalDate latestMaintenanceDate;

public LocalDate getLatestMaintenanceDate() {
    return latestMaintenanceDate;
}

public void setLatestMaintenanceDate(LocalDate latestMaintenanceDate) {
    this.latestMaintenanceDate = latestMaintenanceDate;
}
```

---

### 파일 3: `backend/src/main/java/HooYah/Yacht/part/dto/response/PartDto.java`

```java
// 추가할 내용:
import java.time.LocalDate;

@JsonProperty("latestMaintenanceDate")
private LocalDate latestMaintenanceDate;

// getter/setter 추가
```

---

### 파일 4: `backend/src/main/java/HooYah/Yacht/part/service/PartService.java`

```java
// PartService.addPart() 메서드 수정
public PartDto addPart(AddPartDto dto, String username) {
    // ...
    
    // latestMaintenanceDate 설정 추가
    if (dto.getLatestMaintenanceDate() != null) {
        part.setLatestMaintenanceDate(dto.getLatestMaintenanceDate());
    }
    
    // ...
}

// toDto() 메서드에도 추가
private PartDto toDto(Part part) {
    PartDto dto = new PartDto();
    // ...
    dto.setLatestMaintenanceDate(part.getLatestMaintenanceDate());
    return dto;
}
```

---

### 파일 5: `backend/src/main/java/HooYah/Yacht/yacht/domain/Yacht.java`

```java
// 추가할 내용:
@Column(name = "alias", length = 100)
private String alias;

public String getAlias() {
    return alias;
}

public void setAlias(String alias) {
    this.alias = alias;
}
```

---

### 파일 6: `backend/src/main/java/HooYah/Yacht/yacht/dto/request/CreateYachtDto.java`

```java
// 추가할 내용:
@JsonProperty("yachtAlias")
private String yachtAlias;

public String getYachtAlias() {
    return yachtAlias;
}

public void setYachtAlias(String yachtAlias) {
    this.yachtAlias = yachtAlias;
}
```

---

### 파일 7: `backend/src/main/java/HooYah/Yacht/yacht/dto/response/ResponseYachtDto.java`

```java
// 추가할 내용:
@JsonProperty("alias")
private String alias;

// getter/setter 추가
```

---

### 파일 8: (신규) `backend/src/main/java/HooYah/Yacht/yacht/dto/request/CreateYachtWithPartsDto.java`

```java
package HooYah.Yacht.yacht.dto.request;

import HooYah.Yacht.part.dto.request.AddPartDto;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

import java.util.List;

@Data
public class CreateYachtWithPartsDto {
    
    @NotBlank(message = "Yacht name is required")
    @JsonProperty("yachtName")
    private String yachtName;
    
    @JsonProperty("yachtAlias")
    private String yachtAlias;
    
    @JsonProperty("parts")
    @Valid
    private List<AddPartDto> parts;
}
```

---

### 파일 9: `backend/src/main/java/HooYah/Yacht/yacht/controller/YachtController.java`

```java
// 추가할 메서드:
@PostMapping
@ResponseStatus(HttpStatus.CREATED)
public ResponseEntity<ResponseYachtDto> createYachtWithParts(
        @Valid @RequestBody CreateYachtWithPartsDto dto,
        Authentication authentication) {
    String username = authentication.getName();
    ResponseYachtDto result = yachtService.createYachtWithParts(dto, username);
    return ResponseEntity.ok(result);
}
```

---

### 파일 10: `backend/src/main/java/HooYah/Yacht/yacht/service/YachtService.java`

```java
// 추가할 메서드:
import HooYah.Yacht.part.domain.Part;
import HooYah.Yacht.part.dto.request.AddPartDto;

@Transactional
public ResponseYachtDto createYachtWithParts(CreateYachtWithPartsDto dto, String username) {
    // 1. User 조회
    User user = userRepository.findByEmail(username)
        .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "User not found"));
    
    // 2. Yacht 생성
    Yacht yacht = new Yacht();
    yacht.setName(dto.getYachtName());
    yacht.setAlias(dto.getYachtAlias());
    yacht.setUser(user);
    Yacht savedYacht = yachtRepository.save(yacht);
    
    // 3. Parts 생성 (if provided)
    if (dto.getParts() != null && !dto.getParts().isEmpty()) {
        for (AddPartDto partDto : dto.getParts()) {
            Part part = new Part();
            part.setName(partDto.getName());
            part.setManufacturer(partDto.getManufacturer());
            part.setModel(partDto.getModel());
            part.setLatestMaintenanceDate(partDto.getLatestMaintenanceDate());
            part.setInterval(partDto.getInterval());
            part.setYacht(savedYacht);
            partRepository.save(part);
        }
    }
    
    // 4. Response 생성
    return toResponseDto(savedYacht);
}
```

---

## ✅ 작업 체크리스트

### Phase 1: 즉시 수정 (오늘)
- [ ] Part Entity에 `latestMaintenanceDate` 추가
- [ ] Part DTOs에 `latestMaintenanceDate` 추가
- [ ] PartService 수정
- [ ] Yacht Entity에 `alias` 추가
- [ ] Yacht DTOs에 `alias/yachtAlias` 추가
- [ ] `CreateYachtWithPartsDto` 생성
- [ ] YachtController에 통합 생성 API 추가
- [ ] YachtService에 통합 생성 로직 추가

### Phase 2: 단기 작업 (내일~모레)
- [ ] yacht_parts_database.json DB Import
- [ ] yacht_specifications.json DB Import
- [ ] 디자인 시스템 색상 추출 및 적용

### Phase 3: 장기 작업 (이번 주)
- [ ] Swagger 문서화
- [ ] Schedule 모듈 구현
- [ ] 통합 테스트 작성

---

## 🚀 Git 작업 순서

### 1. 현재 Staged 파일 커밋
```bash
git commit -m "feat: Integrate Part, Repair, Calendar modules from feat/part and feat/calendar"
```

### 2. Frontend 호환성 수정
```bash
# 수정 작업 진행
git add .
git commit -m "fix: Add latestMaintenanceDate to Part and alias to Yacht for frontend compatibility"
```

### 3. 통합 생성 API 추가
```bash
git add .
git commit -m "feat: Add createYachtWithParts API endpoint"
```

### 4. Push
```bash
git push origin feat/yachthappy
```

---

## 📞 팀 협업 체크

### Pull Request #3 (feat/calendar by pu2rile)
- ✅ 통합 완료
- 📝 리뷰 완료 후 PR 승인 필요

### Pull Request #4 (feat/part by kwonhee1)
- ✅ 통합 완료
- ⚠️ `latestMaintenanceDate` 추가 필요 → 이슈 코멘트 남기기
- 📝 리뷰 완료 후 PR 승인 필요

---

## 📊 완료 후 예상 상태

```
✅ Part Module:     Domain ✅  Repository ✅  Controller ✅  Service ✅  DTO ✅
✅ Repair Module:   Domain ✅  Repository ✅  Controller ✅  Service ✅  DTO ✅
✅ Calendar Module: Domain ✅  Repository ✅  Controller ✅  Service ✅  DTO ✅
✅ Yacht Module:    Domain ✅  Repository ✅  Controller ✅  Service ✅  DTO ✅
⏳ Schedule Module: Domain ✅  Repository ✅  Controller ⏳  Service ⏳  DTO ⏳
✅ Config:          OffsetDateTimeConfig ✅
✅ Frontend 호환:   Part ✅  Yacht ✅  Calendar ✅  Repair ✅
✅ 데이터베이스:    yacht_parts ✅  yacht_specifications ✅
```

---

**Last Updated**: 2024-11-15  
**Priority**: High  
**Estimated Time**: Phase 1 (2-3 hours), Phase 2 (1 day), Phase 3 (2-3 days)  
**Next Action**: Phase 1 수정 사항 즉시 구현

