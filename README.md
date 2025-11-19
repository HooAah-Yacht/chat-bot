# 🛥️ 요트 정보 챗봇 (Yacht Information Chatbot)

20종 세일링 요트의 상세 정보를 제공하는 AI 기반 챗봇입니다.

## 📊 데이터 개요

### 포함된 데이터
- **요트 종류**: 20종
- **PDF 매뉴얼**: 17개 원본 매뉴얼
- **부품 데이터**: 51개 물리적 부품 + 1,020개 점검 항목
- **상세 스펙**: 치수, 돛 면적, 엔진, 탱크, 숙박시설 등

### 데이터 파일
| 파일명 | 크기 | 설명 |
|--------|------|------|
| `yacht_specifications.json` | 35KB | 20종 요트 상세 스펙 (LOA, Beam, Draft, 돛 면적, 엔진 등) |
| `yacht_parts_database.json` | 688KB | 부품 및 점검 항목 데이터베이스 |
| `yacht_manual_resources.json` | 10KB | PDF 매뉴얼 리소스 맵핑 |
| `extracted_yacht_parts_detailed.json` | - | 상세 부품 정보 (PDF 분석 결과) |
| `extracted_yacht_parts.json` | - | 간단한 부품 목록 (PDF 분석 결과) |
| `yacht_parts_app_data.json` | - | 모바일 앱용 부품 데이터 |
| `registered_yachts.json` | - | PDF로 등록된 요트의 전체 등록 정보 |
| `YachtList01.json` | - | 기존 요트 리스트 (기본 정보) |

---

## 🚀 빠른 시작

### 필수 요구사항
- **Python 3.8 이상**

### 설치 및 실행

```bash
# 1. 레포지토리 클론
git clone https://github.com/HooAah-Yacht/chat-bot.git
cd chat-bot

# 2. 챗봇 실행 (대화형 모드)
python chatbot.py
```

---

## 💬 사용법

### 1️⃣ 대화형 모드 (추천)

```bash
python chatbot.py
```

**대화 예시:**
```
💬 질문: Laser 크기
🤖 챗봇:
'Laser (ILCA 7 / Standard)'의 크기 정보는 아래와 같습니다:

📏 **기본 치수**
- LOA (전장): 4.23m (13.83ft)
- LWL (수선장): 3.81m (12.5ft)
- Beam (폭): 1.39m (4.56ft)
- Draft (흘수): 0.787m (2.58ft)
- Displacement (배수량): 59kg
- Mast Height (마스트 높이): 6.43m

💬 질문: FarEast 28 정보
🤖 챗봇:
🛥️ **FarEast 28** - 상세 정보

제조사: FarEast Yachts
타입: One-Design Racing
디자이너: Tom Schnackenberg
제작년도: 1992-Present

📏 **치수**
- LOA: 8.53m (28ft)
- Beam (폭): 2.75m
- Draft (흘수): 1.80m
- Displacement (배수량): 2200kg
- Mast Height: 11.5m

⛵ **돛 면적**
- Main: 21.5 m²
- Jib: 18.0 m²
- Spinnaker: 60.0 m²
- Total: 39.5m² (upwind)

🔧 **엔진**
- Type: Outboard
- Power: 9.9 HP
- Model: Yamaha or equivalent
```

### 2️⃣ 단일 질문 모드

```bash
# 크기 정보 질문
python chatbot.py -q "Beneteau Oceanis 46.1 크기"

# 전체 정보 질문
python chatbot.py --question "J24 정보"

# 상세 스펙 질문
python chatbot.py -q "Swan 50 스펙"
```

### 3️⃣ 모델 목록 확인

```bash
python chatbot.py --list
```

**출력 예시:**
```
📋 총 20개의 요트 모델:

  1. FarEast 28 (One-Design Racing)
  2. Farr 40 (One-Design Racing)
  3. Beneteau 473 (Cruiser)
  4. Laser (ILCA 7 / Standard) (One-Design Dinghy)
  5. Beneteau First 36.7 (Cruiser-Racer)
  ... (15개 더)
```

