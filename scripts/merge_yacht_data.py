"""
yacht_parts_app_data.json과 yacht_parts_database.json을 병합하는 스크립트
앱용 상세 데이터를 데이터베이스 형식으로 변환합니다.
"""

import json
from pathlib import Path

def load_json(filepath):
    """JSON 파일 로드"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, filepath):
    """JSON 파일 저장"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def convert_app_data_to_database_format(app_data):
    """앱 데이터를 데이터베이스 형식으로 변환"""
    
    database = {
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
    
    # 각 요트 데이터 변환
    for yacht in app_data.get("yachts", []):
        yacht_entry = {
            "id": yacht.get("id"),
            "name": yacht.get("name"),
            "manufacturer": yacht.get("manufacturer"),
            "type": yacht.get("type"),
            "length": yacht.get("lengthFeet"),
            "lengthMeters": yacht.get("lengthMeters"),
            "beam": yacht.get("beam"),
            "draft": yacht.get("draft"),
            "displacement": yacht.get("displacement"),
            "officialWebsite": yacht.get("officialWebsite", yacht.get("classWebsite")),
            "manualPDF": yacht.get("manualPDF"),
            "parts": {}
        }
        
        # 부품 정보를 카테고리별로 분류
        common_parts = yacht.get("commonParts", [])
        
        # 카테고리별로 부품 분류
        parts_by_category = {
            "hull": [],
            "deck": [],
            "rigging": [],
            "sails": [],
            "winches": [],
            "blocks": [],
            "engine": [],
            "electrical": [],
            "plumbing": [],
            "navigation": [],
            "interior": [],
            "foils": []
        }
        
        for part in common_parts:
            category = part.get("category", "").lower()
            
            # 카테고리 매핑
            category_map = {
                "rigging": "rigging",
                "sails": "sails",
                "deck hardware": "deck",
                "hull": "hull",
                "foils": "foils",
                "propulsion": "engine",
                "electronics": "electrical",
                "electrical": "electrical",
                "plumbing": "plumbing",
                "navigation": "navigation",
                "interior": "interior"
            }
            
            mapped_category = category_map.get(category, "deck")
            
            # Winch 특별 처리
            if "winch" in part.get("name", "").lower():
                mapped_category = "winches"
            
            # 부품 정보 생성
            part_entry = {
                "partNumber": part.get("partNumber", part.get("id", "")),
                "name": part.get("name"),
                "category": part.get("category"),
                "manufacturer": part.get("manufacturer"),
                "model": part.get("model", ""),
                "material": part.get("material", ""),
                "specifications": {},
                "price": part.get("price"),
                "availability": part.get("availability"),
                "maintenanceInterval": part.get("maintenanceInterval")
            }
            
            # 사양 정보 추가
            if "length" in part:
                part_entry["specifications"]["length"] = part["length"]
            if "weight" in part:
                part_entry["specifications"]["weight"] = part["weight"]
            if "area" in part:
                part_entry["specifications"]["area"] = part["area"]
            if "horsepower" in part:
                part_entry["specifications"]["horsepower"] = part["horsepower"]
            if "type" in part:
                part_entry["specifications"]["type"] = part["type"]
            
            # 빈 사양은 제거
            if not part_entry["specifications"]:
                del part_entry["specifications"]
            
            parts_by_category[mapped_category].append(part_entry)
        
        # 빈 카테고리 제거하고 추가
        for cat, parts_list in parts_by_category.items():
            if parts_list:
                yacht_entry["parts"][cat] = parts_list
        
        database["yachts"].append(yacht_entry)
    
    return database

def merge_databases(app_data_file, database_file, output_file):
    """데이터베이스 병합"""
    print("="*60)
    print("요트 부품 데이터베이스 병합 시작")
    print("="*60)
    
    # 앱 데이터 로드
    print(f"\n[1] 앱 데이터 로드: {app_data_file}")
    app_data = load_json(app_data_file)
    print(f"    요트 수: {len(app_data.get('yachts', []))}개")
    
    # 데이터베이스 형식으로 변환
    print(f"\n[2] 데이터베이스 형식으로 변환 중...")
    new_database = convert_app_data_to_database_format(app_data)
    print(f"    변환 완료: {len(new_database['yachts'])}개 요트")
    
    # 기존 데이터베이스 로드 (있는 경우)
    try:
        print(f"\n[3] 기존 데이터베이스 로드: {database_file}")
        existing_db = load_json(database_file)
        print(f"    기존 요트 수: {len(existing_db.get('yachts', []))}개")
        
        # 기존 데이터와 병합
        existing_ids = {y["id"]: y for y in existing_db.get("yachts", [])}
        new_ids = {y["id"]: y for y in new_database["yachts"]}
        
        # 새 데이터로 업데이트
        for yacht_id, yacht_data in new_ids.items():
            if yacht_id in existing_ids:
                # 기존 데이터 업데이트
                existing_ids[yacht_id] = yacht_data
            else:
                # 새 요트 추가
                existing_ids[yacht_id] = yacht_data
        
        # 최종 데이터베이스 생성
        merged_database = existing_db.copy()
        merged_database["yachts"] = list(existing_ids.values())
        
    except FileNotFoundError:
        print(f"    기존 파일 없음 - 새로 생성")
        merged_database = new_database
    
    # 저장
    print(f"\n[4] 저장 중: {output_file}")
    save_json(merged_database, output_file)
    
    # 통계
    print(f"\n{'='*60}")
    print(f"병합 완료!")
    print(f"{'='*60}")
    print(f"총 요트: {len(merged_database['yachts'])}개")
    
    # 각 요트별 부품 수 집계
    total_parts = 0
    for yacht in merged_database['yachts']:
        yacht_parts = sum(len(parts) for parts in yacht.get('parts', {}).values())
        total_parts += yacht_parts
        if yacht_parts > 0:
            print(f"  - {yacht['name']}: {yacht_parts}개 부품")
    
    print(f"\n총 부품 수: {total_parts}개")
    print(f"{'='*60}\n")

def main():
    """메인 실행"""
    script_dir = Path(__file__).parent
    
    app_data_file = script_dir / "yacht_parts_app_data.json"
    database_file = script_dir / "yacht_parts_database.json"
    output_file = script_dir / "yacht_parts_database.json"
    
    # 파일 존재 확인
    if not app_data_file.exists():
        print(f"[ERROR] 파일을 찾을 수 없습니다: {app_data_file}")
        return
    
    # 병합 실행
    merge_databases(app_data_file, database_file, output_file)
    
    print("[SUCCESS] 완료! yacht_parts_database.json 파일을 확인하세요.")

if __name__ == "__main__":
    main()

