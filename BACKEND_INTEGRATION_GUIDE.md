# 🔍 Backend 분석 및 MySQL 작업 가이드

## 📋 **팀원 요구사항**

```
1. ✅ PDF는 backend에서 받음
2. ✅ AI 추출 데이터는 DB에 저장하지 않고 바로 JSON 반환
3. ❌ yacht 테이블 사용 불가 (다른 용도로 사용 중)
4. ✅ AI API: PDF → JSON Response (서버에 저장 안 함)
```

---

## 🏗️ **Backend 현재 구조 분석**

### **1. `yacht` 테이블 현재 용도**

#### **Yacht Entity** (`Yacht.java`)
```java
@Entity
@Table(name = "yacht")
public class Yacht {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;              // Auto Increment ID
    
    private String name;          // 요트 이름 (사용자 입력)
    private String nickName;      // 요트 별명 (사용자 입력)
    
    @OneToMany(mappedBy = "yacht")
    private List<YachtUser> yachtUser;  // 요트 소유자/사용자 관계
}
```

**용도:**
- ✅ **사용자가 직접 등록한 요트 정보**
- ✅ `name`: 사용자가 입력한 요트 이름
- ✅ `nickName`: 사용자가 지정한 별명
- ✅ `YachtUser`: 다대다 관계 (여러 사용자가 한 요트 공유 가능)
- ❌ **AI 분석 데이터와 무관**

**결론:** 
- `yacht` 테이블은 **사용자의 요트 소유권 관리**용
- AI 분석 데이터와는 **완전히 별개**

---

### **2. AI API 기존 구현** (`YachtDefaultService.java`)

#### **현재 상태**
```java
@Service
public class YachtDefaultService {
    
    @PostMapping("/part-list")  // 🔴 이미 구현된 엔드포인트
    public List<PartDto> getPartList(String name, List<MultipartFile> files) {
        List<PartDto> partList = getDefaultPartList(name);
        if(files != null && !files.isEmpty()) {
            partList = getAdditionalPartList(partList, files);
        }
        return partList;
    }
    
    public List<PartDto> getDefaultPartList(String name) {
        // todo : add ai  🔴 여기에 AI 연동 필요!
        return dummyData;
    }
    
    private List<PartDto> getAdditionalPartList(List<PartDto> defaultPartList, List<MultipartFile> files) {
        // todo : add ai  🔴 여기에 AI 연동 필요!
        return defaultPartList;
    }
}
```

**분석:**
- ✅ **이미 `/api/yacht/part-list` 엔드포인트 존재**
- ✅ PDF 파일 업로드 받을 수 있음 (`MultipartFile`)
- ✅ 요트 이름 (`name`) 받음
- 🔴 **AI 연동이 `todo` 상태** (더미 데이터 반환 중)
- ✅ **DB 저장 없이 바로 반환** (이미 요구사항 충족)

---

### **3. Response 구조**

#### **PartDto** (응답 형식)
```java
@Getter
@Setter
public class PartDto {
    private Long id;              // Part DB ID (nullable)
    private String name;          // 부품 이름
    private String manufacturer;  // 제조사
    private String model;         // 모델명
    private Long interval;        // 정비 주기 (개월)
    private OffsetDateTime lastRepair;  // 마지막 정비일
}
```

#### **SuccessResponse** (표준 응답)
```java
@Getter
@Setter
public class SuccessResponse {
    private int status;          // HTTP 상태 코드
    private String message;      // 메시지
    private Object response;     // 실제 데이터
}
```

**API 응답 예시:**
```json
{
  "status": 200,
  "message": "success",
  "response": [
    {
      "id": null,
      "name": "엔진",
      "manufacturer": "Yanmar",
      "model": "3YM30",
      "interval": 12,
      "lastRepair": null
    },
    {
      "name": "Hull",
      "manufacturer": "Beneteau",
      "model": "Oceanis 46.1",
      "interval": 24
    }
  ]
}
```

---

## 🎯 **MySQL 작업 가이드**

### **결론: MySQL 작업이 필요 없습니다!** ✅

#### **이유:**

1. **Backend는 이미 PDF → JSON 반환 구조** ✅
   ```
   PDF 업로드 → AI 분석 → JSON 반환 (DB 저장 안 함)
   ```

