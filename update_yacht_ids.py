# -*- coding: utf-8 -*-
"""
기존 20종 요트 데이터를 JSON 형식으로 추출하고 5개 파일 업데이트
"""

import sys
import json
from pathlib import Path
from datetime import datetime

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

def generate_yacht_id(yacht_name: str) -> str:
    """요트 ID 생성"""
    import re
    yacht_id = yacht_name.lower()
    yacht_id = yacht_id.replace("/", "-")
    yacht_id = yacht_id.replace(" ", "-")
    yacht_id = re.sub(r'[^a-z0-9\-\.]', '', yacht_id)
    yacht_id = re.sub(r'-+', '-', yacht_id)
    yacht_id = yacht_id.strip('-')
    return yacht_id


def update_all_json_files():
    """5개 JSON 파일 모두 업데이트"""
    
    print("\n" + "="*80)
    print("🔄 기존 20종 요트 데이터 업데이트 시작")
    print("="*80)
    
    # 1. yacht_specifications.json 로드
    spec_file = Path('data/yacht_specifications.json')
    if not spec_file.exists():
        print(f"❌ {spec_file} 파일을 찾을 수 없습니다.")
        return
    
    with open(spec_file, 'r', encoding='utf-8') as f:
        spec_data = json.load(f)
    
    yachts = spec_data.get('yachts', [])
    
    if not yachts:
        print("❌ 요트 데이터가 없습니다.")
        return
    
    print(f"\n📊 총 {len(yachts)}개 요트 발견")
    
    # 2. 각 요트에 ID가 있는지 확인하고 없으면 추가
    updated_yachts = []
    yacht_ids_added = []
    
    for yacht in yachts:
        yacht_name = yacht.get('name', '')
        
        # ID가 없으면 생성
        if 'id' not in yacht or not yacht['id']:
            yacht_id = generate_yacht_id(yacht_name)
            yacht['id'] = yacht_id
            yacht_ids_added.append(f"{yacht_name} → {yacht_id}")
        
        # ID를 최상위로 이동
        yacht_with_id = {'id': yacht['id']}
        yacht_with_id.update({k: v for k, v in yacht.items() if k != 'id'})
        updated_yachts.append(yacht_with_id)
    
    if yacht_ids_added:
        print(f"\n🆕 {len(yacht_ids_added)}개 요트에 ID 추가:")
        for item in yacht_ids_added:
            print(f"  - {item}")
    else:
        print("\n✅ 모든 요트에 ID가 이미 존재합니다.")
    
    # 3. yacht_specifications.json 업데이트
    spec_data['yachts'] = updated_yachts
    spec_data['lastUpdated'] = datetime.now().strftime("%Y-%m-%d")
    
    with open(spec_file, 'w', encoding='utf-8') as f:
        json.dump(spec_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ {spec_file} 업데이트 완료")
    
    # 4. yacht_parts_database.json 업데이트
    update_yacht_parts_database(updated_yachts)
    
    # 5. yacht_parts_app_data.json 업데이트
    update_yacht_parts_app_data(updated_yachts)
    
    # 6. extracted_yacht_parts.json 업데이트
    update_extracted_yacht_parts(updated_yachts)
    
    # 7. yacht_manual_resources.json 업데이트
    update_yacht_manual_resources(updated_yachts)
    
    # 8. registered_yachts.json은 사용자 등록 데이터이므로 건드리지 않음
    print("\n📝 registered_yachts.json은 사용자 등록 데이터이므로 업데이트하지 않습니다.")
    
    print("\n" + "="*80)
    print("✅ 모든 JSON 파일 업데이트 완료!")
    print("="*80)
    
    # 요약 출력
    print(f"\n📊 업데이트 요약:")
    print(f"  - 총 요트 수: {len(updated_yachts)}개")
    print(f"  - 업데이트된 파일:")
    print(f"    1. yacht_specifications.json")
    print(f"    2. yacht_parts_database.json")
    print(f"    3. yacht_parts_app_data.json")
    print(f"    4. extracted_yacht_parts.json")
    print(f"    5. yacht_manual_resources.json")


def update_yacht_parts_database(yachts):
    """yacht_parts_database.json 업데이트"""
    
    db_file = Path('data/yacht_parts_database.json')
    
    if not db_file.exists():
        print(f"\n⚠️ {db_file} 파일을 찾을 수 없습니다. 건너뜁니다.")
        return
    
    with open(db_file, 'r', encoding='utf-8') as f:
        db_data = json.load(f)
    
    db_yachts = db_data.get('yachts', [])
    
    # ID 매핑 생성
    yacht_id_map = {yacht['name']: yacht['id'] for yacht in yachts}
    
    updated_count = 0
    for db_yacht in db_yachts:
        yacht_name = db_yacht.get('name', '')
        
        # 이름으로 ID 찾기
        if yacht_name in yacht_id_map:
            correct_id = yacht_id_map[yacht_name]
            
            if db_yacht.get('id') != correct_id:
                db_yacht['id'] = correct_id
                updated_count += 1
            
            # ID를 최상위로 이동
            if list(db_yacht.keys())[0] != 'id':
                temp = {'id': db_yacht['id']}
                temp.update({k: v for k, v in db_yacht.items() if k != 'id'})
                db_yacht.clear()
                db_yacht.update(temp)
    
    db_data['yachts'] = db_yachts
    
    with open(db_file, 'w', encoding='utf-8') as f:
        json.dump(db_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ yacht_parts_database.json 업데이트 완료 ({updated_count}개 ID 수정)")


def update_yacht_parts_app_data(yachts):
    """yacht_parts_app_data.json 업데이트"""
    
    app_file = Path('data/yacht_parts_app_data.json')
    
    if not app_file.exists():
        print(f"\n⚠️ {app_file} 파일을 찾을 수 없습니다. 건너뜁니다.")
        return
    
    with open(app_file, 'r', encoding='utf-8') as f:
        app_data = json.load(f)
    
    app_yachts = app_data.get('yachts', [])
    
    # ID 매핑 생성
    yacht_id_map = {yacht['name']: yacht['id'] for yacht in yachts}
    
    updated_count = 0
    for app_yacht in app_yachts:
        yacht_name = app_yacht.get('name', '')
        
        # 이름으로 ID 찾기
        if yacht_name in yacht_id_map:
            correct_id = yacht_id_map[yacht_name]
            
            if app_yacht.get('id') != correct_id:
                app_yacht['id'] = correct_id
                updated_count += 1
            
            # ID를 최상위로 이동
            if list(app_yacht.keys())[0] != 'id':
                temp = {'id': app_yacht['id']}
                temp.update({k: v for k, v in app_yacht.items() if k != 'id'})
                app_yacht.clear()
                app_yacht.update(temp)
    
    app_data['yachts'] = app_yachts
    
    with open(app_file, 'w', encoding='utf-8') as f:
        json.dump(app_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ yacht_parts_app_data.json 업데이트 완료 ({updated_count}개 ID 수정)")


def update_extracted_yacht_parts(yachts):
    """extracted_yacht_parts.json 업데이트"""
    
    extracted_file = Path('data/extracted_yacht_parts.json')
    
    if not extracted_file.exists():
        print(f"\n⚠️ {extracted_file} 파일을 찾을 수 없습니다. 건너뜁니다.")
        return
    
    with open(extracted_file, 'r', encoding='utf-8') as f:
        extracted_data = json.load(f)
    
    # 데이터 구조 확인 및 정규화
    if isinstance(extracted_data, list):
        extracted_yachts = extracted_data
    elif isinstance(extracted_data, dict) and 'yachts' in extracted_data:
        extracted_yachts = extracted_data.get('yachts', [])
    else:
        print(f"\n⚠️ extracted_yacht_parts.json 구조가 예상과 다릅니다.")
        return
    
    # ID 매핑 생성
    yacht_id_map = {yacht['name']: yacht['id'] for yacht in yachts}
    
    updated_count = 0
    for extracted_yacht in extracted_yachts:
        if not isinstance(extracted_yacht, dict):
            continue
        
        yacht_name = extracted_yacht.get('name', '')
        
        # 이름으로 ID 찾기
        if yacht_name in yacht_id_map:
            correct_id = yacht_id_map[yacht_name]
            
            if extracted_yacht.get('id') != correct_id:
                extracted_yacht['id'] = correct_id
                updated_count += 1
            
            # ID를 최상위로 이동
            if list(extracted_yacht.keys())[0] != 'id':
                temp = {'id': extracted_yacht['id']}
                temp.update({k: v for k, v in extracted_yacht.items() if k != 'id'})
                extracted_yacht.clear()
                extracted_yacht.update(temp)
    
    # 데이터 구조 복원
    if isinstance(extracted_data, dict):
        extracted_data['yachts'] = extracted_yachts
        final_data = extracted_data
    else:
        final_data = {"yachts": extracted_yachts}
    
    with open(extracted_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ extracted_yacht_parts.json 업데이트 완료 ({updated_count}개 ID 수정)")


def update_yacht_manual_resources(yachts):
    """yacht_manual_resources.json 업데이트"""
    
    manual_file = Path('data/yacht_manual_resources.json')
    
    if not manual_file.exists():
        print(f"\n⚠️ {manual_file} 파일을 찾을 수 없습니다. 새로 생성합니다.")
        # 새로 생성
        manual_data = {
            "version": "1.0",
            "description": "요트 매뉴얼 다운로드 링크 및 리소스",
            "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
            "yachts": []
        }
    else:
        with open(manual_file, 'r', encoding='utf-8') as f:
            manual_data = json.load(f)
    
    manual_yachts = manual_data.get('yachts', [])
    
    # ID 매핑 생성
    yacht_id_map = {yacht['name']: yacht['id'] for yacht in yachts}
    
    # 기존 매뉴얼 데이터 업데이트
    existing_yacht_names = {my.get('name', '') for my in manual_yachts}
    
    updated_count = 0
    for manual_yacht in manual_yachts:
        yacht_name = manual_yacht.get('name', '')
        
        # 이름으로 ID 찾기
        if yacht_name in yacht_id_map:
            correct_id = yacht_id_map[yacht_name]
            
            if manual_yacht.get('id') != correct_id:
                manual_yacht['id'] = correct_id
                updated_count += 1
            
            # ID를 최상위로 이동
            if list(manual_yacht.keys())[0] != 'id':
                temp = {'id': manual_yacht['id']}
                temp.update({k: v for k, v in manual_yacht.items() if k != 'id'})
                manual_yacht.clear()
                manual_yacht.update(temp)
    
    # 누락된 요트 추가
    added_count = 0
    for yacht in yachts:
        yacht_name = yacht['name']
        if yacht_name not in existing_yacht_names:
            new_entry = {
                "id": yacht['id'],
                "name": yacht_name,
                "manufacturer": yacht.get('manufacturer', ''),
                "manualPDF": yacht.get('manual', ''),
                "officialWebsite": yacht.get('officialWebsite', ''),
                "downloadLinks": []
            }
            manual_yachts.append(new_entry)
            added_count += 1
    
    manual_data['yachts'] = manual_yachts
    manual_data['lastUpdated'] = datetime.now().strftime("%Y-%m-%d")
    
    with open(manual_file, 'w', encoding='utf-8') as f:
        json.dump(manual_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ yacht_manual_resources.json 업데이트 완료 ({updated_count}개 ID 수정, {added_count}개 추가)")


if __name__ == "__main__":
    try:
        update_all_json_files()
        print("\n✨ 모든 작업이 성공적으로 완료되었습니다!\n")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

