# -*- coding: utf-8 -*-
"""
Notion API를 사용하여 기존 Notion 데이터베이스 업데이트
"""

import sys
import os
import json
import requests
from datetime import datetime

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Notion API 설정
NOTION_API_KEY = os.getenv('NOTION_API_KEY', '')
NOTION_VERSION = '2022-06-28'

# Notion 데이터베이스 ID (환경변수 또는 직접 입력)
DATABASE_IDS = {
    'yacht_specifications': os.getenv('NOTION_DB_YACHT_SPECS', ''),
    'yacht_parts_database': os.getenv('NOTION_DB_PARTS', ''),
    'yacht_parts_app_data': os.getenv('NOTION_DB_PARTS_APP', ''),
    'registered_yachts': os.getenv('NOTION_DB_REGISTERED', ''),
    'yacht_manual_resources': os.getenv('NOTION_DB_MANUALS', '')
}

headers = {
    'Authorization': f'Bearer {NOTION_API_KEY}',
    'Content-Type': 'application/json',
    'Notion-Version': NOTION_VERSION
}


def check_notion_setup():
    """Notion API 설정 확인"""
    print("=" * 80)
    print("🔧 Notion API 설정 확인")
    print("=" * 80)
    print()
    
    if not NOTION_API_KEY:
        print("❌ NOTION_API_KEY가 설정되지 않았습니다.")
        print()
        print("다음 단계를 따라주세요:")
        print()
        print("1️⃣ Notion Integration 생성:")
        print("   https://www.notion.so/my-integrations")
        print("   → 'New integration' 클릭")
        print("   → 이름: 'HooAah Yacht Chatbot'")
        print("   → Workspace 선택")
        print("   → Submit")
        print()
        print("2️⃣ Internal Integration Token 복사")
        print()
        print("3️⃣ 환경변수 설정:")
        print("   Windows:")
        print("   set NOTION_API_KEY=secret_xxxxxxxxxxxxx")
        print()
        print("   또는 .env 파일 생성:")
        print("   NOTION_API_KEY=secret_xxxxxxxxxxxxx")
        print()
        print("4️⃣ Notion 페이지에서 데이터베이스 연결:")
        print("   → 데이터베이스 열기")
        print("   → 우측 상단 '⋯' → 'Add connections'")
        print("   → 'HooAah Yacht Chatbot' 선택")
        print()
        print("5️⃣ 데이터베이스 ID 가져오기:")
        print("   URL: https://www.notion.so/xxxxx?v=yyyyy")
        print("   데이터베이스 ID = xxxxx")
        print()
        return False
    
    print(f"✅ NOTION_API_KEY: {NOTION_API_KEY[:20]}...")
    print()
    
    # 데이터베이스 ID 확인
    missing_dbs = []
    for db_name, db_id in DATABASE_IDS.items():
        if not db_id:
            missing_dbs.append(db_name)
            print(f"⚠️  {db_name}: ID 없음")
        else:
            print(f"✅ {db_name}: {db_id[:20]}...")
    
    print()
    
    if missing_dbs:
        print("❌ 일부 데이터베이스 ID가 설정되지 않았습니다.")
        print()
        print("환경변수로 설정해주세요:")
        for db_name in missing_dbs:
            env_var = f"NOTION_DB_{db_name.upper().replace('_', '_')}"
            print(f"   set {env_var}=데이터베이스_ID")
        print()
        return False
    
    return True


def query_database(database_id):
    """Notion 데이터베이스 조회"""
    url = f'https://api.notion.com/v1/databases/{database_id}/query'
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ 조회 실패: {response.status_code}")
        print(response.text)
        return None


