# HooAah Yacht AI Connector - 사용 예제

## 통합 모듈 사용법

`ai_connector.py` 모듈은 챗봇의 핵심 필터링/매칭/라우팅 로직을 재사용 가능한 형태로 제공합니다.

### 설치

```bash
# 필요한 패키지 없음 (표준 라이브러리만 사용)
```

### 기본 사용

```python
from ai_connector import YachtAIConnector
import json

# 데이터 로드
with open('data/yacht_specifications.json', 'r', encoding='utf-8') as f:
    yacht_data = json.load(f)

with open('data/yacht_parts_app_data.json', 'r', encoding='utf-8') as f:
    parts_data = json.load(f)

# 커넥터 초기화
connector = YachtAIConnector(yacht_data, parts_data)
```

## 주요 기능

### 1. 섹션 키워드 추출

```python
user_message = "Farr 40 적합성 평가와 정비 권장사항 알려줘"
sections = connector.extract_section_keywords(user_message)
print(sections)
# 출력: ['사용 목적에 따른 적합성 평가', '관리 및 정비 권장사항']
```

### 2. 요트 이름 추출 (별칭 지원)

```python
# 정확한 이름
yacht_name = connector.extract_yacht_name_from_message("Nautor Swan 41 정보")
print(yacht_name)  # "Swan 41" 또는 "SWAN 41"

# 별칭 사용
yacht_name = connector.extract_yacht_name_from_message("swan41 분석해줘")
print(yacht_name)  # "Swan 41"
```

### 3. 요트 후보 매칭 (퍼지 매칭)

```python
query = "swan 41"
candidates = connector.match_yacht_candidates(query)

for candidate in candidates:
    print(f"{candidate['name']} ({candidate['manufacturer']})")
    print(f"  점수: {candidate['score']} | 신뢰도: {candidate['confidence']}")
    print(f"  근거: {candidate['evidence']}")
```

출력 예:

```
SWAN 41 (Nautor)
  점수: 0.95 | 신뢰도: high
  근거: {'jaccard_name': 0.8, 'levenshtein_name': 0.9, 'alias_bonus': 0.25, ...}

Nautor Swan 48 (Nautor)
  점수: 0.65 | 신뢰도: medium
  근거: {'jaccard_name': 0.5, 'levenshtein_name': 0.6, ...}
```

### 4. 라우팅 헬퍼

```python
# 목록 조회 여부
should_list = connector.should_route_to_list("요트 목록 보여줘")
print(should_list)  # True

should_list = connector.should_route_to_list("Farr 40 적합성 평가 보여줘")
print(should_list)  # False (섹션 요청 시 차단)

# 정비 키워드 포함 여부
has_maint = connector.has_maintenance_keyword("정비 주기 알려줘")
print(has_maint)  # True

has_maint = connector.has_maintenance_keyword("크기 정보 알려줘")
print(has_maint)  # False
```

### 5. 멘토 리스트 대조

```python
mentor_list = [
    'OCEANIS 46.1', 'Farr 40', 'J/24', 'SWAN 41', 'TP52'
]

audit_report = connector.audit_yacht_data(mentor_list)
print(f"등록 누락: {audit_report['missing']}")
print(f"추가 등록: {audit_report['extra']}")
print(f"퍼지 제안: {audit_report['suggestions']}")
```

출력 예:

```json
{
  "counts": {
    "mentor": 5,
    "registered": 4,
    "missing": 1,
    "extra": 0
  },
  "missing": ["oceanis 46.1"],
  "extra": [],
  "suggestions": {
    "oceanis 46.1": [
      {
        "name": "OCEANIS 473",
        "manufacturer": "Beneteau",
        "score": 0.68,
        "confidence": "medium"
      }
    ]
  }
}
```

## 다른 API에서 사용

### manual_part_api.py에서 활용

