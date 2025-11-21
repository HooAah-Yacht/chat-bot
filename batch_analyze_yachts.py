#!/usr/bin/env python3
"""
요트 매뉴얼 배치 분석 및 JSON 업데이트 스크립트
- 실제 요트 매뉴얼만 분석 (멘토링, 디자인 문서 제외)
- 새로운 Schema 5.0으로 분석
- 모든 JSON 파일 업데이트
"""

import os
import sys
import json
import shutil
from datetime import datetime
from chatbot_unified import UnifiedYachtChatbot

# 제외할 파일 목록 (요트 매뉴얼이 아닌 문서들)
EXCLUDED_FILES = [
    "11월11일 멘토링.pdf",
    "11월17일 멘토링.pdf",
    "정비 관련 자료.pdf",
    "풀리퀘스트1.pdf",
    "풀리퀘스트3.pdf",
    "후아_디자인 (1).pdf"
]

# PDF 디렉토리
PDF_DIR = "data/yachtpdf"

# API 키
API_KEY = "AIzaSyBhPZDNBTEqYu8ahBIVpK2B1h_CAKgo7JI"

# 백업 디렉토리
BACKUP_DIR = f"data/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


def backup_json_files():
    """기존 JSON 파일 백업"""
    print(f"\n{'='*80}")
    print(f"💾 JSON 파일 백업 시작")
    print(f"📁 백업 디렉토리: {BACKUP_DIR}")
    print(f"{'='*80}\n")
    
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    json_files = [
        "data/yacht_specifications.json",
        "data/yacht_parts_database.json",
        "data/yacht_manual_resources.json",
        "data/registered_yachts.json",
        "data/yacht_parts_app_data.json"
    ]
    
    for json_file in json_files:
        if os.path.exists(json_file):
            backup_path = os.path.join(BACKUP_DIR, os.path.basename(json_file))
            shutil.copy2(json_file, backup_path)
            print(f"✅ 백업: {json_file} → {backup_path}")
        else:
            print(f"⚠️ 파일 없음: {json_file}")
    
    print(f"\n✅ 백업 완료!\n")


def get_yacht_pdf_files():
    """분석할 요트 매뉴얼 PDF 파일 목록 가져오기"""
    if not os.path.exists(PDF_DIR):
        print(f"❌ PDF 디렉토리를 찾을 수 없습니다: {PDF_DIR}")
        return []
    
    all_pdfs = [f for f in os.listdir(PDF_DIR) if f.endswith('.pdf')]
    
    # 제외할 파일 필터링
    yacht_pdfs = [f for f in all_pdfs if f not in EXCLUDED_FILES]
    
    print(f"\n{'='*80}")
    print(f"📂 PDF 파일 분석 대상")
    print(f"{'='*80}\n")
    print(f"전체 PDF: {len(all_pdfs)}개")
    print(f"제외 파일: {len(EXCLUDED_FILES)}개")
    print(f"✅ 분석 대상: {len(yacht_pdfs)}개\n")
    
    print("제외된 파일:")
    for excluded in EXCLUDED_FILES:
        if excluded in all_pdfs:
            print(f"  ❌ {excluded}")
    
    print("\n분석할 파일:")
    for i, pdf in enumerate(yacht_pdfs, 1):
        print(f"  {i}. {pdf}")
    
    return yacht_pdfs


def analyze_pdf(chatbot, pdf_path, index, total):
    """단일 PDF 분석"""
    pdf_name = os.path.basename(pdf_path)
    
    print(f"\n{'='*80}")
    print(f"[{index}/{total}] 📄 {pdf_name}")
    print(f"{'='*80}\n")
    
    try:
        # 1. 텍스트 추출
        print("📖 텍스트 추출 중...")
        extracted_text = chatbot._extract_text_from_pdf(pdf_path)
        
        if not extracted_text or len(extracted_text.strip()) < 100:
            print(f"❌ 텍스트 추출 실패 (길이: {len(extracted_text)})")
            return None
        
        print(f"✅ 텍스트 추출 완료 (길이: {len(extracted_text)} 문자)")
        
        # 2. AI 분석
        print("🤖 AI 분석 중...")
        result = chatbot._analyze_document_directly(pdf_path, extracted_text)
        
        if "error" in result:
            print(f"❌ 분석 실패: {result.get('error')}")
            return None
        
        # 3. ID 개수 세기
        id_count = count_ids(result)
        print(f"✅ 분석 완료! (생성된 ID: {id_count}개)")
        
        # 4. 결과 저장
        output_file = f"analysis_results/{pdf_name.replace('.pdf', '')}.json"
        os.makedirs("analysis_results", exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"💾 결과 저장: {output_file}")
        
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


