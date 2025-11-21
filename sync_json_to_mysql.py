# -*- coding: utf-8 -*-
"""
JSON 데이터를 MySQL 데이터베이스와 동기화
yacht_specifications.json → MySQL yacht 테이블
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime
import pymysql
from dotenv import load_dotenv

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# .env 파일 로드
load_dotenv()

# MySQL 연결 정보
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'root'),
    'database': os.getenv('DB_NAME', 'HooYah'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}


def connect_mysql():
    """MySQL 연결"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        print(f"✅ MySQL 연결 성공: {DB_CONFIG['database']}")
        return connection
    except Exception as e:
        print(f"❌ MySQL 연결 실패: {e}")
        return None


def load_json_data():
    """yacht_specifications.json 로드"""
    try:
        file_path = Path('data/yacht_specifications.json')
        
        if not file_path.exists():
            print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        yachts = data.get('yachts', [])
        print(f"✅ JSON 데이터 로드 완료: {len(yachts)}개 요트")
        
        return yachts
    except Exception as e:
        print(f"❌ JSON 로드 실패: {e}")
        return None


def check_yacht_table(connection):
    """yacht 테이블 구조 확인"""
    try:
        with connection.cursor() as cursor:
            # 테이블 존재 확인
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM information_schema.tables 
                WHERE table_schema = %s 
                AND table_name = 'yacht'
            """, (DB_CONFIG['database'],))
            
            result = cursor.fetchone()
            
            if result['count'] == 0:
                print("⚠️ yacht 테이블이 존재하지 않습니다.")
                return False
            
            # 테이블 구조 확인
            cursor.execute("DESCRIBE yacht")
            columns = cursor.fetchall()
            
            print("\n📋 yacht 테이블 구조:")
            for col in columns:
                print(f"  - {col['Field']:20s} {col['Type']:20s} {col['Null']:5s} {col['Key']:5s}")
            
            return True
    except Exception as e:
        print(f"❌ 테이블 확인 실패: {e}")
        return False


def create_yacht_table_if_not_exists(connection):
    """yacht 테이블이 없으면 생성"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS yacht (
                    id BIGINT NOT NULL AUTO_INCREMENT,
                    yacht_id VARCHAR(100) UNIQUE,
                    name VARCHAR(255) NOT NULL,
                    manufacturer VARCHAR(255),
                    yacht_type VARCHAR(100),
                    length_overall DECIMAL(10, 2),
                    beam DECIMAL(10, 2),
                    draft DECIMAL(10, 2),
                    displacement DECIMAL(10, 2),
                    sail_area DECIMAL(10, 2),
                    engine_power VARCHAR(100),
                    manual_pdf VARCHAR(255),
                    official_website VARCHAR(500),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    PRIMARY KEY (id),
                    INDEX idx_yacht_id (yacht_id),
                    INDEX idx_name (name)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
            """)
            connection.commit()
            print("✅ yacht 테이블 생성 완료 (또는 이미 존재함)")
            return True
    except Exception as e:
        print(f"❌ 테이블 생성 실패: {e}")
        return False


def extract_dimension_value(dimension_data):
    """치수 데이터에서 숫자 추출"""
    if not dimension_data:
        return None
    
    if isinstance(dimension_data, dict):
        value = dimension_data.get('value')
        if value:
            return float(value) if isinstance(value, (int, float)) else None
    
    if isinstance(dimension_data, str):
        # "14.60m" → 14.60
        import re
        match = re.search(r'(\d+\.?\d*)', dimension_data)
        if match:
            return float(match.group(1))
    
    return None


def sync_yacht_to_mysql(connection, yacht):
    """요트 데이터를 MySQL에 동기화"""
    try:
        yacht_id = yacht.get('id', '')
        yacht_name = yacht.get('name', '')
        
        if not yacht_id or not yacht_name:
            print(f"⚠️ ID 또는 이름 없음: {yacht}")
            return False
        
        # yachtSpecs에서 데이터 추출
        yacht_specs = yacht.get('yachtSpecs', {})
        standard = yacht_specs.get('standard', {})
        dimensions = standard.get('dimensions', {})
        engine = standard.get('engine', {})
        sail_area_data = standard.get('sailArea', {})
        
        # 치수 추출
        loa = extract_dimension_value(dimensions.get('LOA') or dimensions.get('loa'))
        beam = extract_dimension_value(dimensions.get('Beam') or dimensions.get('beam'))
        draft = extract_dimension_value(dimensions.get('Draft') or dimensions.get('draft'))
        displacement = extract_dimension_value(dimensions.get('Displacement') or dimensions.get('displacement'))
        
        # 돛 면적 추출 (total 또는 mainsail)
        sail_area = None
        if isinstance(sail_area_data, dict):
            total = sail_area_data.get('total') or sail_area_data.get('totalSailArea')
            mainsail = sail_area_data.get('mainsail') or sail_area_data.get('mainSailArea')
            sail_area = extract_dimension_value(total or mainsail)
        
        # 엔진 파워 추출
        engine_power = None
        if isinstance(engine, dict):
            engine_power = engine.get('power') or engine.get('Power')
        
        with connection.cursor() as cursor:
            # 기존 요트 확인
            cursor.execute("SELECT id FROM yacht WHERE yacht_id = %s", (yacht_id,))
            existing = cursor.fetchone()
            
            if existing:
                # 업데이트
                cursor.execute("""
                    UPDATE yacht SET
                        name = %s,
                        manufacturer = %s,
                        yacht_type = %s,
                        length_overall = %s,
                        beam = %s,
                        draft = %s,
                        displacement = %s,
                        sail_area = %s,
                        engine_power = %s,
                        manual_pdf = %s,
                        updated_at = NOW()
                    WHERE yacht_id = %s
                """, (
                    yacht_name,
                    yacht.get('manufacturer', ''),
                    yacht.get('type', ''),
                    loa,
                    beam,
                    draft,
                    displacement,
                    sail_area,
                    engine_power,
                    yacht.get('manualPDF', ''),
                    yacht_id
                ))
                action = "업데이트"
            else:
                # 삽입
                cursor.execute("""
                    INSERT INTO yacht (
                        yacht_id, name, manufacturer, yacht_type,
                        length_overall, beam, draft, displacement,
                        sail_area, engine_power, manual_pdf
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    yacht_id,
                    yacht_name,
                    yacht.get('manufacturer', ''),
                    yacht.get('type', ''),
                    loa,
                    beam,
                    draft,
                    displacement,
                    sail_area,
                    engine_power,
                    yacht.get('manualPDF', '')
                ))
                action = "추가"
            
            connection.commit()
            print(f"  ✅ {yacht_name} ({yacht_id}) - {action} 완료")
            return True
            
    except Exception as e:
        print(f"  ❌ {yacht.get('name', 'Unknown')} 동기화 실패: {e}")
        connection.rollback()
        return False