### 4️⃣ 데이터 정보 확인

```bash
python chatbot.py --info
```

**출력 예시:**
```
📊 요트 데이터 정보
==================================================
JSON 경로: C:\...\chat-bot\data\yacht_specifications.json
데이터 버전: new (상세 버전)
총 요트 개수: 20
데이터 버전: 1.0
마지막 업데이트: 2024-11-13

📂 카테고리:
  - racing: 9개
  - cruiser: 3개
  - cruiserRacer: 7개
  - dinghy: 1개
==================================================
```

---

## 📋 질문 예시

### 크기/치수 질문
- "Laser 크기"
- "FarEast 28 길이"
- "Beneteau Oceanis 46.1 폭"
- "J70 마스트 높이"

### 전체 정보 질문
- "FarEast 28 정보"
- "Laser 스펙"
- "Swan 50 상세 정보"
- "Beneteau 473 모든 정보"

---

## 📂 프로젝트 구조

```
chat-bot/
├── README.md                          # 이 파일
├── chatbot.py                         # 메인 챗봇 스크립트 (향상된 버전)
├── chatbot_gemini.py                  # 🤖 Gemini AI 챗봇 (기본 대화형)
├── chatbot_with_pdf_upload.py        # 🤖 PDF 업로드 기능이 있는 챗봇
├── chatbot_api.py                     # 🌐 Flask RESTful API 서버
├── yacht_document_analyzer.py        # 📄 PDF 문서 분석기
├── chatbot.ipynb                      # Jupyter 노트북 버전
├── YachtList01.json                   # 기존 요트 리스트
├── .gitignore                         # Git 제외 파일
│
├── data/                              # 데이터 디렉토리
│   ├── yacht_specifications.json     # ⭐ 상세 요트 스펙 (추천)
│   ├── yacht_parts_database.json     # 부품 및 점검 데이터베이스
│   ├── yacht_manual_resources.json   # 매뉴얼 리소스
│   ├── yacht_parts_app_data.json     # 앱 데이터
│   ├── extracted_yacht_parts.json    # 추출된 원본 데이터
│   ├── extracted_yacht_parts_detailed.json  # 상세 추출 데이터
│   ├── registered_yachts.json         # PDF로 등록된 요트 목록
│   └── yachtpdf/                      # PDF 매뉴얼 (17개)
│       ├── OC15aiiFAREAST28RClassrules-[19458].pdf
│       ├── rulebook.pdf
│       └── ...
│
├── scripts/                           # 데이터 처리 스크립트 (13개)
│   ├── extract_yacht_parts.py         # PDF 데이터 추출
│   ├── extract_yacht_specifications.py  # 스펙 추출
│   ├── add_inspection_parts.py        # 점검 항목 추가
│   ├── restructure_database.py        # DB 재구성
│   ├── create_complete_yacht_specs.py  # 완전한 스펙 생성
│   └── ... (8개 더)
│
└── docs/                              # 문서 (11개)
    ├── README.md                      # 프로젝트 전체 개요
    ├── yacht_specifications_guide.md  # 스펙 사용 가이드
    ├── final_yacht_parts_summary.md   # 부품 데이터베이스 요약
    ├── yacht_database_summary.md      # 데이터베이스 요약
    └── ... (7개 더)
```

---

## 🎯 주요 기능

### ✅ 상세한 요트 정보 제공
- **치수**: LOA, LWL, Beam, Draft, Displacement, Mast Height
- **돛 면적**: Main, Jib, Spinnaker, Total
- **엔진**: Type, Power, Model
- **탱크**: Fuel, Water
- **숙박시설**: Cabins, Berths, Heads

### ✅ 지능형 매칭
- 모델명 자동 정규화 (공백, 구두점 무시)
- 부분 매칭 지원 ("Laser" → "Laser (ILCA 7 / Standard)")
- 대소문자 구분 없음

