# Pull Request 리뷰 수정 사항

## 📋 첨부 파일 분석 결과

### 풀리퀘스트1.pdf (PR #4 - feat/part by kwonhee1)
- **브랜치**: feat/part
- **작성자**: kwonhee1
- **상태**: Review Required

### 풀리퀘스트3.pdf (PR #3 - feat/calendar by pu2rile)
- **브랜치**: feat/calendar  
- **작성자**: pu2rile
- **상태**: Review Required

### 후아_디자인(1).pdf
- **디자인 스펙 및 UI/UX 가이드**

### PNG 이미지
- 우측 상단에 보이는 Pull Request 목록

---

## 🔧 수정해야 할 내용

### 1. Pull Request #4 - Part 모듈 통합 (feat/part)

#### 📌 필요한 작업:
- [ ] **Part Entity 리뷰 및 수정**
  - 기존 `Part.java`와 새로운 Part 모듈간의 충돌 확인
  - yacht_parts_database.json과 매칭되는 스키마 검증
  
- [ ] **Part Controller 검토**
  - RESTful API 엔드포인트 확인
  - DTO 구조 검증
  
- [ ] **Service 로직 리뷰**
  - 비즈니스 로직 검증
  - 예외 처리 확인

#### 📝 예상 충돌 지점:
```java
// 기존 Part Entity와 새로운 Part 모듈 간의 필드 불일치 가능성
// yacht_parts_database.json의 구조와 맞춰야 함
```

---

### 2. Pull Request #3 - Calendar 모듈 (feat/calendar)

#### 📌 필요한 작업:
- [ ] **Calendar Entity 통합**
  - 정비 일정 관리 기능
  - 이벤트 타입 정의
  
- [ ] **Calendar Controller API**
  - CRUD 엔드포인트 검증
  - 날짜/시간 처리 로직 확인
  
- [ ] **Frontend 연동 준비**
  - DTO 구조가 Flutter 앱과 호환되는지 확인

---

### 3. 디자인 가이드 (후아_디자인.pdf) 반영

#### 📌 필요한 작업:
- [ ] **UI 컴포넌트 색상 스키마**
  - 디자인 시스템의 색상 코드 확인
  - Frontend에 적용
  
- [ ] **레이아웃 구조**
  - 화면별 레이아웃 스펙 반영
  - 반응형 디자인 고려
  
- [ ] **아이콘 및 이미지 리소스**
  - 디자인에 명시된 아이콘 확인
  - 이미지 에셋 준비

---

### 4. Backend 통합 작업

#### 📌 필요한 작업:
- [ ] **feat/yachthappy와 feat/part 병합**
  - Part 모듈을 현재 브랜치에 통합
  - 충돌 해결
  
- [ ] **feat/yachthappy와 feat/calendar 병합**
  - Calendar 모듈을 현재 브랜치에 통합
  - 충돌 해결
  
- [ ] **통합 테스트**
  - 모든 모듈이 정상 작동하는지 확인
  - API 엔드포인트 테스트

---

### 5. 데이터베이스 스키마 업데이트

#### 📌 필요한 작업:
- [ ] **Yacht Specification 테이블 추가**
  - yacht_specifications.json 데이터를 DB에 로드
  - Entity 클래스 생성
  
- [ ] **Part 테이블 스키마 확인**
  - yacht_parts_database.json과 일치 여부 검증
  - 인덱스 및 제약조건 추가
  
- [ ] **Calendar 테이블 설계**
  - 정비 일정 관리를 위한 스키마
  - Yacht 및 Part와의 관계 설정

---

### 6. API 문서화

#### 📌 필요한 작업:
- [ ] **Swagger/OpenAPI 스펙 작성**
  - 모든 엔드포인트 문서화
  - Request/Response 예시 추가
  
- [ ] **Postman Collection 생성**
  - API 테스트를 위한 컬렉션
  - 환경 변수 설정

---

### 7. Frontend 호환성 검증

#### 📌 필요한 작업:
- [ ] **Flutter 모델 클래스 업데이트**
  - Backend DTO와 일치하는 Dart 모델
  - JSON 직렬화/역직렬화 확인
  
- [ ] **API 서비스 클래스 작성**
  - HTTP 클라이언트 설정
  - 에러 처리 로직
  
- [ ] **디자인 시스템 적용**
  - 후아_디자인.pdf의 스펙 반영
  - 컴포넌트 라이브러리 구축

---

## 🎯 우선순위

### High Priority (즉시 수행)
1. **Pull Request 리뷰 및 승인** (PR #3, #4)
2. **Backend 모듈 통합** (Part, Calendar)
3. **데이터베이스 스키마 정리**

### Medium Priority (단기)
4. **디자인 시스템 적용**
5. **API 문서화**

### Low Priority (장기)
6. **Frontend 통합 테스트**
7. **성능 최적화**

---

## 📝 상세 작업 계획

### Step 1: Pull Request 검토 (오늘)
```bash
# PR #3 (feat/calendar) 검토
git fetch origin feat/calendar
git checkout feat/calendar
# 코드 리뷰 진행

# PR #4 (feat/part) 검토
git fetch origin feat/part
git checkout feat/part
# 코드 리뷰 진행
```

### Step 2: 모듈 통합 (내일)
```bash
# feat/yachthappy로 돌아와서 병합
git checkout feat/yachthappy
git merge origin/feat/calendar
git merge origin/feat/part
# 충돌 해결
```

### Step 3: 테스트 및 검증 (2일 후)
```bash
# 통합 테스트 실행
./gradlew test
# API 테스트
# Frontend 연동 테스트
```

---

## 🚨 주의사항

1. **데이터 무결성**: yacht_parts_database.json과 yacht_specifications.json의 데이터 구조를 반드시 유지
2. **API 버전 관리**: Breaking changes가 있을 경우 버전 관리 필요
3. **보안**: 민감한 정보(DB 비밀번호, API 키 등) 커밋 금지
4. **테스트 커버리지**: 새로운 기능 추가 시 테스트 코드 필수

---

## 📞 협업 요청 사항

### kwonhee1 (feat/part 작성자)에게:
- Part 모듈의 상세 스펙 문서 요청
- yacht_parts_database.json과의 매핑 확인

### pu2rile (feat/calendar 작성자)에게:
- Calendar 모듈의 사용 시나리오 공유
- Frontend와의 데이터 교환 형식 논의

---

## ✅ 완료 체크리스트

- [ ] PR #3 리뷰 완료
- [ ] PR #4 리뷰 완료
- [ ] 모듈 통합 완료
- [ ] 충돌 해결 완료
- [ ] 통합 테스트 완료
- [ ] 디자인 가이드 반영
- [ ] API 문서화 완료
- [ ] Frontend 호환성 검증

---

**Last Updated**: 2024-11-15  
**Status**: In Progress  
**Next Review**: After completing module integration

