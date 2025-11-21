# -*- coding: utf-8 -*-
"""
AI Chatbot과 MySQL DB 연결
- JSON 파일 대신 DB에서 직접 요트 데이터 조회
- 새로운 요트 등록 시 DB에 저장
"""

import sys
import os
import json
import pymysql
from datetime import datetime
from typing import Dict, List, Optional

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass


class YachtDatabaseConnector:
    """MySQL DB와 AI Chatbot 연결"""
    
    def __init__(self, host='localhost', port=3306, user='root', password='', database='yacht_db'):
        """
        MySQL 연결 초기화
        
        Args:
            host: DB 호스트
            port: DB 포트
            user: DB 사용자
            password: DB 비밀번호
            database: DB 이름
        """
        self.connection_params = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database,
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
        self.conn = None
    
    def connect(self):
        """DB 연결"""
        try:
            self.conn = pymysql.connect(**self.connection_params)
            print("✅ MySQL 연결 성공!")
            return True
        except Exception as e:
            print(f"❌ MySQL 연결 실패: {e}")
            return False
    
    def disconnect(self):
        """DB 연결 해제"""
        if self.conn:
            self.conn.close()
            print("🔌 MySQL 연결 종료")
    
    # ============================================================
    # 1. 요트 조회
    # ============================================================
    
    def get_all_yachts(self) -> List[Dict]:
        """
        DB에서 모든 요트 조회
        
        Returns:
            요트 목록 [
                {
                    "id": 1,
                    "name": "Ocean Dream",
                    "available": True,
                    "capacity": 8,
                    "location": "부산 마리나",
                    "price_per_hour": 150000,
                    "description": "럭셔리 요트",
                    "created_at": "2025-11-21 10:00:00"
                }
            ]
        """
        if not self.conn:
            self.connect()
        
        try:
            with self.conn.cursor() as cursor:
                sql = """
                    SELECT 
                        id, name, available, capacity, location, 
                        price_per_hour, description, thumbnail_path,
                        created_at, updated_at
                    FROM yacht
                    ORDER BY created_at DESC
                """
                cursor.execute(sql)
                yachts = cursor.fetchall()
                
                # bit(1) → bool 변환
                for yacht in yachts:
                    if 'available' in yacht and yacht['available'] is not None:
                        yacht['available'] = bool(yacht['available'])
                
                return yachts
        except Exception as e:
            print(f"❌ 요트 조회 실패: {e}")
            return []
    
    def get_yacht_by_id(self, yacht_id: int) -> Optional[Dict]:
        """
        특정 요트 조회
        
        Args:
            yacht_id: 요트 ID
        
        Returns:
            요트 정보 또는 None
        """
        if not self.conn:
            self.connect()
        
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM yacht WHERE id = %s"
                cursor.execute(sql, (yacht_id,))
                yacht = cursor.fetchone()
                
                if yacht and 'available' in yacht:
                    yacht['available'] = bool(yacht['available'])
                
                return yacht
        except Exception as e:
            print(f"❌ 요트 조회 실패: {e}")
            return None
    
    def search_yachts_by_name(self, name: str) -> List[Dict]:
        """
        이름으로 요트 검색
        
        Args:
            name: 검색할 요트 이름 (부분 일치)
        
        Returns:
            요트 목록
        """
        if not self.conn:
            self.connect()
        
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM yacht WHERE name LIKE %s"
                cursor.execute(sql, (f'%{name}%',))
                yachts = cursor.fetchall()
                
                for yacht in yachts:
                    if 'available' in yacht and yacht['available'] is not None:
                        yacht['available'] = bool(yacht['available'])
                
                return yachts
        except Exception as e:
            print(f"❌ 요트 검색 실패: {e}")
            return []
    
    # ============================================================
    # 2. AI 분석 결과 → DB 저장
    # ============================================================
    
    def save_yacht_from_ai(self, yacht_data: Dict) -> Optional[int]:
        """
        AI 분석 결과를 DB에 저장
        
        Args:
            yacht_data: AI가 추출한 요트 정보
                {
                    "name": "OCEANIS 46.1",
                    "manufacturer": "BENETEAU",
                    "description": "...",
                    "specifications": {...}
                }
        
        Returns:
            생성된 yacht ID 또는 None
        """
        if not self.conn:
            self.connect()
        
        try:
            with self.conn.cursor() as cursor:
                # description 생성 (제조사 + 스펙 요약)
                description = self._create_description_from_specs(yacht_data)
                
                sql = """
                    INSERT INTO yacht (
                        name, available, capacity, description, 
                        location, price_per_hour, created_at, updated_at
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """
                
                now = datetime.now()
                cursor.execute(sql, (
                    yacht_data.get('name', 'Unknown Yacht'),
                    True,  # available (기본값: 예약 가능)
                    yacht_data.get('specifications', {}).get('accommodations', {}).get('berths', None),
                    description,
                    yacht_data.get('location', ''),  # 위치 정보 없으면 빈 문자열
                    None,  # price_per_hour (나중에 수동 설정)
                    now,
                    now
                ))
                
                self.conn.commit()
                yacht_id = cursor.lastrowid
                
                print(f"✅ 요트 저장 완료! ID: {yacht_id}, Name: {yacht_data.get('name')}")
                return yacht_id
                
        except Exception as e:
            print(f"❌ 요트 저장 실패: {e}")
            self.conn.rollback()
            return None
    
    def _create_description_from_specs(self, yacht_data: Dict) -> str:
        """AI 분석 결과에서 description 생성"""
        parts = []
        
        # 제조사
        if yacht_data.get('manufacturer'):
            parts.append(f"제조사: {yacht_data['manufacturer']}")
        
        # 치수
        specs = yacht_data.get('specifications', {})
        dims = specs.get('dimensions', {})
        if dims.get('loa'):
            parts.append(f"전체 길이: {dims['loa']}")
        if dims.get('beam'):
            parts.append(f"폭: {dims['beam']}")
        
        # 엔진
        engine = specs.get('engine', {})
        if engine.get('power'):
            parts.append(f"엔진: {engine['power']}")
        
        # 기본 설명
        if not parts:
            parts.append("AI가 PDF에서 자동 추출한 요트")
        
        return " | ".join(parts)
    
    # ============================================================
    # 3. JSON ↔ DB 동기화
    # ============================================================
    
    def sync_json_to_db(self, json_file_path: str):
        """
        JSON 파일의 요트 데이터를 DB로 동기화
        
        Args:
            json_file_path: yacht_specifications.json 경로
        """
        print(f"📥 JSON 파일 읽는 중: {json_file_path}")
        
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        yachts = data.get('yachts', [])
        print(f"📊 총 {len(yachts)}개 요트 발견")
        
        success_count = 0
        skip_count = 0
        
        for yacht in yachts:
            # 이미 DB에 있는지 확인
            existing = self.search_yachts_by_name(yacht.get('name', ''))
            
            if existing:
                print(f"⏭️  스킵: {yacht.get('name')} (이미 존재)")
                skip_count += 1
                continue
            
            # DB에 저장
            yacht_id = self.save_yacht_from_ai(yacht)
            if yacht_id:
                success_count += 1
        
        print()
        print("=" * 80)
        print(f"✅ 동기화 완료!")
        print(f"   - 성공: {success_count}개")
        print(f"   - 스킵: {skip_count}개")
        print("=" * 80)
    
    def export_db_to_json(self, output_file: str):
        """
        DB의 요트 데이터를 JSON으로 내보내기
        
        Args:
            output_file: 출력할 JSON 파일 경로
        """
        yachts = self.get_all_yachts()
        
        # datetime 객체를 문자열로 변환
        for yacht in yachts:
            for key in ['created_at', 'updated_at']:
                if key in yacht and yacht[key]:
                    yacht[key] = yacht[key].strftime('%Y-%m-%d %H:%M:%S')
        
        output_data = {
            'schemaVersion': '5.0',
            'lastUpdated': datetime.now().strftime('%Y-%m-%d'),
            'totalYachts': len(yachts),
            'yachts': yachts
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ DB 데이터를 JSON으로 내보냄: {output_file}")
        print(f"   총 {len(yachts)}개 요트")


# ============================================================
# 테스트 및 사용 예시
# ============================================================

def test_connection():
    """DB 연결 테스트"""
    print("=" * 80)
    print("🧪 MySQL 연결 테스트")
    print("=" * 80)
    print()
    
    # DB 연결 정보 입력
    print("MySQL 연결 정보를 입력하세요:")
    host = input("Host (기본값: localhost): ").strip() or 'localhost'
    port = input("Port (기본값: 3306): ").strip() or '3306'
    user = input("User (기본값: root): ").strip() or 'root'
    password = input("Password: ").strip()
    database = input("Database (기본값: yacht_db): ").strip() or 'yacht_db'
    
    # 연결
    connector = YachtDatabaseConnector(
        host=host,
        port=int(port),
        user=user,
        password=password,
        database=database
    )
    
    if not connector.connect():
        return
    
    # 요트 조회
    print("\n📊 DB의 요트 목록:")
    yachts = connector.get_all_yachts()
    
    if yachts:
        for yacht in yachts[:5]:  # 최대 5개만 출력
            print(f"   - {yacht['name']} (ID: {yacht['id']}, 위치: {yacht.get('location', 'N/A')})")
        
        if len(yachts) > 5:
            print(f"   ... 외 {len(yachts) - 5}개")
    else:
        print("   (요트 없음)")
    
    connector.disconnect()


if __name__ == "__main__":
    print()
    print("=" * 80)
    print("🚢 HooAah Yacht - AI ↔ DB 연동 시스템")
    print("=" * 80)
    print()
    print("선택:")
    print("1. DB 연결 테스트")
    print("2. JSON → DB 동기화")
    print("3. DB → JSON 내보내기")
    print()
    
    choice = input("번호를 선택하세요 (1-3): ").strip()
    
    if choice == '1':
        test_connection()
    
    elif choice == '2':
        # JSON → DB
        connector = YachtDatabaseConnector(
            host='localhost',
            user='root',
            password=input("MySQL 비밀번호: ").strip(),
            database='yacht_db'
        )
        
        if connector.connect():
            connector.sync_json_to_db('data/yacht_specifications.json')
            connector.disconnect()
    
    elif choice == '3':
        # DB → JSON
        connector = YachtDatabaseConnector(
            host='localhost',
            user='root',
            password=input("MySQL 비밀번호: ").strip(),
            database='yacht_db'
        )
        
        if connector.connect():
            connector.export_db_to_json('yacht_db_export.json')
            connector.disconnect()
    
    else:
        print("❌ 잘못된 선택")

