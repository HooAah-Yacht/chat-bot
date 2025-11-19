"""
요트 문서 분석기 테스트 스크립트
소수의 PDF 파일만 테스트하여 빠르게 확인
"""

import os
from yacht_document_analyzer import YachtDocumentAnalyzer

def main():
    print("=" * 60)
    print("🧪 요트 문서 분석기 테스트")
    print("=" * 60)
    print()
    
    # API 키 설정
    api_key = "AIzaSyBhPZDNBTEqYu8ahBIVpK2B1h_CAKgo7JI"
    
    try:
        # 분석기 초기화
        analyzer = YachtDocumentAnalyzer(api_key=api_key)
        
        # 테스트할 PDF 파일 목록 (소수만)
        test_files = [
            "data/yachtpdf/j70-user-manual.pdf",
            "data/yachtpdf/RS21Riggingguide.pdf",
            "data/yachtpdf/owners_manual.pdf",
        ]
        
        results = []
        
        for pdf_file in test_files:
            if os.path.exists(pdf_file):
                print(f"\n{'='*60}")
                print(f"테스트: {os.path.basename(pdf_file)}")
                print('='*60)
                
                try:
                    result = analyzer.analyze_pdf(pdf_file, use_file_upload=False)
                    results.append(result)
                except Exception as e:
                    print(f"❌ 오류: {e}")
                    results.append({
                        "error": str(e),
                        "fileInfo": {"fileName": os.path.basename(pdf_file)}
                    })
            else:
                print(f"⚠️ 파일을 찾을 수 없습니다: {pdf_file}")
        
        # 결과 저장
        import json
        with open("test_analysis_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 테스트 완료! 결과가 test_analysis_results.json에 저장되었습니다.")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

