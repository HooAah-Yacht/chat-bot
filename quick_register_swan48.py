#!/usr/bin/env python3
"""
Nautor Swan 48 (Galatea) 단독 분석 및 등록
"""

import os
import json
from datetime import datetime
from chatbot_unified import UnifiedYachtChatbot

PDF_PATH = "data/yachtpdf/nautor-swan-48-galatea.pdf"

print(f"\n{'='*80}")
print(f"⛵ Nautor Swan 48 (Galatea) 분석 및 등록")
print(f"{'='*80}\n")

if not os.path.exists(PDF_PATH):
    print(f"❌ PDF 파일을 찾을 수 없습니다: {PDF_PATH}")
    exit(1)

print(f"📂 파일: {PDF_PATH}")
print(f"🕐 시작: {datetime.now().strftime('%H:%M:%S')}\n")

# 챗봇 초기화
print("🔧 챗봇 초기화...")
chatbot = UnifiedYachtChatbot()
print("✅ 초기화 완료\n")

# PDF 파일 업로드 처리
print("📄 PDF 분석 시작...\n")
result = chatbot._handle_file_upload(PDF_PATH)

print(f"\n{'='*80}")
print(f"📊 결과")
print(f"{'='*80}\n")
print(result)

# JSON 확인
print(f"\n{'='*80}")
print(f"💾 JSON 파일 확인")
print(f"{'='*80}\n")

specs_file = "data/yacht_specifications.json"
if os.path.exists(specs_file):
    with open(specs_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        yachts = data.get('yachts', [])
        
        # Swan 48 찾기
        swan48 = None
        for yacht in yachts:
            name = yacht.get('name', '').lower()
            if 'swan' in name and '48' in name:
                swan48 = yacht
                break
        
        if swan48:
            print(f"✅ Nautor Swan 48 발견:")
            print(f"   ID: {swan48.get('id')}")
            print(f"   이름: {swan48.get('name')}")
            print(f"   제조사: {swan48.get('manufacturer')}")
            print(f"   PDF: {swan48.get('manualPDF')}")
            print(f"   업데이트: {swan48.get('updatedAt')}")
            
            # 치수 정보
            yacht_specs = swan48.get('yachtSpecs', {})
            standard = yacht_specs.get('standard', {})
            dims = standard.get('dimensions', {})
            
            if dims:
                print(f"\n   📏 주요 치수:")
                for key, value in list(dims.items())[:5]:
                    print(f"      {key}: {value}")
        else:
            print(f"⚠️  Nautor Swan 48을 찾을 수 없습니다")
            print(f"   등록된 요트 수: {len(yachts)}")

print(f"\n{'='*80}")
print(f"✅ 완료")
print(f"🕐 종료: {datetime.now().strftime('%H:%M:%S')}")
print(f"{'='*80}\n")
