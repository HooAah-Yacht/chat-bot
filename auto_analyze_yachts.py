#!/usr/bin/env python3
"""
요트 매뉴얼 자동 분석 스크립트 (빠른 버전)
- chatbot_unified.py 기반
- 사용자 입력 없이 자동 실행
- 20개 요트 매뉴얼 일괄 분석
- JSON 파일 자동 업데이트
"""

import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path

# chatbot_unified 임포트
from chatbot_unified import UnifiedYachtChatbot

# ============================================================================
# 설정
# ============================================================================

# 제외할 파일 (요트 매뉴얼이 아닌 문서)
EXCLUDED_FILES = [
    "11월11일 멘토링.pdf",
    "11월17일 멘토링.pdf",
    "정비 관련 자료.pdf",
    "풀리퀘스트1.pdf",
    "풀리퀘스트3.pdf",
    "후아_디자인 (1).pdf"
]

PDF_DIR = "data/yachtpdf"
API_KEY = "AIzaSyBhPZDNBTEqYu8ahBIVpK2B1h_CAKgo7JI"

# ============================================================================
# 메인 함수
# ============================================================================

def main():
    """메인 실행"""
    start_time = datetime.now()
    
    print("\n" + "="*80)
    print("🚀 요트 매뉴얼 자동 분석 시작 (빠른 버전)")
    print("="*80)
    print(f"📅 {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # 1. 백업
    backup_dir = f"data/backup_{start_time.strftime('%Y%m%d_%H%M%S')}"
    backup_json_files(backup_dir)
    
    # 2. PDF 목록 가져오기
    pdf_files = get_pdf_files()
    
    if not pdf_files:
        print("❌ 분석할 PDF가 없습니다.")
        return
    
    print(f"\n▶️ {len(pdf_files)}개 PDF 자동 분석 시작!\n")
    
    # 3. Chatbot 초기화
    print("🤖 AI 초기화 중...")
    chatbot = UnifiedYachtChatbot(api_key=API_KEY)
    print("✅ 준비 완료!\n")
    
    # 4. 분석 실행
    results = []
    success = 0
    failed = 0
    
    for i, pdf_file in enumerate(pdf_files, 1):
        pdf_path = os.path.join(PDF_DIR, pdf_file)
        
        print(f"{'='*80}")
        print(f"[{i}/{len(pdf_files)}] 📄 {pdf_file}")
        print(f"{'='*80}")
        
        try:
            # 텍스트 추출
            print("📖 텍스트 추출...", end=" ", flush=True)
            text = chatbot._extract_text_from_pdf(pdf_path)
            
            if not text or len(text.strip()) < 100:
                print(f"❌ 실패 (텍스트: {len(text)}자)")
                failed += 1
                continue
            
            print(f"✅ ({len(text)}자)")
            
            # AI 분석
            print("🤖 AI 분석...", end=" ", flush=True)
            result = chatbot._analyze_document_directly(pdf_path, text)
            
            if "error" in result:
                print(f"❌ 실패: {result.get('error')}")
                failed += 1
                continue
            
            # ID 개수 세기
            id_count = count_ids(result)
            print(f"✅ (ID: {id_count}개)")
            
            results.append(result)
            success += 1
            
            # 진행률
            print(f"진행률: {i}/{len(pdf_files)} (성공: {success}, 실패: {failed})\n")
            
        except Exception as e:
            print(f"❌ 오류: {e}\n")
            failed += 1
    
    # 5. JSON 업데이트
    if results:
        print(f"\n{'='*80}")
        print("💾 JSON 파일 업데이트 중...")
        print(f"{'='*80}\n")
        
        update_all_json_files(results)
        
        print("\n✅ 모든 JSON 업데이트 완료!")
    else:
        print("\n❌ 분석 결과가 없습니다.")
    
    # 6. 완료
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"\n{'='*80}")
    print("✅ 작업 완료!")
    print(f"{'='*80}")
    print(f"⏱️ 소요 시간: {duration:.1f}초 ({duration/60:.1f}분)")
    print(f"📊 성공: {success}개 / 실패: {failed}개 / 전체: {len(pdf_files)}개")
    print(f"💾 백업: {backup_dir}")
    print(f"📅 {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")


# ============================================================================
# 보조 함수
# ============================================================================

def backup_json_files(backup_dir):
    """JSON 파일 백업"""
    print(f"💾 백업 중... → {backup_dir}")
    os.makedirs(backup_dir, exist_ok=True)
    
    files = [
        "data/yacht_specifications.json",
        "data/yacht_parts_database.json",
        "data/yacht_manual_resources.json",
        "data/registered_yachts.json",
        "data/yacht_parts_app_data.json"
    ]
    
    for f in files:
        if os.path.exists(f):
            shutil.copy2(f, os.path.join(backup_dir, os.path.basename(f)))
    
    print("✅ 백업 완료\n")


def get_pdf_files():
    """분석할 PDF 목록"""
    if not os.path.exists(PDF_DIR):
        return []
    
    all_pdfs = [f for f in os.listdir(PDF_DIR) if f.endswith('.pdf')]
    yacht_pdfs = [f for f in all_pdfs if f not in EXCLUDED_FILES]
    
    print(f"📂 PDF 파일")
    print(f"  전체: {len(all_pdfs)}개")
    print(f"  제외: {len(EXCLUDED_FILES)}개")
    print(f"  ✅ 분석: {len(yacht_pdfs)}개")
    
    return yacht_pdfs


def count_ids(obj, count=0):
    """ID 개수 세기"""
    if isinstance(obj, dict):
        if "id" in obj:
            count += 1
        for v in obj.values():
            count = count_ids(v, count)
    elif isinstance(obj, list):
        for item in obj:
            count = count_ids(item, count)
    return count


