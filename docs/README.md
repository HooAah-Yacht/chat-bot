# Yacht Parts Management System - AI-Powered Data Extraction & Management

## 📋 프로젝트 개요

이 프로젝트는 **요트 부품 관리 앱**을 위한 데이터베이스 구축 및 AI 기반 자동화 시스템입니다.
20종의 세일링 요트 매뉴얼에서 부품 정보를 추출하고, 향후 사용자가 새로운 요트나 부품을 추가할 때 AI가 자동으로 처리할 수 있도록 설계되었습니다.

---

## 🚢 지원 요트 20종

### Racing Yachts (레이싱 요트)

1. **FarEast 28** - 소형 레이싱/크루징
2. **Farr 40** - 원디자인 레이싱
3. **J/24** - 세계적인 원디자인
4. **J/70** - 현대적인 스포츠보트
5. **Laser / ILCA** - 올림픽 클래스 딩기
6. **Melges 32** - 고성능 레이싱
7. **TP52** - 프로페셔널 레이싱
8. **RS21** - 원디자인 킬보트

### Performance Cruisers (퍼포먼스 크루저)

9. **Beneteau 473** - 크루징/레이싱
10. **Beneteau First 36** - 스포티한 크루저
11. **Beneteau Oceanis 46.1** - 현대적 크루저
12. **Dehler 38** - 독일 퍼포먼스 크루저
13. **Jeanneau Sun Fast 3300** - 패스트 크루저
14. **X-35** - 원디자인 스포츠보트
15. **X-Yachts XP 44** - 고급 퍼포먼스 요트

### Luxury Performance (럭셔리 퍼포먼스)

16. **Swan 50 / ClubSwan 50** - 이탈리아 명품
17. **Nautor Swan 48** - 핀란드 명품
18. **Grand Soleil GC 42** - 이탈리아 고급 요트
19. **Solaris 44** - 고급 블루워터 크루저
20. **Hanse 458** - 독일 프리미엄 크루저

---

## 🔄 데이터 추출 프로세스

### Phase 1: PDF 매뉴얼 수집

```
yachtpdf/
├── OC15aiiFAREAST28RClassrules-[19458].pdf
├── rulebook.pdf (Farr 40)
├── Handbook_2109.pdf (Laser)
├── owners_manual.pdf (Beneteau First 36)
├── X352012CR080412-[12381].pdf (X-35)
└── ... (총 20개 PDF 매뉴얼)
```

**수집 경로:**

- 제조사 공식 웹사이트
- 클래스 협회 (Class Association)
- 소유자 매뉴얼 라이브러리
- 정비 문서 (정비 관련 자료.pdf)

### Phase 2: 텍스트 추출 시도

#### 방법 1: PyPDF2 / pdfplumber

```python
import pdfplumber
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    """PDF에서 텍스트 추출"""
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text
```

**문제점:**

- ❌ 스캔된 이미지 PDF (OCR 필요)
- ❌ 복잡한 테이블 구조
- ❌ 다이어그램과 텍스트 혼재
- ❌ 불규칙한 포맷

#### 방법 2: 수동 구조화

```python
# yacht_parts_app_data.json 생성
{
  "yachts": [
    {
      "id": "fareast-28",
      "name": "FarEast 28",
      "commonParts": [
        {
          "id": "fe28-mast-01",
          "category": "Rigging",
          "name": "Mast",
          "material": "Aluminum",
          "price": 8500,
          "manufacturer": "Selden/Z-Spars"
        }
      ]
    }
  ]
}
```

### Phase 3: 데이터베이스 구축

#### 3.1 기본 구조 생성

```bash
python extract_yacht_parts_advanced.py
# → extracted_yacht_parts_detailed.json (278KB, 4023 lines)
```

#### 3.2 점검 항목 추가

```bash
python add_inspection_parts.py
# → 실제 정비 데이터 추가 (엔진, 돛, 리깅, 부식 등)
```

#### 3.3 데이터 분리 (Physical vs Maintenance)

```bash
python restructure_database.py
# → physicalParts (실제 부품 51개)
# → maintenanceItems (점검 항목 1,020개)
```

#### 3.4 명명 규칙 적용

```bash
python complete_maintenance_rename.py
# → 점검 항목 이름 변경 (780개)
# → "Engine Oil" → "Engine Oil Check"
# → "Mast" → "Mast Inspection"
```

