"""
HooAah Yacht AI Chatbot - Gemini API 기반 대화형 챗봇
요트 관련 질문에 대해 자연스럽게 대화하는 AI 어시스턴트
"""

import os
import json
import google.generativeai as genai
from datetime import datetime
from typing import List, Dict, Optional

class YachtAIChatbot:
    def __init__(self, api_key: str = None):
        """
        Gemini API 기반 요트 챗봇 초기화
        
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
        
        # 모델 초기화 (gemini-pro 사용)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # 대화 히스토리
        self.chat_history: List[Dict[str, str]] = []
        
        # 요트 데이터 로드
        self.yacht_data = self._load_yacht_data()
        self.parts_data = self._load_parts_data()
        
        # 시스템 프롬프트 설정
        self.system_prompt = self._create_system_prompt()
        
        print("✅ HooAah Yacht AI 챗봇이 준비되었습니다!")
        print("💬 자연스럽게 요트에 대해 질문해보세요.\n")
    
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
- 자연스럽고 대화적인 톤으로 소통

**지원하는 요트 20종:**
{', '.join(yacht_list)}

**답변 가이드라인:**
1. 친근하고 자연스러운 대화체 사용 (존댓말)
2. 요트 이름이 언급되면 해당 요트의 상세 정보 제공
3. 크기/치수 질문: LOA, Beam, Draft, Displacement, Mast Height 등 제공
4. 부품 질문: 해당 요트의 부품 목록과 정비 주기 안내
5. 비교 질문: 여러 요트를 비교하여 차이점 설명
6. 추천 질문: 사용 목적에 맞는 요트 추천
7. 정비/관리 질문: 정비 주기, 점검 항목, 유지보수 팁 제공
8. 모르는 내용은 솔직히 모른다고 답변

**답변 형식:**
- 짧고 명확하게 (모바일 화면에 적합)
- 필요시 이모지 사용 (⛵, 🔧, 📏, ⚓ 등)
- 숫자는 단위와 함께 명시
- 추가 질문 유도

**데이터 활용:**
아래 JSON 데이터를 참고하여 정확한 정보 제공:

요트 스펙 데이터:
{json.dumps(self.yacht_data, ensure_ascii=False, indent=2)[:5000]}...

부품 데이터 (샘플):
{json.dumps(self.parts_data, ensure_ascii=False, indent=2)[:3000]}...

**예시 대화:**
사용자: "Farr 40 크기 알려줘"
어시스턴트: "Farr 40의 크기 정보입니다! ⛵

📏 주요 치수:
- 전장(LOA): 12.19m (40ft)
- 폭(Beam): 3.63m
- 흘수(Draft): 2.74m
- 배수량: 4,536kg
- 마스트 높이: 18.29m

레이싱에 최적화된 크기네요! 다른 궁금한 점 있으신가요?"

사용자: "정비는 언제 해야 해?"
어시스턴트: "Farr 40의 주요 정비 항목입니다! 🔧

정기 점검 (매 항해 전):
- 리깅 점검
- 세일 상태 확인
- 안전장비 체크

월간 정비:
- 윈치 윤활
- 블록 점검
- 라인 마모 확인

연간 정비:
- 엔진 오버홀
- 리깅 전문 점검
- 선체 검사

더 자세한 부품별 정비 주기가 필요하신가요?"
"""
        return prompt
    
    def chat(self, user_message: str) -> str:
        """
        사용자 메시지에 대한 응답 생성
        
        Args:
            user_message: 사용자 입력 메시지
            
        Returns:
            AI 응답 메시지
        """
        try:
            # 대화 히스토리에 사용자 메시지 추가
            self.chat_history.append({
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now().isoformat()
            })
            
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
    
    def clear_history(self):
        """대화 히스토리 초기화"""
        self.chat_history = []
        print("🔄 대화 기록이 초기화되었습니다.")
    
    def get_history(self) -> List[Dict[str, str]]:
        """대화 히스토리 반환"""
        return self.chat_history
    
    def save_history(self, filename: str = "chat_history.json"):
        """대화 히스토리 저장"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.chat_history, f, ensure_ascii=False, indent=2)
            print(f"💾 대화 기록이 {filename}에 저장되었습니다.")
        except Exception as e:
            print(f"❌ 저장 실패: {e}")
    
    def load_history(self, filename: str = "chat_history.json"):
        """대화 히스토리 로드"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.chat_history = json.load(f)
            print(f"📂 대화 기록을 {filename}에서 불러왔습니다.")
        except FileNotFoundError:
            print(f"⚠️ {filename} 파일을 찾을 수 없습니다.")
        except Exception as e:
            print(f"❌ 로드 실패: {e}")


def main():
    """메인 함수 - 터미널 대화형 인터페이스"""
    print("=" * 60)
    print("🛥️  HooAah Yacht AI Chatbot (Gemini)")
    print("=" * 60)
    print()
    
    # API 키 입력 받기
    api_key = input("🔑 Gemini API 키를 입력하세요 (Enter: 환경변수 사용): ").strip()
    if not api_key:
        api_key = None
    
    try:
        # 챗봇 초기화
        chatbot = YachtAIChatbot(api_key=api_key)
        
        print("\n💡 사용 팁:")
        print("  - 자연스럽게 질문하세요 (예: '레이싱에 좋은 요트 추천해줘')")
        print("  - '/clear' - 대화 기록 초기화")
        print("  - '/save' - 대화 기록 저장")
        print("  - '/history' - 대화 기록 보기")
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
            
            elif user_input.lower() == '/save':
                chatbot.save_history()
                continue
            
            elif user_input.lower() == '/history':
                history = chatbot.get_history()
                print("\n📜 대화 기록:")
                for i, msg in enumerate(history, 1):
                    role = "👤" if msg["role"] == "user" else "🤖"
                    print(f"{i}. {role} {msg['content'][:100]}...")
                print()
                continue
            
            # AI 응답 생성
            print("\n🤖 AI: ", end="", flush=True)
            response = chatbot.chat(user_input)
            print(response)
            print()
    
    except KeyboardInterrupt:
        print("\n\n👋 프로그램을 종료합니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")


if __name__ == "__main__":
    main()