```python
from flask import Flask, request, jsonify
from ai_connector import YachtAIConnector
import json

app = Flask(__name__)

# 데이터 로드
with open('data/yacht_specifications.json', 'r', encoding='utf-8') as f:
    yacht_data = json.load(f)

connector = YachtAIConnector(yacht_data)

@app.route('/api/parts/search', methods=['POST'])
def search_parts():
    data = request.get_json()
    user_query = data.get('query', '')

    # 요트 이름 추출
    yacht_name = connector.extract_yacht_name_from_message(user_query)
    if not yacht_name:
        # 퍼지 매칭으로 후보 제시
        candidates = connector.match_yacht_candidates(user_query)
        return jsonify({
            'success': False,
            'error': 'Yacht not found',
            'suggestions': candidates
        }), 404

    # 섹션 필터링
    sections = connector.extract_section_keywords(user_query)

    # 부품 검색 로직...
    return jsonify({
        'success': True,
        'yacht_name': yacht_name,
        'sections': sections,
        'parts': []  # 실제 부품 데이터
    })
```

### parts_selector_api.py에서 활용

```python
from ai_connector import YachtAIConnector

connector = YachtAIConnector(yacht_data, parts_data)

def filter_parts_by_user_intent(user_message, all_parts):
    """사용자 의도에 따라 부품 필터링"""
    # 정비 키워드 확인
    if connector.has_maintenance_keyword(user_message):
        # 정비 관련 부품만
        return [p for p in all_parts if p.get('category') in ['Engine', 'Maintenance']]

    # 섹션 키워드로 필터
    sections = connector.extract_section_keywords(user_message)
    if '부품' in ' '.join(sections):
        return all_parts

    return []
```

## 테스트

```python
import unittest
from ai_connector import YachtAIConnector

class TestAIConnector(unittest.TestCase):
    def setUp(self):
        self.connector = YachtAIConnector()

    def test_section_extraction(self):
        sections = self.connector.extract_section_keywords("적합성 평가 보여줘")
        self.assertIn("사용 목적에 따른 적합성 평가", sections)

    def test_yacht_matching(self):
        candidates = self.connector.match_yacht_candidates("swan 41")
        self.assertGreater(len(candidates), 0)
        self.assertEqual(candidates[0]['confidence'], 'high')

    def test_normalization(self):
        norm = self.connector.normalize_text("Farr-40/Racing")
        self.assertEqual(norm, "farr 40 racing")

if __name__ == '__main__':
    unittest.main()
```

## 커스터마이징

### 별칭 맵 확장

```python
connector = YachtAIConnector(yacht_data, parts_data)

# 새 별칭 추가
connector.alias_map['custom yacht'] = ['custom', 'cust yacht', 'cy']
```

### 섹션 맵 확장

```python
# 새 섹션 추가
connector.section_alias_map['커스텀 섹션'] = ['커스텀', 'custom', '맞춤']
```

## 성능 최적화

### 캐싱 활용

```python
from functools import lru_cache

class CachedConnector(YachtAIConnector):
    @lru_cache(maxsize=128)
    def match_yacht_candidates(self, query: str):
        return super().match_yacht_candidates(query)
```

### 배치 처리

```python
# 여러 쿼리를 한 번에 처리
queries = ["swan 41", "farr 40", "j/70"]
results = [connector.match_yacht_candidates(q) for q in queries]
```

## 에러 처리

```python
try:
    yacht_name = connector.extract_yacht_name_from_message(user_query)
    if not yacht_name:
        raise ValueError("Yacht name not found")

    candidates = connector.match_yacht_candidates(yacht_name)
    if not candidates or candidates[0]['confidence'] == 'low':
        print(f"Low confidence match. Did you mean: {candidates[0]['name']}?")
except Exception as e:
    print(f"Error: {e}")
```

## 로깅

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('AIConnector')

# 매칭 스코어 로깅
candidates = connector.match_yacht_candidates("swan")
for c in candidates:
    logger.info(f"Matched {c['name']} with score {c['score']}")
```
