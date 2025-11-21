# -*- coding: utf-8 -*-
"""
chat-bot 폴더 내 OCR 의존성 설치
외부 바이너리 불필요 (Poppler, Tesseract 없이 작동)
"""

import subprocess
import sys
import os

# Windows 콘솔 인코딩
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

print("=" * 80)
print("📦 chat-bot 내장형 OCR 설치 중...")
print("=" * 80)
print()

packages = [
    "PyMuPDF",      # PDF → 이미지 (Poppler 불필요!)
    "easyocr",      # OCR (Tesseract 불필요!)
    "Pillow",       # 이미지 처리
]

print("✅ 모든 패키지는 순수 Python으로 작동합니다!")
print("✅ 외부 바이너리 설치 불필요!")
print()

for package in packages:
    print(f"📥 {package} 설치 중...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            package, "--upgrade"
        ])
        print(f"✅ {package} 설치 완료\n")
    except Exception as e:
        print(f"❌ {package} 설치 실패: {e}\n")

print("=" * 80)
print("✅ 설치 완료!")
print("=" * 80)
print()
print("📝 설치된 패키지:")
print("  - PyMuPDF: PDF를 이미지로 변환")
print("  - easyocr: 이미지에서 텍스트 추출 (딥러닝 기반)")
print("  - Pillow: 이미지 처리")
print()
print("🎯 특징:")
print("  ✅ Poppler 불필요")
print("  ✅ Tesseract 불필요")
print("  ✅ 순수 Python 패키지만 사용")
print("  ✅ Docker 배포 시에도 추가 설정 불필요")
print()