### Phase 4: 최종 데이터베이스

**`yacht_parts_database.json` (688KB, 19,209 lines)**

```json
{
  "yachts": [
    {
      "id": "fareast-28",
      "name": "FarEast 28",
      "manufacturer": "FarEast Yachts",
      "manualPDF": "yachtpdf/OC15aiiFAREAST28RClassrules-[19458].pdf",
      "parts": {
        "rigging": {
          "physicalParts": [
            {
              "id": "fe28-mast-01",
              "name": "Mast",
              "material": "Aluminum",
              "length": "11.5m",
              "manufacturer": "Selden/Z-Spars",
              "price": 8500,
              "availability": "Order from manufacturer"
            }
          ],
          "maintenanceItems": [
            {
              "id": "rig-001",
              "name": "Standing Rigging Inspection - Stays & Shrouds",
              "nameKo": "고정 리깅 - 스테이/슈라우드",
              "inspectionItems": [
                "스테이 부식 점검 (스테인리스 강)",
                "턴버클 장력 확인",
                "마스트 헤드 핀/스프레더 부근 균열"
              ],
              "checkInterval": "6개월 / 폭풍 후",
              "material": "Stainless Steel 316",
              "corrosionRisk": "중간 - 스테인리스 부식",
              "repairMethod": "와이어 교체, 턴버클 조정",
              "estimatedCost": "$2000-8000",
              "maintenanceLevel": "전문가"
            }
          ]
        },
        "engine": {
          "physicalParts": [],
          "maintenanceItems": [
            {
              "id": "eng-001",
              "name": "Engine Oil Check",
              "checkInterval": "100~150시간 운항 / 1년",
              "estimatedCost": "$50-150"
            }
          ]
        }
      }
    }
  ]
}
```

---

## 🤖 AI 기반 자동화 시스템

### 1. 신규 요트 등록 자동화

#### 사용자 작업 흐름

```
1. 사용자가 앱에서 "새 요트 추가" 클릭
2. 요트 매뉴얼 PDF 업로드
3. 기본 정보 입력 (요트명, 제조사, 길이 등)
4. AI가 자동으로 부품 정보 추출
5. 사용자 확인 후 저장
```

#### AI 처리 파이프라인

##### Step 1: PDF 텍스트 추출 (OCR)

```python
import pytesseract
from pdf2image import convert_from_path

def extract_text_with_ocr(pdf_path):
    """OCR을 사용한 PDF 텍스트 추출"""
    images = convert_from_path(pdf_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image, lang='eng')
    return text
```

**필요 기술:**

- **Tesseract OCR**: 스캔된 문서 텍스트 추출
- **pdf2image**: PDF → 이미지 변환
- **OpenCV**: 이미지 전처리 (노이즈 제거, 대비 조정)

##### Step 2: NLP 기반 정보 추출

```python
from transformers import pipeline

# Named Entity Recognition (NER)
ner = pipeline("ner", model="dslim/bert-base-NER")

def extract_part_info(text):
    """텍스트에서 부품 정보 추출"""
    entities = ner(text)

    parts = []
    for entity in entities:
        if entity['entity'] in ['PRODUCT', 'PART']:
            parts.append({
                'name': entity['word'],
                'confidence': entity['score']
            })
    return parts
```

**사용 모델:**

- **BERT-NER**: 부품명, 제조사, 규격 인식
- **GPT-4**: 복잡한 매뉴얼 문장 이해
- **Custom Fine-tuned Model**: 요트 도메인 특화 모델

##### Step 3: 테이블 데이터 추출

```python
import camelot

def extract_parts_table(pdf_path):
    """PDF에서 부품 테이블 추출"""
    tables = camelot.read_pdf(pdf_path, pages='all')

    parts_list = []
    for table in tables:
        df = table.df
        # 테이블 컬럼: Part Number, Name, Material, Price 등
        for _, row in df.iterrows():
            parts_list.append({
                'partNumber': row['Part Number'],
                'name': row['Name'],
                'material': row['Material'],
                'price': row['Price']
            })
    return parts_list
```

**필요 라이브러리:**

- **Camelot**: PDF 테이블 추출
- **Tabula**: 대체 테이블 추출 도구
- **Pandas**: 데이터 정제

