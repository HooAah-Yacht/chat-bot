#!/usr/bin/env python3
"""모든 요트 목록 확인 스크립트"""
import json

def list_yacht_names():
    """yacht_specifications.json의 모든 요트 이름 출력"""
    try:
        with open('data/yacht_specifications.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"\n📋 yacht_specifications.json: 총 {data['totalYachts']}개 요트")
        print("=" * 80)
        for i, yacht in enumerate(data['yachts'], 1):
            print(f"{i:2d}. {yacht['name']:30s} (ID: {yacht['id']})")
        
        print("\n" + "=" * 80)
        
        # registered_yachts.json도 확인
        try:
            with open('data/registered_yachts.json', 'r', encoding='utf-8') as f:
                reg_data = json.load(f)
            print(f"\n📋 registered_yachts.json: 총 {reg_data['totalYachts']}개 요트")
            print("=" * 80)
            for i, yacht in enumerate(reg_data['yachts'], 1):
                name = yacht['registrationData']['basicInfo']['name']
                yacht_id = yacht['id']
                print(f"{i:2d}. {name:30s} (ID: {yacht_id})")
        except Exception as e:
            print(f"registered_yachts.json 읽기 오류: {e}")
            
    except Exception as e:
        print(f"오류: {e}")

if __name__ == "__main__":
    list_yacht_names()
