# 📝 커스텀 매뉴얼 등록 가이드

## 🎯 시나리오

사용자가 **이미 등록된 요트**(예: J/70, OCEANIS 46.1)에 대해:
- 자신만의 정비 노트
- 추가 부품 정보
- 커스텀 매뉴얼 PDF
- 정비 기록

이런 커스텀 정보를 추가로 등록하고 싶을 때

---

## 🔄 현재 구조 분석

### 현재 데이터 구조:
```
yacht_specifications.json (마스터 데이터)
├── oceanis-46.1
├── j-70
└── dehler-38

registered_yachts.json (사용자 등록 데이터)
└── (비어있음)
```

### 문제점:
- ❌ 동일한 yacht ID에 여러 매뉴얼 등록 불가
- ❌ 사용자별 커스텀 정보 저장 방법 없음
- ❌ 마스터 데이터와 사용자 데이터 구분 없음

---

## ✅ 해결 방안

### 방안 1: 사용자 인스턴스 생성 (권장)

각 사용자가 동일한 요트 모델에 대해 **자신만의 인스턴스**를 만듦

```json
{
  "registered_yachts": [
    {
      "userYachtId": "user-j70-001",           // 사용자 요트 고유 ID
      "baseYachtId": "j-70",                   // 마스터 데이터 참조
      "userId": "user123",                     // 사용자 ID
      "nickname": "내 J/70",                   // 사용자 지정 이름
      "registrationDate": "2025-11-21",
      "customManuals": [
        {
          "id": "custom-manual-001",
          "title": "내 정비 노트",
          "type": "Custom Maintenance Log",
          "pdfPath": "uploads/user123/my-j70-notes.pdf",
          "uploadDate": "2025-11-21"
        }
      ],
      "customParts": [
        {
          "id": "custom-part-001",
          "name": "교체한 윈치",
          "manufacturer": "Harken",
          "model": "B60.2STC",
          "installDate": "2025-10-01",
          "maintenanceInterval": 6,
          "notes": "2025년 10월에 새로 교체함"
        }
      ],
      "maintenanceHistory": [
        {
          "date": "2025-11-01",
          "partId": "custom-part-001",
          "description": "윈치 그리스 주입",
          "cost": 50000,
          "nextMaintenanceDate": "2026-05-01"
        }
      ]
    }
  ]
}
```

---

## 🚀 구현: 커스텀 매뉴얼 등록 기능

### 1. 사용자 요청 플로우

```
사용자: "J/70에 내 정비 매뉴얼 추가하고 싶어"
   ↓
챗봇: "이미 등록된 J/70이 있나요?"
   ↓
사용자: "네" 또는 "아니요"
   ↓
챗봇 (네인 경우): 
  "기존 J/70에 추가할까요, 아니면 새로운 J/70 인스턴스를 만들까요?"
   ↓
사용자: "기존에 추가"
   ↓
챗봇: "매뉴얼 PDF 파일 경로를 입력하세요"
   ↓
사용자: "C:\Users\...\my-j70-manual.pdf"
   ↓
챗봇: 
  1. PDF 분석
  2. customManuals에 추가
  3. 새로운 부품 정보 추출
  4. customParts에 추가
   ↓
챗봇: "✅ 커스텀 매뉴얼이 추가되었습니다!"
```

### 2. 챗봇 명령어

```
# 새 요트 인스턴스 생성
"J/70 내 요트로 등록하고 싶어"
"새 J/70 추가"

# 커스텀 매뉴얼 추가
"J/70에 매뉴얼 추가"
"내 J/70에 정비 노트 업로드"

# 커스텀 부품 추가
"J/70에 부품 추가"
"내 J/70 윈치 정보 등록"
```

---

## 📊 데이터 구조 설계

### A. registered_yachts.json (확장)

```json
{
  "schemaVersion": "5.0",
  "lastUpdated": "2025-11-21",
  "userYachts": [
    {
      "userYachtId": "user-j70-001",
      "baseYachtId": "j-70",
      "userId": "user123",
      "nickname": "내 J/70",
      "registrationDate": "2025-11-21",
      
      "baseData": {
        "source": "yacht_specifications.json",
        "inheritSpecs": true,
        "inheritParts": true
      },
      
      "customManuals": [
        {
          "id": "custom-manual-001",
          "title": "내 정비 노트",
          "type": "Custom Maintenance Log",
          "pdfPath": "uploads/user123/my-j70-notes.pdf",
          "uploadDate": "2025-11-21",
          "analyzedData": {
            "parts": [...],
            "maintenance": [...]
          }
        }
      ],
      
      "customParts": [
        {
          "id": "custom-part-001",
          "name": "Harken 윈치",
          "category": "Deck Hardware",
          "manufacturer": "Harken",
          "model": "B60.2STC",
          "installDate": "2025-10-01",
          "purchasePrice": 500000,
          "maintenanceInterval": 6,
          "notes": "기존 윈치를 Harken으로 교체",
          "photos": [
            "uploads/user123/winch-photo1.jpg"
          ]
        }
      ],
      
      "maintenanceHistory": [
        {
          "id": "maint-001",
          "date": "2025-11-01",
          "partId": "custom-part-001",
          "type": "정기 점검",
          "description": "윈치 그리스 주입 및 베어링 점검",
          "cost": 50000,
          "technician": "직접",
          "nextMaintenanceDate": "2026-05-01",
          "photos": []
        }
      ],
      
      "modifications": [
        {
          "id": "mod-001",
          "date": "2025-10-01",
          "title": "윈치 업그레이드",
          "description": "기존 윈치를 Harken B60.2STC로 교체",
          "cost": 500000,
          "affectedParts": ["custom-part-001"]
        }
      ]
    }
  ]
}
```

