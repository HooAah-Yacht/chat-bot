"""
HooAah Yacht AI Chatbot - 통합 버전
모든 챗봇 기능을 하나로 통합한 통합 챗봇

기능:
- 자연어 대화 (Gemini AI)
- PDF 업로드 및 분석 (자동 스펙 및 부품 추출)
- 기존 20종 요트 정보 조회
- API 서버 모드 (Flutter 앱 연동)
- 자동 명령어 인식 및 처리
- JSON 파일 자동 저장

사용법:
    # 대화형 모드
    python chatbot_unified.py
    
    # API 서버 모드
    python chatbot_unified.py --mode api
    
    # API 키 지정
    python chatbot_unified.py --api-key YOUR_API_KEY
"""

import os
import json
import sys
import argparse
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

# Environment variables (.env 파일 로드)
try:
    from dotenv import load_dotenv
    load_dotenv()  # .env 파일에서 환경 변수 로드
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False
    print("⚠️ python-dotenv 패키지가 설치되지 않았습니다. pip install python-dotenv")

# Gemini AI 관련
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False
    print("⚠️ google-generativeai 패키지가 설치되지 않았습니다. pip install google-generativeai")

# Flask API 관련
try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    from werkzeug.utils import secure_filename
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False
    secure_filename = None
    print("⚠️ flask 패키지가 설치되지 않았습니다.")
    print("📦 자동 설치를 시도합니다...")
    import subprocess
    import sys
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "flask-cors", "--quiet"])
        from flask import Flask, request, jsonify
        from flask_cors import CORS
        from werkzeug.utils import secure_filename
        HAS_FLASK = True
        print("✅ Flask 패키지 설치 완료!")
    except Exception as e:
        print(f"❌ Flask 자동 설치 실패: {e}")
        print("💡 수동 설치: pip install flask flask-cors")

# PDF 분석 관련
try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False
    try:
        import pdfplumber
        HAS_PDFPLUMBER = True
    except ImportError:
        HAS_PDFPLUMBER = False


