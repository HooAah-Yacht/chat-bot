"""
yacht_parts_app_data.json을 yacht_parts_database.json으로 직접 변환
"""

import json
from pathlib import Path

# 앱 데이터 로드
app_data_file = Path("yacht_parts_app_data.json")
with open(app_data_file, 'r', encoding='utf-8') as f:
    app_data = json.load(f)

print("="*60)
print("요트 부품 데이터베이스 생성")
print("="*60)
print(f"\n앱 데이터에서 {len(app_data['yachts'])}개 요트 로드")

# 새 데이터베이스 생성
new_database = {
    "yachts": [],
    "commonPartCategories": {
        "hull": ["Hull", "Keel", "Rudder", "Transom", "Bow", "Deck"],
        "rigging": ["Mast", "Boom", "Spinnaker Pole", "Standing Rigging", "Running Rigging", "Halyards", "Sheets"],
        "sails": ["Mainsail", "Genoa", "Jib", "Spinnaker", "Gennaker", "Code Zero"],
        "winches": ["Primary Winches", "Halyard Winches", "Mainsheet Winch", "Jib Sheet Winches"],
        "blocks": ["Mainsheet Blocks", "Jib Blocks", "Spinnaker Blocks", "Traveler"],
        "engine": ["Engine", "Propeller", "Shaft", "Fuel Tank", "Exhaust System"],
        "electrical": ["Batteries", "Alternator", "Solar Panels", "Navigation Lights", "Interior Lights"],
        "plumbing": ["Water Tanks", "Holding Tank", "Bilge Pump", "Manual Pump"],
        "navigation": ["Compass", "GPS", "Chartplotter", "VHF Radio", "Depth Sounder", "Wind Instruments", "Autopilot"],
        "interior": ["Galley Stove", "Refrigerator", "Berths", "Table", "Cushions"],
        "safety": ["Life Raft", "Life Jackets", "Flares", "Fire Extinguisher", "EPIRB"],
        "deck": ["Hatches", "Portlights", "Chainplates", "Cleats", "Fairleads"]
    },
    "manufacturers": {
        "winches": ["Harken", "Lewmar", "Andersen", "Antal"],
        "blocks": ["Harken", "Lewmar", "Ronstan", "Spinlock"],
        "sails": ["North Sails", "Quantum Sails", "UK Sailmakers", "Doyle Sails", "Elvstrom"],
        "engines": ["Yanmar", "Volvo Penta", "Westerbeke", "Beta Marine"],
        "electronics": ["Garmin", "Raymarine", "B&G", "Simrad", "Furuno"],
        "rigging": ["Selden", "Z-Spars", "Hall Spars", "Navtec", "Southern Spars"]
    }
}

# 각 요트 변환
total_parts = 0
for yacht in app_data["yachts"]:
    print(f"\n변환 중: {yacht['name']}")
    
    # 기본 정보
    yacht_entry = {
        "id": yacht["id"],
        "name": yacht["name"],
        "manufacturer": yacht["manufacturer"],
        "type": yacht["type"],
        "length": yacht["lengthFeet"],
        "lengthMeters": yacht.get("lengthMeters"),
        "beam": yacht.get("beam"),
        "draft": yacht.get("draft"),
        "displacement": yacht.get("displacement"),
        "officialWebsite": yacht.get("officialWebsite") or yacht.get("classWebsite"),
        "manualPDF": yacht.get("manualPDF"),
        "parts": {}
    }
    
    # 부품을 카테고리별로 분류
    parts_by_category = {
        "rigging": [],
        "sails": [],
        "winches": [],
        "deck": [],
        "hull": [],
        "engine": [],
        "electrical": [],
        "plumbing": [],
        "navigation": [],
        "interior": [],
        "foils": [],
        "blocks": []
    }
    
    # 각 부품 처리
    for part in yacht.get("commonParts", []):
        category = part.get("category", "").lower()
        
        # 카테고리 매핑
        if category == "rigging":
            cat = "rigging"
        elif category == "sails":
            cat = "sails"
        elif category == "deck hardware":
            # Winch인지 확인
            if "winch" in part.get("name", "").lower():
                cat = "winches"
            else:
                cat = "deck"
        elif category == "hull":
            cat = "hull"
        elif category == "foils":
            cat = "foils"
        elif category == "propulsion":
            cat = "engine"
        elif category == "electronics":
            cat = "electrical"
        elif category == "electrical":
            cat = "electrical"
        elif category == "plumbing":
            cat = "plumbing"
        elif category == "navigation":
            cat = "navigation"
        elif category == "interior":
            cat = "interior"
        else:
            cat = "deck"
        
        # 부품 정보 생성
        part_entry = {
            "partNumber": part.get("partNumber", part.get("id", "")),
            "name": part.get("name"),
            "category": part.get("category"),
            "manufacturer": part.get("manufacturer", ""),
            "model": part.get("model", ""),
            "material": part.get("material", ""),
            "price": part.get("price"),
            "availability": part.get("availability", ""),
            "maintenanceInterval": part.get("maintenanceInterval", "")
        }
        
        # 사양 정보 추가
        specs = {}
        if "length" in part:
            specs["length"] = part["length"]
        if "weight" in part:
            specs["weight"] = part["weight"]
        if "area" in part:
            specs["area"] = part["area"]
        if "horsepower" in part:
            specs["horsepower"] = part["horsepower"]
        if "type" in part:
            specs["type"] = part["type"]
        
        if specs:
            part_entry["specifications"] = specs
        
        parts_by_category[cat].append(part_entry)
    
    # 빈 카테고리 제거하고 추가
    for cat, parts_list in parts_by_category.items():
        if parts_list:
            yacht_entry["parts"][cat] = parts_list
    
    part_count = sum(len(p) for p in yacht_entry["parts"].values())
    print(f"  - {part_count}개 부품 추가됨")
    total_parts += part_count
    
    new_database["yachts"].append(yacht_entry)

# 저장
output_file = Path("yacht_parts_database.json")
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(new_database, f, indent=2, ensure_ascii=False)

print(f"\n{'='*60}")
print(f"완료!")
print(f"{'='*60}")
print(f"총 요트: {len(new_database['yachts'])}개")
print(f"총 부품: {total_parts}개")
print(f"저장됨: {output_file}")
print(f"{'='*60}\n")

