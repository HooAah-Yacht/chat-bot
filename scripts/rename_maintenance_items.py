# -*- coding: utf-8 -*-
"""
maintenanceItems 이름을 명확하게 변경하여 physicalParts와 구분
"""
import json
from pathlib import Path
import sys

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def rename_maintenance_items():
    script_dir = Path(__file__).parent
    db_file = script_dir / "yacht_parts_database.json"
    backup_file = script_dir / "yacht_parts_database_backup3.json"
    
    print("=" * 70)
    print("Maintenance Items 이름 변경 (점검 항목임을 명확히)")
    print("=" * 70)
    
    # 데이터 로드
    with open(db_file, 'r', encoding='utf-8') as f:
        database = json.load(f)
    
    # 백업 생성
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    
    print(f"백업 생성: {backup_file}")
    
    # 이름 변경 규칙
    name_mapping = {
        # Rigging
        "Standing Rigging - Stays & Shrouds": "Standing Rigging Inspection - Stays & Shrouds",
        "Running Rigging - Halyards & Sheets": "Running Rigging Inspection - Halyards & Sheets",
        "Mast": "Mast Inspection",
        
        # Sails
        "Mainsail": "Mainsail Inspection",
        "Genoa / Jib": "Genoa / Jib Inspection",
        
        # Engine
        "Engine Oil": "Engine Oil Check",
        "Gear Oil": "Gear Oil Check",
        "Impeller": "Impeller Inspection",
        "Fuel System": "Fuel System Inspection",
        "Coolant System": "Coolant System Check",
        "Belts": "Belt Inspection",
        "Alternator": "Alternator Check",
        "Starter Motor": "Starter Motor Check",
        "Propeller": "Propeller Inspection",
        "Shaft": "Shaft Inspection",
        
        # Electrical
        "Battery Bank": "Battery Bank Check",
        
        # Steering
        "Rudder": "Rudder Inspection",
        "Rudder Bearings": "Rudder Bearing Check",
        "Steering Cables": "Steering Cable Inspection",
        "Wheel/Tiller": "Wheel/Tiller Check",
        "Autopilot": "Autopilot System Check",
        "Emergency Tiller": "Emergency Tiller Check",
        "Steering Quadrant": "Steering Quadrant Inspection",
        "Pedestal": "Pedestal Check",
        "Chain/Linkage": "Chain/Linkage Inspection",
        "Helm Bearing": "Helm Bearing Check",
        
        # Bilge/Plumbing
        "Bilge Pump": "Bilge Pump Check",
        "Through-Hull Fittings": "Through-Hull Fitting Inspection",
        "Seacocks": "Seacock Inspection",
        "Hoses": "Hose Inspection",
        "Fresh Water System": "Fresh Water System Check",
        "Holding Tank": "Holding Tank Inspection",
        "Manual Bilge Pump": "Manual Bilge Pump Check",
        "High Water Alarm": "High Water Alarm Check",
        "Thru-hull Plugs": "Thru-hull Plug Inspection",
        "Drain System": "Drain System Check",
        
        # Safety
        "Life Jackets": "Life Jacket Inspection",
        "Flares": "Flare Check",
        
        # Deck Hardware
        "Deck Hardware": "Deck Hardware Inspection",
        "Stanchions": "Stanchion Inspection",
        "Lifelines": "Lifeline Inspection",
        "Cleats": "Cleat Inspection",
        "Winches": "Winch Service",
        "Blocks": "Block Inspection",
        "Hatches": "Hatch Inspection",
        "Portlights": "Portlight Inspection",
        "Anchor Windlass": "Anchor Windlass Check",
        "Bow Roller": "Bow Roller Inspection",
        "Deck Fittings": "Deck Fitting Inspection",
        
        # Hull
        "Hull Structure": "Hull Structure Inspection",
        "Gelcoat / Paint": "Gelcoat / Paint Inspection",
        "Keel Bolts": "Keel Bolt Inspection",
    }
    
    total_renamed = 0
    
    # 각 요트의 maintenanceItems 처리
    for yacht in database.get("yachts", []):
        yacht_name = yacht.get("name")
        print(f"\n처리 중: {yacht_name}")
        
        for category, parts_data in yacht.get("parts", {}).items():
            if isinstance(parts_data, dict) and "maintenanceItems" in parts_data:
                for item in parts_data["maintenanceItems"]:
                    old_name = item.get("name", "")
                    
                    if old_name in name_mapping:
                        new_name = name_mapping[old_name]
                        item["name"] = new_name
                        print(f"  {category}: '{old_name}' → '{new_name}'")
                        total_renamed += 1
    
    # 저장
    with open(db_file, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 70)
    print(f"완료! 총 {total_renamed}개 항목 이름 변경")
    print("=" * 70)

if __name__ == "__main__":
    rename_maintenance_items()

