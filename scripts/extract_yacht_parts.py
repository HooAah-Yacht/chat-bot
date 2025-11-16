import PyPDF2
import json
import re
import os
import sys
from pathlib import Path

# Windows 콘솔 인코딩 문제 해결
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def extract_text_from_pdf(pdf_path):
    """PDF 파일에서 텍스트를 추출합니다."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""

def extract_parts_info(text, yacht_name):
    """텍스트에서 부품 정보를 추출합니다."""
    parts_data = {
        "yacht": yacht_name,
        "rigging": [],
        "sails": [],
        "winches": [],
        "engine": [],
        "electrical": [],
        "plumbing": [],
        "deck": [],
        "navigation": []
    }
    
    # 일반적인 부품 키워드 패턴
    patterns = {
        "rigging": r"(?i)(mast|boom|forestay|backstay|shroud|spreader|tang|chainplate)",
        "sails": r"(?i)(mainsail|genoa|jib|spinnaker|gennaker|sail area)",
        "winches": r"(?i)(winch|halyard winch|sheet winch|primary winch)",
        "engine": r"(?i)(engine|motor|propeller|fuel tank|horsepower|hp|diesel)",
        "electrical": r"(?i)(battery|alternator|solar|panel|light|navigation light)",
        "plumbing": r"(?i)(water tank|holding tank|pump|bilge pump|galley)",
        "deck": r"(?i)(hatch|portlight|cleat|fairlead|track)",
        "navigation": r"(?i)(gps|compass|chartplotter|vhf|radio|depth|wind instrument)"
    }
    
    lines = text.split('\n')
    
    for category, pattern in patterns.items():
        for i, line in enumerate(lines):
            if re.search(pattern, line):
                # 현재 라인과 다음 몇 라인을 확인
                context = ' '.join(lines[i:min(i+3, len(lines))])
                
                # 부품 정보 추출
                part_info = {
                    "description": line.strip(),
                    "context": context.strip()[:200]  # 처음 200자만
                }
                
                # 숫자나 모델명 찾기
                numbers = re.findall(r'\b\d+[\d\.\-/]*\b', line)
                if numbers:
                    part_info["specifications"] = numbers
                
                if part_info not in parts_data[category]:
                    parts_data[category].append(part_info)
    
    return parts_data

def process_pdf_files(pdf_directory):
    """디렉토리의 모든 PDF 파일을 처리합니다."""
    pdf_dir = Path(pdf_directory)
    all_parts = []
    
    # PDF 파일과 요트 이름 매핑
    pdf_yacht_mapping = {
        "14670061006300089_USER_MANUAL_OCEANIS_46.1.pdf": "Beneteau Oceanis 46",
        "2020_03_31_11_03_39-48 owners manual.pdf": "Nautor Swan 48",
        "Beneteau 473 Owner's Manual_compressed.pdf": "Beneteau 473",
        "ClubSwan50ClassRules07042021-[27210].pdf": "Swan 50",
        "GS42LC_Brochure-1.pdf": "Grand Soleil GC 42",
        "J242019CR220319-[24866].pdf": "J/24",
        "j70-user-manual.pdf": "J/70",
        "M32_CR_2025-03March-30.pdf": "Melges 32",
        "OC15aiiFAREAST28RClassrules-[19458].pdf": "FarEast 28",
        "Owners-Manual-458-Buch-eng-V8-allg.pdf": "Hanse 458",
        "press-manual-dehler38.pdf": "Dehler 38",
        "RS21Riggingguide.pdf": "RS21",
        "Solaris-44.pdf": "Solaris 44",
        "Sun-Fast-3300-technical-inventory.pdf": "Jeanneau Sun Fast 3300",
        "TP52_CR20220124.pdf": "TP52",
        "Xp44-Brochure_July2018_ONLINE.pdf": "X-Yachts XP 44"
    }
    
    for pdf_file in pdf_dir.glob("*.pdf"):
        filename = pdf_file.name
        yacht_name = pdf_yacht_mapping.get(filename, filename.replace('.pdf', ''))
        
        print(f"\n처리 중: {yacht_name}")
        print(f"파일: {filename}")
        
        text = extract_text_from_pdf(pdf_file)
        
        if text:
            parts_info = extract_parts_info(text, yacht_name)
            all_parts.append(parts_info)
            print(f"  ✓ 텍스트 추출 완료 ({len(text)} 문자)")
        else:
            print(f"  ✗ 텍스트 추출 실패")
    
    return all_parts

def save_parts_to_json(parts_data, output_file="extracted_yacht_parts.json"):
    """추출된 부품 정보를 JSON 파일로 저장합니다."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(parts_data, f, indent=2, ensure_ascii=False)
    print(f"\n✓ 부품 정보가 {output_file}에 저장되었습니다.")

if __name__ == "__main__":
    # 스크립트 파일의 디렉토리를 기준으로 경로 찾기
    script_dir = Path(__file__).parent
    pdf_directory = script_dir / "yachtpdf"
    
    print("=" * 60)
    print("요트 매뉴얼 PDF 부품 추출 스크립트")
    print("=" * 60)
    print(f"PDF 디렉토리: {pdf_directory}")
    
    # PDF 파일 처리
    all_parts = process_pdf_files(pdf_directory)
    
    # JSON 파일로 저장
    output_file = script_dir / "extracted_yacht_parts.json"
    save_parts_to_json(all_parts, output_file)
    
    print("\n" + "=" * 60)
    print(f"총 {len(all_parts)}개의 요트 매뉴얼 처리 완료")
    print("=" * 60)

