# -*- coding: utf-8 -*-
"""
JSON 데이터를 Notion 형식으로 변환
- Notion에 붙여넣기 가능한 CSV 생성
- Notion Database 형식 마크다운 생성
"""

import sys
import os
import json
import csv
from datetime import datetime

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# 출력 디렉토리
OUTPUT_DIR = "notion_export"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 80)
print("📝 JSON → Notion 변환 스크립트")
print("=" * 80)
print()


def export_yacht_specifications():
    """yacht_specifications.json → Notion CSV"""
    print("1️⃣ yacht_specifications.json 변환 중...")
    
    with open("data/yacht_specifications.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # CSV 생성
    csv_file = os.path.join(OUTPUT_DIR, "yacht_specifications.csv")
    
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        
        # 헤더
        writer.writerow([
            "ID", "Name", "Manufacturer", "Type", "Schema Version",
            "LOA (m)", "Beam (m)", "Draft (m)", "Displacement (kg)",
            "Main Sail (m²)", "Jib Sail (m²)", "Spinnaker (m²)",
            "Engine Type", "Engine Power", "Manual PDF", "Updated At"
        ])
        
        # 데이터
        for yacht in data.get('yachts', []):
            specs = yacht.get('yachtSpecs', {}).get('standard', {})
            dims = specs.get('dimensions', {})
            sail = specs.get('sailArea', {})
            engine = specs.get('engine', {})
            
            writer.writerow([
                yacht.get('id', ''),
                yacht.get('name', ''),
                yacht.get('manufacturer', ''),
                yacht.get('type', ''),
                yacht.get('schemaVersion', ''),
                extract_value(dims.get('LOA', '')),
                extract_value(dims.get('Beam', '')),
                extract_value(dims.get('Draft', '')),
                extract_value(dims.get('Displacement', '')),
                extract_value(sail.get('mainsail', '')),
                extract_value(sail.get('jib', '')),
                extract_value(sail.get('spinnaker', '')),
                engine.get('type', ''),
                engine.get('power', ''),
                yacht.get('manualPDF', ''),
                yacht.get('updatedAt', '')
            ])
    
    print(f"   ✅ 생성: {csv_file}")
    print(f"   📊 요트: {len(data.get('yachts', []))}척")


def export_yacht_parts_database():
    """yacht_parts_database.json → Notion CSV"""
    print("\n2️⃣ yacht_parts_database.json 변환 중...")
    
    with open("data/yacht_parts_database.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # CSV 생성
    csv_file = os.path.join(OUTPUT_DIR, "yacht_parts_database.csv")
    
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        
        # 헤더
        writer.writerow([
            "Yacht ID", "Yacht Name", "Part ID", "Part Name", 
            "Category", "Manufacturer", "Model", 
            "Maintenance Interval", "Specifications"
        ])
        
        # 데이터
        total_parts = 0
        for yacht in data.get('yachts', []):
            yacht_id = yacht.get('id', '')
            yacht_name = yacht.get('name', '')
            
            for part in yacht.get('parts', []):
                specs = part.get('specifications', {})
                specs_str = json.dumps(specs, ensure_ascii=False) if specs else ''
                
                writer.writerow([
                    yacht_id,
                    yacht_name,
                    part.get('id', ''),
                    part.get('name', ''),
                    part.get('category', ''),
                    part.get('manufacturer', ''),
                    part.get('model', ''),
                    part.get('interval', ''),
                    specs_str[:200]  # 200자로 제한
                ])
                total_parts += 1
    
    print(f"   ✅ 생성: {csv_file}")
    print(f"   📦 부품: {total_parts}개")


def export_yacht_parts_app_data():
    """yacht_parts_app_data.json → Notion CSV"""
    print("\n3️⃣ yacht_parts_app_data.json 변환 중...")
    
    with open("data/yacht_parts_app_data.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # CSV 생성
    csv_file = os.path.join(OUTPUT_DIR, "yacht_parts_app_data.csv")
    
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        
        # 헤더
        writer.writerow([
            "Yacht ID", "Yacht Name", "Part ID", "Part Name",
            "Category", "Manufacturer", "Interval (months)"
        ])
        
        # 데이터
        total_parts = 0
        for yacht in data.get('yachts', []):
            for part in yacht.get('parts', []):
                writer.writerow([
                    yacht.get('id', ''),
                    yacht.get('name', ''),
                    part.get('id', ''),
                    part.get('name', ''),
                    part.get('category', ''),
                    part.get('manufacturer', ''),
                    part.get('interval', '')
                ])
                total_parts += 1
    
    print(f"   ✅ 생성: {csv_file}")
    print(f"   📱 앱용 부품: {total_parts}개")


def export_registered_yachts():
    """registered_yachts.json → Notion CSV"""
    print("\n4️⃣ registered_yachts.json 변환 중...")
    
    with open("data/registered_yachts.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # CSV 생성
    csv_file = os.path.join(OUTPUT_DIR, "registered_yachts.csv")
    
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        
        # 헤더
        writer.writerow([
            "Registration Date", "Yacht Name", "Manufacturer",
            "Source", "PDF File", "Parts Count", "Status"
        ])
        
        # 데이터
        for entry in data.get('yachts', []):
            reg_data = entry.get('registrationData', {})
            basic_info = reg_data.get('basicInfo', {})
            parts = reg_data.get('parts', [])
            
            writer.writerow([
                entry.get('registrationDate', ''),
                basic_info.get('name', ''),
                basic_info.get('manufacturer', ''),
                entry.get('source', ''),
                entry.get('pdfFile', ''),
                len(parts),
                entry.get('analysisResult', {}).get('analysisStatus', '')
            ])
    
    print(f"   ✅ 생성: {csv_file}")
    print(f"   📝 등록: {len(data.get('yachts', []))}개")


def export_yacht_manual_resources():
    """yacht_manual_resources.json → Notion CSV"""
    print("\n5️⃣ yacht_manual_resources.json 변환 중...")
    
    with open("data/yacht_manual_resources.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # CSV 생성
    csv_file = os.path.join(OUTPUT_DIR, "yacht_manual_resources.csv")
    
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        
        # 헤더
        writer.writerow([
            "Yacht Model", "Manufacturer", "Manual PDF",
            "Document Type", "Can Analyze", "Updated At"
        ])
        
        # 데이터
        for resource in data.get('resources', []):
            writer.writerow([
                resource.get('yachtModel', ''),
                resource.get('manufacturer', ''),
                resource.get('manualPDF', ''),
                resource.get('documentType', ''),
                'Yes' if resource.get('canAnalyze') else 'No',
                resource.get('updatedAt', '')
            ])
    
    print(f"   ✅ 생성: {csv_file}")
    print(f"   📚 매뉴얼: {len(data.get('resources', []))}개")


def extract_value(text):
    """텍스트에서 숫자만 추출"""
    if not text:
        return ''
    import re
    match = re.search(r'(\d+\.?\d*)', str(text))
    return match.group(1) if match else text


def create_notion_import_guide():
    """Notion 가져오기 가이드 생성"""
    guide = """# Notion 가져오기 가이드

## 📥 CSV 파일 가져오기

### 1. yacht_specifications.csv
1. Notion에서 새 데이터베이스 생성
2. 우측 상단 `⋯` → `Import` 클릭
3. `yacht_specifications.csv` 선택
4. 데이터 확인 후 완료

**컬럼:**
- ID (Text)
- Name (Title)
- Manufacturer (Text)
- Type (Select)
- LOA, Beam, Draft, Displacement (Number)
- Main Sail, Jib Sail, Spinnaker (Number)
- Engine Type, Engine Power (Text)
- Manual PDF (URL)
- Updated At (Date)

### 2. yacht_parts_database.csv
**용도:** 전체 부품 데이터베이스

**컬럼:**
- Yacht ID, Yacht Name (Relation)
- Part ID (Text)
- Part Name (Title)
- Category (Select)
- Manufacturer (Text)
- Maintenance Interval (Number)

### 3. yacht_parts_app_data.csv
**용도:** 모바일 앱용 간소화 데이터

**컬럼:**
- Part ID, Part Name (Title)
- Category (Multi-select)
- Interval (Number)

### 4. registered_yachts.csv
**용도:** 사용자 등록 이력

**컬럼:**
- Registration Date (Date)
- Yacht Name (Title)
- Source (Select)
- Parts Count (Number)
- Status (Select)

### 5. yacht_manual_resources.csv
**용도:** 매뉴얼 다운로드 정보

**컬럼:**
- Yacht Model (Title)
- Manufacturer (Text)
- Manual PDF (Files & media)
- Document Type (Select)
- Can Analyze (Checkbox)

---

## 🔄 데이터 업데이트 방법

### 자동 업데이트:
```bash
cd chat-bot
python export_to_notion.py
```

### 수동 업데이트:
1. CSV 파일 다운로드 (`notion_export/`)
2. Notion에서 기존 데이터베이스 열기
3. `⋯` → `Merge with CSV` 선택
4. ID 기준으로 병합

---

## 📊 Notion 데이터베이스 뷰 추천

### yacht_specifications
- **Table View**: 전체 데이터
- **Gallery View**: 요트 이미지 + 기본 정보
- **Board View**: Type별 그룹화

### yacht_parts_database
- **Table View**: 전체 부품 목록
- **Board View**: Category별 그룹화
- **Timeline View**: Maintenance Interval 기준

---

## ✅ 완료!

모든 CSV 파일이 `notion_export/` 폴더에 생성되었습니다.

Notion에서 Import 후 자유롭게 수정하세요! 🎉
"""
    
    with open(os.path.join(OUTPUT_DIR, "NOTION_IMPORT_GUIDE.md"), 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print(f"\n📖 가이드 생성: {OUTPUT_DIR}/NOTION_IMPORT_GUIDE.md")


# 실행
if __name__ == "__main__":
    try:
        export_yacht_specifications()
        export_yacht_parts_database()
        export_yacht_parts_app_data()
        export_registered_yachts()
        export_yacht_manual_resources()
        create_notion_import_guide()
        
        print()
        print("=" * 80)
        print("✅ 모든 CSV 생성 완료!")
        print("=" * 80)
        print()
        print(f"📁 출력 위치: {OUTPUT_DIR}/")
        print()
        print("다음 단계:")
        print("1. Notion에서 새 데이터베이스 생성")
        print("2. CSV 파일 Import")
        print("3. NOTION_IMPORT_GUIDE.md 참조")
        print()
        
    except Exception as e:
        print(f"\n❌ 오류: {e}")
        import traceback
        traceback.print_exc()

