"""
PDF 경로 감지 테스트
"""

import os
from chatbot_with_pdf_upload import YachtAIChatbotWithPDF

def test_pdf_path_detection():
    print("=" * 60)
    print("🧪 PDF 경로 감지 테스트")
    print("=" * 60)
    print()
    
    # API 키 설정
    api_key = "AIzaSyBhPZDNBTEqYu8ahBIVpK2B1h_CAKgo7JI"
    
    try:
        # 챗봇 초기화
        chatbot = YachtAIChatbotWithPDF(api_key=api_key)
        
        # 테스트할 PDF 경로
        test_paths = [
            '"C:\\Users\\user\\Documents\\Sun Odyssey 380 Owners manual.pdf"',
            'C:\\Users\\user\\Documents\\Sun Odyssey 380 Owners manual.pdf',
            'data/yachtpdf/j70-user-manual.pdf',
        ]
        
        print("📋 PDF 경로 감지 테스트:\n")
        
        for test_path in test_paths:
            print(f"입력: {test_path}")
            extracted = chatbot._extract_pdf_path_from_message(test_path)
            
            if extracted:
                print(f"✅ 감지됨: {extracted}")
                if os.path.exists(extracted):
                    print(f"   파일 존재: ✅")
                else:
                    print(f"   파일 존재: ❌")
            else:
                print(f"❌ 감지 실패")
            print()
        
        # 실제 파일로 테스트
        real_pdf = "data/yachtpdf/j70-user-manual.pdf"
        if os.path.exists(real_pdf):
            print(f"\n📄 실제 파일 테스트: {real_pdf}")
            print("-" * 60)
            
            # 경로 추출 테스트
            test_messages = [
                f'"{real_pdf}"',
                real_pdf,
                f'이 파일 업로드: "{real_pdf}"',
            ]
            
            for msg in test_messages:
                print(f"\n입력: {msg}")
                extracted = chatbot._extract_pdf_path_from_message(msg)
                if extracted:
                    print(f"✅ 감지: {extracted}")
                else:
                    print(f"❌ 감지 실패")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pdf_path_detection()

