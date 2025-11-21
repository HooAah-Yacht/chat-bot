# -*- coding: utf-8 -*-
"""
요트 ID 리스트 추출 스크립트
모든 JSON 파일에서 yacht ID를 추출합니다.
"""

import sys
import json
from pathlib import Path

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def extract_yacht_ids():
    """모든 JSON 파일에서 yacht ID 추출"""
    
    json_files = [
        'data/yacht_specifications.json',
        'data/yacht_parts_database.json',
        'data/yacht_parts_app_data.json',
        'data/yacht_manual_resources.json',
        'data/registered_yachts.json'
    ]
    
    results = {}
    
    for json_file in json_files:
        file_path = Path(json_file)
        
        if not file_path.exists():
            print(f"⚠️  {json_file} 파일을 찾을 수 없습니다.")
            continue
        
        print(f"\n📄 {json_file} 분석 중...")
        print("=" * 80)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        yacht_ids = []
        yachts = data.get('yachts', [])
        
        for yacht in yachts:
            yacht_id = yacht.get('id', '')
            yacht_name = yacht.get('name', 'Unknown')
            
            if yacht_id:
                yacht_ids.append({
                    'id': yacht_id,
                    'name': yacht_name
                })
        
        results[json_file] = yacht_ids
        
        # 결과 출력
        print(f"총 {len(yacht_ids)}개 요트 발견")
        print()
        
        if yacht_ids:
            print("ID 리스트:")
            for item in yacht_ids:
                print(f"  - {item['id']:<30} | {item['name']}")
        else:
            print("  (ID 없음)")
    
    return results


def generate_summary_report(results):
    """요약 보고서 생성"""
    print("\n\n")
    print("=" * 80)
    print("📊 요트 ID 요약 보고서")
    print("=" * 80)
    print()
    
    # 모든 ID 수집
    all_ids = {}
    
    for json_file, yacht_list in results.items():
        for yacht in yacht_list:
            yacht_id = yacht['id']
            yacht_name = yacht['name']
            
            if yacht_id not in all_ids:
                all_ids[yacht_id] = {
                    'name': yacht_name,
                    'files': []
                }
            
            all_ids[yacht_id]['files'].append(json_file)
    
    # ID별로 정렬
    sorted_ids = sorted(all_ids.items())
    
    print(f"총 **{len(sorted_ids)}개** 고유 요트 ID 발견\n")
    
    print("┌─────────────────────────────────┬──────────────────────────────────────┬────────────┐")
    print("│ Yacht ID                        │ Name                                 │ File Count │")
    print("├─────────────────────────────────┼──────────────────────────────────────┼────────────┤")
    
    for yacht_id, info in sorted_ids:
        name = info['name'][:36]  # 36자로 제한
        file_count = len(info['files'])
        print(f"│ {yacht_id:<31} │ {name:<36} │ {file_count:^10} │")
    
    print("└─────────────────────────────────┴──────────────────────────────────────┴────────────┘")
    
    # Python 리스트 형식으로 출력
    print("\n\n📋 Python 리스트 형식:")
    print("=" * 80)
    print("\nyacht_ids = [")
    for yacht_id, info in sorted_ids:
        print(f"    '{yacht_id}',  # {info['name']}")
    print("]")
    
    # JSON 형식으로 출력
    print("\n\n📋 JSON 형식:")
    print("=" * 80)
    print("\n{")
    print('  "yachtIds": [')
    for i, (yacht_id, info) in enumerate(sorted_ids):
        comma = "," if i < len(sorted_ids) - 1 else ""
        print(f'    {{')
        print(f'      "id": "{yacht_id}",')
        print(f'      "name": "{info["name"]}"')
        print(f'    }}{comma}')
    print('  ]')
    print('}')
    
    # 파일별 분포
    print("\n\n📊 파일별 ID 분포:")
    print("=" * 80)
    
    for json_file, yacht_list in results.items():
        filename = Path(json_file).name
        print(f"\n{filename}: {len(yacht_list)}개")
    
    return all_ids


if __name__ == "__main__":
    print()
    print("=" * 80)
    print("🔍 요트 ID 추출 시작")
    print("=" * 80)
    
    results = extract_yacht_ids()
    all_ids = generate_summary_report(results)
    
    print("\n\n✅ 완료!")
    print()