---

## 🛠️ 구현 코드

### 1. 커스텀 매뉴얼 등록 함수

```python
def register_custom_manual(self, base_yacht_id: str, user_yacht_id: str, pdf_path: str, user_id: str = "default"):
    """
    기존 요트에 커스텀 매뉴얼 추가
    
    Args:
        base_yacht_id: 마스터 데이터의 yacht ID (예: "j-70")
        user_yacht_id: 사용자 요트 인스턴스 ID (예: "user-j70-001")
        pdf_path: 커스텀 매뉴얼 PDF 경로
        user_id: 사용자 ID
    """
    
    # 1. 마스터 데이터 확인
    base_yacht = self._find_yacht_by_id(base_yacht_id)
    if not base_yacht:
        return f"❌ '{base_yacht_id}' 요트를 찾을 수 없습니다."
    
    # 2. PDF 분석
    analysis_result = self._analyze_document_directly(pdf_path, self._extract_text_from_pdf(pdf_path))
    
    # 3. registered_yachts.json 로드
    registered_data = self._load_registered_yachts()
    
    # 4. 사용자 요트 찾기 또는 생성
    user_yacht = None
    for yacht in registered_data.get('userYachts', []):
        if yacht.get('userYachtId') == user_yacht_id:
            user_yacht = yacht
            break
    
    if not user_yacht:
        # 새 인스턴스 생성
        user_yacht = {
            "userYachtId": user_yacht_id,
            "baseYachtId": base_yacht_id,
            "userId": user_id,
            "nickname": f"내 {base_yacht.get('name')}",
            "registrationDate": datetime.now().isoformat(),
            "baseData": {
                "source": "yacht_specifications.json",
                "inheritSpecs": True,
                "inheritParts": True
            },
            "customManuals": [],
            "customParts": [],
            "maintenanceHistory": [],
            "modifications": []
        }
        
        if 'userYachts' not in registered_data:
            registered_data['userYachts'] = []
        
        registered_data['userYachts'].append(user_yacht)
    
    # 5. 커스텀 매뉴얼 추가
    custom_manual = {
        "id": f"custom-manual-{len(user_yacht['customManuals']) + 1:03d}",
        "title": analysis_result.get('documentInfo', {}).get('title', 'Custom Manual'),
        "type": analysis_result.get('documentInfo', {}).get('documentType', 'Custom Manual'),
        "pdfPath": pdf_path,
        "uploadDate": datetime.now().isoformat(),
        "analyzedData": {
            "parts": analysis_result.get('parts', []),
            "maintenance": analysis_result.get('maintenance', [])
        }
    }
    
    user_yacht['customManuals'].append(custom_manual)
    
    # 6. 새로운 부품 추가
    for part in analysis_result.get('parts', []):
        custom_part = {
            "id": f"custom-part-{len(user_yacht['customParts']) + 1:03d}",
            "name": part.get('name'),
            "category": part.get('category', 'Custom'),
            "manufacturer": part.get('manufacturer', ''),
            "model": part.get('model', ''),
            "installDate": datetime.now().isoformat(),
            "maintenanceInterval": part.get('interval', 12),
            "notes": f"커스텀 매뉴얼에서 추출: {custom_manual['title']}"
        }
        user_yacht['customParts'].append(custom_part)
    
    # 7. 저장
    self._save_registered_yachts(registered_data)
    
    return f"""✅ 커스텀 매뉴얼이 추가되었습니다!

**사용자 요트**: {user_yacht['nickname']}
**기반 모델**: {base_yacht.get('name')}
**추가된 매뉴얼**: {custom_manual['title']}
**추출된 부품**: {len(analysis_result.get('parts', []))}개
**추출된 정비 정보**: {len(analysis_result.get('maintenance', []))}개

이제 '{user_yacht['nickname']}'에 대한 정보를 조회할 수 있습니다!
"""
```

### 2. 사용자 요트 조회 함수

