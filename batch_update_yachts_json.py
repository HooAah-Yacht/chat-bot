# -*- coding: utf-8 -*-
"""
기존 20종 요트 데이터를 빠르게 JSON 형식으로 업데이트
chatbot_unified.py와 동일한 로직을 사용하되 배치 처리에 최적화
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime
import re

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

def generate_yacht_id(yacht_name: str) -> str:
    """요트 ID 생성 (chatbot_unified.py와 동일)"""
    yacht_id = yacht_name.lower()
    yacht_id = yacht_id.replace("/", "-")
    yacht_id = yacht_id.replace(" ", "-")
    yacht_id = re.sub(r'[^a-z0-9\-\.]', '', yacht_id)
    yacht_id = re.sub(r'-+', '-', yacht_id)
    yacht_id = yacht_id.strip('-')
    return yacht_id


def load_json_file(file_path: Path):
    """JSON 파일 로드"""
    if not file_path.exists():
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json_file(file_path: Path, data: dict):
    """JSON 파일 저장"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def ensure_yacht_id_in_data(yacht: dict) -> dict:
    """요트 데이터에 ID 추가/검증"""
    yacht_name = yacht.get('name', '')
    
    if not yacht_name:
        return yacht
    
    # ID가 없거나 잘못된 경우 생성
    expected_id = generate_yacht_id(yacht_name)
    
    if 'id' not in yacht or yacht['id'] != expected_id:
        yacht['id'] = expected_id
    
    # ID를 최상위로 이동
    if list(yacht.keys())[0] != 'id':
        temp = {'id': yacht['id']}
        temp.update({k: v for k, v in yacht.items() if k != 'id'})
        yacht.clear()
        yacht.update(temp)
    
    return yacht


def update_yacht_specifications():
    """yacht_specifications.json 업데이트"""
    print("\n" + "="*80)
    print("📋 1. yacht_specifications.json 업데이트 시작...")
    print("="*80)
    
    file_path = Path('data/yacht_specifications.json')
    
    if not file_path.exists():
        print(f"❌ {file_path} 파일을 찾을 수 없습니다.")
        return 0
    
    data = load_json_file(file_path)
    yachts = data.get('yachts', [])
    
    updated_count = 0
    yacht_id_map = {}
    
    for yacht in yachts:
        yacht_name = yacht.get('name', '')
        original_id = yacht.get('id', '')
        
        yacht = ensure_yacht_id_in_data(yacht)
        
        if yacht.get('id') != original_id:
            updated_count += 1
        
        yacht_id_map[yacht_name] = yacht['id']
    
    data['yachts'] = yachts
    data['lastUpdated'] = datetime.now().strftime("%Y-%m-%d")
    
    save_json_file(file_path, data)
    
    print(f"✅ 완료: {len(yachts)}개 요트, {updated_count}개 ID 업데이트")
    
    return yacht_id_map