def sync_all_yachts():
    """모든 요트 데이터 동기화"""
    print("\n" + "="*80)
    print("🔄 JSON → MySQL 동기화 시작")
    print("="*80)
    
    # 1. JSON 데이터 로드
    yachts = load_json_data()
    if not yachts:
        return
    
    # 2. MySQL 연결
    connection = connect_mysql()
    if not connection:
        return
    
    try:
        # 3. 테이블 확인/생성
        if not check_yacht_table(connection):
            print("\n⚠️ yacht 테이블 생성 시도...")
            if not create_yacht_table_if_not_exists(connection):
                return
            check_yacht_table(connection)
        
        # 4. 데이터 동기화
        print(f"\n🔄 {len(yachts)}개 요트 동기화 중...")
        print("-" * 80)
        
        success_count = 0
        fail_count = 0
        
        for yacht in yachts:
            if sync_yacht_to_mysql(connection, yacht):
                success_count += 1
            else:
                fail_count += 1
        
        print("-" * 80)
        print(f"\n📊 동기화 완료:")
        print(f"  ✅ 성공: {success_count}개")
        print(f"  ❌ 실패: {fail_count}개")
        
        # 5. 결과 확인
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM yacht")
            total = cursor.fetchone()['count']
            print(f"  📦 MySQL 총 요트 수: {total}개")
            
            # 최근 추가된 요트 5개 출력
            cursor.execute("""
                SELECT yacht_id, name, manufacturer, updated_at 
                FROM yacht 
                ORDER BY updated_at DESC 
                LIMIT 5
            """)
            recent = cursor.fetchall()
            
            print(f"\n📋 최근 업데이트된 요트 (상위 5개):")
            for yacht in recent:
                print(f"  - {yacht['name']:30s} (ID: {yacht['yacht_id']:20s}) - {yacht['updated_at']}")
        
        print("\n" + "="*80)
        print("✅ 동기화 완료!")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ 동기화 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        connection.close()
        print("\n🔌 MySQL 연결 종료")


def verify_sync():
    """동기화 검증"""
    print("\n" + "="*80)
    print("🔍 동기화 검증")
    print("="*80)
    
    connection = connect_mysql()
    if not connection:
        return
    
    try:
        with connection.cursor() as cursor:
            # JSON 데이터 개수
            yachts = load_json_data()
            json_count = len(yachts) if yachts else 0
            
            # MySQL 데이터 개수
            cursor.execute("SELECT COUNT(*) as count FROM yacht")
            mysql_count = cursor.fetchone()['count']
            
            print(f"\n📊 데이터 개수 비교:")
            print(f"  JSON:  {json_count}개")
            print(f"  MySQL: {mysql_count}개")
            
            if json_count == mysql_count:
                print(f"  ✅ 일치!")
            else:
                print(f"  ⚠️ 불일치 ({abs(json_count - mysql_count)}개 차이)")
            
            # ID 일치 확인
            print(f"\n🔍 ID 일치 확인:")
            json_ids = {y.get('id') for y in yachts if y.get('id')}
            
            cursor.execute("SELECT yacht_id FROM yacht")
            mysql_ids = {row['yacht_id'] for row in cursor.fetchall()}
            
            missing_in_mysql = json_ids - mysql_ids
            extra_in_mysql = mysql_ids - json_ids
            
            if missing_in_mysql:
                print(f"  ⚠️ MySQL에 없는 ID: {missing_in_mysql}")
            
            if extra_in_mysql:
                print(f"  ⚠️ JSON에 없는 ID: {extra_in_mysql}")
            
            if not missing_in_mysql and not extra_in_mysql:
                print(f"  ✅ 모든 ID가 일치합니다!")
            
            print("\n" + "="*80)
            
    except Exception as e:
        print(f"❌ 검증 실패: {e}")
    finally:
        connection.close()


if __name__ == "__main__":
    try:
        # 동기화 실행
        sync_all_yachts()
        
        # 검증
        verify_sync()
        
        print("\n✨ 모든 작업이 완료되었습니다!\n")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