2. **`yacht` 테이블은 사용자 데이터 전용** ✅
   ```
   yacht 테이블: 사용자가 등록한 요트 (AI 분석과 무관)
   AI 분석: Part 정보만 반환 (DB 저장 안 함)
   ```

3. **Part는 별도 테이블에 저장 (사용자가 선택 시)** ✅
   ```
   사용자가 AI 응답에서 부품 선택 → part 테이블에 저장
   AI 응답 자체는 저장 안 함
   ```

---

## 🔧 **해야 할 작업**

### **1. Python AI API를 Backend에서 호출** ⭐

#### **방법 1: HTTP 요청** (권장)

**Backend → Python Flask API 호출**

```java
// YachtDefaultService.java
@Service
@RequiredArgsConstructor
public class YachtDefaultService {
    
    private final RestTemplate restTemplate;
    private final String AI_API_URL = "http://localhost:5000/api/yacht/analyze";
    
    public List<PartDto> getDefaultPartList(String name) {
        // Python AI API 호출
        try {
            ResponseEntity<AiAnalysisResponse> response = restTemplate.getForEntity(
                AI_API_URL + "?yacht_name=" + name,
                AiAnalysisResponse.class
            );
            
            if (response.getStatusCode() == HttpStatus.OK) {
                return convertToPartDto(response.getBody());
            }
        } catch (Exception e) {
            log.error("AI API 호출 실패", e);
        }
        
        return Collections.emptyList();
    }
    
    private List<PartDto> getAdditionalPartList(List<PartDto> defaultPartList, List<MultipartFile> files) {
        // Python AI API에 PDF 전송
        try {
            MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
            
            for (MultipartFile file : files) {
                body.add("file", new FileSystemResource(convertToFile(file)));
            }
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.MULTIPART_FORM_DATA);
            
            HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
            
            ResponseEntity<AiAnalysisResponse> response = restTemplate.postForEntity(
                AI_API_URL + "/analyze-pdf",
                requestEntity,
                AiAnalysisResponse.class
            );
            
            if (response.getStatusCode() == HttpStatus.OK) {
                List<PartDto> aiParts = convertToPartDto(response.getBody());
                defaultPartList.addAll(aiParts);
            }
        } catch (Exception e) {
            log.error("PDF AI 분석 실패", e);
        }
        
        return defaultPartList;
    }
    
    private List<PartDto> convertToPartDto(AiAnalysisResponse aiResponse) {
        return aiResponse.getParts().stream()
            .map(part -> PartDto.builder()
                .name(part.getName())
                .manufacturer(part.getManufacturer())
                .model(part.getModel())
                .interval(part.getInterval())
                .build())
            .collect(Collectors.toList());
    }
}
```

**AI API Response DTO:**
```java
@Getter
@Setter
@NoArgsConstructor
public class AiAnalysisResponse {
    private String yachtName;
    private String manufacturer;
    private List<AiPartInfo> parts;
    
    @Getter
    @Setter
    @NoArgsConstructor
    public static class AiPartInfo {
        private String name;
        private String manufacturer;
        private String model;
        private Long interval;
        private String category;
    }
}
```

---

#### **방법 2: Python Script 직접 실행** (비권장)

```java
public List<PartDto> getDefaultPartList(String name) {
    try {
        ProcessBuilder pb = new ProcessBuilder(
            "python", 
            "path/to/chatbot_unified.py",
            "--yacht-name", name
        );
        
        Process process = pb.start();
        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        
        String json = reader.lines().collect(Collectors.joining());
        ObjectMapper mapper = new ObjectMapper();
        AiAnalysisResponse response = mapper.readValue(json, AiAnalysisResponse.class);
        
        return convertToPartDto(response);
    } catch (Exception e) {
        log.error("Python 실행 실패", e);
        return Collections.emptyList();
    }
}
```

---

### **2. Python Flask API 엔드포인트 추가** ⭐

#### **`chatbot_unified.py`에 추가**