def update_yacht_parts_database(yacht_id_map: dict):
    """yacht_parts_database.json 업데이트"""
    print("\n" + "="*80)
    print("📋 2. yacht_parts_database.json 업데이트 시작...")
    print("="*80)
    
    file_path = Path('data/yacht_parts_database.json')
    
    if not file_path.exists():
        print(f"❌ {file_path} 파일을 찾을 수 없습니다.")
        return
    
    data = load_json_file(file_path)
    yachts = data.get('yachts', [])
    
    updated_count = 0
    
    for yacht in yachts:
        yacht_name = yacht.get('name', '')
        
        if yacht_name in yacht_id_map:
            correct_id = yacht_id_map[yacht_name]
            
            if yacht.get('id') != correct_id:
                yacht['id'] = correct_id
                updated_count += 1
            
            # ID를 최상위로 이동
            if list(yacht.keys())[0] != 'id':
                temp = {'id': yacht['id']}
                temp.update({k: v for k, v in yacht.items() if k != 'id'})
                yacht.clear()
                yacht.update(temp)
    
    data['yachts'] = yachts
    data['lastUpdated'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    
    save_json_file(file_path, data)
    
    print(f"✅ 완료: {len(yachts)}개 요트, {updated_count}개 ID 업데이트")


def update_yacht_parts_app_data(yacht_id_map: dict):
    """yacht_parts_app_data.json 업데이트"""
    print("\n" + "="*80)
    print("📋 3. yacht_parts_app_data.json 업데이트 시작...")
    print("="*80)
    
    file_path = Path('data/yacht_parts_app_data.json')
    
    if not file_path.exists():
        print(f"❌ {file_path} 파일을 찾을 수 없습니다.")
        return
    
    data = load_json_file(file_path)
    yachts = data.get('yachts', [])
    
    updated_count = 0
    
    for yacht in yachts:
        yacht_name = yacht.get('name', '')
        
        if yacht_name in yacht_id_map:
            correct_id = yacht_id_map[yacht_name]
            
            if yacht.get('id') != correct_id:
                yacht['id'] = correct_id
                updated_count += 1
            
            # ID를 최상위로 이동
            if list(yacht.keys())[0] != 'id':
                temp = {'id': yacht['id']}
                temp.update({k: v for k, v in yacht.items() if k != 'id'})
                yacht.clear()
                yacht.update(temp)
    
    data['yachts'] = yachts
    data['lastUpdated'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    
    save_json_file(file_path, data)
    
    print(f"✅ 완료: {len(yachts)}개 요트, {updated_count}개 ID 업데이트")


def update_extracted_yacht_parts(yacht_id_map: dict):
    """extracted_yacht_parts.json 업데이트"""
    print("\n" + "="*80)
    print("📋 4. extracted_yacht_parts.json 업데이트 시작...")
    print("="*80)
    
    file_path = Path('data/extracted_yacht_parts.json')
    
    if not file_path.exists():
        print(f"⚠️ {file_path} 파일을 찾을 수 없습니다. 건너뜁니다.")
        return
    
    data = load_json_file(file_path)
    
    # 데이터 구조 확인
    if isinstance(data, list):
        yachts = data
    elif isinstance(data, dict) and 'yachts' in data:
        yachts = data.get('yachts', [])
    else:
        print(f"⚠️ 알 수 없는 데이터 구조입니다.")
        return
    
    updated_count = 0
    
    for yacht in yachts:
        if not isinstance(yacht, dict):
            continue
        
        yacht_name = yacht.get('name', '')
        
        if yacht_name in yacht_id_map:
            correct_id = yacht_id_map[yacht_name]
            
            if yacht.get('id') != correct_id:
                yacht['id'] = correct_id
                updated_count += 1
            
            # ID를 최상위로 이동
            if list(yacht.keys())[0] != 'id':
                temp = {'id': yacht['id']}
                temp.update({k: v for k, v in yacht.items() if k != 'id'})
                yacht.clear()
                yacht.update(temp)
    
    # 데이터 구조 복원
    if isinstance(data, dict):
        data['yachts'] = yachts
        final_data = data
    else:
        final_data = {"yachts": yachts}
    
    save_json_file(file_path, final_data)
    
    print(f"✅ 완료: {len(yachts)}개 요트, {updated_count}개 ID 업데이트")


def update_extracted_yacht_parts_detailed(yacht_id_map: dict):
    """extracted_yacht_parts_detailed.json 업데이트"""
    print("\n" + "="*80)
    print("📋 5. extracted_yacht_parts_detailed.json 업데이트 시작...")
    print("="*80)
    
    file_path = Path('data/extracted_yacht_parts_detailed.json')
    
    if not file_path.exists():
        print(f"⚠️ {file_path} 파일을 찾을 수 없습니다. 건너뜁니다.")
        return
    
    data = load_json_file(file_path)
    
    # 데이터 구조 확인
    if isinstance(data, list):
        yachts = data
    elif isinstance(data, dict) and 'yachts' in data:
        yachts = data.get('yachts', [])
    else:
        print(f"⚠️ 알 수 없는 데이터 구조입니다.")
        return
    
    updated_count = 0
    
    for yacht in yachts:
        if not isinstance(yacht, dict):
            continue
        
        yacht_name = yacht.get('name', '')
        
        if yacht_name in yacht_id_map:
            correct_id = yacht_id_map[yacht_name]
            
            if yacht.get('id') != correct_id:
                yacht['id'] = correct_id
                updated_count += 1
            
            # ID를 최상위로 이동
            if list(yacht.keys())[0] != 'id':
                temp = {'id': yacht['id']}
                temp.update({k: v for k, v in yacht.items() if k != 'id'})
                yacht.clear()
                yacht.update(temp)
    
    # 데이터 구조 복원
    if isinstance(data, dict):
        data['yachts'] = yachts
        final_data = data
    else:
        final_data = {"yachts": yachts}
    
    save_json_file(file_path, final_data)
    
    print(f"✅ 완료: {len(yachts)}개 요트, {updated_count}개 ID 업데이트")


def update_registered_yachts(yacht_id_map: dict):
    """registered_yachts.json 업데이트"""
    print("\n" + "="*80)
    print("📋 6. registered_yachts.json 업데이트 시작...")
    print("="*80)
    
    file_path = Path('data/registered_yachts.json')
    
    if not file_path.exists():
        print(f"⚠️ {file_path} 파일을 찾을 수 없습니다. 건너뜁니다.")
        return
    
    data = load_json_file(file_path)
    yachts = data.get('yachts', [])
    
    if not yachts:
        print(f"✅ 완료: 등록된 요트 없음 (사용자가 등록 시 자동 생성됨)")
        return
    
    updated_count = 0
    
    for yacht_entry in yachts:
        # registered_yachts.json의 구조: { registrationData: { basicInfo: { name: ... } } }
        registration_data = yacht_entry.get('registrationData', {})
        basic_info = registration_data.get('basicInfo', {})
        yacht_name = basic_info.get('name', '')
        
        if not yacht_name:
            continue
        
        # ID 생성
        yacht_id = generate_yacht_id(yacht_name)
        
        # yacht_entry에 id 추가 (최상위)
        if yacht_entry.get('id') != yacht_id:
            yacht_entry['id'] = yacht_id
            updated_count += 1
        
        # registrationData에도 id 추가
        if registration_data.get('id') != yacht_id:
            registration_data['id'] = yacht_id
        
        # basicInfo에도 id 추가
        if basic_info.get('id') != yacht_id:
            basic_info['id'] = yacht_id
        
        # ID를 최상위로 이동
        if list(yacht_entry.keys())[0] != 'id':
            temp = {'id': yacht_entry['id']}
            temp.update({k: v for k, v in yacht_entry.items() if k != 'id'})
            yacht_entry.clear()
            yacht_entry.update(temp)
    
    data['yachts'] = yachts
    
    save_json_file(file_path, data)
    
    print(f"✅ 완료: {len(yachts)}개 등록된 요트, {updated_count}개 ID 업데이트")


def update_yacht_manual_resources(yacht_id_map: dict):
    """yacht_manual_resources.json 업데이트"""
    print("\n" + "="*80)
    print("📋 7. yacht_manual_resources.json 업데이트 시작...")
    print("="*80)
    
    file_path = Path('data/yacht_manual_resources.json')
    
    data = load_json_file(file_path)
    
    if not data:
        print(f"⚠️ {file_path} 파일을 찾을 수 없습니다. 새로 생성합니다.")
        data = {
            "schemaVersion": "5.0",
            "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
            "description": "요트 매뉴얼 다운로드 링크 및 리소스",
            "totalResources": 0,
            "resources": [],
            "yachts": []
        }
    
    # resources 섹션은 그대로 유지
    resources = data.get('resources', [])
    
    # yachts 섹션 업데이트
    yachts_section = data.get('yachts', [])
    
    # 기존 요트 업데이트
    existing_yacht_names = {y.get('name', '') for y in yachts_section}
    updated_count = 0
    
    for yacht in yachts_section:
        yacht_name = yacht.get('name', '')
        
        if yacht_name in yacht_id_map:
            correct_id = yacht_id_map[yacht_name]
            
            if yacht.get('id') != correct_id:
                yacht['id'] = correct_id
                updated_count += 1
            
            # ID를 최상위로 이동
            if list(yacht.keys())[0] != 'id':
                temp = {'id': yacht['id']}
                temp.update({k: v for k, v in yacht.items() if k != 'id'})
                yacht.clear()
                yacht.update(temp)
    
    # 누락된 요트 추가
    added_count = 0
    for yacht_name, yacht_id in yacht_id_map.items():
        if yacht_name not in existing_yacht_names:
            # resources에서 정보 찾기
            resource_info = next(
                (r for r in resources if r.get('yachtModel', '') == yacht_name),
                {}
            )
            
            new_entry = {
                "id": yacht_id,
                "name": yacht_name,
                "manufacturer": resource_info.get('manufacturer', ''),
                "manualPDF": resource_info.get('manualPDF', ''),
                "officialWebsite": "",
                "downloadLinks": []
            }
            yachts_section.append(new_entry)
            added_count += 1
    
    data['yachts'] = yachts_section
    data['lastUpdated'] = datetime.now().strftime("%Y-%m-%d")
    data['totalResources'] = len(resources)
    
    save_json_file(file_path, data)
    
    print(f"✅ 완료: {len(yachts_section)}개 요트")
    print(f"   - {updated_count}개 ID 업데이트")
    print(f"   - {added_count}개 신규 추가")


def verify_updates(yacht_id_map: dict):
    """업데이트 검증"""
    print("\n" + "="*80)
    print("🔍 업데이트 검증 중...")
    print("="*80)
    
    files_to_check = [
        'data/yacht_specifications.json',
        'data/yacht_parts_database.json',
        'data/yacht_parts_app_data.json',
        'data/extracted_yacht_parts_detailed.json',
        'data/registered_yachts.json',
        'data/yacht_manual_resources.json',
    ]
    
    all_good = True
    
    for file_path_str in files_to_check:
        file_path = Path(file_path_str)
        
        if not file_path.exists():
            print(f"⚠️ {file_path_str}: 파일 없음")
            continue
        
        data = load_json_file(file_path)
        yachts = data.get('yachts', [])
        
        missing_ids = []
        wrong_ids = []
        
        for yacht in yachts:
            yacht_name = yacht.get('name', '')
            yacht_id = yacht.get('id', '')
            
            if not yacht_id:
                missing_ids.append(yacht_name)
            elif yacht_name in yacht_id_map and yacht_id != yacht_id_map[yacht_name]:
                wrong_ids.append(f"{yacht_name} (예상: {yacht_id_map[yacht_name]}, 실제: {yacht_id})")
        
        if missing_ids or wrong_ids:
            all_good = False
            print(f"❌ {file_path_str}:")
            if missing_ids:
                print(f"   - ID 없음: {missing_ids}")
            if wrong_ids:
                print(f"   - ID 불일치: {wrong_ids}")
        else:
            print(f"✅ {file_path_str}: 모든 ID 정상 ({len(yachts)}개)")
    
    return all_good


def print_summary(yacht_id_map: dict):
    """요약 출력"""
    print("\n" + "="*80)
    print("📊 업데이트 완료 요약")
    print("="*80)
    
    print(f"\n✅ 총 {len(yacht_id_map)}개 요트 처리")
    print("\n업데이트된 파일:")
    print("  1. ✅ yacht_specifications.json")
    print("  2. ✅ yacht_parts_database.json")
    print("  3. ✅ yacht_parts_app_data.json")
    print("  4. ✅ extracted_yacht_parts.json")
    print("  5. ✅ extracted_yacht_parts_detailed.json")
    print("  6. ✅ registered_yachts.json")
    print("  7. ✅ yacht_manual_resources.json")
    
    print("\n생성된 요트 ID 목록:")
    print("-" * 80)
    
    for i, (yacht_name, yacht_id) in enumerate(sorted(yacht_id_map.items()), 1):
        print(f"{i:2d}. {yacht_name:40s} → {yacht_id}")
    
    print("\n" + "="*80)
    print("🎉 모든 작업이 완료되었습니다!")
    print("="*80)


def main():
    """메인 실행 함수"""
    print("\n")
    print("="*80)
    print("🚀 기존 20종 요트 JSON 업데이트 시작")
    print("="*80)
    print("\n이 스크립트는 다음 파일들을 업데이트합니다:")
    print("  - yacht_specifications.json")
    print("  - yacht_parts_database.json")
    print("  - yacht_parts_app_data.json")
    print("  - extracted_yacht_parts.json")
    print("  - extracted_yacht_parts_detailed.json")
    print("  - registered_yachts.json")
    print("  - yacht_manual_resources.json")
    print("\n모든 요트에 일관된 ID가 추가됩니다.")
    print("="*80)
    
    try:
        # 1. yacht_specifications.json 업데이트 및 ID 맵 생성
        yacht_id_map = update_yacht_specifications()
        
        if not yacht_id_map:
            print("\n❌ yacht_specifications.json 처리 실패. 종료합니다.")
            return
        
        # 2. 나머지 파일들 업데이트
        update_yacht_parts_database(yacht_id_map)
        update_yacht_parts_app_data(yacht_id_map)
        update_extracted_yacht_parts(yacht_id_map)
        update_extracted_yacht_parts_detailed(yacht_id_map)
        update_registered_yachts(yacht_id_map)
        update_yacht_manual_resources(yacht_id_map)
        
        # 3. 검증
        if verify_updates(yacht_id_map):
            print("\n✅ 모든 파일이 정상적으로 업데이트되었습니다!")
        else:
            print("\n⚠️ 일부 파일에 문제가 있습니다. 위 메시지를 확인해주세요.")
        
        # 4. 요약
        print_summary(yacht_id_map)
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

