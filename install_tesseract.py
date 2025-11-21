# -*- coding: utf-8 -*-
"""
Windows용 Tesseract OCR 자동 다운로드 및 설치 안내
"""

import sys
import os
import webbrowser

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

print("=" * 80)
print("🔍 Tesseract OCR 설치")
print("=" * 80)
print()

# 다운로드 URL
download_url = "https://github.com/UB-Mannheim/tesseract/wiki"
installer_url = "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe"

print("📥 Tesseract OCR 다운로드 페이지를 엽니다...")
print()
print(f"📍 다운로드 URL: {download_url}")
print(f"📦 직접 다운로드: {installer_url}")
print()

# 브라우저로 다운로드 페이지 열기
try:
    webbrowser.open(download_url)
    print("✅ 브라우저가 열렸습니다!")
except:
    print("❌ 브라우저 열기 실패. 수동으로 위 URL을 방문하세요.")

print()
print("=" * 80)
print("📋 설치 방법")
print("=" * 80)
print()
print("1. 다운로드한 tesseract-ocr-w64-setup-v5.x.x.exe 실행")
print("2. 설치 진행")
print("   - 기본 설치 경로 권장: C:\\Program Files\\Tesseract-OCR")
print("   - ✅ 'Add to PATH' 옵션 체크 (중요!)")
print("3. 한글 지원을 위해 'Additional language data' 선택 시:")
print("   - Korean 선택")
print("4. 설치 완료 후 터미널 재시작")
print()
print("=" * 80)
print("🔧 설치 확인")
print("=" * 80)
print()
print("설치 후 다음 명령어로 확인:")
print("  tesseract --version")
print()
print("또는 Python으로 확인:")
print("  python -c \"import pytesseract; print(pytesseract.get_tesseract_version())\"")
print()
print("=" * 80)
print("⚡ 빠른 설치 (Chocolatey 사용 시)")
print("=" * 80)
print()
print("Chocolatey가 설치되어 있다면:")
print("  choco install tesseract")
print()