### ✅ 다양한 질문 형식 지원
- 크기/치수 질문: "크기", "길이", "폭", "높이"
- 전체 정보 질문: "정보", "스펙", "사양", "상세"
- 자연어 질문 가능

---

## 📊 데이터 구조

### yacht_specifications.json 구조

```json
{
  "version": "1.0",
  "lastUpdated": "2024-11-13",
  "totalYachts": 20,
  "categories": {
    "racing": ["fareast-28", "farr-40", ...],
    "cruiser": ["beneteau-473", ...],
    "cruiserRacer": [...],
    "dinghy": ["laser"]
  },
  "yachts": [
    {
      "id": "fareast-28",
      "name": "FarEast 28",
      "manufacturer": "FarEast Yachts",
      "type": "One-Design Racing",
      "designer": "Tom Schnackenberg",
      "year": "1992-Present",
      "manual": "data/yachtpdf/OC15aiiFAREAST28RClassrules-[19458].pdf",
      
      "dimensions": {
        "loa": {"value": 8.53, "unit": "m", "display": "8.53m (28ft)"},
        "beam": {"value": 2.75, "unit": "m", "display": "2.75m"},
        "draft": {"value": 1.8, "unit": "m", "display": "1.80m"},
        "displacement": {"value": 2200, "unit": "kg", "display": "2200kg"},
        "mastHeight": {"value": 11.5, "unit": "m", "display": "11.5m"}
      },
      
      "sailArea": {
        "main": {"value": 21.5, "unit": "m²"},
        "jib": {"value": 18.0, "unit": "m²"},
        "spinnaker": {"value": 60.0, "unit": "m²"},
        "total": {"value": 39.5, "unit": "m²", "display": "39.5m² (upwind)"}
      },
      
      "engine": {
        "type": "Outboard",
        "power": "9.9 HP",
        "model": "Yamaha or equivalent"
      },
      
      "accommodation": {
        "crew": "6-7 people",
        "racing": "5-6 crew typical"
      }
    }
  ]
}
```

---

## 🔧 문제 해결

### FileNotFoundError 발생 시
- `data/yacht_specifications.json` 파일이 있는지 확인
- 또는 `YachtList01.json` 파일을 스크립트와 같은 폴더에 배치

### 요트를 찾을 수 없다는 오류 발생 시
1. `python chatbot.py --list`로 모델 목록 확인
2. 정확한 모델명 사용
3. 부분 이름도 가능 (예: "Laser", "FarEast")

### Python이 인식되지 않는 경우
```bash
# Python 버전 확인
python --version
py --version

# Python 설치 확인
# Windows: Microsoft Store 또는 python.org에서 설치
# 설치 시 "Add Python to PATH" 옵션 체크 필수
```

---

## 🤖 통합 AI 챗봇 (chatbot_unified.py) ⭐ **추천**

### 모든 기능을 통합한 단일 챗봇

**`chatbot_unified.py`**는 모든 챗봇 기능을 하나로 통합한 통합 챗봇입니다.

#### 주요 기능
- ✅ **자연어 대화**: 정해진 형식 없이 자유롭게 질문 (Gemini AI 기반)
- ✅ **지능형 의도 파악**: 사용자의 의도를 자동으로 파악하여 적절한 응답
- ✅ **컨텍스트 이해**: 이전 대화 내용을 기억하고 연관된 답변
- ✅ **PDF 문서 분석**: 요트 매뉴얼 PDF를 업로드하여 자동으로 스펙 및 부품 정보 추출
- ✅ **전체 스펙 추출**: 외부 치수(LOA, Beam, Draft 등), 엔진 정보, 부품 정보 자동 추출
- ✅ **자동 JSON 저장**: 분석 결과를 여러 JSON 파일에 자동 저장
- ✅ **모바일 앱 지원**: iOS, Android 앱에서 파일 업로드 지원
- ✅ **RESTful API**: Flutter 앱 및 웹 연동 지원

#### 빠른 시작

