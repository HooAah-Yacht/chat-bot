"""
요트 데이터 중복 확인 스크립트
여러 JSON 파일에서 중복된 요트를 찾아 정리합니다.
"""

import json
import os
import sys
from collections import defaultdict
from pathlib import Path

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

def load_json_file(file_path):
    """JSON 파일 로드"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ {file_path} 로드 실패: {e}")
        return None

def extract_yacht_names_from_specifications(data):
    """yacht_specifications.json에서 요트 이름 추출"""
    yachts = []
    if isinstance(data, dict) and "yachts" in data:
        for yacht in data["yachts"]:
            name = yacht.get("name", "")
            if name:
                yachts.append({
                    "name": name,
                    "id": yacht.get("id", ""),
                    "manufacturer": yacht.get("manufacturer", "")
                })
    return yachts

def extract_yacht_names_from_registered(data):
    """registered_yachts.json에서 요트 이름 추출"""
    yachts = []
    if isinstance(data, dict) and "yachts" in data:
        for yacht in data["yachts"]:
            reg_data = yacht.get("registrationData", {})
            basic_info = reg_data.get("basicInfo", {})
            name = basic_info.get("name", "")
            if name:
                yachts.append({
                    "name": name,
                    "nickName": basic_info.get("nickName", ""),
                    "manufacturer": basic_info.get("manufacturer", ""),
                    "pdfFile": yacht.get("pdfFile", "")
                })
    return yachts

def extract_yacht_names_from_parts_database(data):
    """yacht_parts_database.json에서 요트 이름 추출"""
    yachts = []
    if isinstance(data, dict) and "yachts" in data:
        for yacht in data["yachts"]:
            name = yacht.get("name", "")
            if name:
                yachts.append({
                    "name": name,
                    "id": yacht.get("id", ""),
                    "manufacturer": yacht.get("manufacturer", "")
                })
    return yachts

def extract_yacht_names_from_extracted_parts_detailed(data):
    """extracted_yacht_parts_detailed.json에서 요트 이름 추출"""
    yachts = []
    if isinstance(data, list):
        for item in data:
            yacht_name = item.get("yacht", "")
            if yacht_name:
                yachts.append({
                    "name": yacht_name,
                    "source": "extracted_yacht_parts_detailed"
                })
    elif isinstance(data, dict) and "yachts" in data:
        for yacht in data["yachts"]:
            name = yacht.get("name", "")
            if name:
                yachts.append({
                    "name": name,
                    "id": yacht.get("id", "")
                })
    return yachts

def extract_yacht_names_from_parts_app_data(data):
    """yacht_parts_app_data.json에서 요트 이름 추출"""
    yachts = []
    if isinstance(data, dict) and "yachts" in data:
        for yacht in data["yachts"]:
            name = yacht.get("name", "")
            if name:
                yachts.append({
                    "name": name,
                    "id": yacht.get("id", ""),
                    "manufacturer": yacht.get("manufacturer", "")
                })
    return yachts

def extract_yacht_names_from_manual_resources(data):
    """yacht_manual_resources.json에서 요트 이름 추출"""
    yachts = []
    if isinstance(data, dict):
        # 구조에 따라 다를 수 있음
        if "yachts" in data:
            for yacht in data["yachts"]:
                name = yacht.get("name", "")
                if name:
                    yachts.append({
                        "name": name,
                        "id": yacht.get("id", "")
                    })
    return yachts

def normalize_yacht_name(name):
    """요트 이름 정규화 (비교용)"""
    if not name:
        return ""
    # 소문자 변환, 공백/하이픈 제거
    normalized = name.lower().strip()
    normalized = normalized.replace("-", "").replace(" ", "").replace("_", "")
    return normalized

def check_duplicates():
    """모든 JSON 파일에서 중복 확인"""
    data_dir = Path("data")
    
    print("="*80)
    print("[중복 확인] 요트 데이터 중복 확인")
    print("="*80)
    print()
    
    # 각 파일에서 요트 이름 추출
    all_yachts = defaultdict(list)
    
    # 1. yacht_specifications.json
    specs_file = data_dir / "yacht_specifications.json"
    if specs_file.exists():
        data = load_json_file(specs_file)
        if data:
            yachts = extract_yacht_names_from_specifications(data)
            for yacht in yachts:
                normalized = normalize_yacht_name(yacht["name"])
                all_yachts[normalized].append({
                    "name": yacht["name"],
                    "file": "yacht_specifications.json",
                    "id": yacht.get("id", ""),
                    "manufacturer": yacht.get("manufacturer", "")
                })
            print(f"[OK] yacht_specifications.json: {len(yachts)}개 요트")
    
    # 2. registered_yachts.json
    registered_file = data_dir / "registered_yachts.json"
    if registered_file.exists():
        data = load_json_file(registered_file)
        if data:
            yachts = extract_yacht_names_from_registered(data)
            for yacht in yachts:
                normalized = normalize_yacht_name(yacht["name"])
                all_yachts[normalized].append({
                    "name": yacht["name"],
                    "file": "registered_yachts.json",
                    "nickName": yacht.get("nickName", ""),
                    "manufacturer": yacht.get("manufacturer", ""),
                    "pdfFile": yacht.get("pdfFile", "")
                })
            print(f"[OK] registered_yachts.json: {len(yachts)}개 요트")
    
    # 3. yacht_parts_database.json
    parts_db_file = data_dir / "yacht_parts_database.json"
    if parts_db_file.exists():
        data = load_json_file(parts_db_file)
        if data:
            yachts = extract_yacht_names_from_parts_database(data)
            for yacht in yachts:
                normalized = normalize_yacht_name(yacht["name"])
                all_yachts[normalized].append({
                    "name": yacht["name"],
                    "file": "yacht_parts_database.json",
                    "id": yacht.get("id", ""),
                    "manufacturer": yacht.get("manufacturer", "")
                })
            print(f"[OK] yacht_parts_database.json: {len(yachts)}개 요트")
    
    # 4. extracted_yacht_parts_detailed.json
    extracted_file = data_dir / "extracted_yacht_parts_detailed.json"
    if extracted_file.exists():
        data = load_json_file(extracted_file)
        if data:
            yachts = extract_yacht_names_from_extracted_parts_detailed(data)
            for yacht in yachts:
                normalized = normalize_yacht_name(yacht["name"])
                all_yachts[normalized].append({
                    "name": yacht["name"],
                    "file": "extracted_yacht_parts_detailed.json",
                    "id": yacht.get("id", "")
                })
            print(f"[OK] extracted_yacht_parts_detailed.json: {len(yachts)}개 요트")
    
    # 5. yacht_parts_app_data.json
    app_data_file = data_dir / "yacht_parts_app_data.json"
    if app_data_file.exists():
        data = load_json_file(app_data_file)
        if data:
            yachts = extract_yacht_names_from_parts_app_data(data)
            for yacht in yachts:
                normalized = normalize_yacht_name(yacht["name"])
                all_yachts[normalized].append({
                    "name": yacht["name"],
                    "file": "yacht_parts_app_data.json",
                    "id": yacht.get("id", ""),
                    "manufacturer": yacht.get("manufacturer", "")
                })
            print(f"[OK] yacht_parts_app_data.json: {len(yachts)}개 요트")
    
    # 6. yacht_manual_resources.json
    manual_resources_file = data_dir / "yacht_manual_resources.json"
    if manual_resources_file.exists():
        data = load_json_file(manual_resources_file)
        if data:
            yachts = extract_yacht_names_from_manual_resources(data)
            for yacht in yachts:
                normalized = normalize_yacht_name(yacht["name"])
                all_yachts[normalized].append({
                    "name": yacht["name"],
                    "file": "yacht_manual_resources.json",
                    "id": yacht.get("id", "")
                })
            print(f"[OK] yacht_manual_resources.json: {len(yachts)}개 요트")
    
    print()
    print("="*80)
    print("📊 중복 분석 결과")
    print("="*80)
    print()
    
    # 중복 찾기
    duplicates = {}
    unique_yachts = {}
    
    for normalized_name, yacht_list in all_yachts.items():
        if len(yacht_list) > 1:
            # 여러 파일에 나타나는 경우
            files = [y["file"] for y in yacht_list]
            if len(set(files)) > 1:
                duplicates[normalized_name] = yacht_list
        else:
            unique_yachts[normalized_name] = yacht_list[0]
    
    # 결과 출력
    print(f"[통계] 총 고유 요트 수: {len(unique_yachts) + len(duplicates)}개")
    print(f"[OK] 중복 없음: {len(unique_yachts)}개")
    print(f"[WARNING] 중복 발견: {len(duplicates)}개")
    print()
    
    if duplicates:
        print("="*80)
        print("⚠️ 중복된 요트 목록")
        print("="*80)
        print()
        
        for normalized_name, yacht_list in sorted(duplicates.items()):
            print(f"[중복] 요트: {yacht_list[0]['name']}")
            print(f"   정규화된 이름: {normalized_name}")
            print(f"   발견된 파일 수: {len(yacht_list)}개")
            print()
            
            for yacht in yacht_list:
                print(f"   [파일] {yacht['file']}")
                print(f"      - 이름: {yacht['name']}")
                if yacht.get("id"):
                    print(f"      - ID: {yacht['id']}")
                if yacht.get("manufacturer"):
                    print(f"      - 제조사: {yacht['manufacturer']}")
                if yacht.get("nickName"):
                    print(f"      - 별명: {yacht['nickName']}")
                if yacht.get("pdfFile"):
                    print(f"      - PDF: {yacht['pdfFile']}")
                print()
            print("-"*80)
            print()
    else:
        print("✅ 중복된 요트가 없습니다!")
    
    # 리포트 생성
    report = generate_duplicate_report(unique_yachts, duplicates, all_yachts)
    
    # 리포트 파일로 저장
    report_file = "yacht_duplicates_report.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n[저장] 리포트 저장: {report_file}")
    print("\n[완료] 중복 확인 완료!")


def generate_duplicate_report(unique_yachts, duplicates, all_yachts):
    """중복 리포트 생성"""
    report = f"""# 요트 데이터 중복 확인 리포트

