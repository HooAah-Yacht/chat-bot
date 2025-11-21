#!/usr/bin/env python3
"""
JSON 파일 업데이트 스크립트
- 기존 JSON 파일 백업
- 새로운 Schema 5.0 데이터로 업데이트
"""

import os
import json
import shutil
from datetime import datetime
from glob import glob

# 백업 디렉토리
BACKUP_DIR = "data/backup_" + datetime.now().strftime("%Y%m%d_%H%M%S")

# 업데이트할 JSON 파일들
JSON_FILES = [
    "data/registered_yachts.json",
    "data/yacht_manual_resources.json",
    "data/yacht_parts_app_data.json",
    "data/yacht_parts_database.json",
    "data/yacht_specifications.json"
]

def backup_json_files():
    """기존 JSON 파일 백업"""
    print(f"\n{'='*80}")
    print(f"💾 JSON 파일 백업 시작")
    print(f"📁 백업 디렉토리: {BACKUP_DIR}")
    print(f"{'='*80}\n")
    
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    for json_file in JSON_FILES:
        if os.path.exists(json_file):
            backup_path = os.path.join(BACKUP_DIR, os.path.basename(json_file))
            shutil.copy2(json_file, backup_path)
            print(f"✅ 백업: {json_file} → {backup_path}")
        else:
            print(f"⚠️ 파일 없음: {json_file}")
    
    print(f"\n✅ 백업 완료!\n")


def load_analysis_results():
    """분석 결과 파일 로드"""
    print(f"\n{'='*80}")
    print(f"📂 분석 결과 로드")
    print(f"{'='*80}\n")
    
    # 가장 최근 분석 결과 찾기
    result_files = glob("test_all_results_*.json")
    if not result_files:
        print("❌ 분석 결과 파일을 찾을 수 없습니다.")
        print("   먼저 'python test_new_schema.py --all'을 실행하세요.")
        return None
    
    latest_file = max(result_files, key=os.path.getmtime)
    print(f"📄 최신 결과 파일: {latest_file}")
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ {data['totalFiles']}개 파일 분석 결과 로드 완료")
    print(f"   성공: {data['successCount']}개")
    
    return data


