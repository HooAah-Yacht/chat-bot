#!/usr/bin/env python3
"""
단일 요트 PDF 분석 및 JSON 저장 스크립트
Usage: python analyze_single_yacht.py <pdf_path>
"""

import os
import sys
import json
from datetime import datetime
from chatbot_unified import UnifiedYachtChatbot

def analyze_single_yacht(pdf_path: str):
    """단일 요트 PDF 분석 및 저장"""
    
    if not os.path.exists(pdf_path):
        print(f"❌ 오류: 파일을 찾을 수 없습니다 - {pdf_path}")
        return False
    
    print(f"\n{'='*80}")
    print(f"📄 요트 PDF 분석 시작")
    print(f"{'='*80}\n")
    print(f"📂 파일: {pdf_path}")
    print(f"🕐 시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # 챗봇 초기화
    try:
        chatbot = UnifiedYachtChatbot()
        print("✅ 챗봇 초기화 완료\n")
    except Exception as e:
        print(f"❌ 챗봇 초기화 실패: {e}")
        return False
    
    # PDF 분석
    try:
        print(f"🔍 PDF 분석 중...")
        
        # chat() 메서드로 PDF 분석 (pdf_file_path 파라미터 사용)
        response = chatbot.chat("", pdf_file_path=pdf_path)
        
        print(f"\n{'='*80}")
        print(f"📊 분석 결과")
        print(f"{'='*80}\n")
        print(response)
        print()
        
        # 요트 이름 추출 (응답에서)
        yacht_name = None
        if "등록되었습니다" in response or "업데이트되었습니다" in response:
            # 응답에서 요트 이름 추출 시도
            import re
            match = re.search(r'\*\*(.*?)\*\*.*?등록되었습니다', response)
            if not match:
                match = re.search(r'\*\*(.*?)\*\*.*?업데이트되었습니다', response)
            if match:
                yacht_name = match.group(1).strip()
        
        if not yacht_name:
            # PDF 파일명에서 추출 시도
            filename = os.path.basename(pdf_path).replace('.pdf', '').replace('-', ' ').title()
            yacht_name = filename
        
        # JSON 파일들 확인
        print(f"\n{'='*80}")
        print(f"💾 저장된 JSON 파일 확인")
        print(f"{'='*80}\n")
        
        json_files = {
            'yacht_specifications.json': 'data/yacht_specifications.json',
            'yacht_parts_app_data.json': 'data/yacht_parts_app_data.json',
            'yacht_parts_database.json': 'data/yacht_parts_database.json',
            'yacht_manual_resources.json': 'data/yacht_manual_resources.json',
            'registered_yachts.json': 'data/registered_yachts.json'
        }
        
        for name, path in json_files.items():
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # 요트 이름으로 검색
                found = False
                if name == 'yacht_specifications.json':
                    yachts = data.get('yachts', [])
                    for yacht in yachts:
                        if yacht.get('name', '').lower() == yacht_name.lower():
                            found = True
                            print(f"✅ {name}: 요트 '{yacht_name}' 등록됨")
                            break
                elif name == 'yacht_parts_app_data.json':
                    parts_list = data.get('parts', [])
                    yacht_parts = [p for p in parts_list if p.get('yachtName', '').lower() == yacht_name.lower()]
                    if yacht_parts:
                        found = True
                        print(f"✅ {name}: {len(yacht_parts)}개 부품 등록됨")
                elif name == 'registered_yachts.json':
                    yachts = data.get('yachts', [])
                    for yacht in yachts:
                        if yacht.get('name', '').lower() == yacht_name.lower():
                            found = True
                            print(f"✅ {name}: 요트 '{yacht_name}' 등록됨")
                            break
                else:
                    # 다른 파일들
                    print(f"ℹ️  {name}: 존재함")
                    found = True
                
                if not found and name in ['yacht_specifications.json', 'yacht_parts_app_data.json', 'registered_yachts.json']:
                    print(f"⚠️  {name}: 요트 '{yacht_name}' 찾을 수 없음")
            else:
                print(f"❌ {name}: 파일 없음")
        
        print(f"\n{'='*80}")
        print(f"✅ 분석 완료!")
        print(f"🕐 종료 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("사용법: python analyze_single_yacht.py <pdf_path>")
        print("예: python analyze_single_yacht.py data/yachtpdf/nautor-swan-48-galatea.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    success = analyze_single_yacht(pdf_path)
    
    sys.exit(0 if success else 1)
