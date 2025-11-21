# -*- coding: utf-8 -*-
"""
AI Chatbot MySQL 연결 테스트 및 초기 설정
"""

import sys
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

from yacht_db_connector import YachtDatabaseConnector


def test_connection():
    """MySQL 연결 테스트"""
    print("=" * 80)
    print("🔍 MySQL 연결 테스트")
    print("=" * 80)
    print()
    
    # .env 파일에서 읽기
    host = os.getenv('DB_HOST', 'localhost')
    port = int(os.getenv('DB_PORT', 3306))
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '')
    database = os.getenv('DB_NAME', 'HooYah')
    
    print("📋 연결 정보:")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   User: {user}")
    print(f"   Password: {'*' * len(password) if password else '(없음)'}")
    print(f"   Database: {database}")
    print()
    
    # 연결 시도
    connector = YachtDatabaseConnector(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    
    if not connector.connect():
        print()
        print("❌ 연결 실패!")
        print()
        print("문제 해결 방법:")
        print("1. MySQL 서버가 실행 중인지 확인")
        print("2. .env 파일의 DB_PASSWORD가 정확한지 확인")
        print("3. HooYah 데이터베이스가 존재하는지 확인:")
        print("   mysql -u root -p")
        print("   SHOW DATABASES;")
        return False
    
    # 데이터베이스 확인
    print()
    print("📊 데이터베이스 테이블:")
    
    try:
        with connector.conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if tables:
                for table in tables:
                    table_name = list(table.values())[0]
                    cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
                    count = cursor.fetchone()['count']
                    print(f"   ✅ {table_name} ({count}개 레코드)")
            else:
                print("   ⚠️  테이블 없음")
    except Exception as e:
        print(f"   ❌ 오류: {e}")
    
    print()
    
    # yacht 테이블 확인
    print("🚢 yacht 테이블 조회:")
    yachts = connector.get_all_yachts()
    
    if yachts:
        print(f"   총 {len(yachts)}개 요트 발견")
        for yacht in yachts[:5]:
            print(f"   - ID: {yacht['id']}, Name: {yacht.get('name', 'N/A')}, NickName: {yacht.get('nickName', 'N/A')}")
        
        if len(yachts) > 5:
            print(f"   ... 외 {len(yachts) - 5}개")
    else:
        print("   ℹ️  요트 데이터 없음 (JSON 데이터를 마이그레이션하세요)")
    
    print()
    connector.disconnect()
    
    return True


def check_yacht_table_structure():
    """yacht 테이블 구조 확인"""
    print()
    print("=" * 80)
    print("📋 yacht 테이블 구조 확인")
    print("=" * 80)
    print()
    
    connector = YachtDatabaseConnector(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'HooYah')
    )
    
    if not connector.connect():
        return
    
    try:
        with connector.conn.cursor() as cursor:
            cursor.execute("DESCRIBE yacht")
            columns = cursor.fetchall()
            
            print("컬럼 정보:")
            for col in columns:
                nullable = "NULL" if col['Null'] == 'YES' else "NOT NULL"
                print(f"   - {col['Field']:<20} {col['Type']:<20} {nullable}")
            
            print()
            print("⚠️  주의사항:")
            print("   Backend의 Yacht.java Entity는 현재:")
            print("   - id, name, nickName만 가지고 있음")
            print()
            print("   AI가 저장하려는 필드:")
            print("   - available, capacity, description, location,")
            print("     price_per_hour, thumbnail_path, created_at, updated_at")
            print()
            print("   → Backend Entity를 확장하거나 AI 전용 테이블을 만들어야 합니다!")
            
    except Exception as e:
        print(f"❌ 오류: {e}")
    
    connector.disconnect()


if __name__ == "__main__":
    print()
    print("=" * 80)
    print("🚢 HooAah Yacht - MySQL 연결 설정")
    print("=" * 80)
    print()
    
    # .env 파일 확인
    if not os.path.exists('.env'):
        print("❌ .env 파일이 없습니다!")
        print()
        print(".env 파일이 생성되었습니다. 내용을 확인하세요:")
        print()
        print("=" * 80)
        with open('.env', 'r', encoding='utf-8') as f:
            print(f.read())
        print("=" * 80)
        print()
    
    # 연결 테스트
    if test_connection():
        print()
        choice = input("yacht 테이블 구조를 확인하시겠습니까? (y/n): ").strip().lower()
        
        if choice == 'y':
            check_yacht_table_structure()
        
        print()
        print("=" * 80)
        print("✅ 설정 완료!")
        print("=" * 80)
        print()
        print("다음 단계:")
        print("1. JSON 데이터를 DB로 마이그레이션:")
        print("   python yacht_db_connector.py")
        print("   → 선택: 2")
        print()
        print("2. AI Chatbot에서 DB 조회 테스트:")
        print("   python chatbot_unified.py")
        print()