def update_yacht_specifications(analysis_data):
    """yacht_specifications.json 업데이트"""
    print(f"\n{'='*80}")
    print(f"📝 yacht_specifications.json 업데이트")
    print(f"{'='*80}\n")
    
    yachts = []
    
    for item in analysis_data['results']:
        result = item['result']
        
        # 요트 매뉴얼인지 확인
        if result.get('analysisResult', {}).get('canAnalyze') != True:
            continue
        
        doc_info = result.get('documentInfo', {})
        yacht_model = doc_info.get('yachtModel')
        
        if not yacht_model:
            continue
        
        # ID 생성 (모델명에서)
        yacht_id = yacht_model.lower().replace(' ', '-').replace('/', '-')
        
        yacht_data = {
            "id": yacht_id,
            "name": yacht_model,
            "manufacturer": doc_info.get('manufacturer'),
            "schemaVersion": "5.0",
            "updatedAt": datetime.now().isoformat(),
            "specifications": result.get('yachtSpecs', {}),
            "detailedDimensions": result.get('detailedDimensions', {}),
            "exterior": result.get('exterior', {}),
            "groundTackle": result.get('groundTackle', {}),
            "sailInventory": result.get('sailInventory', []),
            "deckEquipment": result.get('deckEquipment', {}),
            "accommodations": result.get('accommodations', {}),
            "tanks": result.get('tanks', {}),
            "electricalSystem": result.get('electricalSystem', {}),
            "electronics": result.get('electronics', {}),
            "plumbingSystem": result.get('plumbingSystem', {}),
            "manualPDF": item['fileName']
        }
        
        yachts.append(yacht_data)
        print(f"✅ {yacht_model}")
    
    # 저장
    output = {
        "schemaVersion": "5.0",
        "lastUpdated": datetime.now().isoformat(),
        "totalYachts": len(yachts),
        "yachts": yachts
    }
    
    with open("data/yacht_specifications.json", 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ yacht_specifications.json 업데이트 완료 ({len(yachts)}척)")


def update_yacht_parts_database(analysis_data):
    """yacht_parts_database.json 업데이트"""
    print(f"\n{'='*80}")
    print(f"📝 yacht_parts_database.json 업데이트")
    print(f"{'='*80}\n")
    
    yachts = []
    
    for item in analysis_data['results']:
        result = item['result']
        
        if result.get('analysisResult', {}).get('canAnalyze') != True:
            continue
        
        doc_info = result.get('documentInfo', {})
        yacht_model = doc_info.get('yachtModel')
        
        if not yacht_model or not result.get('parts'):
            continue
        
        yacht_id = yacht_model.lower().replace(' ', '-').replace('/', '-')
        
        yacht_data = {
            "id": yacht_id,
            "name": yacht_model,
            "manufacturer": doc_info.get('manufacturer'),
            "manualPDF": item['fileName'],
            "schemaVersion": "5.0",
            "parts": result.get('parts', [])
        }
        
        yachts.append(yacht_data)
        print(f"✅ {yacht_model}: {len(result.get('parts', []))}개 부품")
    
    # 저장
    output = {
        "schemaVersion": "5.0",
        "lastUpdated": datetime.now().isoformat(),
        "totalYachts": len(yachts),
        "yachts": yachts
    }
    
    with open("data/yacht_parts_database.json", 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ yacht_parts_database.json 업데이트 완료 ({len(yachts)}척)")


def update_yacht_manual_resources(analysis_data):
    """yacht_manual_resources.json 업데이트"""
    print(f"\n{'='*80}")
    print(f"📝 yacht_manual_resources.json 업데이트")
    print(f"{'='*80}\n")
    
    resources = []
    
    for item in analysis_data['results']:
        result = item['result']
        doc_info = result.get('documentInfo', {})
        yacht_model = doc_info.get('yachtModel')
        
        if not yacht_model:
            continue
        
        resource = {
            "yachtModel": yacht_model,
            "manufacturer": doc_info.get('manufacturer'),
            "manualPDF": item['fileName'],
            "documentType": doc_info.get('documentType'),
            "canAnalyze": result.get('analysisResult', {}).get('canAnalyze', False),
            "updatedAt": datetime.now().isoformat()
        }
        
        resources.append(resource)
        print(f"✅ {yacht_model}: {item['fileName']}")
    
    # 저장
    output = {
        "schemaVersion": "5.0",
        "lastUpdated": datetime.now().isoformat(),
        "totalResources": len(resources),
        "resources": resources
    }
    
    with open("data/yacht_manual_resources.json", 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ yacht_manual_resources.json 업데이트 완료 ({len(resources)}개)")


def update_registered_yachts():
    """registered_yachts.json 초기화 (기존 등록 데이터 유지하되 스키마만 업데이트)"""
    print(f"\n{'='*80}")
    print(f"📝 registered_yachts.json 스키마 업데이트")
    print(f"{'='*80}\n")
    
    # 기존 파일 로드
    if os.path.exists("data/registered_yachts.json"):
        with open("data/registered_yachts.json", 'r', encoding='utf-8') as f:
            old_data = json.load(f)
        
        # 기존 등록된 요트 목록
        existing_yachts = old_data.get('yachts', []) if isinstance(old_data, dict) else old_data
        print(f"📊 기존 등록 요트: {len(existing_yachts)}척")
    else:
        existing_yachts = []
    
    # 새로운 형식으로 저장
    output = {
        "schemaVersion": "5.0",
        "lastUpdated": datetime.now().isoformat(),
        "totalYachts": len(existing_yachts),
        "yachts": existing_yachts
    }
    
    with open("data/registered_yachts.json", 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ registered_yachts.json 스키마 업데이트 완료")


def main():
    """메인 실행 함수"""
    print(f"\n{'='*80}")
    print(f"🚀 JSON 파일 업데이트 시작")
    print(f"{'='*80}\n")
    
    # 1. 백업
    backup_json_files()
    
    # 2. 분석 결과 로드
    analysis_data = load_analysis_results()
    
    if not analysis_data:
        print("❌ 분석 결과가 없어 업데이트를 중단합니다.")
        return
    
    # 3. JSON 파일 업데이트
    try:
        update_yacht_specifications(analysis_data)
        update_yacht_parts_database(analysis_data)
        update_yacht_manual_resources(analysis_data)
        update_registered_yachts()
        
        print(f"\n{'='*80}")
        print(f"✅ 모든 JSON 파일 업데이트 완료!")
        print(f"{'='*80}\n")
        print(f"📁 백업 위치: {BACKUP_DIR}")
        print(f"📋 업데이트된 파일:")
        for json_file in JSON_FILES:
            print(f"   - {json_file}")
        print()
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        print(f"\n💾 백업에서 복원하려면:")
        print(f"   cp {BACKUP_DIR}/* data/")


if __name__ == "__main__":
    main()

