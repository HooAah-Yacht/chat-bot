"""
HooAah Yacht AI Connector Module
챗봇의 필터링/매칭/라우팅 로직을 재사용 가능한 모듈로 제공

사용 예:
    from ai_connector import YachtAIConnector
    
    connector = YachtAIConnector(yacht_data, parts_data)
    sections = connector.extract_section_keywords(user_message)
    candidates = connector.match_yacht_candidates(yacht_name)
"""

import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class YachtAIConnector:
    """요트 챗봇 AI 연결 모듈
    
    필터링, 매칭, 라우팅 로직을 독립적으로 제공
    """
    
    def __init__(self, yacht_data: Dict = None, parts_data: Dict = None):
        """
        Args:
            yacht_data: 요트 스펙 데이터 (yacht_specifications.json)
            parts_data: 부품 데이터 (yacht_parts_app_data.json)
        """
        self.yacht_data = yacht_data or {"yachts": []}
        self.parts_data = parts_data or {"yachts": []}
        
        # 별칭 맵 (확장 버전)
        self.alias_map = {
            'swan 41': ['swan41', 'swan 41', 'nautor swan 41', 'nautor 41'],
            'nautor swan 41': ['swan 41', 'swan41', 'nautor swan 41'],
            'nautor swan 48': ['swan48', 'swan 48', 'nautor swan 48', 'nautor 48'],
            'farr 40': ['farr40', 'farr-40', 'farr 40', 'farr yacht 40'],
            'j/24': ['j24', 'j 24', 'j-24', 'j/24'],
            'j/70': ['j70', 'j 70', 'j-70', 'j/70', 'j boats 70'],
            'beneteau oceanis 45': ['oceanis 45', 'beneteau 45']
        }
        
        # 섹션 동의어 맵 (확장 버전)
        self.section_alias_map = {
            '치수 및 성능 분석': ['치수', '크기', '스펙', 'spec', 'dimension', '성능', 'performance', '크기정보', '치수정보'],
            '선체/구조 요약': ['선체', 'hull', '구조', 'structure', '헐'],
            '부품 구성 및 정비 주기 분석': ['부품', '파트', 'rigging', '윈치', 'parts', '컴포넌트', 'component', '스페어', 'spare'],
            '사용 목적에 따른 적합성 평가': ['적합성', '목적', '용도', 'use', 'suitability', '컴플라이언스', 'compliance'],
            '관리 및 정비 권장사항': ['정비', '유지보수', '서비스', 'maintenance', '관리', '점검', '교체', 'service']
        }
    
    # ==================== 정규화 ====================
    
    def normalize_text(self, text: str) -> str:
        """텍스트 정규화: 소문자, 슬래시→공백, 특수문자 제거, 다중 공백 축소"""
        if not text:
            return ''
        t = text.lower().strip()
        t = t.replace('/', ' ')
        t = re.sub(r'\s+', ' ', t)
        t = re.sub(r'[^\w가-힣\s]', '', t)
        return t
    
    def normalize_yacht_name(self, name: str) -> str:
        """요트 이름 정규화 + 별칭 매핑"""
        n = self.normalize_text(name)
        for canonical, variants in self.alias_map.items():
            if n == canonical or n in variants:
                return canonical
        return n
    
    # ==================== 섹션 추출 ====================
    
    def extract_section_keywords(self, message: str) -> List[str]:
        """메시지에서 다중 섹션 키워드 추출
        
        Args:
            message: 사용자 메시지
            
        Returns:
            섹션 리스트 (예: ['적합성 평가', '부품 구성'])
        """
        ml = self.normalize_text(message)
        found = []
        for section, keywords in self.section_alias_map.items():
            for k in keywords:
                if k in ml:
                    found.append(section)
                    break
        # 중복 제거, 순서 유지
        dedup = []
        for s in found:
            if s not in dedup:
                dedup.append(s)
        return dedup
    
    def extract_section_keyword(self, message: str) -> Optional[str]:
        """메시지에서 단일 섹션 키워드 추출 (legacy 호환)
        
        Args:
            message: 사용자 메시지
            
        Returns:
            섹션 제목 또는 None
        """
        sections = self.extract_section_keywords(message)
        return sections[0] if sections else None
    
    # ==================== 요트 매칭 ====================
    
    def extract_yacht_name_from_message(self, message: str) -> Optional[str]:
        """메시지에서 요트 이름 추출 (별칭 우선)
        
        Args:
            message: 사용자 메시지
            
        Returns:
            요트 이름 또는 None
        """
        message_normalized = re.sub(r'[-_\s/]+', '', message.lower())
        
        # 별칭 우선 확인
        for canonical, aliases in self.alias_map.items():
            for alias in aliases:
                alias_norm = re.sub(r'[-_\s/]+', '', alias.lower())
                if alias_norm in message_normalized:
                    return canonical.title() if '/' not in canonical else canonical
        
        # 등록된 요트 검색
        for yacht in self.yacht_data.get('yachts', []):
            yacht_name = yacht.get('name', '')
            if not yacht_name:
                continue
            yacht_name_normalized = re.sub(r'[-_\s/]+', '', yacht_name.lower())
            if yacht_name_normalized in message_normalized:
                return yacht_name
        
        return None
    
    def match_yacht_candidates(self, query: str) -> List[Dict]:
        """메시지로부터 상위 요트 후보 3개를 점수화하여 반환
        
        Args:
            query: 검색 쿼리 (요트 이름 또는 사용자 메시지)
            
        Returns:
            상위 3개 후보 리스트, 각 항목:
                - name: 요트 이름
                - manufacturer: 제조사
                - score: 점수 (0-1)
                - confidence: 신뢰도 (high/medium/low)
                - evidence: 근거 (각 스코어 세부)
        """
        def tokenize(s: str) -> List[str]:
            return [t for t in self.normalize_text(s).split(' ') if t]
        
        def jaccard(a: List[str], b: List[str]) -> float:
            sa, sb = set(a), set(b)
            if not sa and not sb:
                return 0.0
            inter = sa & sb
            union = sa | sb
            return len(inter) / max(1, len(union))
        
        def levenshtein_sim(a: str, b: str) -> float:
            if a == b:
                return 1.0
            if not a or not b:
                return 0.0
            m, n = len(a), len(b)
            dp = [[0] * (n + 1) for _ in range(m + 1)]
            for i in range(m + 1):
                dp[i][0] = i
            for j in range(n + 1):
                dp[0][j] = j
            for i in range(1, m + 1):
                for j in range(1, n + 1):
                    cost = 0 if a[i - 1] == b[j - 1] else 1
                    dp[i][j] = min(
                        dp[i - 1][j] + 1,
                        dp[i][j - 1] + 1,
                        dp[i - 1][j - 1] + cost,
                    )
            dist = dp[m][n]
            return 1.0 - (dist / max(m, n))
        
        def alias_bonus(q: str, c: str) -> float:
            qn = self.normalize_text(q)
            cn = self.normalize_text(c)
            if qn == cn:
                return 0.25
            for canonical, aliases in self.alias_map.items():
                can = self.normalize_text(canonical)
                if qn == can and (cn == can or cn in [self.normalize_text(a) for a in aliases]):
                    return 0.2
                if cn == can and (qn == can or qn in [self.normalize_text(a) for a in aliases]):
                    return 0.2
            return 0.0
        
        msg = self.normalize_text(query)
        qtokens = tokenize(msg)
        ranked = []
        
        for yacht in self.yacht_data.get('yachts', []):
            name = yacht.get('name', '')
            manu = yacht.get('manufacturer', '')
            cname = self.normalize_text(name)
            mname = self.normalize_text(manu)
            ctokens = tokenize(cname)
            mtokens = tokenize(mname)
            
            j_name = jaccard(qtokens, ctokens)
            j_man = jaccard(qtokens, mtokens)
            l_name = levenshtein_sim(msg, cname)
            a_bonus = alias_bonus(msg, cname)
            p_bonus = 0.15 if any(tok and tok in cname for tok in qtokens) else 0.0
            
            score = 0.35 * j_name + 0.15 * j_man + 0.35 * l_name + a_bonus + p_bonus
            
            ranked.append({
                'name': name,
                'manufacturer': manu,
                'score': round(score, 4),
                'evidence': {
                    'jaccard_name': round(j_name, 4),
                    'jaccard_manufacturer': round(j_man, 4),
                    'levenshtein_name': round(l_name, 4),
                    'alias_bonus': round(a_bonus, 4),
                    'partial_bonus': round(p_bonus, 4)
                }
            })
        
        ranked.sort(key=lambda x: x['score'], reverse=True)
        for r in ranked:
            r['confidence'] = 'high' if r['score'] >= 0.75 else ('medium' if r['score'] >= 0.55 else 'low')
        
        return ranked[:3]
    
    # ==================== 라우팅 헬퍼 ====================
    
    def should_route_to_list(self, message: str) -> bool:
        """목록 조회 라우팅 여부 (섹션 요청 시 차단)
        
        Args:
            message: 사용자 메시지
            
        Returns:
            목록 라우팅 여부
        """
        list_keywords = ['목록', '리스트', '전체', '모든 요트', '어떤 요트', '요트 종류']
        if not any(k in message.lower() for k in list_keywords):
            return False
        # 섹션 요청이 있으면 차단
        if self.extract_section_keywords(message):
            return False
        return True
    
    def has_maintenance_keyword(self, message: str) -> bool:
        """정비/유지보수 키워드 포함 여부
        
        Args:
            message: 사용자 메시지
            
        Returns:
            정비 키워드 포함 여부
        """
        maint_keywords = ['정비', '유지보수', '서비스', 'maintenance', '관리', '점검', '교체']
        return any(k in self.normalize_text(message) for k in maint_keywords)
    
    # ==================== 멘토 대조 ====================
    
    def audit_yacht_data(self, mentor_list: List[str]) -> Dict:
        """멘토 리스트와 등록 데이터 비교
        
        Args:
            mentor_list: 멘토 기준 요트 이름 리스트
            
        Returns:
            감사 보고서 딕셔너리:
                - counts: 카운트 정보
                - missing: 등록 누락 리스트
                - extra: 추가 등록 리스트
                - suggestions: 퍼지 매칭 제안
        """
        registered = [y.get('name', '') for y in self.yacht_data.get('yachts', [])]
        
        normalized_mentor = [self.normalize_text(name) for name in mentor_list]
        normalized_registered = [self.normalize_text(name) for name in registered]
        
        missing = sorted(list(set(normalized_mentor) - set(normalized_registered)))
        extra = sorted(list(set(normalized_registered) - set(normalized_mentor)))
        
        # 퍼지 제안
        suggestions = {}
        for miss in missing:
            top3 = self.match_yacht_candidates(miss)
            suggestions[miss] = top3
        
        return {
            'counts': {
                'mentor': len(mentor_list),
                'registered': len(registered),
                'missing': len(missing),
                'extra': len(extra)
            },
            'missing': missing,
            'extra': extra,
            'suggestions': suggestions
        }