```python
# 기존 /api/yacht/register 외에 추가

@app.route('/api/yacht/analyze', methods=['GET'])
def analyze_yacht_by_name():
    """요트 이름으로 기본 부품 정보 조회"""
    yacht_name = request.args.get('yacht_name')
    
    if not yacht_name:
        return jsonify({"error": "yacht_name is required"}), 400
    
    # yacht_specifications.json에서 검색
    yacht_data = chatbot._load_yacht_data()
    yacht = next((y for y in yacht_data.get('yachts', []) 
                  if y.get('name', '').lower() == yacht_name.lower()), None)
    
    if not yacht:
        return jsonify({"error": "Yacht not found"}), 404
    
    # 부품 정보 추출
    parts = []
    for part in yacht.get('parts', []):
        parts.append({
            "name": part.get('name'),
            "manufacturer": part.get('manufacturer', ''),
            "model": part.get('model', ''),
            "interval": part.get('interval', 12),
            "category": part.get('category', '')
        })
    
    response = {
        "yachtName": yacht.get('name'),
        "manufacturer": yacht.get('manufacturer'),
        "parts": parts
    }
    
    return jsonify(response), 200


@app.route('/api/yacht/analyze-pdf', methods=['POST'])
def analyze_pdf():
    """PDF 파일 분석"""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400
    
    # 임시 파일 저장
    temp_path = f"/tmp/{file.filename}"
    file.save(temp_path)
    
    # AI 분석
    chatbot = get_or_create_chatbot('temp-session')
    result = chatbot._handle_file_upload(temp_path)
    
    # registration_data에서 부품 정보 추출
    registration_data = chatbot.get_registration_data()
    
    if not registration_data:
        return jsonify({"error": "Analysis failed"}), 500
    
    parts = []
    for part in registration_data.get('parts', []):
        parts.append({
            "name": part.get('name'),
            "manufacturer": part.get('manufacturer', ''),
            "model": part.get('model', ''),
            "interval": part.get('interval', 12)
        })
    
    response = {
        "yachtName": registration_data.get('basicInfo', {}).get('name'),
        "manufacturer": registration_data.get('basicInfo', {}).get('manufacturer'),
        "parts": parts
    }
    
    # 임시 파일 삭제
    os.remove(temp_path)
    
    return jsonify(response), 200
```

---

### **3. JSON 파일은 참조 데이터로만 사용** ✅

```
┌─────────────────────────────────────────┐
│  chat-bot/data/*.json                   │
│  (20종 요트 마스터 데이터)               │
└─────────────────────────────────────────┘
              ↓ (읽기 전용)
┌─────────────────────────────────────────┐
│  Python Flask API                       │
│  - /api/yacht/analyze (이름으로 조회)   │
│  - /api/yacht/analyze-pdf (PDF 분석)    │
└─────────────────────────────────────────┘
              ↓ (HTTP)
┌─────────────────────────────────────────┐
│  Backend Spring Boot                    │
│  - YachtDefaultService                  │
│  - /api/yacht/part-list                 │
└─────────────────────────────────────────┘
              ↓ (JSON Response)
┌─────────────────────────────────────────┐
│  Frontend (Flutter)                     │
│  - 부품 목록 표시                        │
│  - 사용자가 선택한 부품만 DB 저장        │
└─────────────────────────────────────────┘
```

---

## 📊 **데이터 흐름**

### **시나리오 1: 기존 20종 요트 조회**

```
1. 사용자가 요트 이름 입력 ("J/70")
   ↓
2. Frontend → Backend
   POST /api/yacht/part-list
   { "name": "J/70", "file": null }
   ↓
3. Backend → Python AI
   GET http://localhost:5000/api/yacht/analyze?yacht_name=J/70
   ↓
4. Python: yacht_specifications.json에서 "j-70" 검색
   ↓
5. Python → Backend
   {
     "yachtName": "J/70",
     "manufacturer": "C&C Fiberglass",
     "parts": [
       { "name": "Hull", "manufacturer": "C&C", "interval": 12 },
       { "name": "Mast", "manufacturer": "Southern Spars", "interval": 12 }
     ]
   }
   ↓
6. Backend → Frontend
   {
     "status": 200,
     "message": "success",
     "response": [
       { "name": "Hull", "manufacturer": "C&C", "interval": 12 },
       { "name": "Mast", "manufacturer": "Southern Spars", "interval": 12 }
     ]
   }
   ↓
7. Frontend: 부품 목록 표시
   ↓
8. 사용자가 부품 선택 후 "등록" 클릭
   ↓
9. Frontend → Backend
   POST /api/yacht
   {
     "yacht": { "name": "J/70", "nickName": "My Boat" },
     "partList": [
       { "name": "Hull", "manufacturer": "C&C", "interval": 12 }
     ]
   }
   ↓
10. Backend: yacht 테이블에 저장 (사용자 요트)
    Backend: part 테이블에 저장 (선택한 부품만)
```

