# 🔍 Frontend & Backend 문제점 분석 보고서

카카오톡 대화 내용과 GitHub 저장소 코드를 분석한 결과입니다.

**분석 일시**: 2025-01-19  
**저장소**: 
- Frontend: https://github.com/HooAah-Yacht/frontend.git
- Backend: https://github.com/HooAah-Yacht/backend.git

---

## 📋 발견된 문제점

### 1. ❌ **부품 추가 시 정비내용(content) UI 없음**

**문제:**
- 부품 추가 UI에 정비내용(content) 입력 필드가 없습니다.
- 카카오톡 대화에서 "부품 추가할 때 정비내용(content)를 받을 수 있는 부분이 있나요?"라고 질문했지만, 현재 UI에는 해당 필드가 없습니다.

**현재 상태:**
- `frontend/lib/widgets/yacht/create2/create_yacht_parts_registration_section.dart`
  - 장비명, 제조사명, 모델명, 최근 정비일, 정비 주기만 입력 가능
  - **정비내용(content) 필드 없음**

**해결 방안:**
- 카카오톡 대화에서 "부품에는 default로 들어가도 될듯합니다"라고 했으므로:
  1. **Option 1**: UI에 content 필드를 추가하지 않고, 백엔드에서 default 값으로 처리
  2. **Option 2**: UI에 content 필드를 추가 (선택사항)

**영향 파일:**
- `frontend/lib/widgets/yacht/create2/create_yacht_parts_registration_section.dart`
- `frontend/lib/models/yacht_part.dart`
- `backend/src/main/java/HooYah/Yacht/part/dto/request/AddPartDto.java` (content 필드 추가 필요)

---

### 2. ❌ **PartDto에 lastRepair 필드 없음**

**문제:**
- `PartDto.java`에 `lastRepair` 필드가 없습니다.
- 카카오톡 대화에서 "partDto.lastRepair = lastRepair!=null ? lastRepair.getRepairDate() : null;"로 수정했다고 했지만, 현재 코드에는 반영되지 않았습니다.

**현재 상태:**
```java
// backend/src/main/java/HooYah/Yacht/part/dto/response/PartDto.java
public class PartDto {
    private Long id;
    private String name;
    private String manufacturer;
    private String model;
    private Long interval;
    // ❌ lastRepair 필드 없음
}
```

**카카오톡 대화 내용:**
- "part.getLastRepair()로 고치면 잘 불러와져서"라고 했지만, `Part` 엔티티에는 `getLastRepair()` 메서드가 없습니다.
- 실제로는 `RepairPort.findLastRepair(part)`를 통해 조회해야 합니다.

**해결 방안:**
1. `PartDto`에 `lastRepair` 필드 추가
2. `PartDto.of()` 메서드에서 `RepairPort.findLastRepair(part)`를 호출하여 lastRepair 설정
3. 또는 쿼리에서 JOIN하여 한 번에 조회

**영향 파일:**
- `backend/src/main/java/HooYah/Yacht/part/dto/response/PartDto.java`
- `backend/src/main/java/HooYah/Yacht/part/service/PartService.java` (getParListByYacht 메서드)

---

### 3. ❌ **정비 이력 추가 시 part의 last_repair 날짜 업데이트 안됨**

**문제:**
- 정비 이력을 추가해도 `Part` 엔티티의 `last_repair` 날짜가 자동으로 업데이트되지 않습니다.
- 카카오톡 대화에서 "정비 이력 추가하면 part 부분에 last_repair 날짜 변경"이 필요하다고 했습니다.

**현재 상태:**
```java
// backend/src/main/java/HooYah/Yacht/repair/service/RepairService.java
@Transactional
public void addRepair(Long partId, OffsetDateTime repairDate, User user) {
    // ... repair 생성 및 저장
    repairRepository.save(repair);
    
    // ❌ part의 last_repair 업데이트 로직 없음
    updateCalenderAndAlarm(part);
}
```

**문제점:**
- `Part` 엔티티에 `last_repair` 필드가 없습니다.
- `Part` 엔티티는 `Repair`와 `@OneToMany` 관계이므로, 별도 필드 없이 `RepairPort.findLastRepair(part)`로 조회해야 합니다.
- 하지만 `PartDto`에 `lastRepair`를 반환하려면 매번 조회해야 하므로 성능 이슈가 있을 수 있습니다.

**해결 방안:**
1. **Option 1**: `Part` 엔티티에 `lastRepair` 필드 추가 (정규화 위반이지만 성능 향상)
2. **Option 2**: `PartDto`에서 `RepairPort.findLastRepair(part)`로 조회 (현재 방식 유지)
3. **Option 3**: 쿼리에서 JOIN하여 한 번에 조회 (권장)

