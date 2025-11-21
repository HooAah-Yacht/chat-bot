# -*- coding: utf-8 -*-
"""
실제 PDF 파일 분석 테스트
11월11일 멘토링.pdf, 11월17일 멘토링.pdf 분석
"""

import sys
import json
from datetime import datetime
from chatbot_unified import UnifiedYachtChatbot

# UTF-8 인코딩 설정
sys.stdout.reconfigure(encoding='utf-8')

def test_pdf_analysis():
    """실제 PDF 파일 분석"""
    
    # 챗봇 초기화
    print("챗봇 초기화 중...")
    chatbot = UnifiedYachtChatbot()
    
    # 테스트할 PDF 파일들
    test_files = [
        {
            "name": "11월11일 멘토링.pdf",
            "path": "data/yachtpdf/11월11일 멘토링.pdf"
        },
        {
            "name": "11월17일 멘토링.pdf",
            "path": "data/yachtpdf/11월17일 멘토링.pdf"
        }
    ]
    
    results = {
        "testDate": datetime.now().isoformat(),
        "totalFiles": len(test_files),
        "results": []
    }
    
    for file_info in test_files:
        print(f"\n{'='*80}")
        print(f"파일 분석 시작: {file_info['name']}")
        print(f"{'='*80}\n")
        
        try:
            # 파일 분석
            response = chatbot._handle_file_upload(file_info['path'])
            
            # 현재 등록 데이터 가져오기
            registration_data = chatbot.current_yacht_registration
            
            result = {
                "fileName": file_info['name'],
                "filePath": file_info['path'],
                "timestamp": datetime.now().isoformat(),
                "status": "success",
                "chatbotResponse": response,
                "registrationData": registration_data
            }
            
            print(f"\n✅ 분석 완료: {file_info['name']}")
            print(f"\n챗봇 응답:\n{response}")
            
            if registration_data:
                print(f"\n등록 데이터 (JSON):")
                print(json.dumps(registration_data, ensure_ascii=False, indent=2))
            
        except Exception as e:
            result = {
                "fileName": file_info['name'],
                "filePath": file_info['path'],
                "timestamp": datetime.now().isoformat(),
                "status": "failed",
                "error": str(e)
            }
            print(f"\n❌ 분석 실패: {file_info['name']}")
            print(f"오류: {e}")
        
        results["results"].append(result)
    
    # 결과 저장
    output_file = "actual_pdf_analysis_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*80}")
    print(f"✅ 분석 결과가 {output_file}에 저장되었습니다.")
    print(f"{'='*80}\n")
    
    return results

if __name__ == "__main__":
    results = test_pdf_analysis()
    
    print("\n📊 분석 요약:")
    print(f"총 파일 수: {results['totalFiles']}")
    
    success_count = sum(1 for r in results['results'] if r['status'] == 'success')
    fail_count = results['totalFiles'] - success_count
    
    print(f"성공: {success_count}개")
    print(f"실패: {fail_count}개")

