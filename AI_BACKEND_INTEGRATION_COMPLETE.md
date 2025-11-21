# 🚀 Python AI ↔ Spring Boot Backend 연동 완료!

## ✅ 완료된 작업

### 1️⃣ **Python Flask API 엔드포인트 추가**

#### 📡 엔드포인트 1: 요트 이름으로 부품 조회
```http
GET /api/yacht/analyze?yacht_name={name}
```

**요청 예시:**
```bash
curl "http://localhost:5000/api/yacht/analyze?yacht_name=J/70"
```

**응답 예시:**
```json
{
  "success": true,
  "yachtId": "j-70",
  "yachtName": "J/70",
  "parts": [
    {
      "id": "j-70-part-hull-001",
      "name": "Hull",
      "manufacturer": "J Boats",
      "model": "J70-Hull",
      "interval": 12,
      "maintenanceDetails": {
        "recommendedInterval": "매년",
        "maintenanceMethod": "육안 검사 및 청소",
        "notes": "스크래치 및 균열 확인"
      }
    }
  ],
  "totalParts": 15
}
```

---

#### 📡 엔드포인트 2: PDF 파일 분석
```http
POST /api/yacht/analyze-pdf
Content-Type: multipart/form-data
```

**요청 예시:**
```bash
curl -X POST http://localhost:5000/api/yacht/analyze-pdf \
  -F "file=@owners_manual.pdf"
```

**응답 예시:**
```json
{
  "success": true,
  "yachtId": "dehler-38",
  "yachtName": "Dehler 38",
  "parts": [
    {
      "id": "dehler-38-part-engine-001",
      "name": "Engine",
      "manufacturer": "Yanmar",
      "model": "3YM30",
      "interval": 6,
      "maintenanceDetails": {
        "recommendedInterval": "6개월마다",
        "maintenanceMethod": "오일 교체 및 필터 점검",
        "notes": "엔진 시간 50시간마다"
      }
    }
  ],
  "totalParts": 22,
  "documentInfo": {
    "fileName": "owners_manual.pdf",
    "manufacturer": "Dehler",
    "model": "38",
    "year": 2020
  }
}
```

---

#### 📡 엔드포인트 3: 헬스체크
```http
GET /api/health
```

**응답 예시:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-21T10:30:00",
  "yachtCount": 20,
  "version": "5.0"
}
```

---

### 2️⃣ **Backend DTO 클래스 생성**

#### 📄 파일: `AiAnalysisResponse.java`
```java
package HooYah.Yacht.yacht.dto.response;

@Getter
@NoArgsConstructor
@AllArgsConstructor
public class AiAnalysisResponse {
    private Boolean success;
    private String yachtId;
    private String yachtName;
    private List<AiPartDto> parts;
    private Integer totalParts;
    private DocumentInfo documentInfo;
    private String error;
    
    @Getter
    @NoArgsConstructor
    @AllArgsConstructor
    public static class AiPartDto {
        private String id;
        private String name;
        private String manufacturer;
        private String model;
        private Integer interval;
        private MaintenanceDetails maintenanceDetails;
    }
    
    @Getter
    @NoArgsConstructor
    @AllArgsConstructor
    public static class MaintenanceDetails {
        private String recommendedInterval;
        private String maintenanceMethod;
        private String notes;
    }
    
    @Getter
    @NoArgsConstructor
    @AllArgsConstructor
    public static class DocumentInfo {
        private String fileName;
        private String manufacturer;
        private String model;
        private Integer year;
    }
}
```

---

### 3️⃣ **Backend RestTemplate 설정**

#### 📄 파일: `RestTemplateConfig.java`
```java
package HooYah.Yacht.conf;

@Configuration
public class RestTemplateConfig {
    
