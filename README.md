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

## 🚀 향후 계획

- [ ] 요트 부품 정보 조회 기능 추가
- [ ] 점검 주기 계산 기능
- [ ] 유지보수 비용 예측
- [ ] 웹 API 서버 버전
- [ ] Flutter 앱 통합
- [ ] AI 기반 PDF 자동 파싱

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
