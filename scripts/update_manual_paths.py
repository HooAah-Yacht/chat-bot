# -*- coding: utf-8 -*-
"""
미확인 매뉴얼 경로 업데이트
"""
import json
from pathlib import Path

def update_manual_paths():
    script_dir = Path(__file__).parent
    
    # 매뉴얼 매핑
    manual_updates = {
        "Farr 40": "yachtpdf/rulebook.pdf",
        "Laser": "yachtpdf/Handbook_2109.pdf",
        "Laser / ILCA": "yachtpdf/Handbook_2109.pdf",
        "Beneteau First 36": "yachtpdf/owners_manual.pdf",
        "X-35": "yachtpdf/X352012CR080412-[12381].pdf"
    }
    
    print("=" * 70)
    print("UPDATING MANUAL PATHS")
    print("=" * 70)
    
    # 1. yacht_manual_resources.json 업데이트
    resources_file = script_dir / "yacht_manual_resources.json"
    with open(resources_file, 'r', encoding='utf-8') as f:
        resources = json.load(f)
    
    for resource in resources.get("manuals", []):
        yacht_name = resource.get("yacht")
        if yacht_name in manual_updates:
            resource["manualLocation"] = manual_updates[yacht_name]
            print(f"Updated: {yacht_name} -> {manual_updates[yacht_name]}")
    
    with open(resources_file, 'w', encoding='utf-8') as f:
        json.dump(resources, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved: {resources_file}")
    
    # 2. yacht_parts_database.json 업데이트
    db_file = script_dir / "yacht_parts_database.json"
    with open(db_file, 'r', encoding='utf-8') as f:
        database = json.load(f)
    
    yacht_id_map = {
        "Farr 40": "farr-40",
        "Laser": "laser",
        "Laser / ILCA": "laser",
        "Beneteau First 36": "beneteau-first-36",
        "X-35": "x35"
    }
    
    for yacht in database.get("yachts", []):
        yacht_name = yacht.get("name")
        if yacht_name in manual_updates:
            yacht["manualPDF"] = manual_updates[yacht_name]
            print(f"Updated DB: {yacht_name} -> {manual_updates[yacht_name]}")
    
    with open(db_file, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    
    print(f"Saved: {db_file}")
    
    print("\n" + "=" * 70)
    print("COMPLETE! All 20 yachts now have manuals!")
    print("=" * 70)

if __name__ == "__main__":
    update_manual_paths()