**영향 파일:**
- `backend/src/main/java/HooYah/Yacht/part/domain/Part.java` (필드 추가 시)
- `backend/src/main/java/HooYah/Yacht/repair/service/RepairService.java`
- `backend/src/main/java/HooYah/Yacht/part/dto/response/PartDto.java`

---

### 4. ⚠️ **부품 삭제 기능 확인 필요**

**현재 상태:**
- `PartController`에 `deletePart` 메서드가 있습니다.
- 카카오톡 대화에서 "부품 삭제 안됨"이라고 했지만, 코드상으로는 구현되어 있습니다.

**확인 필요:**
- 실제로 삭제가 안 되는 이유 확인 필요
- 권한 체크 문제일 수 있음
- CASCADE 설정 문제일 수 있음

**영향 파일:**
- `backend/src/main/java/HooYah/Yacht/part/controller/PartController.java`
- `backend/src/main/java/HooYah/Yacht/part/service/PartService.java`

---

### 5. ⚠️ **정비 이력에 content 필드 없음**

**문제:**
- `Repair` 엔티티에 `content` 필드가 없습니다.
- 카카오톡 대화에서 "정비 이력 추가할 때만 필요한거같아요!"라고 했습니다.

**현재 상태:**
```java
// backend/src/main/java/HooYah/Yacht/repair/domain/Repair.java
public class Repair {
    private Long id;
    private User user;
    private Part part;
    private OffsetDateTime repairDate;
    // ❌ content 필드 없음
}
```

**해결 방안:**
- `Repair` 엔티티에 `content` 필드 추가
- `RequestRepairDto`에 `content` 필드 추가
- `RepairDto`에 `content` 필드 추가

**영향 파일:**
- `backend/src/main/java/HooYah/Yacht/repair/domain/Repair.java`
- `backend/src/main/java/HooYah/Yacht/repair/dto/RequestRepairDto.java`
- `backend/src/main/java/HooYah/Yacht/repair/dto/RepairDto.java`
- `backend/src/main/java/HooYah/Yacht/repair/service/RepairService.java`

---

## 🔧 수정이 필요한 파일 목록

### Backend

1. **`backend/src/main/java/HooYah/Yacht/part/dto/response/PartDto.java`**
   - `lastRepair` 필드 추가
   - `of()` 메서드 수정

2. **`backend/src/main/java/HooYah/Yacht/part/service/PartService.java`**
   - `getParListByYacht()` 메서드에서 lastRepair 조회 로직 추가

3. **`backend/src/main/java/HooYah/Yacht/repair/domain/Repair.java`**
   - `content` 필드 추가 (선택사항)

4. **`backend/src/main/java/HooYah/Yacht/repair/dto/RequestRepairDto.java`**
   - `content` 필드 추가 (선택사항)

5. **`backend/src/main/java/HooYah/Yacht/repair/dto/RepairDto.java`**
   - `content` 필드 추가 (선택사항)

6. **`backend/src/main/java/HooYah/Yacht/repair/service/RepairService.java`**
   - `addRepair()` 메서드에서 content 처리 (선택사항)

### Frontend

1. **`frontend/lib/widgets/yacht/create2/create_yacht_parts_registration_section.dart`**
   - 정비내용(content) 입력 필드 추가 (선택사항, default 값 사용 시 불필요)

2. **`frontend/lib/models/yacht_part.dart`**
   - `content` 필드 추가 (선택사항)

---

## 📝 우선순위

### 🔴 높음 (필수)
1. **PartDto에 lastRepair 필드 추가** - 프론트에서 날짜가 null로 불러와지는 문제 해결
2. **정비 이력 추가 시 part의 last_repair 업데이트** - 데이터 일관성 유지

### 🟡 중간 (권장)
3. **정비 이력에 content 필드 추가** - 사용자 요구사항 반영
4. **부품 삭제 기능 확인 및 수정** - 실제 동작 확인 필요

### 🟢 낮음 (선택)
5. **부품 추가 시 정비내용(content) UI 추가** - default 값 사용 시 불필요

---

## 🚀 다음 단계

1. **Backend 수정**
   - PartDto에 lastRepair 필드 추가
   - PartService에서 lastRepair 조회 로직 추가
   - Repair 엔티티에 content 필드 추가 (선택)

2. **Frontend 수정**
   - PartDto의 lastRepair 필드 표시
   - 정비 이력 추가 UI에 content 필드 추가 (선택)

3. **테스트**
   - 부품 조회 시 lastRepair 날짜 정상 표시 확인
   - 정비 이력 추가 시 part의 last_repair 업데이트 확인
   - 부품 삭제 기능 동작 확인

---

## 📚 참고

- 카카오톡 대화 내용 기반 분석
- GitHub 저장소 코드 분석
- Pull Request #11 참고: https://github.com/HooAah-Yacht/backend/pull/11

---

**작성자**: AI Assistant  
**최종 업데이트**: 2025-01-19