    @Bean
    public RestTemplate restTemplate(RestTemplateBuilder builder) {
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(5000);  // 5초
        factory.setReadTimeout(30000);    // 30초 (AI 분석 시간)
        
        return builder
                .setConnectTimeout(Duration.ofSeconds(5))
                .setReadTimeout(Duration.ofSeconds(30))
                .requestFactory(() -> factory)
                .build();
    }
}
```

**특징:**
- ✅ 연결 타임아웃: 5초
- ✅ 읽기 타임아웃: 30초 (AI 분석 시간 고려)
- ✅ Spring Bean으로 등록

---

### 4️⃣ **Backend YachtDefaultService AI 연동**

#### 📄 파일: `YachtDefaultService.java`

**주요 기능:**

1. **기본 부품 리스트 조회 (요트 이름)**
```java
public List<PartDto> getDefaultPartList(String name) {
    try {
        String url = aiApiBaseUrl + "/api/yacht/analyze?yacht_name=" + name;
        
        ResponseEntity<AiAnalysisResponse> response = restTemplate.getForEntity(
                url,
                AiAnalysisResponse.class
        );
        
        if (response.getStatusCode() == HttpStatus.OK && response.getBody() != null) {
            AiAnalysisResponse aiResponse = response.getBody();
            
            if (aiResponse.isSuccess() && aiResponse.getParts() != null) {
                return convertAiPartsToPartDto(aiResponse.getParts());
            }
        }
        
    } catch (RestClientException e) {
        log.error("❌ AI API 호출 실패, Fallback 데이터 반환", e);
        return getFallbackPartList(name);
    }
}
```

2. **추가 부품 리스트 조회 (PDF 분석)**
```java
private List<PartDto> analyzePdfFile(MultipartFile file) throws IOException {
    String url = aiApiBaseUrl + "/api/yacht/analyze-pdf";
    
    ByteArrayResource resource = new ByteArrayResource(file.getBytes()) {
        @Override
        public String getFilename() {
            return file.getOriginalFilename();
        }
    };
    
    MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
    body.add("file", resource);
    
    HttpHeaders headers = new HttpHeaders();
    headers.setContentType(MediaType.MULTIPART_FORM_DATA);
    
    HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
    
    ResponseEntity<AiAnalysisResponse> response = restTemplate.exchange(
            url,
            HttpMethod.POST,
            requestEntity,
            AiAnalysisResponse.class
    );
    
    if (response.getStatusCode() == HttpStatus.OK && response.getBody() != null) {
        AiAnalysisResponse aiResponse = response.getBody();
        
        if (aiResponse.isSuccess() && aiResponse.getParts() != null) {
            return convertAiPartsToPartDto(aiResponse.getParts());
        }
    }
}
```

3. **Fallback 로직 (AI 서버 다운 시)**
```java
private List<PartDto> getFallbackPartList(String name) {
    log.warn("⚠️ Fallback 데이터 반환: {}", name);
    
    return List.of(
            PartDto.builder()
                    .name("Hull")
                    .manufacturer("Unknown")
                    .model(name + "-Hull")
                    .interval(12L)
                    .build(),
            PartDto.builder()
                    .name("Mast")
                    .manufacturer("Unknown")
                    .model(name + "-Mast")
                    .interval(12L)
                    .build()
    );
}
```

---

### 5️⃣ **application.yml 설정 추가**

```yaml
# AI API 설정
ai:
  api:
    base-url: ${AI_API_BASE_URL:http://localhost:5000}
    # 기본값: http://localhost:5000
    # 배포 시 환경변수로 변경 가능
```

**환경변수 설정:**
```bash
# 로컬 개발
AI_API_BASE_URL=http://localhost:5000

# 배포 환경
AI_API_BASE_URL=http://ai-chatbot:5000
```

---

## 🔄 전체 데이터 흐름

```
사용자 (앱)
    ↓
[Frontend - Flutter]
    ↓ POST /api/yacht/part-list
    ↓ { "name": "J/70", "files": [pdf] }
    ↓
[Backend - Spring Boot]
    ↓
YachtController.getPartList()
    ↓
YachtDefaultService.getPartList(name, files)
    ├─ getDefaultPartList(name)
    │   ↓ GET /api/yacht/analyze?yacht_name=J/70
    │   [Python Flask AI]
    │   ↓ JSON 데이터 로드 (yacht_parts_app_data.json)
    │   ↓ 부품 정보 반환
    │   ↑
    └─ getAdditionalPartList(files)
        ↓ POST /api/yacht/analyze-pdf
        [Python Flask AI]
        ↓ PDF 텍스트 추출
        ↓ Gemini AI 분석
        ↓ 부품 정보 추출
        ↑
    ↓
List<PartDto> (통합된 부품 리스트)
    ↓
사용자 (앱에 표시)
```

---

## 🧪 테스트 방법

### 1️⃣ **Python AI 서버 시작**
```bash
cd chat-bot
python chatbot_unified.py --mode api --port 5000
```

**확인:**
```bash
curl http://localhost:5000/api/health
```

**예상 응답:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-21T10:30:00",
  "yachtCount": 20,
  "version": "5.0"
}
```

---

### 2️⃣ **Backend 서버 시작**
```bash
cd backend
./gradlew bootRun
```

**확인:**
```bash
curl http://localhost:8080/actuator/health
```

---

### 3️⃣ **요트 이름으로 부품 조회 테스트**
```bash
curl "http://localhost:8080/api/yacht/part-list?name=J/70"
```

**예상 응답:**
```json
{
  "success": true,
  "data": [
    {
      "id": null,
      "name": "Hull",
      "manufacturer": "J Boats",
      "model": "J70-Hull",
      "interval": 12,
      "lastRepair": null
    }
  ]
}
```

---

### 4️⃣ **PDF 파일 분석 테스트**
```bash
curl -X POST http://localhost:8080/api/yacht/part-list \
  -F "name=Dehler 38" \
  -F "files=@owners_manual.pdf"
```

**예상 응답:**
```json
{
  "success": true,
  "data": [
    {
      "name": "Engine",
      "manufacturer": "Yanmar",
      "model": "3YM30",
      "interval": 6
    }
  ]
}
```

---

## 🐳 Docker 배포

### 1️⃣ **Python AI Docker**
```dockerfile
# chat-bot/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "chatbot_unified.py", "--mode", "api", "--port", "5000"]
```

**빌드 및 실행:**
```bash
cd chat-bot
docker build -t yacht-ai:latest .
docker run -d -p 5000:5000 --name yacht-ai yacht-ai:latest
```

---

### 2️⃣ **Docker Compose (전체 시스템)**
```yaml
# docker-compose.yml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: HooYah
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  ai-chatbot:
    build: ./chat-bot
    ports:
      - "5000:5000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    depends_on:
      - mysql
    restart: always

  backend:
    build: ./backend
    ports:
      - "8080:8080"
    environment:
      - DB_URL=mysql:3306/HooYah
      - DB_USERNAME=root
      - DB_PASSWORD=root
      - AI_API_BASE_URL=http://ai-chatbot:5000
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - mysql
      - ai-chatbot
    restart: always

volumes:
  mysql_data:
```

**실행:**
```bash
docker-compose up -d
```

---

## 📊 모니터링

### 1️⃣ **AI 서버 헬스체크**
```bash
curl http://localhost:5000/api/health
```

### 2️⃣ **Backend 로그 확인**
```bash
# Docker 환경
docker logs -f yacht-backend

# 로컬 환경
tail -f logs/spring.log
```

**확인할 로그:**
```
✅ AI 분석 성공: 15 부품
⚠️ AI API 호출 실패, Fallback 데이터 반환
🤖 AI API 호출: http://localhost:5000/api/yacht/analyze?yacht_name=J/70
```

---

## 🎯 핵심 특징

### ✅ **Stateless 설계**
- AI 분석 결과는 DB에 저장하지 않음
- API 응답으로만 사용
- 서버 재시작 시 자동 초기화

### ✅ **Fallback 메커니즘**
- AI 서버 다운 시 기본 데이터 반환
- 사용자에게 에러 노출 없이 안정적인 서비스

### ✅ **타임아웃 설정**
- 연결 타임아웃: 5초
- 읽기 타임아웃: 30초 (AI 분석 시간 고려)

### ✅ **로깅**
- 모든 API 호출 로깅
- 성공/실패 상태 명확히 표시
- 디버깅 용이

---

## 🚀 다음 단계

1. ✅ Python AI API 엔드포인트 추가 (완료!)
2. ✅ Backend DTO 클래스 생성 (완료!)
3. ✅ Backend RestTemplate 설정 (완료!)
4. ✅ Backend YachtDefaultService AI 연동 (완료!)
5. ⭐ Frontend Flutter 앱에서 테스트
6. ⭐ 실제 배포 환경 테스트
7. ⭐ 성능 모니터링 및 최적화

---

## 📞 문의

문제가 발생하면 다음을 확인하세요:

1. **AI 서버가 실행 중인가?**
   ```bash
   curl http://localhost:5000/api/health
   ```

2. **Backend 설정이 올바른가?**
   ```yaml
   ai:
     api:
       base-url: http://localhost:5000
   ```

3. **네트워크 연결이 정상인가?**
   ```bash
   curl "http://localhost:5000/api/yacht/analyze?yacht_name=J/70"
   ```

---

**완료! 🎉**

