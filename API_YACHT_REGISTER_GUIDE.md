# 🚀 요트 등록 API 가이드 - JSON 응답

## ✅ 새로운 API: `/api/yacht/register`

### 📋 요청 (Request)

```http
POST /api/yacht/register HTTP/1.1
Host: localhost:5000
Content-Type: multipart/form-data

file: [PDF 파일]
session_id: "optional-session-id"
```

### 📦 응답 (Response) - **JSON 형식**

```json
{
  "success": true,
  "fileName": "J70_owners_manual.pdf",
  "timestamp": "2025-11-21T21:30:00Z",
  "yacht": {
    "basicInfo": {
      "name": "J/70",
      "nickName": "J/70",
      "manufacturer": "J Boats",
      "type": "Owner's Manual",
      "year": "",
      "designer": "",
      "manual": "J70_owners_manual.pdf"
    },
    "specifications": {
      "dimensions": {
        "loa": 7.0,
        "lwl": null,
        "beam": 2.4,
        "draft": 1.2,
        "displacement": 800,
        "mastHeight": 9.5
      },
      "sailArea": {
        "mainSailArea": 18.5,
        "jibSailArea": 12.3,
        "spinnakerSailArea": 45.0,
        "totalSailArea": 75.8
      },
      "engine": {
        "type": "Outboard",
        "power": "6HP",
        "model": "Yamaha 6"
      },
      "hull": {
        "hullMaterial": "Fiberglass",
        "deckMaterial": "Carbon",
        "keelType": "Retractable"
      },
      "accommodations": {
        "berths": null,
        "cabins": null,
        "heads": null
      },
      "capacity": {
        "fuelCapacity": null,
        "waterCapacity": null
      },
      "performance": {
        "maxSpeed": null,
        "cruisingSpeed": null
      },
      "ceCertification": "",
      "description": "PDF 매뉴얼에서 자동 추출: J/70 Owner's Manual",
      "features": ""
    },
    "parts": [
      {
        "name": "Mast",
        "manufacturer": "Selden",
        "model": "J70-MAST-01",
        "interval": 12
      },
      {
        "name": "Boom",
        "manufacturer": "Selden",
        "model": "J70-BOOM-01",
        "interval": 12
      },
      {
        "name": "Standing Rigging",
        "manufacturer": "Dyform",
        "model": "J70-RIG-01",
        "interval": 24
      }
    ]
  },
  "analysisResult": {
    "documentInfo": {
      "title": "J/70 Owner's Manual",
      "yachtModel": "J/70",
      "manufacturer": "J Boats",
      "documentType": "Owner's Manual"
    },
    "yachtSpecs": {
      "standard": {
        "dimensions": {
          "LOA": {"value": 7.0, "unit": "m", "display": "7.0m"},
          "Beam": {"value": 2.4, "unit": "m", "display": "2.4m"},
          "Draft": {"value": 1.2, "unit": "m", "display": "1.2m"}
        },
        "engine": {
          "type": "Outboard",
          "power": "6HP",
          "model": "Yamaha 6"
        },
        "sailArea": {
          "mainsail": 18.5,
          "jib": 12.3,
          "spinnaker": 45.0,
          "total": 75.8
        }
      },
      "additional": {
        "hullMaterial": "Fiberglass",
        "keelType": "Retractable"
      }
    },
    "detailedDimensions": {
      "hullLength": "6.5m",
      "airDraftClassicalMast": "9.5m"
    },
    "exterior": {
      "hull": {
        "id": "ext-hull-01",
        "name": "Hull",
        "category": "Structure",
        "specifications": {
          "type": "Monohull",
          "material": "Fiberglass",
          "color": "White"
        }
      }
    },
    "groundTackle": {},
    "sailInventory": [
      {
        "id": "sail-main-01",
        "name": "Mainsail",
        "category": "Sails",
        "specifications": {
          "area": "18.5 m²",
          "material": "Dacron"
        },
        "maintenanceDetails": {
          "interval": 6,
          "inspectionItems": ["Stitching", "UV cover"]
        }
      }
    ],
    "deckEquipment": {
      "winches": [
        {
          "id": "deck-winch-primary-port-01",
          "name": "Primary Winch Port",
          "manufacturer": "Harken",
          "specifications": {
            "type": "Two-speed self-tailing",
            "location": "Cockpit coaming port"
          }
        }
      ]
    },
    "accommodations": {},
    "tanks": {},
    "electricalSystem": {},
    "electronics": {},
    "plumbingSystem": {},
    "parts": [
      {
        "id": "part-rigging-mast-01",
        "name": "Mast",
        "manufacturer": "Selden",
        "model": "J70-MAST-01",
        "interval": 12,
        "category": "Rigging",
        "specifications": {
          "material": "Aluminum",
          "length": "9.5 m"
        },
        "maintenanceDetails": {
          "interval": 12,
          "inspectionItems": ["Corrosion", "Bolts"]
        }
      }
    ],
    "maintenance": [
      {
        "item": "Mast inspection",
        "interval": "12 개월",
        "method": "Check for corrosion and loose fittings"
      }
    ]
  }
}
```

