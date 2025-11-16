# -*- coding: utf-8 -*-
"""
모든 maintenanceItems 이름을 점검/체크 형태로 완전히 변경
"""
import json
from pathlib import Path
import sys

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def complete_maintenance_rename():
    script_dir = Path(__file__).parent
    db_file = script_dir / "yacht_parts_database.json"
    backup_file = script_dir / "yacht_parts_database_backup4.json"
    
    print("=" * 70)
    print("모든 Maintenance Items 이름 완전 변경")
    print("=" * 70)
    
    # 데이터 로드
    with open(db_file, 'r', encoding='utf-8') as f:
        database = json.load(f)
    
    # 백업 생성
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    
    print(f"백업 생성: {backup_file}")
    
    # 완전한 이름 변경 매핑
    name_mapping = {
        # 이미 변경된 것들 (유지)
        "Standing Rigging Inspection - Stays & Shrouds": "Standing Rigging Inspection - Stays & Shrouds",
        "Running Rigging Inspection - Halyards & Sheets": "Running Rigging Inspection - Halyards & Sheets",
        "Mast Inspection": "Mast Inspection",
        "Mainsail Inspection": "Mainsail Inspection",
        "Genoa / Jib Inspection": "Genoa / Jib Inspection",
        "Engine Oil Check": "Engine Oil Check",
        "Impeller Inspection": "Impeller Inspection",
        "Alternator Check": "Alternator Check",
        "Life Jacket Inspection": "Life Jacket Inspection",
        "Rudder Inspection": "Rudder Inspection",
        "Hull Damage Inspection": "Hull Damage Inspection",
        "Battery Voltage Check": "Battery Voltage Check",
        
        # 새로 변경해야 할 항목들
        "Air Filter": "Air Filter Inspection",
        "Batteries": "Battery Bank Inspection",
        "Bilge Cleaning": "Bilge Cleaning & Inspection",
        "Block": "Block Inspection",
        "Canvas / Cover": "Canvas/Cover Inspection",
        "Chain & Cable": "Chain & Cable Inspection",
        "Check Valve (Non-return Valve)": "Check Valve Inspection",
        "Cleat": "Cleat Inspection",
        "Coolant": "Coolant System Check",
        "Deck Sealing / Caulking": "Deck Sealing Inspection",
        "Exhaust System": "Exhaust System Inspection",
        "Float Switch": "Float Switch Check",
        "Fuel Filter": "Fuel Filter Inspection",
        "Gear Oil / Saildrive Oil": "Gear Oil Check",
        "Helm Wheel": "Helm Wheel Inspection",
        "Hose & Valve": "Hose & Valve Inspection",
        "Hydraulic Cylinder": "Hydraulic Cylinder Inspection",
        "Hydraulic Pump (Hydraulic Type)": "Hydraulic Pump Check",
        "Keel": "Keel Inspection",
        "Life Raft": "Life Raft Inspection",
        "Lines (Rope)": "Lines Inspection",
        "Manual Pump": "Manual Pump Check",
        "Metal Fittings": "Metal Fitting Inspection",
        "Oil Filter": "Oil Filter Check",
        "Quadrant": "Quadrant Inspection",
        "Relay": "Relay Check",
        "Rudder Blade": "Rudder Blade Inspection",
        "Rudder Stock": "Rudder Stock Inspection",
        "Shackle & Pin": "Shackle & Pin Inspection",
        "Spare Pump": "Spare Pump Check",
        "Stanchion / Pulpit": "Stanchion/Pulpit Inspection",
        "Stopper / End Stop": "Stopper/End Stop Inspection",
        "Through-hull": "Through-hull Fitting Inspection",
        "Tiller Arm (Tiller Type)": "Tiller Arm Inspection",
        "Track & Car": "Track & Car Inspection",
        "V-Belt / Serpentine Belt": "Belt Inspection",
        "Winch": "Winch Service & Inspection",
        "Auto Bilge Pump": "Auto Bilge Pump Check",
        "Autopilot Connection": "Autopilot Connection Check",
    }
    
    total_renamed = 0
    unchanged = 0
    
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
                        if old_name != new_name:
                            item["name"] = new_name
                            print(f"  {category}: '{old_name}' → '{new_name}'")
                            total_renamed += 1
                        else:
                            unchanged += 1
                    else:
                        # 매핑에 없는 경우 - 자동으로 처리
                        if not any(suffix in old_name for suffix in ["Inspection", "Check", "Service"]):
                            # 적절한 suffix 추가
                            if "pump" in old_name.lower() or "battery" in old_name.lower() or "switch" in old_name.lower():
                                new_name = f"{old_name} Check"
                            else:
                                new_name = f"{old_name} Inspection"
                            
                            item["name"] = new_name
                            print(f"  {category}: '{old_name}' → '{new_name}' (자동)")
                            total_renamed += 1
                        else:
                            unchanged += 1
    
    # 저장
    with open(db_file, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 70)
    print(f"완료!")
    print(f"  변경됨: {total_renamed}개")
    print(f"  유지됨: {unchanged}개")
    print("=" * 70)

if __name__ == "__main__":
    complete_maintenance_rename()

