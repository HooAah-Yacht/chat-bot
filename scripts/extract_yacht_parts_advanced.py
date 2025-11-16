"""
고급 요트 부품 추출 스크립트
PDF 매뉴얼에서 부품 정보를 추출하여 yacht_parts_database.json 형식으로 저장
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any

# Windows 콘솔 인코딩 문제 해결 (먼저 설정)
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# PDF 라이브러리 import (여러 옵션 지원)
try:
    import pdfplumber
    PDF_LIBRARY = "pdfplumber"
    print("[OK] pdfplumber 사용")
except ImportError:
    try:
        import PyPDF2
        PDF_LIBRARY = "PyPDF2"
        print("[OK] PyPDF2 사용")
    except ImportError:
        print("[ERROR] PDF 라이브러리가 설치되지 않았습니다.")
        print("설치: pip install pdfplumber")
        print("또는: pip install PyPDF2")
        sys.exit(1)

# 요트 매핑 정보
YACHT_MAPPING = {
    "14670061006300089_USER_MANUAL_OCEANIS_46.1.pdf": {
        "id": "beneteau-oceanis-46",
        "name": "Beneteau Oceanis 46.1",
        "manufacturer": "Beneteau"
    },
    "2020_03_31_11_03_39-48 owners manual.pdf": {
        "id": "nautor-swan-48",
        "name": "Nautor Swan 48",
        "manufacturer": "Nautor's Swan"
    },
    "Beneteau 473 Owner's Manual_compressed.pdf": {
        "id": "beneteau-473",
        "name": "Beneteau 473",
        "manufacturer": "Beneteau"
    },
    "ClubSwan50ClassRules07042021-[27210].pdf": {
        "id": "swan-50",
        "name": "Swan 50",
        "manufacturer": "Nautor's Swan"
    },
    "GS42LC_Brochure-1.pdf": {
        "id": "grand-soleil-gc42",
        "name": "Grand Soleil GC 42",
        "manufacturer": "Grand Soleil"
    },
    "J242019CR220319-[24866].pdf": {
        "id": "j24",
        "name": "J/24",
        "manufacturer": "J/Boats"
    },
    "j70-user-manual.pdf": {
        "id": "j70",
        "name": "J/70",
        "manufacturer": "J/Boats"
    },
    "M32_CR_2025-03March-30.pdf": {
        "id": "melges-32",
        "name": "Melges 32",
        "manufacturer": "Melges Performance Sailboats"
    },
    "OC15aiiFAREAST28RClassrules-[19458].pdf": {
        "id": "fareast-28",
        "name": "FarEast 28",
        "manufacturer": "FarEast Yachts"
    },
    "Owners-Manual-458-Buch-eng-V8-allg.pdf": {
        "id": "hanse-458",
        "name": "Hanse 458",
        "manufacturer": "Hanse Yachts"
    },
    "press-manual-dehler38.pdf": {
        "id": "dehler-38",
        "name": "Dehler 38",
        "manufacturer": "Dehler Yachts"
    },
    "RS21Riggingguide.pdf": {
        "id": "rs21",
        "name": "RS21",
        "manufacturer": "RS Sailing"
    },
    "Solaris-44.pdf": {
        "id": "solaris-44",
        "name": "Solaris 44",
        "manufacturer": "Solaris Yachts"
    },
    "Sun-Fast-3300-technical-inventory.pdf": {
        "id": "jeanneau-sun-fast-3300",
        "name": "Jeanneau Sun Fast 3300",
        "manufacturer": "Jeanneau"
    },
    "TP52_CR20220124.pdf": {
        "id": "tp52",
        "name": "TP52",
        "manufacturer": "Various"
    },
    "Xp44-Brochure_July2018_ONLINE.pdf": {
        "id": "x-yachts-xp44",
        "name": "X-Yachts XP 44",
        "manufacturer": "X-Yachts"
    }
}

# 부품 키워드 패턴 (더 정교하게)
PART_PATTERNS = {
    "rigging": {
        "keywords": [
            r"(?i)\bmast\b",
            r"(?i)\bboom\b",
            r"(?i)\bforestay\b",
            r"(?i)\bbackstay\b",
            r"(?i)\bshroud[s]?\b",
            r"(?i)\bspreader[s]?\b",
            r"(?i)\brigging\b",
            r"(?i)\bstay[s]?\b",
            r"(?i)\bspinnaker pole\b"
        ],
        "specs": [r"(\d+\.?\d*)\s*(m|meter|metre|ft|feet)", r"(\d+)\s*(kg|lb)"]
    },
    "sails": {
        "keywords": [
            r"(?i)\bmainsail\b",
            r"(?i)\bgenoa\b",
            r"(?i)\bjib\b",
            r"(?i)\bspinnaker\b",
            r"(?i)\bgennaker\b",
            r"(?i)\bsail\s+area\b",
            r"(?i)\bcode\s+zero\b"
        ],
        "specs": [r"(\d+\.?\d*)\s*(m²|m2|sq\.?\s*m|sqm)", r"(\d+\.?\d*)\s*(ft²|ft2|sq\.?\s*ft)"]
    },
    "winches": {
        "keywords": [
            r"(?i)\bwinch(es)?\b",
            r"(?i)\bprimary\s+winch\b",
            r"(?i)\bhalyard\s+winch\b",
            r"(?i)\bsheet\s+winch\b",
            r"(?i)\bself[-\s]?tailing\b"
        ],
        "specs": [r"(\d+)\s*(ST|est)", r"Harken|Lewmar|Andersen|Antal"]
    },
    "engine": {
        "keywords": [
            r"(?i)\bengine\b",
            r"(?i)\bmotor\b",
            r"(?i)\bdiesel\b",
            r"(?i)\bpropeller\b",
            r"(?i)\bfuel\s+tank\b"
        ],
        "specs": [
            r"(\d+)\s*(hp|HP|cv|CV|kW)",
            r"Yanmar|Volvo\s+Penta|Westerbeke|Beta",
            r"(\d+)\s*(liter|litre|l|gal|gallon)"
        ]
    },
    "electrical": {
        "keywords": [
            r"(?i)\bbattery\b",
            r"(?i)\balternator\b",
            r"(?i)\bsolar\s+panel\b",
            r"(?i)\bnavigation\s+light[s]?\b",
            r"(?i)\belectrical\b"
        ],
        "specs": [r"(\d+)\s*(V|v|volt)", r"(\d+)\s*(Ah|ah|amp)"]
    },
    "deck": {
        "keywords": [
            r"(?i)\bhatch(es)?\b",
            r"(?i)\bportlight[s]?\b",
            r"(?i)\bcleat[s]?\b",
            r"(?i)\bfairlead[s]?\b",
            r"(?i)\btrack[s]?\b",
            r"(?i)\bfurler\b"
        ],
        "specs": []
    },
    "navigation": {
        "keywords": [
            r"(?i)\bGPS\b",
            r"(?i)\bcompass\b",
            r"(?i)\bchartplotter\b",
            r"(?i)\bVHF\b",
            r"(?i)\bradio\b",
            r"(?i)\bdepth\s+(sounder|gauge)\b",
            r"(?i)\bwind\s+instrument[s]?\b",
            r"(?i)\bautopilot\b"
        ],
        "specs": [r"Garmin|Raymarine|B&G|Simrad|Furuno"]
    },
    "plumbing": {
        "keywords": [
            r"(?i)\bwater\s+tank\b",
            r"(?i)\bholding\s+tank\b",
            r"(?i)\bbilge\s+pump\b",
            r"(?i)\bpump\b"
        ],
        "specs": [r"(\d+)\s*(liter|litre|l|gal|gallon)"]
    }
}


def extract_text_pdfplumber(pdf_path: Path) -> str:
    """pdfplumber를 사용하여 PDF에서 텍스트 추출"""
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        print(f"      [ERROR] pdfplumber 오류: {e}")
        return ""


def extract_text_pypdf2(pdf_path: Path) -> str:
    """PyPDF2를 사용하여 PDF에서 텍스트 추출"""
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        print(f"      [ERROR] PyPDF2 오류: {e}")
        return ""


def extract_text_from_pdf(pdf_path: Path) -> str:
    """PDF에서 텍스트 추출 (사용 가능한 라이브러리 사용)"""
    if PDF_LIBRARY == "pdfplumber":
        return extract_text_pdfplumber(pdf_path)
    else:
        return extract_text_pypdf2(pdf_path)


def extract_specs(text: str, spec_patterns: List[str]) -> List[str]:
    """텍스트에서 사양 정보 추출"""
    specs = []
    for pattern in spec_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            for match in matches:
                if isinstance(match, tuple):
                    spec = ' '.join(str(m) for m in match if m)
                else:
                    spec = str(match)
                if spec and spec not in specs:
                    specs.append(spec)
    return specs[:5]  # 최대 5개만


def find_parts_in_text(text: str, category: str, pattern_info: Dict) -> List[Dict[str, Any]]:
    """텍스트에서 특정 카테고리의 부품 찾기"""
    parts = []
    lines = text.split('\n')
    
    for keyword_pattern in pattern_info['keywords']:
        for i, line in enumerate(lines):
            if re.search(keyword_pattern, line) and len(line.strip()) > 5:
                # 컨텍스트: 현재 라인과 앞뒤 2줄
                start = max(0, i - 1)
                end = min(len(lines), i + 3)
                context = ' '.join(lines[start:end])
                
                # 사양 추출
                specs = extract_specs(context, pattern_info['specs'])
                
                # 부품 정보 생성
                part = {
                    "name": line.strip()[:100],  # 최대 100자
                    "description": context.strip()[:300],  # 최대 300자
                }
                
                if specs:
                    part["specifications"] = specs
                
                # 중복 방지
                if not any(p["name"] == part["name"] for p in parts):
                    parts.append(part)
                    
                    if len(parts) >= 10:  # 카테고리당 최대 10개
                        return parts
    
    return parts


def extract_yacht_dimensions(text: str) -> Dict[str, Any]:
    """요트 기본 치수 정보 추출"""
    dimensions = {}
    
    # LOA (Length Overall)
    loa_match = re.search(r"(?i)LOA|length\s+overall[\s:]+(\d+\.?\d*)\s*(m|ft)", text)
    if loa_match:
        dimensions["loa"] = f"{loa_match.group(1)} {loa_match.group(2)}"
    
    # Beam
    beam_match = re.search(r"(?i)beam[\s:]+(\d+\.?\d*)\s*(m|ft)", text)
    if beam_match:
        dimensions["beam"] = f"{beam_match.group(1)} {beam_match.group(2)}"
    
    # Draft
    draft_match = re.search(r"(?i)draft[\s:]+(\d+\.?\d*)\s*(m|ft)", text)
    if draft_match:
        dimensions["draft"] = f"{draft_match.group(1)} {draft_match.group(2)}"
    
    # Displacement
    disp_match = re.search(r"(?i)displacement[\s:]+(\d+\.?\d*)\s*(kg|lbs)", text)
    if disp_match:
        dimensions["displacement"] = f"{disp_match.group(1)} {disp_match.group(2)}"
    
    return dimensions


def process_single_pdf(pdf_path: Path, yacht_info: Dict) -> Dict[str, Any]:
    """단일 PDF 파일 처리"""
    print(f"\n{'='*60}")
    print(f"[PDF] 처리 중: {yacht_info['name']}")
    print(f"      파일: {pdf_path.name}")
    
    # PDF 텍스트 추출
    text = extract_text_from_pdf(pdf_path)
    
    if not text or len(text) < 100:
        print(f"      [WARN] 텍스트 추출 실패 또는 내용 부족 ({len(text)} 문자)")
        return None
    
    print(f"      [OK] 텍스트 추출 완료 ({len(text):,} 문자)")
    
    # 요트 정보 생성
    yacht_data = {
        "id": yacht_info["id"],
        "name": yacht_info["name"],
        "manufacturer": yacht_info["manufacturer"],
        "manualPDF": f"yachtpdf/{pdf_path.name}",
        "parts": {}
    }
    
    # 치수 정보 추출
    dimensions = extract_yacht_dimensions(text)
    if dimensions:
        yacht_data["dimensions"] = dimensions
        print(f"      [OK] 치수 정보: {len(dimensions)}개 항목")
    
    # 각 카테고리별 부품 추출
    total_parts = 0
    for category, pattern_info in PART_PATTERNS.items():
        parts = find_parts_in_text(text, category, pattern_info)
        if parts:
            yacht_data["parts"][category] = parts
            total_parts += len(parts)
            print(f"      [OK] {category}: {len(parts)}개 부품")
    
    print(f"      [DONE] 총 {total_parts}개 부품 추출 완료")
    
    return yacht_data


def process_all_pdfs(pdf_directory: Path) -> List[Dict[str, Any]]:
    """모든 PDF 파일 처리"""
    all_yacht_data = []
    
    print("\n" + "="*60)
    print("요트 매뉴얼 PDF 부품 추출 시작")
    print("="*60)
    
    processed_count = 0
    for pdf_file in sorted(pdf_directory.glob("*.pdf")):
        filename = pdf_file.name
        
        if filename in YACHT_MAPPING:
            yacht_info = YACHT_MAPPING[filename]
            yacht_data = process_single_pdf(pdf_file, yacht_info)
            
            if yacht_data:
                all_yacht_data.append(yacht_data)
                processed_count += 1
        else:
            print(f"\n[WARN] 매핑 정보 없음: {filename}")
    
    print("\n" + "="*60)
    print(f"[COMPLETE] 처리 완료: {processed_count}개 요트")
    print("="*60)
    
    return all_yacht_data


def merge_with_existing_database(extracted_data: List[Dict], existing_file: Path) -> Dict:
    """추출된 데이터를 기존 데이터베이스와 병합"""
    try:
        with open(existing_file, 'r', encoding='utf-8') as f:
            existing_db = json.load(f)
    except FileNotFoundError:
        existing_db = {"yachts": []}
    
    # 기존 요트 ID 목록
    existing_ids = {yacht["id"] for yacht in existing_db.get("yachts", [])}
    
    # 새로운 데이터 병합
    for new_yacht in extracted_data:
        yacht_id = new_yacht["id"]
        
        # 기존 요트 찾기
        existing_yacht = next(
            (y for y in existing_db["yachts"] if y["id"] == yacht_id),
            None
        )
        
        if existing_yacht:
            # 부품 정보 병합
            if "parts" in new_yacht:
                if "parts" not in existing_yacht:
                    existing_yacht["parts"] = {}
                
                for category, parts in new_yacht["parts"].items():
                    if category not in existing_yacht["parts"]:
                        existing_yacht["parts"][category] = []
                    existing_yacht["parts"][category].extend(parts)
            
            # 치수 정보 업데이트
            if "dimensions" in new_yacht:
                existing_yacht["dimensions"] = new_yacht["dimensions"]
        else:
            # 새 요트 추가
            existing_db["yachts"].append(new_yacht)
    
    return existing_db


def save_to_json(data: Dict, output_file: Path):
    """JSON 파일로 저장"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n[SAVE] 저장 완료: {output_file}")
    print(f"       총 요트: {len(data.get('yachts', []))}개")


def main():
    """메인 실행 함수"""
    # 경로 설정
    script_dir = Path(__file__).parent
    pdf_dir = script_dir / "yachtpdf"
    
    if not pdf_dir.exists():
        print(f"[ERROR] PDF 디렉토리를 찾을 수 없습니다: {pdf_dir}")
        return
    
    # PDF 처리
    extracted_data = process_all_pdfs(pdf_dir)
    
    if not extracted_data:
        print("\n[WARN] 추출된 데이터가 없습니다.")
        return
    
    # 기존 데이터베이스와 병합
    database_file = script_dir / "yacht_parts_database.json"
    merged_db = merge_with_existing_database(extracted_data, database_file)
    
    # 저장
    save_to_json(merged_db, database_file)
    
    # 추출된 원본 데이터도 별도 저장
    extracted_file = script_dir / "extracted_yacht_parts_detailed.json"
    save_to_json({"yachts": extracted_data}, extracted_file)
    
    print("\n" + "="*60)
    print("모든 작업 완료!")
    print("="*60)


if __name__ == "__main__":
    main()

