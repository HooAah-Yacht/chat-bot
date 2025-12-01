import re

def normalize_text(s: str) -> str:
    """텍스트 정규화"""
    s = (s or '').lower().strip()
    s = s.replace('-', ' ').replace('/', ' ')
    s = re.sub(r'\s+', ' ', s)
    return s

def get_section_alias_map() -> dict:
    """섹션 동의어 매핑"""
    return {
        # 치수/성능
        '치수 및 성능 분석': ['치수', '크기', '스펙', 'spec', 'dimension', '성능', 'performance', '크기정보', '치수정보'],
        # 선체/구조
        '선체/구조 요약': ['선체', 'hull', '구조', 'structure', '헐', '선체세부', '선체항목'],
        # 부품
        '부품 구성 및 정비 주기 분석': ['부품', '파트', 'rigging', '윈치', 'parts', '컴포넌트', 'component', '스페어', 'spare'],
        # 적합성
        '사용 목적에 따른 적합성 평가': ['적합성', '목적', '용도', 'use', 'suitability', '컴플라이언스', 'compliance'],
        # 정비/관리
        '관리 및 정비 권장사항': ['정비', '유지보수', '서비스', 'maintenance', '관리', '점검', '교체', 'service']
    }

def extract_section_keywords(message: str) -> list:
    """메시지에서 다중 섹션 키워드 추출"""
    ml = normalize_text(message)
    aliases = get_section_alias_map()
    found = []
    for section, keys in aliases.items():
        for k in keys:
            if k in ml:
                found.append(section)
                print(f"  키워드 '{k}' 매칭 → 섹션: {section}")
                break
    # 중복 제거, 순서 유지
    dedup = []
    for s in found:
        if s not in dedup:
            dedup.append(s)
    return dedup

# 테스트
test_messages = [
    "Farr 40 선체 세부 항목 요약해줘",
    "Nautor Swan 48 치수",
    "OCEANIS 46.1 엔진",
    "Farr 40 정비"
]

print("=" * 80)
print("섹션 키워드 추출 테스트")
print("=" * 80)

for msg in test_messages:
    print(f"\n메시지: {msg}")
    print(f"정규화: {normalize_text(msg)}")
    sections = extract_section_keywords(msg)
    print(f"추출된 섹션: {sections if sections else '없음'}")