class UnifiedYachtChatbot:
    """
    통합 요트 챗봇 클래스
    모든 챗봇 기능을 통합
    """
    
    def __init__(self, api_key: str = None, mode: str = "interactive"):
        """
        통합 챗봇 초기화
        
        Args:
            api_key: Gemini API 키 (기본값: 제공된 API 키)
            mode: 실행 모드 ("interactive", "api", "cli")
        """
        self.mode = mode
        # API 키 우선순위: 인자 > 환경변수 (.env 파일) > 없으면 오류
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            print("⚠️ 경고: GEMINI_API_KEY가 설정되지 않았습니다.")
            print("💡 .env 파일에 GEMINI_API_KEY를 설정하거나 --api-key 옵션을 사용하세요.")
            print("📝 .env.example 파일을 참고하여 .env 파일을 생성하세요.")
        
        # Gemini AI 초기화
        if HAS_GEMINI and self.api_key:
            genai.configure(api_key=self.api_key)
            try:
                self.model = genai.GenerativeModel('gemini-2.5-flash')
                print("✅ Gemini 2.5 Flash 모델 사용")
            except Exception as e:
                print(f"⚠️ Gemini 2.5 Flash 사용 실패, gemini-pro로 전환: {e}")
                self.model = genai.GenerativeModel('gemini-pro')
                print("✅ gemini-pro 모델 사용 (fallback)")
            self.has_gemini = True
        else:
            self.has_gemini = False
            print("⚠️ Gemini AI를 사용할 수 없습니다. 기본 모드로 실행됩니다.")
        
        # 대화 히스토리
        self.chat_history: List[Dict[str, str]] = []
        
        # 요트 데이터 로드
        self.yacht_data = self._load_yacht_data()
        self.parts_data = self._load_parts_data()
        
        # 시스템 프롬프트
        if self.has_gemini:
            self.system_prompt = self._create_system_prompt()
        
        # 등록 데이터
        self.current_yacht_registration = None
        
        print("✅ HooAah Yacht 통합 챗봇이 준비되었습니다!")
        if mode == "interactive":
            print("💬 자연스럽게 요트에 대해 질문해보세요.")
            print("📄 PDF 파일 경로를 입력하면 자동으로 분석합니다.\n")
    
    def _load_yacht_data(self) -> Dict:
        """요트 스펙 데이터 로드"""
        try:
            with open('data/yacht_specifications.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ yacht_specifications.json 파일을 찾을 수 없습니다.")
            return {"yachts": []}
    
    def _load_parts_data(self) -> Dict:
        """부품 데이터 로드"""
        try:
            with open('data/yacht_parts_database.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ yacht_parts_database.json 파일을 찾을 수 없습니다.")
            return {"yachts": []}
    
    def _create_system_prompt(self) -> str:
        """시스템 프롬프트 생성"""
        yacht_list = [yacht.get('name', '') for yacht in self.yacht_data.get('yachts', [])]
        
        prompt = f"""당신은 HooAah Yacht의 전문 AI 어시스턴트입니다.

**역할:**
- 요트 소유자와 관리자를 돕는 친절하고 전문적인 어시스턴트
- 요트 스펙, 부품, 정비, 관리에 대한 모든 질문에 답변
- 자연스럽고 대화적인 톤으로 소통
- 사용자의 의도를 파악하여 적절한 응답 제공

**지원하는 요트 20종:**
{', '.join(yacht_list)}

**데이터베이스 구조 (ERD 기반):**
- User: 사용자 정보
- Yacht: 요트 정보 (name)
- Yacht_User: 사용자-요트 연결 (다대다 관계)
- Part: 부품 정보 (name, manufacturer, model, interval)
- Repair: 정비 내역 (repairDate만 저장, content 필드 없음)
- Calendar: 캘린더 이벤트 (content 필드 있음, part_id와 연결)
- Alert: 알림 (part_id와 일대일 관계)

**의도 파악 및 응답 가이드라인:**

1. **요트 정보 조회 의도:**
   - 키워드: "정보", "스펙", "사양", "크기", "치수", "길이", "폭", "높이", 요트 이름 등
   - 응답: 해당 요트의 상세 정보 제공 (치수, 엔진, 돛 면적 등)

2. **요트 등록/PDF 업로드 의도:**
   - 키워드: "등록", "업로드", "pdf", "문서", "매뉴얼", "새 요트", "요트 등록", "추가", "입력" 등
   - 응답: PDF 파일 업로드 안내 메시지 반환
   - 예시 문장:
     * "새 요트 등록하고 싶어요"
     * "pdf 매뉴얼 업로드해줘"
     * "요트 정보 추가할게"
     * "문서 등록하고 싶어"
     * "매뉴얼 파일 올릴 수 있어?"

3. **도움말 요청 의도:**
   - 키워드: "도움말", "도움", "help", "사용법", "어떻게", "방법", "사용", "사용법", "가이드" 등
   - 응답: 도움말 메시지 반환

4. **요트 목록 조회 의도:**
   - 키워드: "목록", "리스트", "전체", "모든 요트", "어떤 요트", "요트 종류" 등
   - 응답: 요트 목록 반환

5. **요트 비교 의도:**
   - 키워드: "비교", "차이", "어떤 게", "vs", "대" 등
   - 응답: 여러 요트를 비교하여 차이점 설명

6. **요트 추천 의도:**
   - 키워드: "추천", "어떤 게 좋아", "선택", "고르" 등
   - 응답: 사용 목적에 맞는 요트 추천

7. **정비/관리 질문:**
   - 키워드: "정비", "관리", "주기", "점검", "교체" 등
   - 응답: 정비 주기, 정비 이력, 관리 방법 안내

**답변 형식:**
- 짧고 명확하게 (모바일 화면에 적합)
- 필요시 이모지 사용 (⛵, 🔧, 📏, ⚓ 등)
- 숫자는 단위와 함께 명시
- 추가 질문 유도

**중요:**
- 사용자의 의도를 정확히 파악하여 적절한 응답 제공
- 자연어로 된 모든 요청을 이해하고 처리
- 특정 명령어가 아닌 관련 키워드만 있어도 의도 파악
- 모르는 내용은 솔직히 모른다고 답변

**데이터 활용:**
아래 JSON 데이터를 참고하여 정확한 정보 제공:

요트 스펙 데이터:
{json.dumps(self.yacht_data, ensure_ascii=False, indent=2)[:5000]}...

부품 데이터 (샘플):
{json.dumps(self.parts_data, ensure_ascii=False, indent=2)[:3000]}...
"""
        return prompt
    
    def _extract_pdf_path_from_message(self, message: str) -> Optional[str]:
        """
        사용자 메시지에서 PDF 파일 경로 추출
        모바일 앱에서 전달된 파일 경로도 지원 (iOS, Android)
        """
        import re
        
        # 1. 따옴표로 감싸진 경로 찾기 (공백 포함 경로 지원)
        quoted_patterns = [
            r'["\']([^"\']+\.pdf)["\']',
            r'["\']([^"\']+\.pdf)',
            r'([^"\']+\.pdf)["\']',
        ]
        
        for pattern in quoted_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                path = match.group(1).strip()
                # 절대 경로 확인
                if os.path.isabs(path) and os.path.exists(path):
                    return os.path.abspath(path)
                # 상대 경로 확인
                elif os.path.exists(path):
                    return os.path.abspath(path)
        
        # 2. Windows 절대 경로 패턴 (C:\... 또는 D:\...)
        windows_abs_pattern = r'([A-Za-z]:[\\/](?:[^"\']+[\\/])*[^"\']+\.pdf)'
        match = re.search(windows_abs_pattern, message, re.IGNORECASE)
        if match:
            path = match.group(1).strip()
            if os.path.exists(path):
                return os.path.abspath(path)
        
        # 3. Unix/Linux/Mac 절대 경로 패턴 (/Users/... 또는 /storage/...)
        unix_abs_pattern = r'(/[^"\']+\.pdf)'
        match = re.search(unix_abs_pattern, message, re.IGNORECASE)
        if match:
            path = match.group(1).strip()
            if os.path.exists(path):
                return os.path.abspath(path)
        
        # 4. 모바일 앱 경로 패턴 (Android: /storage/..., iOS: /var/mobile/...)
        mobile_patterns = [
            r'(/storage/[^"\']+\.pdf)',  # Android
            r'(/var/mobile/[^"\']+\.pdf)',  # iOS
            r'(/data/[^"\']+\.pdf)',  # Android data
            r'(file://[^"\']+\.pdf)',  # file:// URI
        ]
        
        for pattern in mobile_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                path = match.group(1).strip()
                # file:// URI 처리
                if path.startswith('file://'):
                    path = path.replace('file://', '')
                if os.path.exists(path):
                    return os.path.abspath(path)
        
        # 5. 메시지 전체가 파일 경로인지 확인
        message_clean = message.strip().strip('"').strip("'")
        
        # 절대 경로인 경우
        if os.path.isabs(message_clean) and message_clean.endswith('.pdf'):
            if os.path.exists(message_clean):
                return os.path.abspath(message_clean)
        
        # 상대 경로인 경우
        if message_clean.endswith('.pdf'):
            # 현재 작업 디렉토리 기준
            if os.path.exists(message_clean):
                return os.path.abspath(message_clean)
            # 절대 경로로 변환 시도
            abs_path = os.path.abspath(message_clean)
            if os.path.exists(abs_path):
                return abs_path
        
        return None
    
    def _is_pdf_upload_request(self, message: str) -> bool:
        """PDF 업로드 요청인지 확인"""
        pdf_keywords = ['pdf', '문서', '매뉴얼', '업로드', '등록', '파일']
        return any(keyword in message.lower() for keyword in pdf_keywords) or \
               self._extract_pdf_path_from_message(message) is not None
    
    def _is_yacht_info_request(self, message: str) -> bool:
        """요트 정보 요청인지 확인"""
        info_keywords = ['정보', '스펙', '사양', '크기', '치수', '길이', '폭', '높이', '추천']
        yacht_names = [y.get('name', '').lower() for y in self.yacht_data.get('yachts', [])]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in info_keywords) or \
               any(name in message_lower for name in yacht_names)
    
    def chat(self, user_message: str, pdf_file_path: str = None) -> str:
        """
        사용자 메시지에 대한 응답 생성
        
        Args:
            user_message: 사용자 입력 메시지
            pdf_file_path: PDF 파일 경로 (모바일 앱에서 직접 전달되는 경우)
            
        Returns:
            AI 응답 메시지
        """
        try:
            # 1. 직접 전달된 PDF 파일 경로 확인 (모바일 앱에서 파일 업로드)
            if pdf_file_path and os.path.exists(pdf_file_path):
                return self._handle_pdf_upload(pdf_file_path)
            
            # 2. 메시지에서 PDF 파일 경로 추출
            pdf_path = self._extract_pdf_path_from_message(user_message)
            if pdf_path and os.path.exists(pdf_path):
                return self._handle_pdf_upload(pdf_path)
            
            # 3. 명령어 처리 (빠른 응답)
            message_lower = user_message.lower().strip()
            if message_lower in ['/list', '/목록']:
                return self._list_yachts()
            
            if message_lower in ['/info', '/정보']:
                return self._get_data_info()
            
            if message_lower in ['/help', '/도움말']:
                return self._get_help()
            
            # 4. 대화 히스토리에 추가
            self.chat_history.append({
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now().isoformat()
            })
            
            # 5. Gemini AI로 의도 파악 및 응답 생성
            if self.has_gemini:
                # AI가 의도를 파악하여 적절한 응답 생성
                response = self._generate_intelligent_response(user_message)
            else:
                # 기본 모드: 키워드 기반 응답
                response = self._generate_keyword_based_response(user_message)
            
            # 6. 대화 히스토리에 추가
            self.chat_history.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().isoformat()
            })
            
            return response
            
        except Exception as e:
            error_msg = f"죄송합니다. 응답 생성 중 오류가 발생했습니다: {str(e)}"
            print(f"❌ Error: {e}")
            return error_msg
    
    def _generate_intelligent_response(self, user_message: str) -> str:
        """Gemini AI를 사용한 지능형 응답 생성 (의도 파악)"""
        try:
            # 의도 파악을 위한 프롬프트
            intent_prompt = f"""사용자 메시지: "{user_message}"

위 메시지를 분석하여 사용자의 의도를 파악하고 적절한 응답을 생성해주세요.

**의도 분류:**
1. **요트 정보 조회**: 요트 이름, 스펙, 치수 등에 대한 질문
2. **요트 등록/PDF 업로드**: 새 요트를 등록하거나 PDF 매뉴얼을 업로드하려는 의도
3. **도움말 요청**: 사용법, 가이드, 도움말을 요청하는 의도
4. **요트 목록 조회**: 전체 요트 목록을 보려는 의도
5. **요트 비교/추천**: 여러 요트를 비교하거나 추천을 요청하는 의도
6. **정비/관리 질문**: 정비 주기, 관리 방법 등에 대한 질문
7. **일반 대화**: 기타 요트 관련 질문

**응답 규칙:**
- 요트 등록/PDF 업로드 의도가 감지되면: PDF 파일 업로드 안내 메시지를 반환
- 도움말 요청 의도가 감지되면: 도움말 내용을 반환
- 요트 목록 조회 의도가 감지되면: 요트 목록을 반환
- 요트 정보 조회 의도가 감지되면: 해당 요트의 상세 정보를 제공
- 그 외: 자연스럽게 답변

**지원하는 요트 20종:**
{', '.join([yacht.get('name', '') for yacht in self.yacht_data.get('yachts', [])])}

위 규칙에 따라 사용자에게 적절한 응답을 생성해주세요."""
            
            # 의도 파악 및 응답 생성
            response = self.model.generate_content(intent_prompt)
            ai_response = response.text.strip()
            
            # 특수 응답 처리 (PDF 업로드, 도움말 등)
            ai_response_lower = ai_response.lower()
            
            # PDF 업로드 의도가 명확한 경우
            if any(keyword in ai_response_lower for keyword in ['pdf', '업로드', '등록', '파일 경로']):
                # PDF 업로드 안내 메시지로 대체
                return self._suggest_pdf_upload()
            
            # 도움말 의도가 명확한 경우
            if any(keyword in ai_response_lower for keyword in ['도움말', '사용법', '가이드']):
                # 도움말 메시지로 대체
                return self._get_help()
            
            # 요트 목록 의도가 명확한 경우
            if any(keyword in ai_response_lower for keyword in ['목록', '리스트', '전체 요트']):
                # 요트 목록으로 대체
                return self._list_yachts()
            
            # 일반 응답 반환
            return ai_response
            
        except Exception as e:
            # 오류 발생 시 키워드 기반 응답으로 fallback
            return self._generate_keyword_based_response(user_message)
    
    def _generate_keyword_based_response(self, user_message: str) -> str:
        """키워드 기반 응답 생성 (Gemini AI 없을 때)"""
        message_lower = user_message.lower()
        
        # 1. 도움말 관련 키워드
        help_keywords = ['도움말', '도움', 'help', '사용법', '어떻게', '방법', '사용', '가이드', '안내']
        if any(keyword in message_lower for keyword in help_keywords):
            return self._get_help()
        
        # 2. PDF 업로드/등록 관련 키워드
        pdf_keywords = ['pdf', '문서', '매뉴얼', '업로드', '등록', '파일', '새 요트', '요트 등록', '추가', '입력', '올리', '넣']
        if any(keyword in message_lower for keyword in pdf_keywords):
            return self._suggest_pdf_upload_without_ai()
        
        # 3. 요트 목록 관련 키워드
        list_keywords = ['목록', '리스트', '전체', '모든 요트', '어떤 요트', '요트 종류', '요트 목록']
        if any(keyword in message_lower for keyword in list_keywords):
            return self._list_yachts()
        
        # 4. 요트 정보 조회 (기존 로직)
        return self._generate_basic_response(user_message)
    
    def _generate_ai_response(self, user_message: str) -> str:
        """Gemini AI를 사용한 응답 생성"""
        try:
            context = self._build_context()
            response = self.model.generate_content(context)
            return response.text
        except Exception as e:
            return f"AI 응답 생성 중 오류가 발생했습니다: {str(e)}"
    
    def _generate_basic_response(self, user_message: str) -> str:
        """기본 모드 응답 생성 (Gemini AI 없이)"""
        # 기존 chatbot.py의 로직 사용
        message_lower = user_message.lower()
        
        # 요트 이름 찾기
        for yacht in self.yacht_data.get('yachts', []):
            yacht_name = yacht.get('name', '').lower()
            if yacht_name in message_lower:
                return self._format_yacht_info(yacht)
        
        return "죄송합니다. 요트 정보를 찾을 수 없습니다. '/list' 명령어로 요트 목록을 확인하세요."
    
    def _format_yacht_dimensions(self, yacht: Dict) -> str:
        """요트 치수 정보 포맷팅"""
        model_name = yacht.get('name', 'Unknown')
        dim = yacht.get('dimensions', {})
        
        response = f"'{model_name}'의 크기 정보는 아래와 같습니다:\n\n"
        response += "📏 **기본 치수**\n"
        
        if dim.get('loa'):
            loa = dim['loa']
            if isinstance(loa, dict):
                response += f"- LOA (전장): {loa.get('display', loa.get('value', ''))}\n"
            else:
                response += f"- LOA (전장): {loa}\n"
        
        if dim.get('lwl'):
            lwl = dim['lwl']
            if isinstance(lwl, dict):
                response += f"- LWL (수선장): {lwl.get('display', lwl.get('value', ''))}\n"
            else:
                response += f"- LWL (수선장): {lwl}\n"
        
        if dim.get('beam'):
            beam = dim['beam']
            if isinstance(beam, dict):
                response += f"- Beam (폭): {beam.get('display', beam.get('value', ''))}\n"
            else:
                response += f"- Beam (폭): {beam}\n"
        
        if dim.get('draft'):
            draft = dim['draft']
            if isinstance(draft, dict):
                response += f"- Draft (흘수): {draft.get('display', draft.get('value', ''))}\n"
            else:
                response += f"- Draft (흘수): {draft}\n"
        
        if dim.get('displacement'):
            disp = dim['displacement']
            if isinstance(disp, dict):
                response += f"- Displacement (배수량): {disp.get('display', disp.get('value', ''))}\n"
            else:
                response += f"- Displacement (배수량): {disp}\n"
        
        if dim.get('mastHeight'):
            mast = dim['mastHeight']
            if isinstance(mast, dict):
                response += f"- Mast Height (마스트 높이): {mast.get('display', mast.get('value', ''))}\n"
            else:
                response += f"- Mast Height (마스트 높이): {mast}\n"
        
        return response
    
    def _format_full_yacht_info(self, yacht: Dict) -> str:
        """요트 전체 정보 포맷팅"""
        model_name = yacht.get('name', 'Unknown')
        response = f"🛥️ **{model_name}** - 상세 정보\n\n"
        
        if yacht.get('manufacturer'):
            response += f"제조사: {yacht['manufacturer']}\n"
        if yacht.get('type'):
            response += f"타입: {yacht['type']}\n"
        if yacht.get('designer'):
            response += f"디자이너: {yacht['designer']}\n"
        if yacht.get('year'):
            response += f"제작년도: {yacht['year']}\n"
        
        response += "\n"
        
        # 치수 정보
        dim = yacht.get('dimensions', {})
        if dim:
            response += "📏 **치수**\n"
            if dim.get('loa'):
                loa = dim['loa']
                if isinstance(loa, dict):
                    response += f"- LOA: {loa.get('display', loa.get('value', ''))}\n"
                else:
                    response += f"- LOA: {loa}\n"
            if dim.get('beam'):
                beam = dim['beam']
                if isinstance(beam, dict):
                    response += f"- Beam (폭): {beam.get('display', beam.get('value', ''))}\n"
                else:
                    response += f"- Beam (폭): {beam}\n"
            if dim.get('draft'):
                draft = dim['draft']
                if isinstance(draft, dict):
                    response += f"- Draft (흘수): {draft.get('display', draft.get('value', ''))}\n"
                else:
                    response += f"- Draft (흘수): {draft}\n"
            if dim.get('displacement'):
                disp = dim['displacement']
                if isinstance(disp, dict):
                    response += f"- Displacement (배수량): {disp.get('display', disp.get('value', ''))}\n"
                else:
                    response += f"- Displacement (배수량): {disp}\n"
            if dim.get('mastHeight'):
                mast = dim['mastHeight']
                if isinstance(mast, dict):
                    response += f"- Mast Height: {mast.get('display', mast.get('value', ''))}\n"
                else:
                    response += f"- Mast Height: {mast}\n"
            response += "\n"
        
        # 돛 면적
        sail_area = yacht.get('sailArea', {})
        if sail_area:
            response += "⛵ **돛 면적**\n"
            if sail_area.get('main'):
                main = sail_area['main']
                if isinstance(main, dict):
                    response += f"- Main: {main.get('value', '')} {main.get('unit', '')}\n"
                else:
                    response += f"- Main: {main} m²\n"
            if sail_area.get('jib'):
                jib = sail_area['jib']
                if isinstance(jib, dict):
                    response += f"- Jib: {jib.get('value', '')} {jib.get('unit', '')}\n"
                else:
                    response += f"- Jib: {jib} m²\n"
            if sail_area.get('spinnaker'):
                spin = sail_area['spinnaker']
                if isinstance(spin, dict):
                    response += f"- Spinnaker: {spin.get('value', '')} {spin.get('unit', '')}\n"
                else:
                    response += f"- Spinnaker: {spin} m²\n"
            if sail_area.get('total'):
                total = sail_area['total']
                if isinstance(total, dict):
                    response += f"- Total: {total.get('display', total.get('value', ''))}\n"
                else:
                    response += f"- Total: {total} m²\n"
            response += "\n"
        
        # 엔진 정보
        engine = yacht.get('engine', {})
        if engine:
            response += "🔧 **엔진**\n"
            if engine.get('type'):
                response += f"- Type: {engine['type']}\n"
            if engine.get('power'):
                response += f"- Power: {engine['power']}\n"
            if engine.get('model'):
                response += f"- Model: {engine['model']}\n"
        
        return response
    
    def _build_context(self) -> str:
        """대화 컨텍스트 구성"""
        context = self.system_prompt + "\n\n**대화 기록:**\n"
        recent_history = self.chat_history[-10:]
        
        for msg in recent_history:
            role = "사용자" if msg["role"] == "user" else "어시스턴트"
            context += f"\n{role}: {msg['content']}\n"
        
        return context
    
    def _handle_pdf_upload(self, pdf_path: str) -> str:
        """PDF 업로드 및 분석 처리 (완전한 버전)"""
        try:
            print(f"\n📄 PDF 분석 시작: {os.path.basename(pdf_path)}")
            
            # PDF 분석 시작 메시지
            analyzing_msg = "📄 문서를 분석 중입니다...\n잠시만 기다려주세요! ⏳"
            
            self.chat_history.append({
                "role": "user",
                "content": f"[PDF 업로드: {os.path.basename(pdf_path)}]",
                "timestamp": datetime.now().isoformat()
            })
            
            self.chat_history.append({
                "role": "assistant",
                "content": analyzing_msg,
                "timestamp": datetime.now().isoformat()
            })
            
            # YachtDocumentAnalyzer 사용 (있는 경우)
            try:
                from yacht_document_analyzer import YachtDocumentAnalyzer
                document_analyzer = YachtDocumentAnalyzer(api_key=self.api_key)
                analysis_result = document_analyzer.analyze_pdf(pdf_path, use_file_upload=False)
            except ImportError:
                # yacht_document_analyzer가 없으면 직접 분석
                analysis_result = self._analyze_pdf_directly(pdf_path)
            
            # 분석 결과 확인
            if "error" in analysis_result:
                error_msg = f"❌ 문서 분석 중 오류가 발생했습니다:\n{analysis_result.get('error', '알 수 없는 오류')}"
                self.chat_history.append({
                    "role": "assistant",
                    "content": error_msg,
                    "timestamp": datetime.now().isoformat()
                })
                return error_msg
            
            # 분석 결과를 요트 등록 형식으로 변환
            registration_data = self._convert_analysis_to_registration(analysis_result)
            
            # 등록 완료 메시지 생성
            completion_msg = self._generate_registration_completion_message(analysis_result, registration_data)
            
            # 등록 데이터 저장 (메모리 + JSON 파일)
            self.current_yacht_registration = registration_data
            
            # JSON 파일로 저장
            self._save_registration_to_json(registration_data, analysis_result)
            
            # 대화 히스토리에 추가
            self.chat_history.append({
                "role": "assistant",
                "content": completion_msg,
                "timestamp": datetime.now().isoformat()
            })
            
            print("✅ PDF 분석 및 등록 준비 완료!")
            
            return completion_msg
            
        except Exception as e:
            error_msg = f"❌ PDF 처리 중 오류가 발생했습니다: {str(e)}"
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            
            self.chat_history.append({
                "role": "assistant",
                "content": error_msg,
                "timestamp": datetime.now().isoformat()
            })
            
            return error_msg
    
    def _analyze_pdf_directly(self, pdf_path: str) -> Dict:
        """PDF 직접 분석 (yacht_document_analyzer 없이)"""
        extracted_text = self._extract_text_from_pdf(pdf_path)
        
        if not extracted_text or len(extracted_text.strip()) < 100:
            return {
                "error": "PDF에서 텍스트를 추출할 수 없습니다.",
                "fileInfo": {
                    "fileName": os.path.basename(pdf_path),
                    "filePath": pdf_path
                }
            }
        
        # 텍스트가 너무 길면 앞부분만 사용
        if len(extracted_text) > 30000:
            extracted_text = extracted_text[:30000] + "\n\n[... 텍스트가 너무 길어 일부만 분석합니다 ...]"
        
        if not self.has_gemini:
            return {
                "error": "PDF 분석 기능은 Gemini API가 필요합니다.",
                "fileInfo": {
                    "fileName": os.path.basename(pdf_path),
                    "filePath": pdf_path
                }
            }
        
        # 분석 프롬프트
        prompt = f"""다음은 요트 매뉴얼 또는 부품 정보 문서에서 추출한 텍스트입니다:

{extracted_text}

위 텍스트를 분석하여 다음 정보를 추출하여 JSON 형식으로 반환해주세요:

1. **문서 기본 정보:**
   - 문서 제목
   - 요트 모델명 (있는 경우)
   - 제조사 (있는 경우)
   - 문서 유형 (매뉴얼, 부품 목록, 기술 사양서 등)

2. **요트 스펙 정보 (있는 경우):**
   - 전장 (LOA)
   - 폭 (Beam)
   - 흘수 (Draft)
   - 배수량 (Displacement)
   - 마스트 높이
   - 엔진 정보 (타입, 출력, 모델)
   - 돛 면적

3. **부품 정보 (있는 경우):**
   - 부품명 (name) - 필수, 매뉴얼에서 언급된 모든 부품을 추출하세요
   - 제조사 (manufacturer)
   - 모델명 (model)
   - 정비 주기 (interval, 단위: 개월)
   - 부품 카테고리 (Rigging, Sails, Engine, Hull, Electrical, Plumbing 등)
   
   **중요**: 매뉴얼에서 언급된 모든 부품, 정비 항목, 교체 부품을 최대한 많이 추출하세요.
   예: 마스트(Mast), 붐(Boom), 리깅(Rigging), 세일(Sails), 윈치(Winch), 엔진 부품, 전기 부품, 배관 부품 등
   부품명이 명확하지 않더라도 가능한 한 추출하세요.

4. **정비 정보 (있는 경우):**
   - 정비 항목
   - 정비 주기
   - 정비 방법

5. **문서 형식 평가:**
   - 텍스트 추출 가능 여부
   - 분석 가능 여부 (가능/불가능)
   - 불가능한 경우 이유

**응답 형식:**
```json
{{
  "documentInfo": {{
    "title": "...",
    "yachtModel": "...",
    "manufacturer": "...",
    "documentType": "..."
  }},
  "yachtSpecs": {{
    "dimensions": {{}},
    "engine": {{}},
    "sailArea": {{}}
  }},
  "parts": [
    {{
      "name": "...",
      "manufacturer": "...",
      "model": "...",
      "interval": 12,
      "category": "..."
    }}
  ],
  "maintenance": [],
  "analysisResult": {{
    "canExtractText": true/false,
    "canAnalyze": true/false,
    "reason": "..."
  }}
}}
```

JSON 형식으로만 응답해주세요. 다른 설명은 필요 없습니다."""
        
        # Gemini API 호출
        print("🤖 AI 분석 중...")
        response = self.model.generate_content(prompt)
        
        # 응답 파싱
        result_text = response.text
        
        # JSON 추출 (마크다운 코드 블록 제거)
        if "```json" in result_text:
            json_start = result_text.find("```json") + 7
            json_end = result_text.find("```", json_start)
            result_text = result_text[json_start:json_end].strip()
        elif "```" in result_text:
            json_start = result_text.find("```") + 3
            json_end = result_text.find("```", json_start)
            result_text = result_text[json_start:json_end].strip()
        
        # JSON 파싱
        try:
            result = json.loads(result_text)
        except json.JSONDecodeError:
            result = {
                "rawResponse": result_text,
                "error": "JSON 파싱 실패",
                "extractedTextLength": len(extracted_text)
            }
        
        # 파일 정보 추가
        result["fileInfo"] = {
            "fileName": os.path.basename(pdf_path),
            "filePath": pdf_path,
            "fileSize": os.path.getsize(pdf_path)
        }
        
        print("✅ 분석 완료!")
        return result
    
    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """PDF에서 텍스트 추출"""
        text = ""
        
        if HAS_PYPDF2:
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                return text
            except Exception as e:
                print(f"⚠️ PyPDF2로 텍스트 추출 실패: {e}")
        
        if HAS_PDFPLUMBER:
            try:
                import pdfplumber
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                return text
            except Exception as e:
                print(f"⚠️ pdfplumber로 텍스트 추출 실패: {e}")
        
        return ""
    
    def _list_yachts(self) -> str:
        """요트 목록 반환"""
        yachts = self.yacht_data.get('yachts', [])
        if not yachts:
            return "요트 데이터를 찾을 수 없습니다."
        
        result = f"📋 총 {len(yachts)}개의 요트 모델:\n\n"
        for i, yacht in enumerate(yachts, 1):
            name = yacht.get('name', 'Unknown')
            yacht_type = yacht.get('type', '')
            result += f"  {i}. {name}"
            if yacht_type:
                result += f" ({yacht_type})"
            result += "\n"
        
        return result
    
    def _get_data_info(self) -> str:
        """데이터 정보 반환"""
        yachts = self.yacht_data.get('yachts', [])
        result = "📊 요트 데이터 정보\n"
        result += "=" * 50 + "\n"
        result += f"총 요트 개수: {len(yachts)}개\n"
        result += f"데이터 버전: {self.yacht_data.get('version', 'N/A')}\n"
        result += f"마지막 업데이트: {self.yacht_data.get('lastUpdated', 'N/A')}\n"
        return result
    
    def _get_help(self) -> str:
        """도움말 반환"""
        help_text = """📖 HooAah Yacht 챗봇 도움말

**사용 가능한 명령어:**
- `/list` 또는 `/목록` - 요트 목록 보기
- `/info` 또는 `/정보` - 데이터 정보 보기
- `/help` 또는 `/도움말` - 이 도움말 보기

**질문 예시:**
- "Farr 40 크기 알려줘"
- "레이싱에 좋은 요트 추천해줘"
- "PDF 파일 경로" (PDF 업로드 및 분석)

**PDF 업로드:**
PDF 파일 경로를 입력하면 자동으로 분석합니다.
예: "C:\\Users\\user\\Documents\\manual.pdf"
"""
        return help_text
    
    def _suggest_pdf_upload(self) -> str:
        """PDF 업로드 안내 메시지 (Gemini AI 사용 가능 시)"""
        message = """📄 요트 문서를 등록하세요!

요트 매뉴얼 PDF 파일을 업로드해주시면:
1. 📋 문서를 자동으로 분석합니다
2. ⛵ 요트 정보를 추출합니다
3. 🔧 부품 정보를 정리합니다
4. ✅ 데이터베이스에 등록합니다

**PDF 파일 업로드 방법:**
PDF 파일의 전체 경로를 입력해주세요.

예시:
- `C:\\Users\\user\\Documents\\Sun Odyssey 380 Owners manual.pdf`
- `"C:\\Users\\user\\Documents\\manual.pdf"` (공백이 있는 경우 따옴표 사용)

PDF 파일 경로를 입력해주세요! 📎"""
        
        return message
    
    def _suggest_pdf_upload_without_ai(self) -> str:
        """PDF 업로드 안내 메시지 (Gemini AI 없을 때)"""
        message = """📄 요트 문서를 등록하세요!

요트 매뉴얼 PDF 파일을 업로드해주시면 자동으로 분석하고 등록합니다.

**PDF 파일 업로드 방법:**
PDF 파일의 전체 경로를 입력해주세요.

예시:
- `C:\\Users\\user\\Documents\\Sun Odyssey 380 Owners manual.pdf`
- `"C:\\Users\\user\\Documents\\manual.pdf"` (공백이 있는 경우 따옴표 사용)

⚠️ **참고**: PDF 분석 기능은 Gemini API가 필요합니다.
현재 Gemini API가 설정되지 않아 PDF 분석 기능을 사용할 수 없습니다.

Gemini API 키를 설정하려면:
1. 환경변수에 `GEMINI_API_KEY` 설정
2. 또는 실행 시 `--api-key YOUR_API_KEY` 옵션 사용

PDF 파일 경로를 입력해주세요! 📎"""
        
        return message
    
    def clear_history(self):
        """대화 히스토리 초기화"""
        self.chat_history = []
        self.current_yacht_registration = None
        print("🔄 대화 기록이 초기화되었습니다.")
    
    def get_history(self) -> List[Dict[str, str]]:
        """대화 히스토리 반환"""
        return self.chat_history
    
    def _convert_analysis_to_registration(self, analysis_result: Dict) -> Dict:
        """분석 결과를 요트 등록 형식으로 변환"""
        doc_info = analysis_result.get("documentInfo", {})
        yacht_specs = analysis_result.get("yachtSpecs", {})
        parts = analysis_result.get("parts", [])
        
        yacht_name = doc_info.get("yachtModel") or doc_info.get("title", "Unknown Yacht")
        manufacturer = doc_info.get("manufacturer", "")
        
        dimensions = yacht_specs.get("dimensions", {})
        loa_str = dimensions.get("LOA", "") or dimensions.get("loa", "")
        loa = self._parse_number(loa_str)
        beam_str = dimensions.get("Beam", "") or dimensions.get("beam", "")
        beam = self._parse_number(beam_str)
        draft_str = dimensions.get("Draft", "") or dimensions.get("draft", "")
        draft = self._parse_number(draft_str)
        displacement_str = dimensions.get("Displacement", "") or dimensions.get("displacement", "")
        displacement = self._parse_number(displacement_str)
        mast_height_str = dimensions.get("mastHeight", "") or dimensions.get("mastHeight", "")
        mast_height = self._parse_number(mast_height_str)
        
        engine = yacht_specs.get("engine", {})
        sail_area = yacht_specs.get("sailArea", {})
        
        part_list = []
        for part in parts:
            part_list.append({
                "name": part.get("name", ""),
                "manufacturer": part.get("manufacturer", ""),
                "model": part.get("model", ""),
                "interval": part.get("interval") if part.get("interval") else None
            })
        
        registration_data = {
            "basicInfo": {
                "name": yacht_name,
                "nickName": yacht_name,
                "manufacturer": manufacturer,
                "type": doc_info.get("documentType", ""),
                "year": "",
                "designer": "",
                "manual": analysis_result.get("fileInfo", {}).get("fileName", "")
            },
            "specifications": {
                "dimensions": {
                    "loa": loa,
                    "lwl": None,
                    "beam": beam,
                    "draft": draft,
                    "displacement": displacement,
                    "mastHeight": mast_height
                },
                "sailArea": {
                    "mainSailArea": self._parse_number(sail_area.get("mainsail", "")),
                    "jibSailArea": self._parse_number(sail_area.get("jib", "")),
                    "spinnakerSailArea": self._parse_number(sail_area.get("spinnaker", "")),
                    "totalSailArea": self._parse_number(sail_area.get("total", ""))
                },
                "engine": {
                    "type": engine.get("type", ""),
                    "power": engine.get("output") or engine.get("power", ""),
                    "model": engine.get("model", "")
                },
                "hull": {"hullMaterial": "", "deckMaterial": "", "keelType": ""},
                "accommodations": {"berths": None, "cabins": None, "heads": None},
                "capacity": {"fuelCapacity": None, "waterCapacity": None},
                "performance": {"maxSpeed": None, "cruisingSpeed": None},
                "ceCertification": "",
                "description": f"PDF 매뉴얼에서 자동 추출: {doc_info.get('title', '')}",
                "features": ""
            },
            "parts": part_list
        }
        
        return registration_data
    
    def _parse_number(self, value) -> Optional[float]:
        """문자열에서 숫자 추출"""
        if not value or not isinstance(value, str):
            return None
        import re
        match = re.search(r'(\d+\.?\d*)', value)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
        return None
    
    def _generate_registration_completion_message(self, analysis_result: Dict, registration_data: Dict) -> str:
        """등록 완료 메시지 생성"""
        doc_info = analysis_result.get("documentInfo", {})
        yacht_name = doc_info.get("yachtModel") or doc_info.get("title", "요트")
        parts_count = len(analysis_result.get("parts", []))
        
        message = f"""✅ 등록이 완료됐습니다! 🎉

**등록된 요트 정보:**
⛵ 모델: {yacht_name}
🏭 제조사: {doc_info.get('manufacturer', 'N/A')}
📄 문서 유형: {doc_info.get('documentType', 'N/A')}

**추출된 정보:**
📏 치수 정보: {'추출됨' if registration_data['specifications']['dimensions']['loa'] else '없음'}
🔧 부품 정보: {parts_count}개 부품 추출됨
⚙️ 엔진 정보: {'추출됨' if registration_data['specifications']['engine']['type'] else '없음'}

요트가 성공적으로 등록되었습니다! 이제 부품 관리와 정비 일정을 설정할 수 있습니다.

추가로 궁금한 점이 있으시면 언제든 물어보세요! 💬"""
        
        return message
    
    def _save_registration_to_json(self, registration_data: Dict, analysis_result: Dict):
        """등록 데이터를 JSON 파일로 저장"""
        try:
            self._add_to_yacht_specifications(registration_data, analysis_result)
            self._save_to_registered_yachts(registration_data, analysis_result)
            self._save_parts_to_json_files(registration_data, analysis_result)
            print("💾 JSON 파일에 저장 완료!")
        except Exception as e:
            print(f"⚠️ JSON 파일 저장 중 오류: {e}")
    
    def _add_to_yacht_specifications(self, registration_data: Dict, analysis_result: Dict):
        """yacht_specifications.json에 요트 추가"""
        try:
            spec_file = 'data/yacht_specifications.json'
            if os.path.exists(spec_file):
                with open(spec_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {
                    "version": "1.0",
                    "description": "요트 상세 스펙 데이터베이스",
                    "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
                    "yachts": []
                }
            
            basic_info = registration_data.get("basicInfo", {})
            specs = registration_data.get("specifications", {})
            yacht_id = basic_info.get("name", "").lower().replace(" ", "-").replace("/", "-")
            
            existing_ids = [y.get("id") for y in data.get("yachts", [])]
            if yacht_id in existing_ids:
                for yacht in data["yachts"]:
                    if yacht.get("id") == yacht_id:
                        yacht.update({
                            "name": basic_info.get("name", ""),
                            "manufacturer": basic_info.get("manufacturer", ""),
                            "type": basic_info.get("type", ""),
                            "manual": basic_info.get("manual", ""),
                            **self._convert_specs_to_yacht_format(specs)
                        })
                        break
            else:
                new_yacht = {
                    "id": yacht_id,
                    "name": basic_info.get("name", ""),
                    "manufacturer": basic_info.get("manufacturer", ""),
                    "type": basic_info.get("type", ""),
                    "manual": basic_info.get("manual", ""),
                    **self._convert_specs_to_yacht_format(specs)
                }
                data["yachts"].append(new_yacht)
            
            data["lastUpdated"] = datetime.now().strftime("%Y-%m-%d")
            with open(spec_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ {spec_file}에 저장됨")
        except Exception as e:
            print(f"⚠️ yacht_specifications.json 저장 실패: {e}")
    
    def _convert_specs_to_yacht_format(self, specs: Dict) -> Dict:
        """등록 데이터 스펙을 yacht_specifications.json 형식으로 변환"""
        dimensions = specs.get("dimensions", {})
        sail_area = specs.get("sailArea", {})
        engine = specs.get("engine", {})
        hull = specs.get("hull", {})
        accommodations = specs.get("accommodations", {})
        capacity = specs.get("capacity", {})
        performance = specs.get("performance", {})
        
        def format_dimension(value, unit="m"):
            if value is None:
                return None
            return {"value": value, "unit": unit, "display": f"{value}{unit}"}
        
        result = {}
        
        if dimensions:
            result["dimensions"] = {}
            if dimensions.get("loa"):
                result["dimensions"]["loa"] = format_dimension(dimensions.get("loa"))
            if dimensions.get("lwl"):
                result["dimensions"]["lwl"] = format_dimension(dimensions.get("lwl"))
            if dimensions.get("beam"):
                result["dimensions"]["beam"] = format_dimension(dimensions.get("beam"))
            if dimensions.get("draft"):
                result["dimensions"]["draft"] = format_dimension(dimensions.get("draft"))
            if dimensions.get("displacement"):
                result["dimensions"]["displacement"] = format_dimension(dimensions.get("displacement"), "kg")
            if dimensions.get("mastHeight"):
                result["dimensions"]["mastHeight"] = format_dimension(dimensions.get("mastHeight"))
        
        if sail_area:
            result["sailArea"] = {
                "mainSailArea": sail_area.get("mainSailArea"),
                "jibSailArea": sail_area.get("jibSailArea"),
                "spinnakerSailArea": sail_area.get("spinnakerSailArea"),
                "totalSailArea": sail_area.get("totalSailArea")
            }
        
        if engine:
            result["engine"] = {
                "type": engine.get("type", ""),
                "power": engine.get("power", ""),
                "model": engine.get("model", "")
            }
        
        if hull:
            result["hull"] = {
                "hullMaterial": hull.get("hullMaterial", ""),
                "deckMaterial": hull.get("deckMaterial", ""),
                "keelType": hull.get("keelType", "")
            }
        
        if accommodations:
            result["accommodations"] = {
                "berths": accommodations.get("berths"),
                "cabins": accommodations.get("cabins"),
                "heads": accommodations.get("heads")
            }
        
        if capacity:
            result["capacity"] = {
                "fuelCapacity": capacity.get("fuelCapacity"),
                "waterCapacity": capacity.get("waterCapacity")
            }
        
        if performance:
            result["performance"] = {
                "maxSpeed": performance.get("maxSpeed"),
                "cruisingSpeed": performance.get("cruisingSpeed")
            }
        
        if specs.get("ceCertification"):
            result["ceCertification"] = specs.get("ceCertification")
        if specs.get("description"):
            result["description"] = specs.get("description")
        if specs.get("features"):
            result["features"] = specs.get("features")
        
        return result
    
    def _save_to_registered_yachts(self, registration_data: Dict, analysis_result: Dict):
        """등록된 요트를 registered_yachts.json에 저장"""
        try:
            reg_file = 'data/registered_yachts.json'
            if os.path.exists(reg_file):
                with open(reg_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {
                    "version": "1.0",
                    "description": "PDF로 등록된 요트 목록",
                    "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
                    "yachts": []
                }
            
            registration_entry = {
                "registrationDate": datetime.now().isoformat(),
                "source": "PDF Upload",
                "pdfFile": analysis_result.get("fileInfo", {}).get("fileName", ""),
                "registrationData": registration_data,
                "analysisResult": {
                    "documentInfo": analysis_result.get("documentInfo", {}),
                    "partsCount": len(analysis_result.get("parts", [])),
                    "analysisStatus": "success" if "error" not in analysis_result else "error"
                }
            }
            
            data["yachts"].append(registration_entry)
            data["lastUpdated"] = datetime.now().strftime("%Y-%m-%d")
            
            with open(reg_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ {reg_file}에 저장됨")
        except Exception as e:
            print(f"⚠️ registered_yachts.json 저장 실패: {e}")
    
    def _save_parts_to_json_files(self, registration_data: Dict, analysis_result: Dict):
        """부품 정보를 각 JSON 파일에 저장"""
        try:
            basic_info = registration_data.get("basicInfo", {})
            yacht_name = basic_info.get("name", "")
            yacht_id = basic_info.get("name", "").lower().replace(" ", "-").replace("/", "-")
            manufacturer = basic_info.get("manufacturer", "")
            manual_pdf = basic_info.get("manual", "")
            parts = analysis_result.get("parts", [])
            
            if not parts:
                print("⚠️ 추출된 부품이 없어 부품 JSON 파일 저장을 건너뜁니다.")
                return
            
            self._add_to_yacht_parts_database(yacht_id, yacht_name, manufacturer, manual_pdf, parts)
            self._add_to_extracted_parts_detailed(yacht_id, yacht_name, manufacturer, manual_pdf, parts)
            self._add_to_extracted_parts(yacht_id, yacht_name, manufacturer, manual_pdf, parts)
            self._add_to_parts_app_data(yacht_id, yacht_name, manufacturer, manual_pdf, parts)
            
            print(f"✅ 부품 정보가 {len(parts)}개 JSON 파일에 저장됨")
        except Exception as e:
            print(f"⚠️ 부품 JSON 파일 저장 중 오류: {e}")
            import traceback
            traceback.print_exc()
    
    def _add_to_yacht_parts_database(self, yacht_id: str, yacht_name: str, manufacturer: str, manual_pdf: str, parts: List[Dict]):
        """yacht_parts_database.json에 부품 추가"""
        try:
            db_file = 'data/yacht_parts_database.json'
            if os.path.exists(db_file):
                with open(db_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {"yachts": []}
            
            yacht_entry = None
            for yacht in data.get("yachts", []):
                if yacht.get("id") == yacht_id:
                    yacht_entry = yacht
                    break
            
            if not yacht_entry:
                yacht_entry = {
                    "id": yacht_id,
                    "name": yacht_name,
                    "manufacturer": manufacturer,
                    "type": "",
                    "length": None,
                    "officialWebsite": None,
                    "manualPDF": manual_pdf,
                    "dimensions": {},
                    "parts": {
                        "rigging": {"physicalParts": [], "maintenanceItems": []},
                        "sails": {"physicalParts": [], "maintenanceItems": []},
                        "engine": {"physicalParts": [], "maintenanceItems": []},
                        "hull": {"physicalParts": [], "maintenanceItems": []},
                        "electrical": {"physicalParts": [], "maintenanceItems": []},
                        "plumbing": {"physicalParts": [], "maintenanceItems": []}
                    }
                }
                data["yachts"].append(yacht_entry)
            
            parts_dict = yacht_entry.get("parts", {})
            
            for part in parts:
                category = part.get("category", "rigging").lower()
                name = part.get("name", "")
                if not name:
                    continue
                
                if category in ["rigging", "rig"]:
                    cat_key = "rigging"
                elif category in ["sails", "sail"]:
                    cat_key = "sails"
                elif category in ["engine", "motor"]:
                    cat_key = "engine"
                elif category in ["hull", "deck"]:
                    cat_key = "hull"
                elif category in ["electrical", "electric", "electronics"]:
                    cat_key = "electrical"
                elif category in ["plumbing", "water"]:
                    cat_key = "plumbing"
                else:
                    cat_key = "rigging"
                
                if cat_key not in parts_dict:
                    parts_dict[cat_key] = {"physicalParts": [], "maintenanceItems": []}
                
                physical_part = {
                    "id": f"{yacht_id}-{cat_key}-{len(parts_dict[cat_key]['physicalParts']) + 1:02d}",
                    "category": category.capitalize(),
                    "name": name,
                    "partNumber": part.get("model", ""),
                    "manufacturer": part.get("manufacturer", ""),
                    "maintenanceInterval": f"{part.get('interval', 12)}개월" if part.get("interval") else "Annual inspection"
                }
                
                parts_dict[cat_key]["physicalParts"].append(physical_part)
            
            with open(db_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ yacht_parts_database.json에 저장됨")
        except Exception as e:
            print(f"⚠️ yacht_parts_database.json 저장 실패: {e}")
    
    def _add_to_extracted_parts_detailed(self, yacht_id: str, yacht_name: str, manufacturer: str, manual_pdf: str, parts: List[Dict]):
        """extracted_yacht_parts_detailed.json에 부품 추가"""
        try:
            file_path = 'data/extracted_yacht_parts_detailed.json'
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {"yachts": []}
            
            yacht_entry = None
            for yacht in data.get("yachts", []):
                if yacht.get("id") == yacht_id:
                    yacht_entry = yacht
                    break
            
            if not yacht_entry:
                yacht_entry = {
                    "id": yacht_id,
                    "name": yacht_name,
                    "manufacturer": manufacturer,
                    "manualPDF": manual_pdf,
                    "parts": {
                        "rigging": [], "sails": [], "engine": [],
                        "hull": [], "electrical": [], "plumbing": []
                    }
                }
                data["yachts"].append(yacht_entry)
            
            parts_dict = yacht_entry.get("parts", {})
            
            for part in parts:
                category = part.get("category", "rigging").lower()
                name = part.get("name", "")
                if not name:
                    continue
                
                if category in ["rigging", "rig"]:
                    cat_key = "rigging"
                elif category in ["sails", "sail"]:
                    cat_key = "sails"
                elif category in ["engine", "motor"]:
                    cat_key = "engine"
                elif category in ["hull", "deck"]:
                    cat_key = "hull"
                elif category in ["electrical", "electric", "electronics"]:
                    cat_key = "electrical"
                elif category in ["plumbing", "water"]:
                    cat_key = "plumbing"
                else:
                    cat_key = "rigging"
                
                if cat_key not in parts_dict:
                    parts_dict[cat_key] = []
                
                part_entry = {
                    "name": name,
                    "description": f"{manufacturer} {yacht_name} - {name}",
                    "specifications": [
                        part.get("model", ""),
                        part.get("manufacturer", ""),
                        f"Interval: {part.get('interval', 'N/A')} months" if part.get("interval") else ""
                    ]
                }
                
                parts_dict[cat_key].append(part_entry)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ extracted_yacht_parts_detailed.json에 저장됨")
        except Exception as e:
            print(f"⚠️ extracted_yacht_parts_detailed.json 저장 실패: {e}")
    
    def _add_to_extracted_parts(self, yacht_id: str, yacht_name: str, manufacturer: str, manual_pdf: str, parts: List[Dict]):
        """extracted_yacht_parts.json에 부품 추가 (간단한 형식)"""
        try:
            file_path = 'data/extracted_yacht_parts.json'
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {"yachts": []}
            
            yacht_entry = None
            for yacht in data.get("yachts", []):
                if yacht.get("id") == yacht_id:
                    yacht_entry = yacht
                    break
            
            if not yacht_entry:
                yacht_entry = {
                    "id": yacht_id,
                    "name": yacht_name,
                    "manufacturer": manufacturer,
                    "parts": []
                }
                data["yachts"].append(yacht_entry)
            
            # 기존 부품 목록 가져오기 (중복 방지)
            existing_parts = yacht_entry.get("parts", [])
            existing_part_names = {p.get("name", "") for p in existing_parts if isinstance(p, dict)}
            
            for part in parts:
                # parts가 dict인지 확인
                if not isinstance(part, dict):
                    continue
                    
                name = part.get("name", "")
                if not name or name in existing_part_names:
                    continue
                
                part_entry = {
                    "name": name,
                    "manufacturer": part.get("manufacturer", ""),
                    "model": part.get("model", ""),
                    "category": part.get("category", "rigging"),
                    "interval": part.get("interval")
                }
                
                yacht_entry["parts"].append(part_entry)
                existing_part_names.add(name)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ extracted_yacht_parts.json에 저장됨")
        except Exception as e:
            print(f"⚠️ extracted_yacht_parts.json 저장 실패: {e}")
            import traceback
            traceback.print_exc()
    
    def _add_to_parts_app_data(self, yacht_id: str, yacht_name: str, manufacturer: str, manual_pdf: str, parts: List[Dict]):
        """yacht_parts_app_data.json에 부품 추가"""
        try:
            file_path = 'data/yacht_parts_app_data.json'
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {"yachts": []}
            
            yacht_entry = None
            for yacht in data.get("yachts", []):
                if yacht.get("id") == yacht_id:
                    yacht_entry = yacht
                    break
            
            if not yacht_entry:
                yacht_entry = {
                    "id": yacht_id,
                    "name": yacht_name,
                    "manufacturer": manufacturer,
                    "parts": []
                }
                data["yachts"].append(yacht_entry)
            
            for part in parts:
                name = part.get("name", "")
                if not name:
                    continue
                
                part_entry = {
                    "name": name,
                    "manufacturer": part.get("manufacturer", ""),
                    "model": part.get("model", ""),
                    "category": part.get("category", "rigging"),
                    "maintenanceInterval": part.get("interval", 12)
                }
                
                yacht_entry["parts"].append(part_entry)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ yacht_parts_app_data.json에 저장됨")
        except Exception as e:
            print(f"⚠️ yacht_parts_app_data.json 저장 실패: {e}")
    
    def get_registration_data(self) -> Optional[Dict]:
        """현재 등록 중인 요트 데이터 반환"""
        return self.current_yacht_registration


def run_interactive_mode(api_key: str = None):
    """대화형 모드 실행"""
    chatbot = UnifiedYachtChatbot(api_key=api_key, mode="interactive")
    
    print("\n💡 사용 팁:")
    print("  - 자연스럽게 질문하세요 (예: 'Farr 40 크기 알려줘')")
    print("  - PDF 파일 경로를 입력하면 자동으로 분석합니다")
    print("  - '/list' - 요트 목록 보기")
    print("  - '/info' - 데이터 정보 보기")
    print("  - '/help' - 도움말 보기")
    print("  - '/quit' 또는 '/exit' - 종료")
    print("\n" + "=" * 60 + "\n")
    
    while True:
        try:
            user_input = input("👤 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['/quit', '/exit', '/q']:
                print("\n👋 HooAah Yacht 챗봇을 종료합니다. 안녕히 가세요!")
                break
            
            if user_input.lower() == '/clear':
                chatbot.clear_history()
                continue
            
            print("\n🤖 AI: ", end="", flush=True)
            response = chatbot.chat(user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")


def run_api_server(api_key: str = None, port: int = 5000):
    """API 서버 모드 실행"""
    if not HAS_FLASK:
        print("❌ Flask가 설치되지 않았습니다. pip install flask flask-cors")
        return
    
    chatbot = UnifiedYachtChatbot(api_key=api_key, mode="api")
    
    app = Flask(__name__)
    CORS(app)
    
    chatbot_sessions = {}
    
    def get_or_create_chatbot(session_id: str):
        if session_id not in chatbot_sessions:
            chatbot_sessions[session_id] = UnifiedYachtChatbot(api_key=api_key, mode="api")
        return chatbot_sessions[session_id]
    
    @app.route('/api/chat', methods=['POST'])
    def chat():
        try:
            data = request.get_json()
            if not data or 'message' not in data:
                return jsonify({"success": False, "error": "메시지가 필요합니다."}), 400
            
            user_message = data['message']
            session_id = data.get('session_id', 'default')
            pdf_file_path = data.get('pdf_file_path')  # 모바일 앱에서 파일 경로 전달
            
            chatbot = get_or_create_chatbot(session_id)
            ai_response = chatbot.chat(user_message, pdf_file_path=pdf_file_path)
            
            return jsonify({
                "success": True,
                "response": ai_response,
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    @app.route('/api/chat/upload', methods=['POST'])
    def upload_pdf():
        """
        PDF 파일 업로드 API (모바일 앱용)
        
        Request:
        - multipart/form-data
        - file: PDF 파일
        - message: 사용자 메시지 (선택사항)
        - session_id: 세션 ID (선택사항)
        """
        try:
            if 'file' not in request.files:
                return jsonify({"success": False, "error": "파일이 필요합니다."}), 400
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({"success": False, "error": "파일이 선택되지 않았습니다."}), 400
            
            if not file.filename.lower().endswith('.pdf'):
                return jsonify({"success": False, "error": "PDF 파일만 업로드 가능합니다."}), 400
            
            # 파일 저장
            upload_folder = 'uploads'
            os.makedirs(upload_folder, exist_ok=True)
            
            if secure_filename:
                filename = secure_filename(file.filename)
            else:
                # secure_filename이 없으면 기본 파일명 사용
                filename = file.filename.replace(' ', '_')
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            
            # 세션 정보
            session_id = request.form.get('session_id', 'default')
            user_message = request.form.get('message', f'PDF 파일 업로드: {filename}')
            
            # 챗봇으로 처리
            chatbot = get_or_create_chatbot(session_id)
            ai_response = chatbot.chat(user_message, pdf_file_path=file_path)
            
            return jsonify({
                "success": True,
                "response": ai_response,
                "session_id": session_id,
                "file_name": filename,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    @app.route('/api/chat/history', methods=['GET'])
    def get_history():
        try:
            session_id = request.args.get('session_id', 'default')
            chatbot = get_or_create_chatbot(session_id)
            history = chatbot.get_history()
            return jsonify({"success": True, "history": history})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat()
        })
    
    print("=" * 60)
    print("🌐 HooAah Yacht AI Chatbot API Server")
    print("=" * 60)
    print(f"🚀 서버 시작: http://localhost:{port}")
    print("📡 API 엔드포인트:")
    print("  - POST /api/chat - 채팅 메시지 전송")
    print("  - GET /api/chat/history - 대화 기록 조회")
    print("  - GET /api/health - 서버 상태 확인")
    print("=" * 60)
    print()
    
    app.run(host='0.0.0.0', port=port, debug=True)


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='HooAah Yacht 통합 챗봇')
    parser.add_argument('--mode', choices=['interactive', 'api'], default='interactive',
                        help='실행 모드 (interactive: 대화형, api: API 서버)')
    parser.add_argument('--api-key', type=str, help='Gemini API 키 (선택사항, .env 파일 또는 환경변수 사용)')
    parser.add_argument('--port', type=int, default=5000, help='API 서버 포트 (기본: 5000)')
    
    args = parser.parse_args()
    
    # API 키 우선순위: 명령줄 인자 > 환경변수 (.env 파일)
    api_key = args.api_key or os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ 오류: GEMINI_API_KEY가 설정되지 않았습니다.")
        print("💡 다음 중 하나를 선택하세요:")
        print("   1. .env 파일 생성: .env.example을 참고하여 .env 파일을 만들고 GEMINI_API_KEY를 설정")
        print("   2. 환경변수 설정: export GEMINI_API_KEY=your-api-key (Linux/Mac) 또는 set GEMINI_API_KEY=your-api-key (Windows)")
        print("   3. 명령줄 옵션: --api-key YOUR_API_KEY")
        sys.exit(1)
    
    if args.mode == 'api':
        run_api_server(api_key=api_key, port=args.port)
    else:
        run_interactive_mode(api_key=api_key)


if __name__ == "__main__":
    main()

