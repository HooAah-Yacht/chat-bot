# -*- coding: utf-8 -*-
"""
실제 PDF 파일 분석 테스트 (디버그 버전)
11월11일 멘토링.pdf, 11월17일 멘토링.pdf 분석
"""

import sys
import json
from datetime import datetime
from chatbot_unified import UnifiedYachtChatbot

# UTF-8 인코딩 설정
sys.stdout.reconfigure(encoding='utf-8')

def test_pdf_analysis_debug():
    """실제 PDF 파일 분석 (원본 분석 결과 포함)"""
    
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
            # 텍스트 추출
            extracted_text = chatbot._extract_text_from_file(file_info['path'])
            text_preview = extracted_text[:1000] if extracted_text else "텍스트 없음"
            
            print(f"추출된 텍스트 미리보기 (처음 1000자):\n{text_preview}\n")
            
            # AI 분석
            analysis_result = chatbot._analyze_document_directly(file_info['path'], extracted_text)
            
            result = {
                "fileName": file_info['name'],
                "filePath": file_info['path'],
                "timestamp": datetime.now().isoformat(),
                "status": "success",
                "textLength": len(extracted_text) if extracted_text else 0,
                "textPreview": text_preview,
                "analysisResult": analysis_result
            }
            
            print(f"\n✅ 분석 완료: {file_info['name']}")
            print(f"\n분석 결과 (JSON):")
            print(json.dumps(analysis_result, ensure_ascii=False, indent=2))
            
        except Exception as e:
            import traceback
            result = {
                "fileName": file_info['name'],
                "filePath": file_info['path'],
                "timestamp": datetime.now().isoformat(),
                "status": "failed",
                "error": str(e),
                "traceback": traceback.format_exc()
            }
            print(f"\n❌ 분석 실패: {file_info['name']}")
            print(f"오류: {e}")
            print(f"상세 오류:\n{traceback.format_exc()}")
        
        results["results"].append(result)
    
    # 결과 저장
    output_file = "actual_pdf_analysis_results_debug.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*80}")
    print(f"✅ 분석 결과가 {output_file}에 저장되었습니다.")
    print(f"{'='*80}\n")
    
    return results

if __name__ == "__main__":
    results = test_pdf_analysis_debug()
    
    print("\n📊 분석 요약:")
    print(f"총 파일 수: {results['totalFiles']}")
    
    success_count = sum(1 for r in results['results'] if r['status'] == 'success')
    fail_count = results['totalFiles'] - success_count
    
    print(f"성공: {success_count}개")
    print(f"실패: {fail_count}개")

