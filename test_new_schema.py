#!/usr/bin/env python3
"""
테스트 스크립트: 새로운 Schema 5.0으로 PDF 분석 테스트
"""

import os
import sys
import json
from datetime import datetime

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chatbot_unified import UnifiedYachtChatbot

def test_single_pdf(pdf_path, api_key):
    """단일 PDF 파일 테스트"""
    print(f"\n{'='*80}")
    print(f"📄 테스트 파일: {os.path.basename(pdf_path)}")
    print(f"{'='*80}\n")
    
    # Chatbot 초기화
    chatbot = UnifiedYachtChatbot(api_key=api_key)
    
    # PDF 분석
    try:
        # 1. PDF에서 텍스트 추출
        print("📖 텍스트 추출 중...")
        extracted_text = chatbot._extract_text_from_pdf(pdf_path)
        print(f"   추출된 텍스트 길이: {len(extracted_text)} 문자")
        
        # 2. 문서 분석
        print("🤖 AI 분석 시작...")
        result = chatbot._analyze_document_directly(pdf_path, extracted_text)
        
        # 결과 저장
        output_file = f"test_result_{os.path.basename(pdf_path).replace('.pdf', '')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 분석 완료!")
        print(f"📁 결과 저장: {output_file}")
        
        # 간단한 요약 출력
        print(f"\n📊 분석 요약:")
        if "documentInfo" in result:
            doc_info = result["documentInfo"]
            print(f"  - 문서 제목: {doc_info.get('title', 'N/A')}")
            print(f"  - 요트 모델: {doc_info.get('yachtModel', 'N/A')}")
            print(f"  - 제조사: {doc_info.get('manufacturer', 'N/A')}")
        
        if "schemaVersion" in result:
            print(f"  - 스키마 버전: {result['schemaVersion']}")
        
        # ID 확인
        id_count = count_ids(result)
        print(f"  - 생성된 ID 개수: {id_count}")
        
        # 각 섹션 확인
        sections = [
            "yachtSpecs", "detailedDimensions", "exterior", "groundTackle",
            "sailInventory", "deckEquipment", "accommodations", "tanks",
            "electricalSystem", "electronics", "plumbingSystem", "parts"
        ]
        
        print(f"\n📋 섹션별 데이터:")
        for section in sections:
            if section in result and result[section]:
                print(f"  ✅ {section}")
            else:
                print(f"  ❌ {section} (없음)")
        
        return result
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return None


def count_ids(obj, count=0):
    """재귀적으로 JSON에서 ID 개수 세기"""
    if isinstance(obj, dict):
        if "id" in obj:
            count += 1
        for value in obj.values():
            count = count_ids(value, count)
    elif isinstance(obj, list):
        for item in obj:
            count = count_ids(item, count)
    return count


def test_all_pdfs(pdf_dir, api_key):
    """모든 PDF 파일 테스트"""
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    
    print(f"\n{'='*80}")
    print(f"🚀 전체 PDF 파일 분석 시작")
    print(f"📁 디렉토리: {pdf_dir}")
    print(f"📄 파일 개수: {len(pdf_files)}")
    print(f"{'='*80}\n")
    
    results = []
    
    for i, pdf_file in enumerate(pdf_files, 1):
        pdf_path = os.path.join(pdf_dir, pdf_file)
        print(f"\n[{i}/{len(pdf_files)}] {pdf_file}")
        
        result = test_single_pdf(pdf_path, api_key)
        if result:
            results.append({
                "fileName": pdf_file,
                "result": result,
                "timestamp": datetime.now().isoformat()
            })
    
    # 전체 결과 저장
    summary_file = f"test_all_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            "totalFiles": len(pdf_files),
            "successCount": len(results),
            "results": results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*80}")
    print(f"✅ 전체 분석 완료!")
    print(f"📁 전체 결과: {summary_file}")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    API_KEY = "AIzaSyBhPZDNBTEqYu8ahBIVpK2B1h_CAKgo7JI"
    PDF_DIR = "data/yachtpdf"
    
    # 테스트 모드 선택
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        # 모든 PDF 테스트
        test_all_pdfs(PDF_DIR, API_KEY)
    else:
        # 단일 PDF 테스트 (샘플)
        sample_pdf = os.path.join(PDF_DIR, "owners_manual.pdf")
        if os.path.exists(sample_pdf):
            test_single_pdf(sample_pdf, API_KEY)
        else:
            print(f"❌ 테스트 파일을 찾을 수 없습니다: {sample_pdf}")
            print("\n사용 가능한 PDF 파일:")
            for f in os.listdir(PDF_DIR):
                if f.endswith('.pdf'):
                    print(f"  - {f}")