def update_json_files(results):
    """분석 결과로 JSON 파일들 업데이트"""
    print(f"\n{'='*80}")
    print(f"📝 JSON 파일 업데이트 시작")
    print(f"{'='*80}\n")
    
    # 1. yacht_specifications.json 업데이트
    update_yacht_specifications(results)
    
    # 2. yacht_parts_database.json 업데이트
    update_yacht_parts_database(results)
    
    # 3. yacht_manual_resources.json 업데이트
    update_yacht_manual_resources(results)
    
    # 4. registered_yachts.json 초기화
    initialize_registered_yachts()
    
    print(f"\n✅ 모든 JSON 파일 업데이트 완료!")


def update_yacht_specifications(results):
    """yacht_specifications.json 업데이트"""
    print(f"\n📋 yacht_specifications.json 업데이트...")
    
    yachts = []
    
    for result in results:
        if not result or result.get('analysisResult', {}).get('canAnalyze') != True:
            continue
        
        doc_info = result.get('documentInfo', {})
        yacht_model = doc_info.get('yachtModel')
        
        if not yacht_model:
            continue
        
        yacht_id = yacht_model.lower().replace(' ', '-').replace('/', '-').replace('_', '-')
        
        yacht_data = {
            "id": yacht_id,
            "name": yacht_model,
            "manufacturer": doc_info.get('manufacturer'),
            "type": doc_info.get('documentType', ''),
            "schemaVersion": "5.0",
            "updatedAt": datetime.now().isoformat(),
            "manualPDF": result.get('fileInfo', {}).get('fileName', ''),
            "yachtSpecs": result.get('yachtSpecs', {}),
            "detailedDimensions": result.get('detailedDimensions', {}),
            "exterior": result.get('exterior', {}),
            "groundTackle": result.get('groundTackle', {}),
            "sailInventory": result.get('sailInventory', []),
            "deckEquipment": result.get('deckEquipment', {}),
            "accommodations": result.get('accommodations', {}),
            "tanks": result.get('tanks', {}),
            "electricalSystem": result.get('electricalSystem', {}),
            "electronics": result.get('electronics', {}),
            "plumbingSystem": result.get('plumbingSystem', {})
        }
        
        yachts.append(yacht_data)
        print(f"  ✅ {yacht_model}")
    
    output = {
        "schemaVersion": "5.0",
        "lastUpdated": datetime.now().isoformat(),
        "totalYachts": len(yachts),
        "yachts": yachts
    }
    
    with open("data/yacht_specifications.json", 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ yacht_specifications.json 업데이트 완료 ({len(yachts)}척)")


def update_yacht_parts_database(results):
    """yacht_parts_database.json 업데이트"""
    print(f"\n📦 yacht_parts_database.json 업데이트...")
    
    yachts = []
    
    for result in results:
        if not result or result.get('analysisResult', {}).get('canAnalyze') != True:
            continue
        
        doc_info = result.get('documentInfo', {})
        yacht_model = doc_info.get('yachtModel')
        parts = result.get('parts', [])
        
        if not yacht_model or not parts:
            continue
        
        yacht_id = yacht_model.lower().replace(' ', '-').replace('/', '-').replace('_', '-')
        
        yacht_data = {
            "id": yacht_id,
            "name": yacht_model,
            "manufacturer": doc_info.get('manufacturer'),
            "manualPDF": result.get('fileInfo', {}).get('fileName', ''),
            "schemaVersion": "5.0",
            "parts": parts
        }
        
        yachts.append(yacht_data)
        print(f"  ✅ {yacht_model}: {len(parts)}개 부품")
    
    output = {
        "schemaVersion": "5.0",
        "lastUpdated": datetime.now().isoformat(),
        "totalYachts": len(yachts),
        "yachts": yachts
    }
    
    with open("data/yacht_parts_database.json", 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ yacht_parts_database.json 업데이트 완료 ({len(yachts)}척)")


def update_yacht_manual_resources(results):
    """yacht_manual_resources.json 업데이트"""
    print(f"\n📚 yacht_manual_resources.json 업데이트...")
    
    resources = []
    
    for result in results:
        if not result:
            continue
        
        doc_info = result.get('documentInfo', {})
        yacht_model = doc_info.get('yachtModel')
        
        if not yacht_model:
            continue
        
        resource = {
            "yachtModel": yacht_model,
            "manufacturer": doc_info.get('manufacturer'),
            "manualPDF": result.get('fileInfo', {}).get('fileName', ''),
            "documentType": doc_info.get('documentType'),
            "canAnalyze": result.get('analysisResult', {}).get('canAnalyze', False),
            "schemaVersion": "5.0",
            "updatedAt": datetime.now().isoformat()
        }
        
        resources.append(resource)
        print(f"  ✅ {yacht_model}: {result.get('fileInfo', {}).get('fileName', '')}")
    
    output = {
        "schemaVersion": "5.0",
        "lastUpdated": datetime.now().isoformat(),
        "totalResources": len(resources),
        "resources": resources
    }
    
    with open("data/yacht_manual_resources.json", 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ yacht_manual_resources.json 업데이트 완료 ({len(resources)}개)")


def initialize_registered_yachts():
    """registered_yachts.json 초기화"""
    print(f"\n🔄 registered_yachts.json 초기화...")
    
    output = {
        "schemaVersion": "5.0",
        "lastUpdated": datetime.now().isoformat(),
        "totalYachts": 0,
        "yachts": []
    }
    
    with open("data/registered_yachts.json", 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ registered_yachts.json 초기화 완료")


def main():
    """메인 실행 함수"""
    print(f"\n{'='*80}")
    print(f"🚀 요트 매뉴얼 배치 분석 시작")
    print(f"{'='*80}\n")
    print(f"📅 시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. 백업
    backup_json_files()
    
    # 2. 분석할 PDF 파일 목록 가져오기
    pdf_files = get_yacht_pdf_files()
    
    if not pdf_files:
        print("❌ 분석할 PDF 파일이 없습니다.")
        return
    
    # 3. 자동 시작 (사용자 확인 없이)
    print(f"\n{'='*80}")
    print(f"▶️ 총 {len(pdf_files)}개의 PDF를 자동으로 분석합니다...")
    
    # 4. Chatbot 초기화
    print(f"\n{'='*80}")
    print(f"🤖 AI 챗봇 초기화 중...")
    chatbot = UnifiedYachtChatbot(api_key=API_KEY)
    print(f"✅ 초기화 완료!")
    
    # 5. PDF 분석
    results = []
    success_count = 0
    failed_count = 0
    
    for i, pdf_file in enumerate(pdf_files, 1):
        pdf_path = os.path.join(PDF_DIR, pdf_file)
        result = analyze_pdf(chatbot, pdf_path, i, len(pdf_files))
        
        if result:
            results.append(result)
            success_count += 1
        else:
            failed_count += 1
        
        # 진행 상황 출력
        print(f"\n진행 상황: {i}/{len(pdf_files)} (성공: {success_count}, 실패: {failed_count})")
    
    # 6. JSON 파일 업데이트
    if results:
        update_json_files(results)
    else:
        print("\n❌ 분석 결과가 없어 JSON 파일을 업데이트하지 않습니다.")
    
    # 7. 완료 메시지
    print(f"\n{'='*80}")
    print(f"✅ 모든 작업 완료!")
    print(f"{'='*80}\n")
    print(f"📅 종료 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 분석 결과:")
    print(f"  - 전체: {len(pdf_files)}개")
    print(f"  - 성공: {success_count}개")
    print(f"  - 실패: {failed_count}개")
    print(f"\n💾 백업 위치: {BACKUP_DIR}")
    print(f"📁 분석 결과: analysis_results/")
    print()


if __name__ == "__main__":
    main()