def update_all_json_files(results):
    """모든 JSON 파일 업데이트"""
    
    # 1. yacht_specifications.json
    print("📋 yacht_specifications.json...", end=" ", flush=True)
    yachts_specs = []
    
    for result in results:
        if result.get('analysisResult', {}).get('canAnalyze') != True:
            continue
        
        doc = result.get('documentInfo', {})
        model = doc.get('yachtModel')
        
        if not model:
            continue
        
        yacht_id = model.lower().replace(' ', '-').replace('/', '-').replace('_', '-')
        
        yacht = {
            "id": yacht_id,
            "name": model,
            "manufacturer": doc.get('manufacturer'),
            "type": doc.get('documentType', ''),
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
        
        yachts_specs.append(yacht)
    
    with open("data/yacht_specifications.json", 'w', encoding='utf-8') as f:
        json.dump({
            "schemaVersion": "5.0",
            "lastUpdated": datetime.now().isoformat(),
            "totalYachts": len(yachts_specs),
            "yachts": yachts_specs
        }, f, ensure_ascii=False, indent=2)
    
    print(f"✅ ({len(yachts_specs)}척)")
    
    # 2. yacht_parts_database.json
    print("📦 yacht_parts_database.json...", end=" ", flush=True)
    yachts_parts = []
    
    for result in results:
        if result.get('analysisResult', {}).get('canAnalyze') != True:
            continue
        
        doc = result.get('documentInfo', {})
        model = doc.get('yachtModel')
        parts = result.get('parts', [])
        
        if not model:
            continue
        
        yacht_id = model.lower().replace(' ', '-').replace('/', '-').replace('_', '-')
        
        yacht = {
            "id": yacht_id,
            "name": model,
            "manufacturer": doc.get('manufacturer'),
            "manualPDF": result.get('fileInfo', {}).get('fileName', ''),
            "schemaVersion": "5.0",
            "totalParts": len(parts),
            "parts": parts
        }
        
        yachts_parts.append(yacht)
    
    with open("data/yacht_parts_database.json", 'w', encoding='utf-8') as f:
        json.dump({
            "schemaVersion": "5.0",
            "lastUpdated": datetime.now().isoformat(),
            "totalYachts": len(yachts_parts),
            "yachts": yachts_parts
        }, f, ensure_ascii=False, indent=2)
    
    total_parts = sum(y.get('totalParts', 0) for y in yachts_parts)
    print(f"✅ ({len(yachts_parts)}척, {total_parts}개 부품)")
    
    # 3. yacht_manual_resources.json
    print("📚 yacht_manual_resources.json...", end=" ", flush=True)
    resources = []
    
    for result in results:
        doc = result.get('documentInfo', {})
        model = doc.get('yachtModel')
        
        if not model:
            continue
        
        resource = {
            "yachtModel": model,
            "manufacturer": doc.get('manufacturer'),
            "manualPDF": result.get('fileInfo', {}).get('fileName', ''),
            "documentType": doc.get('documentType'),
            "canAnalyze": result.get('analysisResult', {}).get('canAnalyze', False),
            "schemaVersion": "5.0",
            "updatedAt": datetime.now().isoformat()
        }
        
        resources.append(resource)
    
    with open("data/yacht_manual_resources.json", 'w', encoding='utf-8') as f:
        json.dump({
            "schemaVersion": "5.0",
            "lastUpdated": datetime.now().isoformat(),
            "totalResources": len(resources),
            "resources": resources
        }, f, ensure_ascii=False, indent=2)
    
    print(f"✅ ({len(resources)}개)")
    
    # 4. yacht_parts_app_data.json
    print("📱 yacht_parts_app_data.json...", end=" ", flush=True)
    app_yachts = []
    
    for result in results:
        if result.get('analysisResult', {}).get('canAnalyze') != True:
            continue
        
        doc = result.get('documentInfo', {})
        model = doc.get('yachtModel')
        parts = result.get('parts', [])
        
        if not model or not parts:
            continue
        
        yacht_id = model.lower().replace(' ', '-').replace('/', '-').replace('_', '-')
        
        # 앱용 간단한 부품 정보
        simple_parts = []
        for part in parts:
            simple_parts.append({
                "id": part.get('id', ''),
                "name": part.get('name', ''),
                "category": part.get('category', ''),
                "manufacturer": part.get('manufacturer', ''),
                "interval": part.get('interval', 12)
            })
        
        app_yachts.append({
            "id": yacht_id,
            "name": model,
            "manufacturer": doc.get('manufacturer'),
            "parts": simple_parts
        })
    
    with open("data/yacht_parts_app_data.json", 'w', encoding='utf-8') as f:
        json.dump({
            "schemaVersion": "5.0",
            "lastUpdated": datetime.now().isoformat(),
            "totalYachts": len(app_yachts),
            "yachts": app_yachts
        }, f, ensure_ascii=False, indent=2)
    
    print(f"✅ ({len(app_yachts)}척)")
    
    # 5. registered_yachts.json (초기화)
    print("🔄 registered_yachts.json...", end=" ", flush=True)
    with open("data/registered_yachts.json", 'w', encoding='utf-8') as f:
        json.dump({
            "schemaVersion": "5.0",
            "lastUpdated": datetime.now().isoformat(),
            "description": "사용자가 등록한 요트 목록 (chatbot_unified.py로 등록)",
            "totalYachts": 0,
            "yachts": []
        }, f, ensure_ascii=False, indent=2)
    
    print("✅ (초기화)")


# ============================================================================
# 실행
# ============================================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ 사용자가 중단했습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