##### Step 4: 이미지 인식 (부품 사진)

```python
from transformers import CLIPModel, CLIPProcessor

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def identify_part_from_image(image, candidate_parts):
    """이미지에서 부품 식별"""
    inputs = processor(
        text=candidate_parts,
        images=image,
        return_tensors="pt",
        padding=True
    )
    outputs = model(**inputs)

    # 가장 유사한 부품 찾기
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)
    return candidate_parts[probs.argmax()]
```

**사용 모델:**

- **CLIP**: 이미지-텍스트 매칭
- **YOLO**: 부품 객체 탐지
- **Custom CNN**: 요트 부품 분류 모델

##### Step 5: 자동 분류 및 태깅

```python
def classify_part(part_name, part_description):
    """부품을 카테고리로 자동 분류"""
    categories = {
        'rigging': ['mast', 'boom', 'shroud', 'stay', 'halyard'],
        'sails': ['mainsail', 'genoa', 'jib', 'spinnaker'],
        'engine': ['oil', 'filter', 'impeller', 'belt'],
        'hull': ['keel', 'rudder', 'gelcoat'],
        'deck_hardware': ['winch', 'cleat', 'block'],
        'steering': ['wheel', 'quadrant', 'cable'],
        'electrical': ['battery', 'panel', 'wire'],
        'plumbing': ['pump', 'hose', 'through-hull'],
        'safety': ['lifejacket', 'flare', 'raft']
    }

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in part_name.lower():
                return category
    return 'other'
```

##### Step 6: 정비 일정 자동 생성

```python
def generate_maintenance_schedule(part):
    """부품에 따른 정비 일정 자동 생성"""
    rules = {
        'engine_oil': {'interval': '100시간', 'level': '소유자'},
        'standing_rigging': {'interval': '6개월', 'level': '전문가'},
        'sails': {'interval': '3개월', 'level': '소유자'},
        'hull_inspection': {'interval': '1년', 'level': '전문가'}
    }

    # GPT-4를 사용한 맞춤 정비 일정 생성
    prompt = f"""
    다음 요트 부품에 대한 정비 일정을 생성하세요:
    부품명: {part['name']}
    재질: {part['material']}
    사용 환경: 해수

    다음 정보를 포함하세요:
    - 점검 주기
    - 점검 항목
    - 부식 위험도
    - 수리 방법
    - 예상 비용
    """

    return gpt4_generate(prompt)
```

### 2. 기존 요트에 부품 매뉴얼 추가

#### 사용자 작업 흐름

```
1. 기존 요트 선택
2. "부품 매뉴얼 추가" 클릭
3. 새로운 부품 매뉴얼 PDF 업로드
4. AI가 기존 부품과 비교하여 신규/업데이트 구분
5. 충돌 확인 및 병합
6. 저장
```

#### AI 처리 로직

##### 중복 검사

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_duplicate_parts(new_part, existing_parts):
    """신규 부품과 기존 부품 중복 검사"""
    vectorizer = TfidfVectorizer()

    # 부품명 + 설명을 벡터화
    texts = [f"{p['name']} {p.get('description', '')}"
             for p in existing_parts]
    texts.append(f"{new_part['name']} {new_part.get('description', '')}")

    tfidf_matrix = vectorizer.fit_transform(texts)
    similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    # 유사도 80% 이상이면 중복으로 판단
    threshold = 0.8
    duplicates = []
    for idx, score in enumerate(similarity_scores[0]):
        if score > threshold:
            duplicates.append({
                'existing_part': existing_parts[idx],
                'similarity': score
            })

    return duplicates
```

##### 자동 병합

```python
def merge_part_info(existing_part, new_part):
    """기존 부품 정보와 신규 정보 병합"""
    merged = existing_part.copy()

    # 비어있는 필드 채우기
    for key, value in new_part.items():
        if key not in merged or not merged[key]:
            merged[key] = value
        elif isinstance(value, list):
            # 리스트 항목 병합 (중복 제거)
            merged[key] = list(set(merged[key] + value))
        elif key == 'price':
            # 가격은 최신 정보로 업데이트
            merged[key] = value
            merged['priceHistory'] = merged.get('priceHistory', [])
            merged['priceHistory'].append({
                'price': existing_part.get('price'),
                'date': datetime.now().isoformat()
            })

    merged['lastUpdated'] = datetime.now().isoformat()
    merged['source'] = 'merged'

    return merged