### **시나리오 2: 새 PDF 분석**

```
1. 사용자가 PDF 업로드
   ↓
2. Frontend → Backend
   POST /api/yacht/part-list
   { "name": "Custom Yacht", "file": [yacht.pdf] }
   ↓
3. Backend → Python AI
   POST http://localhost:5000/api/yacht/analyze-pdf
   FormData: { "file": yacht.pdf }
   ↓
4. Python: AI가 PDF 분석
   ↓
5. Python → Backend (JSON 반환, DB 저장 안 함)
   {
     "yachtName": "Custom Yacht",
     "manufacturer": "Unknown",
     "parts": [ ... ]
   }
   ↓
6. Backend → Frontend (JSON 반환, DB 저장 안 함)
   ↓
7. 사용자가 부품 선택 후 등록 (이때만 DB 저장)
```

---

## ✅ **최종 결론**

### **MySQL 작업 필요 여부: ❌ 필요 없음**

**이유:**
1. ✅ Backend는 이미 **PDF → JSON 반환** 구조
2. ✅ AI 분석 데이터는 **DB에 저장하지 않음**
3. ✅ `yacht` 테이블은 **사용자 요트 소유권 관리** 전용
4. ✅ Part 데이터는 **사용자가 선택 시에만** `part` 테이블에 저장

### **해야 할 작업:**

1. ⭐ **Python Flask API에 엔드포인트 추가**
   - `GET /api/yacht/analyze?yacht_name=...` (이름 조회)
   - `POST /api/yacht/analyze-pdf` (PDF 분석)

2. ⭐ **Backend에서 Python API 호출**
   - `YachtDefaultService.getDefaultPartList()` 구현
   - `YachtDefaultService.getAdditionalPartList()` 구현
   - `RestTemplate` 사용

3. ✅ **JSON 파일은 그대로 유지**
   - 참조 데이터로만 사용
   - MySQL과 동기화 불필요

---

## 🚀 **구현 순서**

```
1단계: Python Flask API 엔드포인트 추가
   ├─ /api/yacht/analyze (GET)
   └─ /api/yacht/analyze-pdf (POST)

2단계: Backend에서 Python API 호출
   ├─ RestTemplate 설정
   ├─ AiAnalysisResponse DTO 생성
   └─ YachtDefaultService 구현

3단계: 테스트
   ├─ Postman으로 Python API 테스트
   ├─ Backend 단독 테스트
   └─ Frontend 통합 테스트

4단계: 배포
   ├─ Python Flask 서버 실행 (포트 5000)
   ├─ Backend Spring Boot 실행 (포트 8080)
   └─ Flutter 앱에서 연동
```

---

## 💡 **추가 팁**

### **1. Python Flask와 Backend Spring Boot 통신**

```yaml
# Backend application.yml
ai:
  api:
    url: http://localhost:5000
    analyze-endpoint: /api/yacht/analyze
    analyze-pdf-endpoint: /api/yacht/analyze-pdf
```

### **2. 에러 처리**

```java
@Service
public class YachtDefaultService {
    
    public List<PartDto> getPartList(String name, List<MultipartFile> files) {
        try {
            List<PartDto> partList = getDefaultPartList(name);
            
            if(files != null && !files.isEmpty()) {
                partList = getAdditionalPartList(partList, files);
            }
            
            return partList;
        } catch (Exception e) {
            log.error("AI API 호출 실패, 더미 데이터 반환", e);
            return dummyData;  // Fallback
        }
    }
}
```

### **3. 성능 최적화**

- Python API 타임아웃 설정: 30초
- 비동기 처리: `@Async` (선택사항)
- 캐싱: 동일 요트 이름 반복 조회 시

---

**요약: MySQL 작업 없이 Backend ↔ Python API 연동만 하면 됩니다!** ✅

