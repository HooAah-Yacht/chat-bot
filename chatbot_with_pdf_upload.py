"""
HooAah Yacht AI Chatbot with PDF Upload - PDF 업로드 및 분석 통합 챗봇
요트 매뉴얼 PDF를 업로드하면 자동으로 분석하고 등록하는 챗봇
"""

import os
import json
import google.generativeai as genai
from datetime import datetime
from typing import List, Dict, Optional
from yacht_document_analyzer import YachtDocumentAnalyzer
import tempfile
import shutil

class YachtAIChatbotWithPDF:
    def __init__(self, api_key: str = None):
        """
        PDF 업로드 기능이 있는 요트 챗봇 초기화
        
        Args:
            api_key: Gemini API 키 (없으면 환경변수에서 가져옴)
        """
        # API 키 설정
        if api_key is None:
            api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다. 환경변수 또는 직접 입력해주세요.")
        
        # Gemini API 설정
        genai.configure(api_key=api_key)
        
        # 모델 초기화 - Gemini 2.5 Flash 사용
        try:
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            print("✅ Gemini 2.5 Flash 모델 사용")
        except Exception as e:
            print(f"⚠️ Gemini 2.5 Flash 사용 실패, gemini-pro로 전환: {e}")
            self.model = genai.GenerativeModel('gemini-pro')
            print("✅ gemini-pro 모델 사용 (fallback)")
        
        # 문서 분석기 초기화
        self.document_analyzer = YachtDocumentAnalyzer(api_key=api_key)
        
        # 대화 히스토리
        self.chat_history: List[Dict[str, str]] = []
        
        # 요트 데이터 로드
        self.yacht_data = self._load_yacht_data()
        self.parts_data = self._load_parts_data()
        
        # 시스템 프롬프트 설정
        self.system_prompt = self._create_system_prompt()
        
        # 현재 등록 중인 요트 정보 (PDF 업로드 시 사용)
        self.current_yacht_registration: Optional[Dict] = None
        
        print("✅ HooAah Yacht AI 챗봇이 준비되었습니다!")
        print("💬 자연스럽게 요트에 대해 질문해보세요.")
        print("📄 요트 매뉴얼 PDF를 업로드하면 자동으로 분석하고 등록합니다.\n")
    
    def _load_yacht_data(self) -> Dict:
        """요트 스펙 데이터 로드"""
        try:
            with open('data/yacht_specifications.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ yacht_specifications.json 파일을 찾을 수 없습니다.")
            return {"yachts": []}
    
    def _load_parts_data(self) -> Dict:
        """요트 부품 데이터 로드"""
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
- 요트 매뉴얼 PDF 업로드 및 분석 안내
- 자연스럽고 대화적인 톤으로 소통

**지원하는 요트 20종:**
{', '.join(yacht_list)}

**PDF 업로드 기능:**
- 사용자가 요트 매뉴얼 PDF를 업로드하면 자동으로 분석합니다
- 분석 결과를 바탕으로 요트 정보를 등록합니다
- 진행 상황을 친절하게 안내합니다

**답변 가이드라인:**
1. 친근하고 자연스러운 대화체 사용 (존댓말)
2. 요트 이름이 언급되면 해당 요트의 상세 정보 제공
3. PDF 업로드 시: "요트 문서를 등록하세요" 안내
4. 분석 중: 진행 상황을 알려주고 기다려달라고 안내
5. 분석 완료: 등록 완료 메시지와 함께 요트 정보 요약 제공
6. 모르는 내용은 솔직히 모른다고 답변

**답변 형식:**
- 짧고 명확하게 (모바일 화면에 적합)
- 필요시 이모지 사용 (⛵, 🔧, 📏, ⚓, 📄 등)
- 숫자는 단위와 함께 명시
- 추가 질문 유도
"""
        return prompt
    
    def chat(self, user_message: str, pdf_file_path: str = None) -> str:
        """
        사용자 메시지에 대한 응답 생성
        
        Args:
            user_message: 사용자 입력 메시지
            pdf_file_path: PDF 파일 경로 (선택사항)
            
        Returns:
            AI 응답 메시지
        """
        try:
            # 1. 직접 전달된 PDF 파일 경로 확인
            if pdf_file_path and os.path.exists(pdf_file_path):
                return self._handle_pdf_upload(pdf_file_path)
            
            # 2. 사용자 메시지에서 PDF 파일 경로 추출
            pdf_path = self._extract_pdf_path_from_message(user_message)
            if pdf_path and os.path.exists(pdf_path):
                return self._handle_pdf_upload(pdf_path)
            
            # 대화 히스토리에 사용자 메시지 추가
            self.chat_history.append({
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now().isoformat()
            })
            
            # PDF 업로드 관련 키워드 확인
            if any(keyword in user_message.lower() for keyword in ['pdf', '문서', '매뉴얼', '업로드', '등록']):
                return self._suggest_pdf_upload()
            
            # 컨텍스트 구성 (시스템 프롬프트 + 대화 히스토리)
            context = self._build_context()
            
            # Gemini API 호출
            response = self.model.generate_content(context)
            
            # 응답 추출
            ai_response = response.text
            
            # 대화 히스토리에 AI 응답 추가
            self.chat_history.append({
                "role": "assistant",
                "content": ai_response,
                "timestamp": datetime.now().isoformat()
            })
            
            return ai_response
            
        except Exception as e:
            error_msg = f"죄송합니다. 응답 생성 중 오류가 발생했습니다: {str(e)}"
            print(f"❌ Error: {e}")
            return error_msg
    
    def _extract_pdf_path_from_message(self, message: str) -> Optional[str]:
        """
        사용자 메시지에서 PDF 파일 경로 추출 (절대 경로, 상대 경로 모두 지원)
        
        Args:
            message: 사용자 입력 메시지
            
        Returns:
            PDF 파일 경로 또는 None
        """
        import re
        
        # 1. 따옴표로 감싸진 경로 찾기 (공백 포함 경로 지원)
        # "C:\Users\user\Documents\Sun Odyssey 380 Owners manual.pdf" 같은 경우
        quoted_patterns = [
            r'["\']([^"\']+\.pdf)["\']',  # 기본 따옴표 패턴
            r'["\']([^"\']+\.pdf)',  # 시작 따옴표만
            r'([^"\']+\.pdf)["\']',  # 끝 따옴표만
        ]
        
        for pattern in quoted_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                path = match.group(1).strip()
                # 절대 경로 확인
                if os.path.isabs(path) and os.path.exists(path):
                    return path
                # 상대 경로 확인
                elif os.path.exists(path):
                    return os.path.abspath(path)
        
        # 2. Windows 절대 경로 패턴 (C:\... 또는 D:\...)
        # 공백이 포함된 경로도 지원: C:\Users\user\Documents\Sun Odyssey 380 Owners manual.pdf
        windows_abs_pattern = r'([A-Za-z]:[\\/](?:[^"\']+[\\/])*[^"\']+\.pdf)'
        match = re.search(windows_abs_pattern, message, re.IGNORECASE)
        if match:
            path = match.group(1).strip()
            if os.path.exists(path):
                return os.path.abspath(path)
        
        # 3. UNC 경로 (\\server\share\...)
        unc_pattern = r'(\\\\[^"\']+\.pdf)'
        match = re.search(unc_pattern, message, re.IGNORECASE)
        if match:
            path = match.group(1).strip()
            if os.path.exists(path):
                return os.path.abspath(path)
        
        # 4. 상대 경로 (현재 작업 디렉토리 기준)
        # 공백이 포함된 파일명도 지원
        relative_patterns = [
            r'([^"\']+[\\/][^"\']+\.pdf)',  # 상대 경로 with separator
            r'([^\\s]+\.pdf)',  # 단순 파일명
        ]
        
        for pattern in relative_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                path = match.group(1).strip().strip('"').strip("'")
                # 절대 경로로 변환하여 확인
                abs_path = os.path.abspath(path)
                if os.path.exists(abs_path):
                    return abs_path
                # 원본 경로도 확인
                if os.path.exists(path):
                    return os.path.abspath(path)
        
        # 5. 메시지 전체가 파일 경로인지 확인 (마지막 시도)
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
    
    def _suggest_pdf_upload(self) -> str:
        """PDF 업로드 안내 메시지"""
        message = """📄 요트 문서를 등록하세요!

요트 매뉴얼 PDF 파일을 업로드해주시면:
1. 📋 문서를 자동으로 분석합니다
2. ⛵ 요트 정보를 추출합니다
3. 🔧 부품 정보를 정리합니다
4. ✅ 데이터베이스에 등록합니다

PDF 파일을 업로드해주세요!"""
        
        self.chat_history.append({
            "role": "assistant",
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        
        return message
    
    def _handle_pdf_upload(self, pdf_path: str) -> str:
        """
        PDF 업로드 및 분석 처리
        
        Args:
            pdf_path: PDF 파일 경로
            
        Returns:
            분석 결과 및 등록 완료 메시지
        """
        try:
            # 1. 분석 시작 메시지
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
            
            print(f"\n📄 PDF 분석 시작: {os.path.basename(pdf_path)}")
            
            # 2. PDF 분석
            analysis_result = self.document_analyzer.analyze_pdf(pdf_path, use_file_upload=False)
            
            # 3. 분석 결과 확인
            if "error" in analysis_result:
                error_msg = f"❌ 문서 분석 중 오류가 발생했습니다:\n{analysis_result.get('error', '알 수 없는 오류')}"
                
                self.chat_history.append({
                    "role": "assistant",
                    "content": error_msg,
                    "timestamp": datetime.now().isoformat()
                })
                
                return error_msg
            
            # 4. 분석 결과를 요트 등록 형식으로 변환
            registration_data = self._convert_analysis_to_registration(analysis_result)
            
            # 5. 등록 완료 메시지 생성
            completion_msg = self._generate_registration_completion_message(analysis_result, registration_data)
            
            # 6. 등록 데이터 저장 (메모리 + JSON 파일)
            self.current_yacht_registration = registration_data
            
            # JSON 파일로 저장
            self._save_registration_to_json(registration_data, analysis_result)
            
            # 7. 대화 히스토리에 추가
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
            
            self.chat_history.append({
                "role": "assistant",
                "content": error_msg,
                "timestamp": datetime.now().isoformat()
            })
            
            return error_msg
    
    def _convert_analysis_to_registration(self, analysis_result: Dict) -> Dict:
        """
        분석 결과를 요트 등록 형식으로 변환
        
        Args:
            analysis_result: PDF 분석 결과
            
        Returns:
            요트 등록용 데이터
        """
        doc_info = analysis_result.get("documentInfo", {})
        yacht_specs = analysis_result.get("yachtSpecs", {})
        parts = analysis_result.get("parts", [])
        
        # 기본 정보
        yacht_name = doc_info.get("yachtModel") or doc_info.get("title", "Unknown Yacht")
        manufacturer = doc_info.get("manufacturer", "")
        
        # 치수 정보 추출
        dimensions = yacht_specs.get("dimensions", {})
        
        # LOA 파싱 (예: "6.934m (22.75')" -> 6.934)
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
        
        # 엔진 정보
        engine = yacht_specs.get("engine", {})
        
        # 돛 면적
        sail_area = yacht_specs.get("sailArea", {})
        
        # 부품 리스트 변환
        part_list = []
        for part in parts:
            part_list.append({
                "name": part.get("name", ""),
                "manufacturer": part.get("manufacturer", ""),
                "model": part.get("model", ""),
                "interval": part.get("interval") if part.get("interval") else None
            })
        
        # 등록 데이터 구성
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
                "hull": {
                    "hullMaterial": "",
                    "deckMaterial": "",
                    "keelType": ""
                },
                "accommodations": {
                    "berths": None,
                    "cabins": None,
                    "heads": None
                },
                "capacity": {
                    "fuelCapacity": None,
                    "waterCapacity": None
                },
                "performance": {
                    "maxSpeed": None,
                    "cruisingSpeed": None
                },
                "ceCertification": "",
                "description": f"PDF 매뉴얼에서 자동 추출: {doc_info.get('title', '')}",
                "features": ""
            },
            "parts": part_list
        }
        
        return registration_data
    
    def _parse_number(self, value) -> Optional[float]:
        """
        문자열에서 숫자 추출
        
        Args:
            value: 숫자가 포함된 문자열 (예: "6.934m (22.75')")
            
        Returns:
            추출된 숫자 (float) 또는 None
        """
        if not value or not isinstance(value, str):
            return None
        
        import re
        # 숫자와 소수점 추출 (첫 번째 숫자만)
        match = re.search(r'(\d+\.?\d*)', value)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
        
        return None
    
    def _generate_registration_completion_message(self, analysis_result: Dict, registration_data: Dict) -> str:
        """
        등록 완료 메시지 생성
        
        Args:
            analysis_result: PDF 분석 결과
            registration_data: 등록 데이터
            
        Returns:
            등록 완료 메시지
        """
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
    
    def _build_context(self) -> str:
        """대화 컨텍스트 구성"""
        # 시스템 프롬프트로 시작
        context = self.system_prompt + "\n\n**대화 기록:**\n"
        
        # 최근 10개 대화만 포함 (토큰 제한 고려)
        recent_history = self.chat_history[-10:]
        
        for msg in recent_history:
            role = "사용자" if msg["role"] == "user" else "어시스턴트"
            context += f"\n{role}: {msg['content']}\n"
        
        return context
    
    def _save_registration_to_json(self, registration_data: Dict, analysis_result: Dict):
        """
        등록 데이터를 JSON 파일로 저장
        
        Args:
            registration_data: 등록 데이터
            analysis_result: PDF 분석 결과
        """
        try:
            # 1. yacht_specifications.json에 추가
            self._add_to_yacht_specifications(registration_data, analysis_result)
            
            # 2. registered_yachts.json에 개별 저장 (등록된 요트 목록)
            self._save_to_registered_yachts(registration_data, analysis_result)
            
            # 3. 부품 관련 JSON 파일들에 저장
            self._save_parts_to_json_files(registration_data, analysis_result)
            
            print("💾 JSON 파일에 저장 완료!")
            
        except Exception as e:
            print(f"⚠️ JSON 파일 저장 중 오류: {e}")
    
    def _add_to_yacht_specifications(self, registration_data: Dict, analysis_result: Dict):
        """yacht_specifications.json에 요트 추가"""
        try:
            # 기존 파일 읽기
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
            
            # 새 요트 정보 구성
            basic_info = registration_data.get("basicInfo", {})
            specs = registration_data.get("specifications", {})
            
            # ID 생성 (이름 기반)
            yacht_id = basic_info.get("name", "").lower().replace(" ", "-").replace("/", "-")
            
            # 기존에 같은 ID가 있는지 확인
            existing_ids = [y.get("id") for y in data.get("yachts", [])]
            if yacht_id in existing_ids:
                # 기존 요트 업데이트
                for yacht in data["yachts"]:
                    if yacht.get("id") == yacht_id:
                        # 업데이트
                        yacht.update({
                            "name": basic_info.get("name", ""),
                            "manufacturer": basic_info.get("manufacturer", ""),
                            "type": basic_info.get("type", ""),
                            "manual": basic_info.get("manual", ""),
                            **self._convert_specs_to_yacht_format(specs)
                        })
                        break
            else:
                # 새 요트 추가
                new_yacht = {
                    "id": yacht_id,
                    "name": basic_info.get("name", ""),
                    "manufacturer": basic_info.get("manufacturer", ""),
                    "type": basic_info.get("type", ""),
                    "manual": basic_info.get("manual", ""),
                    **self._convert_specs_to_yacht_format(specs)
                }
                data["yachts"].append(new_yacht)
            
            # 파일 저장
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
        
        # 기존 형식에 맞춰 변환 (value, unit, display 형식)
        def format_dimension(value, unit="m"):
            if value is None:
                return None
            return {
                "value": value,
                "unit": unit,
                "display": f"{value}{unit}"
            }
        
        result = {}
        
        # dimensions (기존 형식 유지)
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
        
        # sailArea
        if sail_area:
            result["sailArea"] = {
                "mainSailArea": sail_area.get("mainSailArea"),
                "jibSailArea": sail_area.get("jibSailArea"),
                "spinnakerSailArea": sail_area.get("spinnakerSailArea"),
                "totalSailArea": sail_area.get("totalSailArea")
            }
        
        # engine
        if engine:
            result["engine"] = {
                "type": engine.get("type", ""),
                "power": engine.get("power", ""),
                "model": engine.get("model", "")
            }
        
        # hull
        if hull:
            result["hull"] = {
                "hullMaterial": hull.get("hullMaterial", ""),
                "deckMaterial": hull.get("deckMaterial", ""),
                "keelType": hull.get("keelType", "")
            }
        
        # accommodations
        if accommodations:
            result["accommodations"] = {
                "berths": accommodations.get("berths"),
                "cabins": accommodations.get("cabins"),
                "heads": accommodations.get("heads")
            }
        
        # capacity
        if capacity:
            result["capacity"] = {
                "fuelCapacity": capacity.get("fuelCapacity"),
                "waterCapacity": capacity.get("waterCapacity")
            }
        
        # performance
        if performance:
            result["performance"] = {
                "maxSpeed": performance.get("maxSpeed"),
                "cruisingSpeed": performance.get("cruisingSpeed")
            }
        
        # 기타
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
            
            # 기존 파일 읽기
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
            
            # 새 등록 정보 추가
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
            
            # 파일 저장
            with open(reg_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ {reg_file}에 저장됨")
            
        except Exception as e:
            print(f"⚠️ registered_yachts.json 저장 실패: {e}")
    
    def _save_parts_to_json_files(self, registration_data: Dict, analysis_result: Dict):
        """
        부품 정보를 각 JSON 파일에 저장
        
        Args:
            registration_data: 등록 데이터
            analysis_result: PDF 분석 결과
        """
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
            
            # 1. yacht_parts_database.json에 추가
            self._add_to_yacht_parts_database(yacht_id, yacht_name, manufacturer, manual_pdf, parts)
            
            # 2. extracted_yacht_parts_detailed.json에 추가
            self._add_to_extracted_parts_detailed(yacht_id, yacht_name, manufacturer, manual_pdf, parts)
            
            # 3. extracted_yacht_parts.json에 추가
            self._add_to_extracted_parts(yacht_id, yacht_name, manufacturer, manual_pdf, parts)
            
            # 4. yacht_parts_app_data.json에 추가
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
            
            # 기존 파일 읽기
            if os.path.exists(db_file):
                with open(db_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {"yachts": []}
            
            # 요트 찾기 또는 생성
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
            
            # 부품을 카테고리별로 분류하여 추가
            parts_dict = yacht_entry.get("parts", {})
            
            for part in parts:
                category = part.get("category", "rigging").lower()
                name = part.get("name", "")
                if not name:
                    continue
                
                # 카테고리 매핑
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
                    cat_key = "rigging"  # 기본값
                
                # physicalParts에 추가
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
            
            # 파일 저장
            with open(db_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ yacht_parts_database.json에 저장됨")
            
        except Exception as e:
            print(f"⚠️ yacht_parts_database.json 저장 실패: {e}")
    
    def _add_to_extracted_parts_detailed(self, yacht_id: str, yacht_name: str, manufacturer: str, manual_pdf: str, parts: List[Dict]):
        """extracted_yacht_parts_detailed.json에 부품 추가"""
        try:
            file_path = 'data/extracted_yacht_parts_detailed.json'
            
            # 기존 파일 읽기
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {"yachts": []}
            
            # 요트 찾기 또는 생성
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
                        "rigging": [],
                        "sails": [],
                        "engine": [],
                        "hull": [],
                        "electrical": [],
                        "plumbing": []
                    }
                }
                data["yachts"].append(yacht_entry)
            
            # 부품을 카테고리별로 분류하여 추가
            parts_dict = yacht_entry.get("parts", {})
            
            for part in parts:
                category = part.get("category", "rigging").lower()
                name = part.get("name", "")
                if not name:
                    continue
                
                # 카테고리 매핑
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
            
            # 파일 저장
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ extracted_yacht_parts_detailed.json에 저장됨")
            
        except Exception as e:
            print(f"⚠️ extracted_yacht_parts_detailed.json 저장 실패: {e}")
    
    def _add_to_extracted_parts(self, yacht_id: str, yacht_name: str, manufacturer: str, manual_pdf: str, parts: List[Dict]):
        """extracted_yacht_parts.json에 부품 추가 (간단한 형식)"""
        try:
            file_path = 'data/extracted_yacht_parts.json'
            
            # 기존 파일 읽기
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {"yachts": []}
            
            # 요트 찾기 또는 생성
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
            
            # 부품 추가
            for part in parts:
                name = part.get("name", "")
                if not name:
                    continue
                
                part_entry = {
                    "name": name,
                    "manufacturer": part.get("manufacturer", ""),
                    "model": part.get("model", ""),
                    "category": part.get("category", "rigging"),
                    "interval": part.get("interval")
                }
                
                yacht_entry["parts"].append(part_entry)
            
            # 파일 저장
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ extracted_yacht_parts.json에 저장됨")
            
        except Exception as e:
            print(f"⚠️ extracted_yacht_parts.json 저장 실패: {e}")
    
    def _add_to_parts_app_data(self, yacht_id: str, yacht_name: str, manufacturer: str, manual_pdf: str, parts: List[Dict]):
        """yacht_parts_app_data.json에 부품 추가"""
        try:
            file_path = 'data/yacht_parts_app_data.json'
            
            # 기존 파일 읽기
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {"yachts": []}
            
            # 요트 찾기 또는 생성
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
            
            # 부품 추가
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
            
            # 파일 저장
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ yacht_parts_app_data.json에 저장됨")
            
        except Exception as e:
            print(f"⚠️ yacht_parts_app_data.json 저장 실패: {e}")
    
    def get_registration_data(self) -> Optional[Dict]:
        """현재 등록 중인 요트 데이터 반환"""
        return self.current_yacht_registration
    
    def clear_history(self):
        """대화 히스토리 초기화"""
        self.chat_history = []
        self.current_yacht_registration = None
        print("🔄 대화 기록이 초기화되었습니다.")
    
    def get_history(self) -> List[Dict[str, str]]:
        """대화 히스토리 반환"""
        return self.chat_history


def main():
    """메인 함수 - 테스트 실행"""
    print("=" * 60)
    print("🛥️  HooAah Yacht AI Chatbot with PDF Upload")
    print("=" * 60)
    print()
    
    # API 키 설정
    api_key = "AIzaSyBhPZDNBTEqYu8ahBIVpK2B1h_CAKgo7JI"
    
    try:
        # 챗봇 초기화
        chatbot = YachtAIChatbotWithPDF(api_key=api_key)
        
        print("\n💡 사용 팁:")
        print("  - 자연스럽게 질문하세요 (예: '요트 등록하고 싶어요')")
        print("  - PDF 파일 경로를 입력하면 자동으로 분석합니다")
        print("  - '/clear' - 대화 기록 초기화")
        print("  - '/register' - 등록 데이터 확인")
        print("  - '/quit' 또는 '/exit' - 종료")
        print("\n" + "=" * 60 + "\n")
        
        # 대화 루프
        while True:
            # 사용자 입력
            user_input = input("👤 You: ").strip()
            
            if not user_input:
                continue
            
            # 명령어 처리
            if user_input.lower() in ['/quit', '/exit', '/q']:
                print("\n👋 HooAah Yacht AI 챗봇을 종료합니다. 안녕히 가세요!")
                break
            
            elif user_input.lower() == '/clear':
                chatbot.clear_history()
                continue
            
            elif user_input.lower() == '/register':
                reg_data = chatbot.get_registration_data()
                if reg_data:
                    print("\n📋 등록 데이터:")
                    print(json.dumps(reg_data, ensure_ascii=False, indent=2))
                else:
                    print("\n⚠️ 등록 중인 요트 데이터가 없습니다.")
                continue
            
            # AI 응답 생성 (chat 메서드 내부에서 PDF 경로를 자동으로 감지)
            print("\n🤖 AI: ", end="", flush=True)
            response = chatbot.chat(user_input)
            print(response)
            print()
    
    except KeyboardInterrupt:
        print("\n\n👋 프로그램을 종료합니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