```

### 3. 실시간 부품 인식 (모바일 앱)

#### 카메라로 부품 촬영 시

```python
import torch
from torchvision import models, transforms

# 사전 학습된 모델 로드
model = models.resnet50(pretrained=True)
model.eval()

def recognize_part_from_photo(image):
    """사진으로 부품 인식"""
    # 이미지 전처리
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)

    # 예측
    with torch.no_grad():
        output = model(input_batch)

    # 결과 반환
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    return {
        'part_id': predicted_class,
        'confidence': probabilities[predicted_class].item(),
        'alternatives': top_5_predictions
    }
```

### 4. 챗봇 지원 (정비 가이드)

#### GPT-4 기반 정비 도우미

```python
from openai import OpenAI

client = OpenAI()

def maintenance_chatbot(user_question, yacht_data):
    """요트 정비 관련 질문 답변"""
    context = f"""
    요트 정보:
    - 모델: {yacht_data['name']}
    - 부품 수: {len(yacht_data['parts'])}
    - 최근 정비: {yacht_data['lastMaintenance']}

    사용자 질문: {user_question}
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "당신은 요트 정비 전문가입니다. 사용자의 요트 관리를 도와주세요."},
            {"role": "user", "content": context}
        ]
    )

    return response.choices[0].message.content
```

**예시 질문:**

- "엔진 오일은 언제 교체해야 하나요?"
- "마스트에 부식이 있는데 어떻게 해야 하나요?"
- "다음 레이스 전에 점검해야 할 항목은?"

---

## 🗄️ 데이터베이스 스키마

### Physical Parts (실제 부품)

```typescript
interface PhysicalPart {
  id: string; // 고유 ID (예: fe28-mast-01)
  category: string; // 카테고리
  name: string; // 부품명
  partNumber: string; // 부품 번호
  material: string; // 재질
  manufacturer: string; // 제조사
  weight?: string; // 무게
  dimensions?: string; // 치수
  price: number; // 가격
  availability: string; // 구매 가능 여부
  maintenanceInterval: string; // 정비 주기
}
```

### Maintenance Items (점검 항목)

```typescript
interface MaintenanceItem {
  id: string; // 고유 ID (예: eng-001)
  partNumber: string; // 부품 번호
  name: string; // 점검 항목명 (영문)
  nameKo: string; // 점검 항목명 (한글)
  category: string; // 카테고리
  inspectionItems: string[]; // 점검 세부 항목
  checkInterval: string; // 점검 주기
  material?: string; // 재질
  corrosionRisk?: string; // 부식 위험도
  failureConsequence?: string; // 고장 시 결과
  repairMethod?: string; // 수리 방법
  estimatedCost?: string; // 예상 비용
  maintenanceLevel?: string; // 정비 난이도 (소유자/전문가)
}
```

### Yacht Model

```typescript
interface Yacht {
  id: string; // 요트 ID
  name: string; // 요트명
  manufacturer: string; // 제조사
  type: string; // 타입 (Racing/Cruising)
  length: number; // 길이 (feet)
  officialWebsite?: string; // 공식 웹사이트
  manualPDF: string; // 매뉴얼 PDF 경로
  dimensions: {
    lengthFeet: number;
    lengthMeters: number;
    beam: number; // 폭
    draft: number; // 흘수
    displacement: number; // 배수량
  };
  parts: {
    [category: string]: {
      physicalParts: PhysicalPart[];
      maintenanceItems: MaintenanceItem[];
    };
  };
}
```

---

## 🚀 API 엔드포인트 (백엔드)

### Yacht API

```
GET    /api/yacht/{yachtId}           - 요트 상세 정보
POST   /api/yacht                     - 새 요트 등록
PUT    /api/yacht/{yachtId}           - 요트 정보 수정
DELETE /api/yacht/{yachtId}           - 요트 삭제
```

### Part API

```
GET    /api/part/{yachtId}            - 요트별 부품 목록
POST   /api/part                      - 부품 추가
PUT    /api/part                      - 부품 수정
DELETE /api/part/{partId}             - 부품 삭제
```

### Repair API

```
GET    /api/repair/{partId}           - 부품별 수리 이력
POST   /api/repair                    - 수리 이력 추가
PUT    /api/repair                    - 수리 이력 수정
DELETE /api/repair/{repairId}         - 수리 이력 삭제
```

### Calendar API

```
GET    /api/calendars                 - 캘린더 목록 (partId 필터링)
GET    /api/calendars/{id}            - 캘린더 상세
POST   /api/calendars                 - 캘린더 이벤트 생성
PUT    /api/calendars/{id}            - 캘린더 이벤트 수정
DELETE /api/calendars/{id}            - 캘린더 이벤트 삭제
```

### AI API (향후 구현)

```
POST   /api/ai/extract-manual         - PDF 매뉴얼에서 부품 정보 추출
POST   /api/ai/recognize-part         - 이미지에서 부품 인식
POST   /api/ai/merge-parts            - 부품 정보 자동 병합
POST   /api/ai/chatbot                - 정비 챗봇
POST   /api/ai/generate-schedule      - 정비 일정 자동 생성
```

---

## 📊 통계

### 데이터베이스 현황

- **요트 종류**: 20종
- **PDF 매뉴얼**: 20개
- **실제 부품 (Physical Parts)**: 51개
- **점검 항목 (Maintenance Items)**: 1,020개
- **카테고리**: 11개
  - Rigging (리깅)
  - Sails (돛)
  - Hull (선체)
  - Engine (엔진)
  - Electrical (전기)
  - Steering (조타)
  - Plumbing (배관)
  - Deck Hardware (데크 하드웨어)
  - Safety (안전)
  - Propulsion (추진)
  - Foils (수중익)

### 파일 크기

- `yacht_parts_database.json`: 688KB (19,209 lines)
- `yacht_parts_app_data.json`: 30KB (975 lines)
- `yacht_manual_resources.json`: 9.9KB (276 lines)

---

## 🛠️ 기술 스택

### 백엔드

- **Framework**: Spring Boot 3.5.7
- **Language**: Java 21
- **Database**: MySQL
- **Security**: Spring Security + JWT
- **ORM**: JPA/Hibernate

### AI/ML

- **OCR**: Tesseract, Google Cloud Vision API
- **NLP**:
  - Transformers (Hugging Face)
  - BERT-NER
  - GPT-4 API
- **이미지 인식**:
  - CLIP (OpenAI)
  - YOLO
  - ResNet
- **데이터 처리**:
  - Python 3.11+
  - Pandas
  - NumPy
  - Camelot (PDF 테이블 추출)

### 프론트엔드 (계획)

- **Mobile**: React Native / Flutter
- **Web**: React / Next.js

---

## 📝 향후 개발 계획

### Phase 1: AI 모델 학습 (1-2개월)

- [ ] 요트 부품 이미지 데이터셋 수집 (10,000+ 이미지)
- [ ] Custom CNN 모델 학습 (부품 분류)
- [ ] NER 모델 Fine-tuning (요트 도메인)
- [ ] OCR 정확도 개선 (스캔 품질 낮은 매뉴얼 대응)

### Phase 2: API 개발 (1개월)

- [ ] PDF 업로드 및 처리 API
- [ ] 부품 인식 API (이미지 → 부품 정보)
- [ ] 자동 병합 API
- [ ] 챗봇 API (GPT-4 통합)

### Phase 3: 모바일 앱 통합 (2개월)

- [ ] 카메라 촬영 → 부품 인식
- [ ] 음성 명령 ("엔진 오일 점검 기록")
- [ ] AR 가이드 (부품 위치 표시)
- [ ] 오프라인 모드 (로컬 AI 모델)

### Phase 4: 커뮤니티 기능 (1개월)

- [ ] 사용자 기여 시스템 (매뉴얼 공유)
- [ ] 부품 정보 크라우드소싱
- [ ] 정비 팁 공유
- [ ] 전문가 Q&A

### Phase 5: 고급 기능 (진행 중)

- [ ] 예측 정비 (Predictive Maintenance)
  - 사용 패턴 분석
  - 고장 예측 알고리즘
- [ ] 부품 가격 추적 및 알림
- [ ] 3D 모델 뷰어 (부품 조립/분해 시뮬레이션)
- [ ] IoT 센서 통합 (실시간 모니터링)

---

## 🔐 보안 및 개인정보

### 데이터 보호

- 사용자 업로드 PDF는 암호화 저장
- 개인 요트 정보는 비공개
- AI 처리는 서버 사이드에서만 수행

### API 보안

- JWT 토큰 기반 인증
- Rate Limiting (API 호출 제한)
- Input Validation (악성 파일 차단)

---

## 📚 참고 자료

### 요트 매뉴얼 소스

- [J/Boats Official Manuals](https://jboats.com)
- [Beneteau Documentation](https://beneteau.com)
- [North Sails Tuning Guides](https://northsails.com)
- [Class Association Websites](https://sailing.org)

### AI/ML 리소스

- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [OpenAI CLIP](https://github.com/openai/CLIP)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Camelot PDF Tables](https://camelot-py.readthedocs.io)

---

## 👥 기여 방법

### 새로운 요트 추가

1. Fork this repository
2. PDF 매뉴얼을 `yachtpdf/` 폴더에 추가
3. `yacht_manual_resources.json`에 정보 추가
4. Pull Request 생성

### AI 모델 개선

1. `models/` 디렉토리에 새 모델 추가
2. 성능 벤치마크 결과 포함
3. 문서 업데이트

---

## 📚 프로젝트 문서

### 통합 및 호환성 문서

- **[INTEGRATION_SUMMARY.md](INTEGRATION_SUMMARY.md)** - 프론트엔드-백엔드 통합 분석 최종 보고서

  - 호환성 검증 결과
  - 핵심 문제점 및 해결 방안
  - 빠른 시작 가이드
  - 배포 전 체크리스트

- **[FRONTEND_BACKEND_COMPATIBILITY_REPORT.md](FRONTEND_BACKEND_COMPATIBILITY_REPORT.md)** - 상세 호환성 분석
  - API 엔드포인트 비교
  - 데이터 모델 비교
  - 수정 코드 예시
  - 테스트 시나리오

### 백엔드 문서

- **[backend/MODULE_INTEGRATION_SUMMARY.md](backend/MODULE_INTEGRATION_SUMMARY.md)** - 모듈 통합 완료 보고서

  - Part, Repair, Calendar 모듈 통합 내역
  - 19개 파일 추가 내역
  - API 엔드포인트 목록

- **[backend/REQUIRED_CHANGES.md](backend/REQUIRED_CHANGES.md)** - 백엔드 필수 수정 사항
  - Entity 수정 가이드
  - DTO 수정 가이드
  - 데이터베이스 스키마 변경
  - 통합 API 구현 예시

### 데이터 문서

- **[yacht_database_summary.md](yacht_database_summary.md)** - 요트 데이터베이스 요약
- **[final_yacht_parts_summary.md](final_yacht_parts_summary.md)** - 요트 부품 최종 요약
- **[manual_check_final.md](manual_check_final.md)** - 매뉴얼 확인 최종 보고

---

## 📞 문의

프로젝트 관련 문의:

- GitHub Issues: [Create Issue](#)
- Email: yacht-parts-team@example.com

---

## 📄 라이선스

MIT License

Copyright (c) 2024 Yacht Parts Management Team

---

## ✅ 체크리스트

### 데이터

- [x] 20종 요트 PDF 매뉴얼 수집
- [x] 텍스트 추출 및 구조화
- [x] Physical Parts / Maintenance Items 분리
- [x] 명명 규칙 적용
- [x] JSON 데이터베이스 생성

### 백엔드

- [x] Part 모듈 API
- [x] Repair 모듈 API
- [x] Calendar 모듈 API
- [x] Yacht 모듈 API
- [ ] AI 처리 API

### AI/ML

- [ ] OCR 모델 배포
- [ ] NER 모델 학습
- [ ] 이미지 인식 모델
- [ ] 챗봇 통합
- [ ] 자동 병합 로직

### 프론트엔드

- [ ] 모바일 앱 (React Native)
- [ ] 카메라 촬영 기능
- [ ] PDF 업로드 UI
- [ ] 부품 검색 및 필터링

---

**Last Updated**: 2024-11-12  
**Version**: 1.0.0  
**Status**: ✅ 데이터베이스 완성, 🚧 AI 개발 중