```python
def get_user_yacht_info(self, user_yacht_id: str):
    """
    사용자 요트 정보 조회 (마스터 데이터 + 커스텀 데이터 병합)
    """
    
    # 1. 사용자 요트 찾기
    registered_data = self._load_registered_yachts()
    user_yacht = None
    
    for yacht in registered_data.get('userYachts', []):
        if yacht.get('userYachtId') == user_yacht_id:
            user_yacht = yacht
            break
    
    if not user_yacht:
        return None
    
    # 2. 기반 데이터 가져오기
    base_yacht = self._find_yacht_by_id(user_yacht['baseYachtId'])
    
    # 3. 병합
    merged_data = {
        "userYachtId": user_yacht_id,
        "nickname": user_yacht['nickname'],
        "baseData": base_yacht,
        "customManuals": user_yacht.get('customManuals', []),
        "allParts": self._merge_parts(base_yacht, user_yacht),
        "maintenanceHistory": user_yacht.get('maintenanceHistory', []),
        "modifications": user_yacht.get('modifications', [])
    }
    
    return merged_data

def _merge_parts(self, base_yacht, user_yacht):
    """마스터 부품 + 커스텀 부품 병합"""
    
    # 마스터 부품
    base_parts = self._get_yacht_parts(base_yacht.get('name'))
    
    # 커스텀 부품
    custom_parts = user_yacht.get('customParts', [])
    
    # 병합
    all_parts = []
    
    # 마스터 부품 (source 표시)
    for part in base_parts:
        part_copy = part.copy()
        part_copy['source'] = 'master'
        all_parts.append(part_copy)
    
    # 커스텀 부품 (source 표시)
    for part in custom_parts:
        part_copy = part.copy()
        part_copy['source'] = 'custom'
        all_parts.append(part_copy)
    
    return all_parts
```

---

## 💬 챗봇 대화 예시

### 시나리오 1: 첫 등록

```
👤 You: J/70 내 요트로 등록하고 싶어

🤖 AI: 📝 **J/70 등록**

J/70을 등록하시겠습니까?

1. 기본 정보만 등록 (마스터 데이터 사용)
2. 커스텀 매뉴얼과 함께 등록

선택해주세요 (1 또는 2):

👤 You: 2

🤖 AI: 📄 커스텀 매뉴얼 PDF 파일 경로를 입력하세요:

👤 You: C:\Users\...\my-j70-manual.pdf

🤖 AI: 📥 파일을 분석하는 중...
✅ 분석 완료!

**사용자 요트**: 내 J/70
**기반 모델**: J/70
**추가된 매뉴얼**: My J/70 Maintenance Log
**추출된 부품**: 5개
**추출된 정비 정보**: 3개

이제 '내 J/70'에 대한 정보를 조회할 수 있습니다!
```

### 시나리오 2: 추가 매뉴얼 등록

```
👤 You: 내 J/70에 정비 노트 추가

🤖 AI: 📄 추가할 정비 노트 PDF 경로를 입력하세요:

👤 You: C:\Users\...\j70-service-2025.pdf

🤖 AI: ✅ 커스텀 매뉴얼이 추가되었습니다!

**사용자 요트**: 내 J/70
**추가된 매뉴얼**: J/70 Service Log 2025
**새로운 부품**: 2개

전체 매뉴얼 목록:
  1. My J/70 Maintenance Log (2025-10-01)
  2. J/70 Service Log 2025 (2025-11-21)
```

---

## 📁 파일 구조

```
chat-bot/
├── data/
│   ├── yacht_specifications.json      (마스터 데이터, 읽기 전용)
│   ├── registered_yachts.json         (사용자 데이터, 읽기/쓰기)
│   └── uploads/                       (사용자 업로드 파일)
│       └── user123/
│           ├── my-j70-manual.pdf
│           ├── j70-service-2025.pdf
│           └── winch-photo1.jpg
└── chatbot_unified.py                 (확장 필요)
```

---

## ✅ 구현 체크리스트

- [ ] `registered_yachts.json` 스키마 확장
- [ ] `register_custom_manual()` 함수 추가
- [ ] `get_user_yacht_info()` 함수 추가
- [ ] `_merge_parts()` 함수 추가
- [ ] 챗봇 명령어 인식 추가
- [ ] 업로드 파일 관리 기능
- [ ] 사용자 인증 연동 (선택)

---

## 🎯 요약

**핵심 아이디어:**
1. 마스터 데이터는 **읽기 전용** 유지
2. 사용자별 **인스턴스** 생성 (`userYachtId`)
3. 커스텀 매뉴얼, 부품, 정비 기록은 사용자 인스턴스에 저장
4. 조회 시 **마스터 + 커스텀 병합**

이렇게 하면:
- ✅ 마스터 데이터 보존
- ✅ 사용자별 커스터마이징 가능
- ✅ 동일 모델 여러 인스턴스 관리 가능
- ✅ 확장성 확보

구현하시겠어요? 🚀

