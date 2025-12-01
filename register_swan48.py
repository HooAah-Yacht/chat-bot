#!/usr/bin/env python3
"""
Nautor Swan 48 (Galatea) 신규 등록 스크립트
기존 Swan 48 데이터를 업데이트하여 새로운 PDF로 재등록
"""

import os
import sys
import json
from datetime import datetime
from chatbot_unified import UnifiedYachtChatbot

def register_swan48():
    """Nautor Swan 48 (Galatea) 등록"""
    
    pdf_path = "data/yachtpdf/nautor-swan-48-galatea.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ 오류: PDF 파일을 찾을 수 없습니다 - {pdf_path}")
        return False
    
    print(f"\n{'='*80}")
    print(f"⛵ Nautor Swan 48 (Galatea) 등록")
    print(f"{'='*80}\n")
    print(f"📂 PDF: {pdf_path}")
    print(f"🕐 시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # 챗봇 초기화
    try:
        print("🔧 챗봇 초기화 중...")
        chatbot = UnifiedYachtChatbot()
        print("✅ 초기화 완료\n")
    except Exception as e:
        print(f"❌ 초기화 실패: {e}")
        return False
    
    # PDF 분석 및 등록
    try:
        print("📄 PDF 분석 및 등록 시작...\n")
        
        # chat() 메서드로 PDF 처리
        response = chatbot.chat("Nautor Swan 48 (Galatea) 등록", pdf_file_path=pdf_path)
        
        print(f"\n{'='*80}")
        print(f"📊 등록 결과")
        print(f"{'='*80}\n")
        print(response)
        print()
        
        # 성공 여부 확인
        success = "등록되었습니다" in response or "업데이트되었습니다" in response
        
        if success:
            print(f"\n{'='*80}")
            print(f"💾 JSON 파일 확인")
            print(f"{'='*80}\n")
            
            # yacht_specifications.json 확인
            specs_path = "data/yacht_specifications.json"
            if os.path.exists(specs_path):
                with open(specs_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    yachts = data.get('yachts', [])
                    
                    swan48 = None
                    for yacht in yachts:
                        if 'swan 48' in yacht.get('name', '').lower():
                            swan48 = yacht
                            break
                    
                    if swan48:
                        print(f"✅ yacht_specifications.json에서 발견:")
                        print(f"   이름: {swan48.get('name')}")
                        print(f"   제조사: {swan48.get('manufacturer')}")
                        print(f"   타입: {swan48.get('type')}")
                        print(f"   연도: {swan48.get('year')}")
                        print(f"   매뉴얼: {swan48.get('manual')}")
                        
                        # 치수 정보
                        dims = swan48.get('dimensions', {})
                        if dims:
                            print(f"\n   📏 치수:")
                            if 'loa' in dims:
                                print(f"      LOA: {dims['loa'].get('display', 'N/A')}")
                            if 'beam' in dims:
                                print(f"      Beam: {dims['beam'].get('display', 'N/A')}")
                            if 'draft' in dims:
                                print(f"      Draft: {dims['draft'].get('display', 'N/A')}")
                    else:
                        print(f"⚠️  yacht_specifications.json에서 Swan 48을 찾을 수 없음")
            
            # yacht_parts_app_data.json 확인
            parts_path = "data/yacht_parts_app_data.json"
            if os.path.exists(parts_path):
                with open(parts_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    parts = data.get('parts', [])
                    
                    swan48_parts = [p for p in parts if 'swan 48' in p.get('yachtName', '').lower()]
                    
                    if swan48_parts:
                        print(f"\n✅ yacht_parts_app_data.json: {len(swan48_parts)}개 부품 발견")
                        
                        # 카테고리별 부품 수
                        categories = {}
                        for part in swan48_parts:
                            cat = part.get('category', '기타')
                            categories[cat] = categories.get(cat, 0) + 1
                        
                        print(f"   카테고리별:")
                        for cat, count in sorted(categories.items()):
                            print(f"      {cat}: {count}개")
                    else:
                        print(f"\n⚠️  yacht_parts_app_data.json에서 Swan 48 부품을 찾을 수 없음")
            
            print(f"\n{'='*80}")
            print(f"✅ 등록 완료!")
            print(f"🕐 종료: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*80}\n")
            
            print(f"💡 테스트:")
            print(f"   웹 UI에서 'Nautor Swan 48 분석해줘' 입력")
            print(f"   또는 'Swan 48 정보'로 확인\n")
            
            return True
        else:
            print(f"\n❌ 등록 실패")
            return False
            
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = register_swan48()
    sys.exit(0 if success else 1)