```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. 환경 변수 설정 (.env 파일 생성)
# .env.example 파일을 복사하여 .env 파일을 만들고 API 키를 입력하세요
cp .env.example .env
# 또는 Windows의 경우:
# copy .env.example .env
# 그 다음 .env 파일을 열어 GEMINI_API_KEY를 설정하세요

# 3. 챗봇 실행
python chatbot_unified.py
```

**실행 모드:**
- **대화형 모드** (기본): `python chatbot_unified.py`
- **API 서버 모드**: `python chatbot_unified.py --mode api`
- **API 키 직접 지정**: `python chatbot_unified.py --api-key YOUR_API_KEY`

**⚠️ 중요: API 키 설정**
- `.env` 파일에 `GEMINI_API_KEY`를 설정하는 것을 권장합니다.
- `.env.example` 파일을 참고하여 `.env` 파일을 생성하세요.
- `.env` 파일은 `.gitignore`에 포함되어 있어 GitHub에 업로드되지 않습니다.

#### 작동 방식

1. **자연어 요청 인식**
   - "요트 등록하고 싶어" → PDF 업로드 안내
   - "도움말 보여줘" → 도움말 표시
   - "요트 목록 알려줘" → 요트 목록 반환
   - "Farr 40 크기 알려줘" → 요트 정보 제공

2. **PDF 업로드 및 분석**
   - 사용자가 PDF 파일 경로 입력
   - 자동으로 텍스트 추출 (PyPDF2 또는 pdfplumber)
   - Gemini AI로 문서 분석
   - 요트 스펙 및 부품 정보 추출
   - 여러 JSON 파일에 자동 저장

3. **데이터 저장 경로**
   - 모든 데이터는 `data/` 디렉토리에 저장됩니다.

#### 챗봇 관련 Python 파일

