"""
HooAah Yacht AI Chatbot 테스트 스크립트
API 서버 없이 직접 챗봇 기능 테스트
"""

from chatbot_gemini import YachtAIChatbot
import os

def test_chatbot():
    """챗봇 기본 기능 테스트"""
    print("=" * 60)
    print("🧪 HooAah Yacht AI Chatbot 테스트")
    print("=" * 60)
    print()
    
    # API 키 확인
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")
        print("   export GEMINI_API_KEY='your-api-key' 로 설정해주세요.")
        return
    
    try:
        # 챗봇 초기화
        print("1️⃣ 챗봇 초기화 중...")
        chatbot = YachtAIChatbot(api_key=api_key)
        print("✅ 초기화 완료!\n")
        
        # 테스트 질문들
        test_questions = [
            "Farr 40 크기 알려줘",
            "레이싱에 좋은 요트 추천해줘",
            "정비는 언제 해야 해?",
        ]
        
        # 각 질문 테스트
        for i, question in enumerate(test_questions, 1):
            print(f"{i}️⃣ 테스트 질문: {question}")
            print("-" * 60)
            
            response = chatbot.chat(question)
            
            print(f"🤖 AI 응답:\n{response}\n")
            print("=" * 60)
            print()
        
        # 대화 기록 확인
        print("4️⃣ 대화 기록 확인")
        print("-" * 60)
        history = chatbot.get_history()
        print(f"총 {len(history)}개의 메시지")
        for msg in history:
            role = "👤 사용자" if msg["role"] == "user" else "🤖 AI"
            content = msg["content"][:50] + "..." if len(msg["content"]) > 50 else msg["content"]
            print(f"{role}: {content}")
        print()
        
        # 대화 기록 저장
        print("5️⃣ 대화 기록 저장")
        print("-" * 60)
        chatbot.save_history("test_chat_history.json")
        print()
        
        print("✅ 모든 테스트 완료!")
        
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")

if __name__ == "__main__":
    test_chatbot()

