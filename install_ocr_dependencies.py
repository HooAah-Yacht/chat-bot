#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR 의존성 설치 스크립트
- PyMuPDF (fitz): Poppler 없이 PDF 처리
- pytesseract: OCR
- Pillow: 이미지 처리
"""

import subprocess
import sys
import os

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

def install_packages():
    """필요한 Python 패키지 설치"""
    packages = [
        "PyMuPDF",  # PDF to image (Poppler 불필요)
        "pytesseract",  # OCR
        "Pillow",  # 이미지 처리
    ]
    
    print("=" * 80)
    print("📦 OCR 의존성 설치 중...")
    print("=" * 80)
    print()
    
    for package in packages:
        print(f"📥 {package} 설치 중...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                package, "--upgrade", "--quiet"
            ])
            print(f"✅ {package} 설치 완료")
        except Exception as e:
            print(f"❌ {package} 설치 실패: {e}")
    
    print()
    print("=" * 80)
    print("✅ Python 패키지 설치 완료!")
    print("=" * 80)
    print()
    
    # Tesseract 확인
    check_tesseract()


def check_tesseract():
    """Tesseract 설치 확인 및 안내"""
    print("\n🔍 Tesseract OCR 확인 중...")
    
    try:
        import pytesseract
        from PIL import Image
        
        # Tesseract 실행 가능한지 확인
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract {version} 설치됨")
        print(f"📍 위치: {pytesseract.pytesseract.tesseract_cmd}")
        return True
        
    except Exception as e:
        print("❌ Tesseract가 설치되어 있지 않습니다.")
        print()
        print("=" * 80)
        print("📋 Tesseract 설치 방법")
        print("=" * 80)
        print()
        print("Windows:")
        print("  1. https://github.com/UB-Mannheim/tesseract/wiki 방문")
        print("  2. tesseract-ocr-w64-setup-v5.x.x.exe 다운로드")
        print("  3. 설치 (PATH에 자동 추가)")
        print()
        print("또는:")
        print("  choco install tesseract")
        print()
        print("Linux:")
        print("  sudo apt-get install tesseract-ocr")
        print("  sudo apt-get install tesseract-ocr-kor  # 한글 지원")
        print()
        print("Mac:")
        print("  brew install tesseract")
        print()
        
        return False


def download_tesseract_windows():
    """Windows용 Tesseract 자동 다운로드 (선택사항)"""
    import urllib.request
    import zipfile
    
    print("📥 Windows용 Tesseract 다운로드 중...")
    
    # Tesseract portable 버전 다운로드
    url = "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe"
    
    tessdata_dir = "chat-bot/tessdata"
    os.makedirs(tessdata_dir, exist_ok=True)
    
    print(f"💡 Tesseract는 수동 설치가 필요합니다.")
    print(f"   위 URL에서 다운로드 후 설치하세요: {url}")


if __name__ == "__main__":
    install_packages()
    
    print("\n" + "=" * 80)
    print("🎉 설치 완료!")
    print("=" * 80)
    print()
    print("다음 단계:")
    print("1. Tesseract가 설치되지 않았다면 위 안내에 따라 설치")
    print("2. 설치 후 chatbot_unified.py 재시작")
    print("3. 스캔된 PDF 파일 업로드 테스트")
    print()