def create_page(database_id, properties):
    """Notion 페이지 생성"""
    url = 'https://api.notion.com/v1/pages'
    data = {
        'parent': {'database_id': database_id},
        'properties': properties
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ 생성 실패: {response.status_code}")
        print(response.text)
        return None


def update_page(page_id, properties):
    """Notion 페이지 업데이트"""
    url = f'https://api.notion.com/v1/pages/{page_id}'
    data = {'properties': properties}
    
    response = requests.patch(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ 업데이트 실패: {response.status_code}")
        print(response.text)
        return None


def delete_page(page_id):
    """Notion 페이지 삭제 (아카이브)"""
    url = f'https://api.notion.com/v1/pages/{page_id}'
    data = {'archived': True}
    
    response = requests.patch(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ 삭제 실패: {response.status_code}")
        print(response.text)
        return None


def update_yacht_specifications():
    """yacht_specifications.json → Notion 업데이트"""
    print("\n1️⃣ yacht_specifications.json 업데이트 중...")
    
    database_id = DATABASE_IDS['yacht_specifications']
    
    with open("data/yacht_specifications.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 기존 데이터 조회
    existing = query_database(database_id)
    if not existing:
        return
    
    existing_map = {}
    for result in existing.get('results', []):
        yacht_id = result['properties'].get('ID', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')
        if yacht_id:
            existing_map[yacht_id] = result['id']
    
    # 업데이트/생성
    created = 0
    updated = 0
    
    for yacht in data.get('yachts', []):
        yacht_id = yacht.get('id', '')
        specs = yacht.get('yachtSpecs', {}).get('standard', {})
        dims = specs.get('dimensions', {})
        sail = specs.get('sailArea', {})
        engine = specs.get('engine', {})
        
        properties = {
            'ID': {'rich_text': [{'text': {'content': yacht_id}}]},
            'Name': {'title': [{'text': {'content': yacht.get('name', '')}}]},
            'Manufacturer': {'rich_text': [{'text': {'content': yacht.get('manufacturer', '')}}]},
            'Type': {'select': {'name': yacht.get('type', 'Unknown')}},
            'LOA (m)': {'number': extract_number(dims.get('LOA', ''))},
            'Beam (m)': {'number': extract_number(dims.get('Beam', ''))},
            'Draft (m)': {'number': extract_number(dims.get('Draft', ''))},
            'Displacement (kg)': {'number': extract_number(dims.get('Displacement', ''))},
            'Main Sail (m²)': {'number': extract_number(sail.get('mainsail', ''))},
            'Jib Sail (m²)': {'number': extract_number(sail.get('jib', ''))},
            'Engine Type': {'rich_text': [{'text': {'content': engine.get('type', '')}}]},
            'Manual PDF': {'url': yacht.get('manualPDF', '') or None}
        }
        
        if yacht_id in existing_map:
            # 업데이트
            update_page(existing_map[yacht_id], properties)
            updated += 1
        else:
            # 생성
            create_page(database_id, properties)
            created += 1
    
    print(f"   ✅ 생성: {created}개, 업데이트: {updated}개")


def update_yacht_parts_database():
    """yacht_parts_database.json → Notion 업데이트"""
    print("\n2️⃣ yacht_parts_database.json 업데이트 중...")
    
    database_id = DATABASE_IDS['yacht_parts_database']
    
    with open("data/yacht_parts_database.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 기존 데이터 조회
    existing = query_database(database_id)
    if not existing:
        return
    
    existing_map = {}
    for result in existing.get('results', []):
        part_id = result['properties'].get('Part ID', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')
        if part_id:
            existing_map[part_id] = result['id']
    
    # 업데이트/생성
    created = 0
    updated = 0
    
    for yacht in data.get('yachts', []):
        yacht_id = yacht.get('id', '')
        yacht_name = yacht.get('name', '')
        
        for part in yacht.get('parts', []):
            part_id = part.get('id', '')
            
            properties = {
                'Part ID': {'rich_text': [{'text': {'content': part_id}}]},
                'Part Name': {'title': [{'text': {'content': part.get('name', '')}}]},
                'Yacht ID': {'rich_text': [{'text': {'content': yacht_id}}]},
                'Yacht Name': {'rich_text': [{'text': {'content': yacht_name}}]},
                'Category': {'select': {'name': part.get('category', 'Unknown')}},
                'Manufacturer': {'rich_text': [{'text': {'content': part.get('manufacturer', '')}}]},
                'Model': {'rich_text': [{'text': {'content': part.get('model', '')}}]},
            }
            
            interval = part.get('interval', '')
            if interval:
                interval_num = extract_number(interval)
                if interval_num:
                    properties['Maintenance Interval'] = {'number': interval_num}
            
            if part_id in existing_map:
                update_page(existing_map[part_id], properties)
                updated += 1
            else:
                create_page(database_id, properties)
                created += 1
    
    print(f"   ✅ 생성: {created}개, 업데이트: {updated}개")


def extract_number(text):
    """텍스트에서 숫자 추출"""
    if not text:
        return None
    import re
    match = re.search(r'(\d+\.?\d*)', str(text))
    if match:
        try:
            return float(match.group(1))
        except:
            return None
    return None


def setup_interactive():
    """대화형 설정 모드"""
    print()
    print("=" * 80)
    print("🔧 대화형 설정 모드")
    print("=" * 80)
    print()
    
    # API 키 입력
    api_key = input("Notion API Key를 입력하세요: ").strip()
    if not api_key:
        print("❌ API Key가 필요합니다.")
        return False
    
    global NOTION_API_KEY
    NOTION_API_KEY = api_key
    headers['Authorization'] = f'Bearer {api_key}'
    
    print()
    print("다음 데이터베이스 ID를 입력하세요:")
    print("(Skip하려면 엔터)")
    print()
    
    for db_name in DATABASE_IDS.keys():
        db_id = input(f"{db_name}: ").strip()
        if db_id:
            DATABASE_IDS[db_name] = db_id
    
    # .env 파일 생성
    env_content = f"NOTION_API_KEY={api_key}\n"
    for db_name, db_id in DATABASE_IDS.items():
        if db_id:
            env_var = f"NOTION_DB_{db_name.upper()}"
            env_content += f"{env_var}={db_id}\n"
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print()
    print("✅ .env 파일 생성 완료!")
    print()
    
    return True


# 메인 실행
if __name__ == "__main__":
    print()
    print("=" * 80)
    print("📝 Notion 데이터베이스 업데이트")
    print("=" * 80)
    
    # 설정 확인
    if not check_notion_setup():
        print()
        choice = input("대화형 설정을 진행하시겠습니까? (y/n): ").strip().lower()
        if choice == 'y':
            if not setup_interactive():
                sys.exit(1)
        else:
            sys.exit(1)
    
    print()
    print("업데이트를 시작합니다...")
    
    try:
        # 각 데이터베이스 업데이트
        if DATABASE_IDS['yacht_specifications']:
            update_yacht_specifications()
        
        if DATABASE_IDS['yacht_parts_database']:
            update_yacht_parts_database()
        
        # 나머지 데이터베이스도 유사하게 추가 가능
        
        print()
        print("=" * 80)
        print("✅ Notion 업데이트 완료!")
        print("=" * 80)
        print()
        
    except Exception as e:
        print(f"\n❌ 오류: {e}")
        import traceback
        traceback.print_exc()

