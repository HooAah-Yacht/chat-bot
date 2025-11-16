# -*- coding: utf-8 -*-
"""
yacht_parts_app_data.json의 실제 부품을 physicalParts에 추가
"""
import json
from pathlib import Path
import sys

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def categorize_part(part):
    """부품의 카테고리를 database 형식에 맞게 변환"""
    category = part.get("category", "").lower()
    
    category_mapping = {
        "rigging": "rigging",
        "sails": "sails",
        "deck hardware": "deck_hardware",
        "propulsion": "propulsion",
        "engine": "engine",
        "electronics": "electronics",
        "electrical": "electrical",
        "foils": "foils",
        "hull": "hull",
        "steering": "steering",
        "safety": "safety",
    }
    
    for key, value in category_mapping.items():
        if key in category:
            return value
    
    return "other"

def add_physical_parts():
    script_dir = Path(__file__).parent
    app_data_file = script_dir / "yacht_parts_app_data.json"
    db_file = script_dir / "yacht_parts_database.json"
    backup_file = script_dir / "yacht_parts_database_backup2.json"
    
    print("=" * 70)
    print("실제 부품(Physical Parts) 추가")
    print("=" * 70)
    
    # 데이터 로드
    with open(app_data_file, 'r', encoding='utf-8') as f:
        app_data = json.load(f)
    
    with open(db_file, 'r', encoding='utf-8') as f:
        database = json.load(f)
    
    # 백업 생성
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    
    print(f"백업 생성: {backup_file}")
    
    # 각 요트별로 실제 부품 추가
    for app_yacht in app_data.get("yachts", []):
        yacht_id = app_yacht.get("id")
        yacht_name = app_yacht.get("name")
        common_parts = app_yacht.get("commonParts", [])
        
        # database에서 해당 요트 찾기
        db_yacht = None
        for yacht in database.get("yachts", []):
            if yacht.get("id") == yacht_id:
                db_yacht = yacht
                break
        
        if not db_yacht:
            print(f"경고: {yacht_name} (ID: {yacht_id})를 찾을 수 없습니다.")
            continue
        
        print(f"\n처리 중: {yacht_name}")
        print(f"  실제 부품 수: {len(common_parts)}개")
        
        # parts가 없으면 초기화
        if "parts" not in db_yacht:
            db_yacht["parts"] = {}
        
        # 각 실제 부품을 적절한 카테고리의 physicalParts에 추가
        for part in common_parts:
            category = categorize_part(part)
            
            # 해당 카테고리가 없으면 초기화
            if category not in db_yacht["parts"]:
                db_yacht["parts"][category] = {
                    "physicalParts": [],
                    "maintenanceItems": []
                }
            
            # 구조가 배열이면 변환
            if isinstance(db_yacht["parts"][category], list):
                db_yacht["parts"][category] = {
                    "physicalParts": [],
                    "maintenanceItems": db_yacht["parts"][category]
                }
            
            # physicalParts 키가 없으면 추가
            if "physicalParts" not in db_yacht["parts"][category]:
                db_yacht["parts"][category]["physicalParts"] = []
            
            # 이미 존재하는지 확인 (id 기준)
            part_id = part.get("id")
            exists = any(p.get("id") == part_id for p in db_yacht["parts"][category]["physicalParts"])
            
            if not exists:
                db_yacht["parts"][category]["physicalParts"].append(part)
                print(f"  ✓ {category}: {part.get('name')} 추가")
            else:
                print(f"  - {category}: {part.get('name')} (이미 존재)")
    
    # 저장
    with open(db_file, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 70)
    print("완료!")
    print("=" * 70)
    
    # 통계
    total_physical = 0
    total_maintenance = 0
    
    for yacht in database.get("yachts", []):
        for category, parts in yacht.get("parts", {}).items():
            if isinstance(parts, dict):
                physical_count = len(parts.get("physicalParts", []))
                maintenance_count = len(parts.get("maintenanceItems", []))
                total_physical += physical_count
                total_maintenance += maintenance_count
    
    print(f"\n전체 실제 부품(Physical Parts): {total_physical}개")
    print(f"전체 점검 항목(Maintenance Items): {total_maintenance}개")
    print(f"총 부품 데이터: {total_physical + total_maintenance}개")

if __name__ == "__main__":
    add_physical_parts()

