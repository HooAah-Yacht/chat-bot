"""
요트 챗봇 PDF 업로드 기능 테스트
사용자 플로우 시뮬레이션
"""

import os
from chatbot_with_pdf_upload import YachtAIChatbotWithPDF

def main():
    print("=" * 60)
    print("🧪 요트 챗봇 PDF 업로드 기능 테스트")
    print("=" * 60)
    print()
    
    # API 키 설정
    api_key = "AIzaSyBhPZDNBTEqYu8ahBIVpK2B1h_CAKgo7JI"
    
    try:
        # 1. 챗봇 초기화
        print("1️⃣ 챗봇 초기화 중...")
        chatbot = YachtAIChatbotWithPDF(api_key=api_key)
        print("✅ 챗봇이 실행 중입니다.\n")
        
        # 2. 요트 문서 등록 안내
        print("2️⃣ 요트 문서 등록 안내")
        print("-" * 60)
        response1 = chatbot.chat("요트 등록하고 싶어요")
        print(f"🤖 AI: {response1}\n")
        
        # 3. PDF 파일 업로드 (테스트용 파일)
        print("3️⃣ 사용자가 요트 매뉴얼 PDF를 넣습니다")
        print("-" * 60)
        
        # 테스트할 PDF 파일 선택
        test_pdf = "data/yachtpdf/j70-user-manual.pdf"
        
        if not os.path.exists(test_pdf):
            print(f"❌ 테스트 파일을 찾을 수 없습니다: {test_pdf}")
            print("다른 PDF 파일을 사용하세요.")
            return
        
        print(f"📄 PDF 파일: {os.path.basename(test_pdf)}\n")
        
        # 4. 챗봇이 분석
        print("4️⃣ 챗봇이 분석합니다")
        print("-" * 60)
        response2 = chatbot.chat("[PDF 업로드]", pdf_file_path=test_pdf)
        print(f"🤖 AI: {response2}\n")
        
        # 5. 등록 완료 확인
        print("5️⃣ 등록 완료 확인")
        print("-" * 60)
        reg_data = chatbot.get_registration_data()
        
        if reg_data:
            print("✅ 등록 데이터가 준비되었습니다!")
            print(f"   요트명: {reg_data['basicInfo']['name']}")
            print(f"   제조사: {reg_data['basicInfo']['manufacturer']}")
            print(f"   부품 수: {len(reg_data['parts'])}개")
            
            # 등록 데이터 저장 (API로 전송 가능)
            import json
            with open("yacht_registration_data.json", "w", encoding="utf-8") as f:
                json.dump(reg_data, f, ensure_ascii=False, indent=2)
            print("\n💾 등록 데이터가 'yacht_registration_data.json'에 저장되었습니다.")
            print("   이 데이터를 백엔드 API로 전송하면 요트가 등록됩니다.")
        else:
            print("⚠️ 등록 데이터가 없습니다.")
        
        print("\n" + "=" * 60)
        print("✅ 테스트 완료!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