---

## 🔄 기존 API와 비교

### 1. `/api/chat/upload` (기존)
- ✅ 자연어 응답
- ❌ JSON 데이터 없음

**응답:**
```json
{
  "success": true,
  "response": "✅ 등록이 완료됐습니다! 🎉\n\n**등록된 요트 정보:**\n⛵ 모델: J/70\n...",
  "session_id": "default",
  "file_name": "manual.pdf",
  "timestamp": "2025-11-21T21:30:00Z"
}
```

### 2. `/api/yacht/register` (신규) ⭐
- ✅ **JSON 형식 데이터**
- ✅ 구조화된 요트 정보
- ✅ 부품 리스트
- ✅ 상세 분석 결과
- ❌ 자연어 없음

**응답:**
```json
{
  "success": true,
  "yacht": {
    "basicInfo": {...},
    "specifications": {...},
    "parts": [...]
  },
  "analysisResult": {
    "documentInfo": {...},
    "yachtSpecs": {...},
    "parts": [...]
  }
}
```

---

## 🚀 사용 예시

### Python (requests)

```python
import requests

# PDF 파일 업로드
url = 'http://localhost:5000/api/yacht/register'
files = {'file': open('J70_manual.pdf', 'rb')}
data = {'session_id': 'user-123'}

response = requests.post(url, files=files, data=data)
result = response.json()

if result['success']:
    yacht = result['yacht']
    print(f"요트 이름: {yacht['basicInfo']['name']}")
    print(f"제조사: {yacht['basicInfo']['manufacturer']}")
    print(f"부품 개수: {len(yacht['parts'])}")
    
    # 부품 리스트
    for part in yacht['parts']:
        print(f"- {part['name']} ({part['manufacturer']})")
else:
    print(f"오류: {result['error']}")
```

### cURL

```bash
curl -X POST http://localhost:5000/api/yacht/register \
  -F "file=@J70_manual.pdf" \
  -F "session_id=user-123"
```

### JavaScript (Fetch)

```javascript
const formData = new FormData();
formData.append('file', pdfFile);
formData.append('session_id', 'user-123');

fetch('http://localhost:5000/api/yacht/register', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  if (data.success) {
    console.log('요트 이름:', data.yacht.basicInfo.name);
    console.log('부품 개수:', data.yacht.parts.length);
  } else {
    console.error('오류:', data.error);
  }
});
```