| 파일명 | 설명 | 실행 방법 | 용도 |
|--------|------|----------|------|
| `chatbot_unified.py` ⭐ | **통합 챗봇 (추천)** | `python chatbot_unified.py` | 모든 기능 통합 (대화형, PDF 업로드, API 서버) |
| `chatbot_gemini.py` | 기본 Gemini AI 챗봇 | `python chatbot_gemini.py` | 터미널 대화형 모드, 자연어 질문 |
| `chatbot_with_pdf_upload.py` | PDF 업로드 기능이 있는 챗봇 | `python chatbot_with_pdf_upload.py` | 요트 매뉴얼 PDF 분석 및 등록 |
| `chatbot_api.py` | Flask RESTful API 서버 | `python chatbot_api.py` | Flutter 앱 및 웹 연동 (http://localhost:5000) |
| `yacht_document_analyzer.py` | PDF 문서 분석기 | `python yacht_document_analyzer.py` | PDF에서 스펙 및 부품 정보 추출 (독립 실행) |
| `chatbot.py` | 기존 챗봇 스크립트 | `python chatbot.py` | 20종 요트 정보 조회 (기존 버전) |

#### 사용 예시

**1. 대화형 모드 (기본)**
```bash
python chatbot_unified.py
```

**대화 예시:**
```
👤 You: 요트 등록하고 싶어

🤖 AI: 📄 요트 문서를 등록하세요!

요트 매뉴얼 PDF 파일을 업로드해주시면:
1. 📋 문서를 자동으로 분석합니다
2. ⛵ 요트 정보를 추출합니다
3. 🔧 부품 정보를 정리합니다
4. ✅ 데이터베이스에 등록합니다

PDF 파일 경로를 입력해주세요! 📎

👤 You: "C:\Users\user\Documents\Swan48-LR-2021.pdf"

🤖 AI: 📄 PDF 분석 시작: Swan48-LR-2021.pdf
      📝 PDF에서 텍스트 추출 중...
      🤖 AI 분석 중...
      ✅ 분석 완료!
      ✅ 등록이 완료됐습니다! 🎉
      
      **등록된 요트 정보:**
      ⛵ 모델: Swan 48
      🏭 제조사: Nautor's Swan
      📏 치수 정보: 추출됨
      🔧 부품 정보: 53개 부품 추출됨
      ⚙️ 엔진 정보: 추출됨
```

**2. API 서버 모드**
```bash
python chatbot_unified.py --mode api
```

서버가 실행되면:
- `POST /api/chat` - 채팅 메시지 전송
- `POST /api/chat/upload` - PDF 파일 업로드 (모바일 앱용)
- `GET /api/chat/history` - 대화 기록 조회
- `GET /api/health` - 서버 상태 확인

#### PDF 업로드 및 자동 분석

새 요트를 등록할 때 PDF 매뉴얼을 업로드하면 자동으로 다음 정보를 추출합니다:

- ✅ **외부 치수**: LOA, LWL, Beam, Draft, Displacement, Mast Height
- ✅ **엔진 정보**: Type, Power, Model
- ✅ **돛 면적**: Main, Jib, Spinnaker, Total
- ✅ **부품 정보**: Rigging, Sails, Engine, Hull, Electrical, Plumbing 등
- ✅ **정비 주기**: 각 부품별 정비 주기(interval)

**사용 예시:**
```
👤 You: "C:\Users\user\Documents\Sun Odyssey 380 Owners manual.pdf"

🤖 AI: 📄 문서를 분석 중입니다...
      잠시만 기다려주세요! ⏳

✅ 등록이 완료됐습니다! 🎉

**등록된 요트 정보:**
⛵ 모델: Sun Odyssey 380
🏭 제조사: JEANNEAU
📄 문서 유형: Owner's Manual

**추출된 정보:**
📏 치수 정보: 추출됨
🔧 부품 정보: 15개 부품 추출됨
⚙️ 엔진 정보: 추출됨
```

#### 저장되는 JSON 파일 및 경로

PDF 분석 후 다음 JSON 파일들에 **자동으로 저장**됩니다:

**저장 경로**: 모든 파일은 `data/` 디렉토리에 저장됩니다.

| 파일명 | 저장 경로 | 설명 | 저장 내용 |
|--------|----------|------|----------|
| `yacht_specifications.json` | `data/yacht_specifications.json` | 요트 스펙 데이터베이스 | 외부 치수(LOA, Beam, Draft, Displacement, Mast Height), 엔진 정보, 돛 면적 등 **전체 스펙** |
| `yacht_parts_database.json` | `data/yacht_parts_database.json` | 부품 데이터베이스 | 카테고리별 부품 정보 (Rigging, Sails, Engine, Hull, Electrical, Plumbing) |
| `extracted_yacht_parts_detailed.json` | `data/extracted_yacht_parts_detailed.json` | 상세 부품 정보 | 부품 상세 정보 (description, specifications) |
| `extracted_yacht_parts.json` | `data/extracted_yacht_parts.json` | 간단한 부품 목록 | 부품 기본 정보 (name, manufacturer, model, category, interval) |
| `yacht_parts_app_data.json` | `data/yacht_parts_app_data.json` | 앱 데이터 | 모바일 앱용 부품 데이터 (maintenanceInterval 포함) |
| `registered_yachts.json` | `data/registered_yachts.json` | 등록 이력 | PDF로 등록된 요트의 전체 등록 정보 (등록 날짜, PDF 파일명, 분석 결과 포함) |

**저장 프로세스:**
1. PDF 파일 업로드 및 텍스트 추출
2. Gemini AI로 문서 분석 (요트 스펙, 부품 정보 추출)
3. 추출된 데이터를 6개 JSON 파일에 자동 저장
4. 기존 데이터와 병합 (동일 요트가 있으면 업데이트, 없으면 추가)

#### 자연어 요청 예시

**요트 정보 조회:**
```
👤 You: Farr 40 크기 알려줘
🤖 AI: 'Farr 40'의 크기 정보는 아래와 같습니다:
      📏 **기본 치수**
      - LOA (전장): 12.15m
      - Beam (폭): 3.58m
      ...
```

**요트 등록:**
```
👤 You: 요트 등록하고 싶어
🤖 AI: 📄 요트 문서를 등록하세요!
      PDF 파일 경로를 입력해주세요! 📎
```

**도움말 요청:**
```
👤 You: 도움말 보여줘
🤖 AI: 📖 HooAah Yacht 챗봇 도움말
      **사용 가능한 명령어:**
      - `/list` - 요트 목록 보기
      ...
```

**요트 목록 조회:**
```
👤 You: 요트 목록 알려줘
🤖 AI: 📋 총 20개의 요트 모델:
      1. FarEast 28
      2. Farr 40
      ...
```

**요트 추천:**
```
👤 You: 레이싱에 좋은 요트 추천해줘
🤖 AI: 레이싱에 최적화된 요트를 추천드립니다! 🏁
      **입문자용:**
      - J/24: 세계적으로 가장 인기 있는 원디자인
      ...
```

#### 작동 흐름

```
사용자 입력
    ↓
의도 파악 (Gemini AI 또는 키워드 기반)
    ↓
┌─────────────────────────────────────┐
│  PDF 업로드 의도?                  │
│  → PDF 파일 경로 추출              │
│  → PDF 텍스트 추출 (PyPDF2/pdfplumber) │
│  → Gemini AI 분석                  │
│  → 요트 스펙 및 부품 정보 추출      │
│  → 6개 JSON 파일에 자동 저장        │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  도움말 요청?                      │
│  → 도움말 메시지 반환              │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  요트 정보 조회?                    │
│  → 기존 20종 요트 데이터에서 검색   │
│  → 상세 정보 제공                   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  일반 대화?                        │
│  → Gemini AI로 자연스러운 응답 생성 │
└─────────────────────────────────────┘
```

#### 상세 가이드

📖 **[AI 챗봇 설정 가이드](AI_CHATBOT_SETUP_GUIDE.md)** - 설치, 설정, Flutter 통합 방법  
📖 **[PDF 업로드 챗봇 가이드](PDF_UPLOAD_CHATBOT_GUIDE.md)** - PDF 분석 및 등록 방법  
📖 **[JSON 저장 정보](JSON_STORAGE_INFO.md)** - 저장되는 JSON 파일 상세 설명

---

## 🚀 향후 계획

- [x] AI 기반 자연어 대화 챗봇 ✅ **완료!**
- [x] 웹 API 서버 버전 ✅ **완료!**
- [x] Flutter 앱 통합 ✅ **완료!**
- [x] AI 기반 PDF 자동 파싱 ✅ **완료!**
- [x] 전체 스펙 추출 (외부 치수, 엔진, 부품) ✅ **완료!**
- [x] 부품 정보 자동 추출 및 JSON 저장 ✅ **완료!**
- [ ] 점검 주기 계산 기능
- [ ] 유지보수 비용 예측
- [ ] 음성 인식 기능
- [ ] 다국어 지원

---

## 📚 참고 문서

더 자세한 정보는 `docs/` 디렉토리를 참조하세요:

- **[README.md](docs/README.md)**: 프로젝트 전체 개요
- **[yacht_specifications_guide.md](docs/yacht_specifications_guide.md)**: 스펙 데이터 사용 가이드
- **[final_yacht_parts_summary.md](docs/final_yacht_parts_summary.md)**: 부품 데이터베이스 요약
- **[yacht_database_summary.md](docs/yacht_database_summary.md)**: 데이터베이스 구조 설명

---

## 📜 라이선스

이 프로젝트는 HooAah-Yacht 팀의 소유입니다.

---

## 👥 기여

버그 리포트, 기능 제안, PR은 언제나 환영합니다!

**Repository**: https://github.com/HooAah-Yacht/chat-bot

---

## 🔗 관련 레포지토리

- **Backend**: https://github.com/HooAah-Yacht/backend
- **Frontend**: https://github.com/HooAah-Yacht/frontend

---

**Made with ⛵ by HooAah-Yacht Team**
