# -*- coding: utf-8 -*-
"""
데이터베이스 구조 재구성: 실제 부품 vs 점검 항목 분리
"""
import json
from pathlib import Path
import sys

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def is_maintenance_item(part):
    """점검 항목인지 확인"""
    # inspectionItems가 있으면 점검 항목
    if "inspectionItems" in part:
        return True
    # checkInterval만 있고 price가 없으면 점검 항목
    if "checkInterval" in part and "price" not in part:
        return True
    # id 패턴으로 판단 (eng-001, hull-001 등)
    part_id = part.get("id", "")
    maintenance_prefixes = ["eng-", "hull-", "rig-", "sail-", "steer-", "bilge-", "safe-", "deck-", "elec-"]
    if any(part_id.startswith(prefix) for prefix in maintenance_prefixes):
        return True
    return False

def restructure_parts_category(parts_list):
    """카테고리별 부품 배열을 physicalParts/maintenanceItems로 분리"""
    if not parts_list:
        return {"physicalParts": [], "maintenanceItems": []}
    
    physical = []
    maintenance = []
    
    for part in parts_list:
        if is_maintenance_item(part):
            maintenance.append(part)
        else:
            physical.append(part)
    
    return {
        "physicalParts": physical,
        "maintenanceItems": maintenance
    }

def restructure_database():
    script_dir = Path(__file__).parent
    db_file = script_dir / "yacht_parts_database.json"
    backup_file = script_dir / "yacht_parts_database_backup.json"
    
    print("=" * 70)
    print("DATABASE RESTRUCTURING")
    print("=" * 70)
    
    # 백업 생성
    with open(db_file, 'r', encoding='utf-8') as f:
        database = json.load(f)
    
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    
    print(f"Backup created: {backup_file}")
    
    # 각 요트의 부품 구조 재구성
    for yacht in database.get("yachts", []):
        yacht_name = yacht.get("name")
        print(f"\nRestructuring: {yacht_name}")
        
        old_parts = yacht.get("parts", {})
        new_parts = {}
        
        for category, parts_list in old_parts.items():
            if isinstance(parts_list, list) and len(parts_list) > 0:
                restructured = restructure_parts_category(parts_list)
                new_parts[category] = restructured
                
                physical_count = len(restructured["physicalParts"])
                maintenance_count = len(restructured["maintenanceItems"])
                
                print(f"  {category}: {physical_count} physical, {maintenance_count} maintenance")
            else:
                # 빈 배열이거나 다른 형식이면 그대로 유지
                new_parts[category] = parts_list
        
        yacht["parts"] = new_parts
    
    # 저장
    with open(db_file, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 70)
    print("COMPLETE!")
    print("=" * 70)
    print(f"Original: {backup_file}")
    print(f"Updated: {db_file}")
    
    # 통계 출력
    total_physical = 0
    total_maintenance = 0
    
    for yacht in database.get("yachts", []):
        for category, parts in yacht.get("parts", {}).items():
            if isinstance(parts, dict):
                total_physical += len(parts.get("physicalParts", []))
                total_maintenance += len(parts.get("maintenanceItems", []))
    
    print(f"\nTotal Physical Parts: {total_physical}")
    print(f"Total Maintenance Items: {total_maintenance}")

if __name__ == "__main__":
    restructure_database()

