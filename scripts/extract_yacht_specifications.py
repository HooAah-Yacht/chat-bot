"""
요트 전체 스펙(크기, 무게, 높이 등) 추출 스크립트
PDF 매뉴얼에서 요트의 상세 스펙을 추출하여 yacht_specifications.json 생성
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional

# UTF-8 인코딩 설정
sys.stdout.reconfigure(encoding='utf-8')

try:
    import pdfplumber
except ImportError:
    print("pdfplumber가 설치되어 있지 않습니다. pip install pdfplumber를 실행하세요.")
    sys.exit(1)


# 20종 요트 정보
YACHT_LIST = [
    {"name": "FarEast 28", "id": "fareast-28", "pdf": "OC15aiiFAREAST28RClassrules-[19458].pdf", "manufacturer": "FarEast Yachts"},
    {"name": "Farr 40", "id": "farr-40", "pdf": "rulebook.pdf", "manufacturer": "Farr Yacht Design"},
    {"name": "Beneteau 473", "id": "beneteau-473", "pdf": "Beneteau 473 Owner's Manual_compressed.pdf", "manufacturer": "Beneteau"},
    {"name": "J/24", "id": "j24", "pdf": "J242019CR220319-[24866].pdf", "manufacturer": "J/Boats"},
    {"name": "Laser", "id": "laser", "pdf": "owners_manual.pdf", "manufacturer": "LaserPerformance"},
    {"name": "Swan 50", "id": "swan-50", "pdf": "ClubSwan50ClassRules07042021-[27210].pdf", "manufacturer": "Nautor's Swan"},
    {"name": "X-35", "id": "x-35", "pdf": "X352012CR080412-[12381].pdf", "manufacturer": "X-Yachts"},
    {"name": "Melges 32", "id": "melges-32", "pdf": "M32_CR_2025-03March-30.pdf", "manufacturer": "Melges Performance Sailboats"},
    {"name": "TP52", "id": "tp52", "pdf": "TP52_CR20220124.pdf", "manufacturer": "Various"},
    {"name": "Beneteau First 36", "id": "beneteau-first-36", "pdf": "2020_03_31_11_03_39-48 owners manual.pdf", "manufacturer": "Beneteau"},
    {"name": "Jeanneau Sun Fast 3300", "id": "jeanneau-sunfast-3300", "pdf": "Sun-Fast-3300-technical-inventory.pdf", "manufacturer": "Jeanneau"},
    {"name": "Dehler 38", "id": "dehler-38", "pdf": "press-manual-dehler38.pdf", "manufacturer": "Dehler"},
    {"name": "X-Yachts XP 44", "id": "xp-44", "pdf": "Xp44-Brochure_July2018_ONLINE.pdf", "manufacturer": "X-Yachts"},
    {"name": "Hanse 458", "id": "hanse-458", "pdf": "Owners-Manual-458-Buch-eng-V8-allg.pdf", "manufacturer": "Hanse Yachts"},
    {"name": "Beneteau Oceanis 46", "id": "beneteau-oceanis-46", "pdf": "14670061006300089_USER_MANUAL_OCEANIS_46.1.pdf", "manufacturer": "Beneteau"},
    {"name": "Nautor Swan 48", "id": "nautor-swan-48", "pdf": "2020_03_31_11_03_39-48 owners manual.pdf", "manufacturer": "Nautor's Swan"},
    {"name": "Grand Soleil GC 42", "id": "grand-soleil-42", "pdf": "GS42LC_Brochure-1.pdf", "manufacturer": "Grand Soleil"},
    {"name": "RS21", "id": "rs21", "pdf": "RS21Riggingguide.pdf", "manufacturer": "RS Sailing"},
    {"name": "J/70", "id": "j70", "pdf": "j70-user-manual.pdf", "manufacturer": "J/Boats"},
    {"name": "Solaris 44", "id": "solaris-44", "pdf": "Solaris-44.pdf", "manufacturer": "Solaris Yachts"}
]


def extract_text_from_pdf(pdf_path: Path, max_pages: int = 20) -> str:
    """PDF에서 텍스트 추출 (처음 max_pages 페이지만)"""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            pages_to_read = min(max_pages, len(pdf.pages))
            for i in range(pages_to_read):
                page = pdf.pages[i]
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"  ⚠️  PDF 읽기 오류 ({pdf_path.name}): {e}")
    return text


def extract_length(text: str) -> Dict[str, Any]:
    """길이 정보 추출 (LOA, LWL)"""
    length_info = {}
    
    # LOA (Length Overall) - 전체 길이
    loa_patterns = [
        r"LOA[\s:]+(\d+\.?\d*)\s*(m|ft|feet)",
        r"Length\s+Overall[\s:]+(\d+\.?\d*)\s*(m|ft|feet)",
        r"Overall\s+Length[\s:]+(\d+\.?\d*)\s*(m|ft|feet)",
        r"길이[\s:]+(\d+\.?\d*)\s*m",
    ]
    
    for pattern in loa_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            unit = match.group(2).lower() if len(match.groups()) > 1 else 'm'
            length_info["loa"] = {"value": value, "unit": unit}
            break
    
    # LWL (Length Waterline) - 수선 길이
    lwl_patterns = [
        r"LWL[\s:]+(\d+\.?\d*)\s*(m|ft|feet)",
        r"Length\s+Waterline[\s:]+(\d+\.?\d*)\s*(m|ft|feet)",
        r"Waterline\s+Length[\s:]+(\d+\.?\d*)\s*(m|ft|feet)",
    ]
    
    for pattern in lwl_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            unit = match.group(2).lower()
            length_info["lwl"] = {"value": value, "unit": unit}
            break
    
    return length_info


def extract_beam(text: str) -> Optional[Dict[str, Any]]:
    """빔/폭 정보 추출"""
    beam_patterns = [
        r"Beam[\s:]+(\d+\.?\d*)\s*(m|ft|feet)",
        r"폭[\s:]+(\d+\.?\d*)\s*m",
        r"Width[\s:]+(\d+\.?\d*)\s*(m|ft|feet)",
    ]
    
    for pattern in beam_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            unit = match.group(2).lower() if len(match.groups()) > 1 else 'm'
            return {"value": value, "unit": unit}
    
    return None


def extract_draft(text: str) -> Optional[Dict[str, Any]]:
    """드래프트/흘수 정보 추출"""
    draft_patterns = [
        r"Draft[\s:]+(\d+\.?\d*)\s*(m|ft|feet)",
        r"흘수[\s:]+(\d+\.?\d*)\s*m",
        r"Draught[\s:]+(\d+\.?\d*)\s*(m|ft|feet)",
    ]
    
    for pattern in draft_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            unit = match.group(2).lower() if len(match.groups()) > 1 else 'm'
            return {"value": value, "unit": unit}
    
    return None


def extract_displacement(text: str) -> Optional[Dict[str, Any]]:
    """배수량 정보 추출"""
    disp_patterns = [
        r"Displacement[\s:]+(\d+[\d,]*\.?\d*)\s*(kg|lbs|tons|t)",
        r"배수량[\s:]+(\d+[\d,]*\.?\d*)\s*(kg|ton)",
    ]
    
    for pattern in disp_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value_str = match.group(1).replace(',', '')
            value = float(value_str)
            unit = match.group(2).lower()
            return {"value": value, "unit": unit}
    
    return None


def extract_sail_area(text: str) -> Optional[Dict[str, Any]]:
    """돛 면적 정보 추출"""
    sail_patterns = [
        r"Sail\s+Area[\s:]+(\d+\.?\d*)\s*(m²|m2|sq\.?m|ft²|sq\.?ft)",
        r"Total\s+Sail\s+Area[\s:]+(\d+\.?\d*)\s*(m²|m2|sq\.?m|ft²|sq\.?ft)",
        r"돛\s*면적[\s:]+(\d+\.?\d*)\s*m",
    ]
    
    for pattern in sail_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            unit = match.group(2) if len(match.groups()) > 1 else 'm²'
            return {"value": value, "unit": unit}
    
    return None


def extract_mast_height(text: str) -> Optional[Dict[str, Any]]:
    """마스트 높이 정보 추출"""
    mast_patterns = [
        r"Mast\s+Height[\s:]+(\d+\.?\d*)\s*(m|ft|feet)",
        r"Air\s+Draft[\s:]+(\d+\.?\d*)\s*(m|ft|feet)",
        r"마스트\s*높이[\s:]+(\d+\.?\d*)\s*m",
    ]
    
    for pattern in mast_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            unit = match.group(2).lower() if len(match.groups()) > 1 else 'm'
            return {"value": value, "unit": unit}
    
    return None


def extract_engine(text: str) -> Optional[str]:
    """엔진 정보 추출"""
    engine_patterns = [
        r"Engine[\s:]+([A-Za-z0-9\s\-]+(?:HP|hp|kW))",
        r"엔진[\s:]+([^\n]+)",
    ]
    
    for pattern in engine_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return None


def extract_fuel_tank(text: str) -> Optional[Dict[str, Any]]:
    """연료 탱크 용량 추출"""
    fuel_patterns = [
        r"Fuel[\s:]+(\d+\.?\d*)\s*(l|liters|gal|gallons)",
        r"Fuel\s+Tank[\s:]+(\d+\.?\d*)\s*(l|liters|gal|gallons)",
        r"연료[\s:]+(\d+\.?\d*)\s*l",
    ]
    
    for pattern in fuel_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            unit = match.group(2).lower()
            return {"value": value, "unit": unit}
    
    return None


def extract_water_tank(text: str) -> Optional[Dict[str, Any]]:
    """물 탱크 용량 추출"""
    water_patterns = [
        r"Water[\s:]+(\d+\.?\d*)\s*(l|liters|gal|gallons)",
        r"Water\s+Tank[\s:]+(\d+\.?\d*)\s*(l|liters|gal|gallons)",
        r"물[\s:]+(\d+\.?\d*)\s*l",
    ]
    
    for pattern in water_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            unit = match.group(2).lower()
            return {"value": value, "unit": unit}
    
    return None


def extract_cabins_berths(text: str) -> Dict[str, Any]:
    """선실 및 침대 수 추출"""
    info = {}
    
    # Cabins
    cabin_patterns = [
        r"Cabins[\s:]+(\d+)",
        r"(\d+)\s+cabins",
        r"선실[\s:]+(\d+)",
    ]
    
    for pattern in cabin_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            info["cabins"] = int(match.group(1))
            break
    
    # Berths
    berth_patterns = [
        r"Berths[\s:]+(\d+)",
        r"(\d+)\s+berths",
        r"침대[\s:]+(\d+)",
    ]
    
    for pattern in berth_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            info["berths"] = int(match.group(1))
            break
    
    return info


def extract_yacht_specifications(yacht_info: Dict[str, str], pdf_dir: Path) -> Dict[str, Any]:
    """단일 요트의 전체 스펙 추출"""
    pdf_path = pdf_dir / yacht_info["pdf"]
    
    print(f"📄 처리 중: {yacht_info['name']} ({yacht_info['pdf']})")
    
    if not pdf_path.exists():
        print(f"  ⚠️  파일 없음: {pdf_path}")
        return create_default_spec(yacht_info)
    
    # PDF에서 텍스트 추출
    text = extract_text_from_pdf(pdf_path)
    
    if not text:
        print(f"  ⚠️  텍스트 추출 실패")
        return create_default_spec(yacht_info)
    
    # 각 스펙 추출
    spec = {
        "id": yacht_info["id"],
        "name": yacht_info["name"],
        "manufacturer": yacht_info["manufacturer"],
        "manual": f"data/yachtpdf/{yacht_info['pdf']}"
    }
    
    # 길이 정보
    length_info = extract_length(text)
    if length_info:
        spec["length"] = length_info
    
    # 빔/폭
    beam = extract_beam(text)
    if beam:
        spec["beam"] = beam
    
    # 드래프트/흘수
    draft = extract_draft(text)
    if draft:
        spec["draft"] = draft
    
    # 배수량
    displacement = extract_displacement(text)
    if displacement:
        spec["displacement"] = displacement
    
    # 돛 면적
    sail_area = extract_sail_area(text)
    if sail_area:
        spec["sailArea"] = sail_area
    
    # 마스트 높이
    mast_height = extract_mast_height(text)
    if mast_height:
        spec["mastHeight"] = mast_height
    
    # 엔진
    engine = extract_engine(text)
    if engine:
        spec["engine"] = engine
    
    # 연료 탱크
    fuel_tank = extract_fuel_tank(text)
    if fuel_tank:
        spec["fuelTank"] = fuel_tank
    
    # 물 탱크
    water_tank = extract_water_tank(text)
    if water_tank:
        spec["waterTank"] = water_tank
    
    # 선실 및 침대
    cabin_info = extract_cabins_berths(text)
    if cabin_info:
        spec.update(cabin_info)
    
    # 추출된 정보 개수 표시
    extracted_count = len([k for k in spec.keys() if k not in ["id", "name", "manufacturer", "manual"]])
    print(f"  ✅ {extracted_count}개 스펙 추출 완료")
    
    return spec


def create_default_spec(yacht_info: Dict[str, str]) -> Dict[str, Any]:
    """기본 스펙 템플릿 생성"""
    return {
        "id": yacht_info["id"],
        "name": yacht_info["name"],
        "manufacturer": yacht_info["manufacturer"],
        "manual": f"data/yachtpdf/{yacht_info['pdf']}",
        "note": "Specifications to be added"
    }


def main():
    """메인 실행 함수"""
    print("=" * 70)
    print("🚤 요트 스펙 추출 시작")
    print("=" * 70)
    
    # 경로 설정
    script_dir = Path(__file__).parent
    backend_dir = script_dir.parent
    pdf_dir = backend_dir / "data" / "yachtpdf"
    output_file = backend_dir / "data" / "yacht_specifications.json"
    
    print(f"\n📂 PDF 디렉토리: {pdf_dir}")
    print(f"💾 출력 파일: {output_file}\n")
    
    if not pdf_dir.exists():
        print(f"❌ PDF 디렉토리가 존재하지 않습니다: {pdf_dir}")
        return
    
    # 모든 요트 스펙 추출
    specifications = []
    
    for i, yacht_info in enumerate(YACHT_LIST, 1):
        print(f"\n[{i}/{len(YACHT_LIST)}] ", end="")
        spec = extract_yacht_specifications(yacht_info, pdf_dir)
        specifications.append(spec)
    
    # JSON 파일로 저장
    output_data = {
        "version": "1.0",
        "description": "20종 세일링 요트 상세 스펙 데이터베이스",
        "lastUpdated": "2024-11-13",
        "yachts": specifications
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 70)
    print(f"✅ 완료! {len(specifications)}개 요트 스펙이 저장되었습니다.")
    print(f"💾 파일 위치: {output_file}")
    print("=" * 70)
    
    # 통계 출력
    total_specs = sum(len([k for k in spec.keys() if k not in ["id", "name", "manufacturer", "manual", "note"]]) 
                     for spec in specifications)
    avg_specs = total_specs / len(specifications) if specifications else 0
    print(f"\n📊 통계:")
    print(f"   - 총 요트 수: {len(specifications)}개")
    print(f"   - 총 추출된 스펙: {total_specs}개")
    print(f"   - 평균 스펙/요트: {avg_specs:.1f}개")


if __name__ == "__main__":
    main()