### Dart (Flutter)

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<void> registerYacht(File pdfFile) async {
  var request = http.MultipartRequest(
    'POST',
    Uri.parse('http://localhost:5000/api/yacht/register'),
  );
  
  request.files.add(await http.MultipartFile.fromPath(
    'file',
    pdfFile.path,
  ));
  request.fields['session_id'] = 'user-123';
  
  var response = await request.send();
  var responseData = await response.stream.bytesToString();
  var result = jsonDecode(responseData);
  
  if (result['success']) {
    print('요트 이름: ${result['yacht']['basicInfo']['name']}');
    print('부품 개수: ${result['yacht']['parts'].length}');
  } else {
    print('오류: ${result['error']}');
  }
}
```

---

## 📊 응답 데이터 구조

### `yacht` 객체
- **`basicInfo`**: 기본 정보 (이름, 제조사, 타입 등)
- **`specifications`**: 스펙 (치수, 엔진, 돛 면적 등)
- **`parts`**: 간단한 부품 리스트 (백엔드 API 호환)

### `analysisResult` 객체 (Schema 5.0)
- **`documentInfo`**: 문서 정보
- **`yachtSpecs`**: 요트 스펙 (표준 + 추가)
- **`detailedDimensions`**: 상세 치수
- **`exterior`**: 외관 (Hull, Deck 등)
- **`groundTackle`**: 앵커 시스템
- **`sailInventory`**: 돛 목록
- **`deckEquipment`**: 갑판 장비
- **`accommodations`**: 시설물
- **`tanks`**: 수조
- **`electricalSystem`**: 전기 시스템
- **`electronics`**: 전자 장비
- **`plumbingSystem`**: 배관 시스템
- **`parts`**: 상세 부품 리스트 (ID, 스펙, 정비 정보 포함)
- **`maintenance`**: 유지보수 정보

---

## ⚠️ 오류 처리

### 1. 파일 없음
```json
{
  "success": false,
  "error": "파일이 필요합니다."
}
```

### 2. PDF 아님
```json
{
  "success": false,
  "error": "PDF 파일만 업로드 가능합니다."
}
```

### 3. 텍스트 추출 실패
```json
{
  "success": false,
  "error": "manual.pdf에서 텍스트를 추출할 수 없습니다."
}
```

### 4. 분석 실패
```json
{
  "success": false,
  "error": "요트 매뉴얼이 아닙니다"
}
```

---

## 🎯 백엔드 연동

### Spring Boot Controller 예시

```java
@RestController
@RequestMapping("/api/yacht")
public class YachtController {
    
    @PostMapping("/register-from-pdf")
    public ResponseEntity<?> registerYachtFromPdf(@RequestParam("file") MultipartFile file) {
        // 1. Python API 호출
        RestTemplate restTemplate = new RestTemplate();
        
        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", new FileSystemResource(file));
        
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);
        
        HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
        
        String pythonApiUrl = "http://localhost:5000/api/yacht/register";
        ResponseEntity<YachtRegistrationResponse> response = restTemplate.exchange(
            pythonApiUrl,
            HttpMethod.POST,
            requestEntity,
            YachtRegistrationResponse.class
        );
        
        YachtRegistrationResponse data = response.getBody();
        
        // 2. DB 저장
        Yacht yacht = new Yacht();
        yacht.setName(data.getYacht().getBasicInfo().getName());
        yacht.setNickName(data.getYacht().getBasicInfo().getNickName());
        yachtRepository.save(yacht);
        
        // 3. 부품 저장
        for (Part part : data.getYacht().getParts()) {
            Part newPart = new Part();
            newPart.setYacht(yacht);
            newPart.setName(part.getName());
            newPart.setManufacturer(part.getManufacturer());
            newPart.setModel(part.getModel());
            newPart.setInterval(part.getInterval());
            partRepository.save(newPart);
        }
        
        return ResponseEntity.ok(yacht);
    }
}
```

---

## 🔧 서버 실행

```bash
# 1. API 서버 모드로 실행
cd chat-bot
python chatbot_unified.py --mode api --port 5000

# 2. 서버 확인
# 출력:
# 🌐 HooAah Yacht AI Chatbot API Server
# 🚀 서버 시작: http://localhost:5000
# 📡 API 엔드포인트:
#   - POST /api/chat - 채팅 메시지 전송
#   - POST /api/chat/upload - PDF 업로드 (자연어 응답)
#   - POST /api/yacht/register - 요트 등록 (JSON 응답) ⭐ NEW
#   - GET /api/chat/history - 대화 기록 조회
#   - GET /api/health - 서버 상태 확인
```

---

## ✅ 요약

| 항목 | `/api/chat/upload` | `/api/yacht/register` ⭐ |
|-----|-------------------|-------------------------|
| **응답 형식** | 자연어 문자열 | JSON 데이터 |
| **용도** | 챗봇 대화 | 데이터 추출 |
| **백엔드 연동** | ❌ 어려움 | ✅ 쉬움 |
| **부품 리스트** | ❌ 없음 | ✅ 있음 |
| **상세 분석** | ❌ 없음 | ✅ Schema 5.0 |

**팀원 요구사항 충족:** ✅

이제 `/api/yacht/register`를 사용하면 PDF 업로드 후 **JSON 형식으로 추출된 데이터를 받을 수 있습니다!** 🎉

