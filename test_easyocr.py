# -*- coding: utf-8 -*-
"""
EasyOCR 테스트 스크립트
"""

import sys
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

from chatbot_unified import UnifiedYachtChatbot

API_KEY = "AIzaSyBhPZDNBTEqYu8ahBIVpK2B1h_CAKgo7JI"

print("=" * 80)
print("🧪 EasyOCR 테스트")
print("=" * 80)
print()

# Chatbot 초기화
print("🤖 챗봇 초기화 중...")
chatbot = UnifiedYachtChatbot(api_key=API_KEY)
print()

# 스캔 PDF 테스트
pdf_path = "data/yachtpdf/2020_03_31_11_03_39-48 owners manual.pdf"

print(f"📄 PDF 테스트: {pdf_path}")
print()

try:
    # 텍스트 추출 테스트
    text = chatbot._extract_text_from_pdf(pdf_path)
    
    if len(text) > 100:
        print("✅ 텍스트 추출 성공!")
        print(f"📊 추출된 텍스트 길이: {len(text)} 문자")
        print()
        print("📝 샘플 (처음 500자):")
        print("-" * 80)
        print(text[:500])
        print("-" * 80)
    else:
        print("❌ 텍스트 추출 실패")
        
except Exception as e:
    print(f"❌ 오류: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 80)