## 📊 전체 통계

- **총 고유 요트 수**: {len(unique_yachts) + len(duplicates)}개
- **중복 없음**: {len(unique_yachts)}개
- **중복 발견**: {len(duplicates)}개

"""
    
    if duplicates:
        report += "## ⚠️ 중복된 요트\n\n"
        
        for normalized_name, yacht_list in sorted(duplicates.items()):
            report += f"### {yacht_list[0]['name']}\n\n"
            report += f"**정규화된 이름**: `{normalized_name}`\n\n"
            report += f"**발견된 파일 수**: {len(yacht_list)}개\n\n"
            report += "| 파일명 | 요트명 | ID | 제조사 | 비고 |\n"
            report += "|--------|--------|----|----|------|\n"
            
            for yacht in yacht_list:
                name = yacht.get("name", "")
                yacht_id = yacht.get("id", "")
                manufacturer = yacht.get("manufacturer", "")
                pdf_file = yacht.get("pdfFile", "")
                note = f"PDF: {pdf_file}" if pdf_file else ""
                
                report += f"| {yacht['file']} | {name} | {yacht_id or 'N/A'} | {manufacturer or 'N/A'} | {note} |\n"
            
            report += "\n"
    else:
        report += "## ✅ 중복 없음\n\n"
        report += "모든 요트가 고유합니다. 중복이 없습니다.\n\n"
    
    # 파일별 요트 목록
    report += "## 📁 파일별 요트 목록\n\n"
    
    file_yachts = defaultdict(list)
    for normalized_name, yacht_list in all_yachts.items():
        for yacht in yacht_list:
            file_yachts[yacht["file"]].append(yacht["name"])
    
    for file_name, yacht_names in sorted(file_yachts.items()):
        report += f"### {file_name}\n\n"
        report += f"**총 {len(yacht_names)}개 요트**\n\n"
        for name in sorted(set(yacht_names)):
            report += f"- {name}\n"
        report += "\n"
    
    return report


if __name__ == "__main__":
    check_duplicates()

