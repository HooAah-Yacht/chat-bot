# -*- coding: utf-8 -*-
"""
yacht_parts_app_data.json의 상세 데이터를 yacht_parts_database.json으로 복사
"""
import json
import sys
from pathlib import Path

# Windows 인코딩 설정
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def rebuild_database():
    script_dir = Path(__file__).parent
    app_data_file = script_dir / "yacht_parts_app_data.json"
    db_file = script_dir / "yacht_parts_database.json"
    
    print("=" * 70)
    print("DATABASE REBUILD")
    print("=" * 70)
    
    # 1. app_data 로드
    with open(app_data_file, 'r', encoding='utf-8') as f:
        app_data = json.load(f)
    
    print(f"Loaded {len(app_data.get('yachts', []))} yachts from app_data")
    
    # 2. 각 요트를 yacht_parts_database 형식으로 변환
    new_yachts = []
    
    for app_yacht in app_data.get("yachts", []):
        db_yacht = {
            "id": app_yacht.get("id"),
            "name": app_yacht.get("name"),
            "manufacturer": app_yacht.get("manufacturer"),
            "type": app_yacht.get("type"),
            "length": app_yacht.get("lengthFeet"),
            "officialWebsite": app_yacht.get("officialWebsite"),
            "manualPDF": app_yacht.get("manualPDF"),
            "dimensions": {
                "lengthFeet": app_yacht.get("lengthFeet"),
                "lengthMeters": app_yacht.get("lengthMeters"),
                "beam": app_yacht.get("beam"),
                "draft": app_yacht.get("draft"),
                "displacement": app_yacht.get("displacement")
            },
            "parts": {}
        }
        
        # commonParts를 카테고리별로 재구성
        for part in app_yacht.get("commonParts", []):
            category = part.get("category", "misc").lower().replace(" ", "_")
            
            if category not in db_yacht["parts"]:
                db_yacht["parts"][category] = []
            
            db_yacht["parts"][category].append(part)
        
        new_yachts.append(db_yacht)
        print(f"  {app_yacht.get('name')}: {len(app_yacht.get('commonParts', []))} parts")
    
    # 3. 최종 데이터베이스 생성
    final_database = {
        "yachts": new_yachts,
        "commonPartCategories": {
            "hull": ["Hull", "Keel", "Rudder", "Transom", "Bow"],
            "deck": ["Deck", "Cockpit", "Hatches", "Portlights", "Chainplates"],
            "rigging": ["Mast", "Boom", "Standing Rigging", "Running Rigging"],
            "sails": ["Mainsail", "Genoa", "Jib", "Spinnaker"],
            "winches": ["Primary Winches", "Halyard Winches"],
            "blocks": ["Mainsheet Blocks", "Jib Blocks"],
            "engine": ["Engine", "Propeller", "Fuel System"],
            "electrical": ["Batteries", "Alternator", "Navigation Lights"],
            "plumbing": ["Water Tanks", "Bilge Pump"],
            "navigation": ["Compass", "GPS", "VHF Radio"],
            "interior": ["Galley", "Berths"],
            "safety": ["Life Raft", "Life Jackets", "Flares"]
        }
    }
    
    # 4. 저장
    with open(db_file, 'w', encoding='utf-8') as f:
        json.dump(final_database, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 70)
    print("COMPLETE!")
    print("=" * 70)
    print(f"Total Yachts: {len(new_yachts)}")
    
    total_parts = sum(len(parts) for yacht in new_yachts for category, parts in yacht['parts'].items())
    print(f"Total Parts: {total_parts}")
    print(f"Saved to: {db_file}")
    print(f"File size: {db_file.stat().st_size:,} bytes")

if __name__ == "__main__":
    rebuild_database()

