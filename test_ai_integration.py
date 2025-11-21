"""
Python AI API 통합 테스트 스크립트
Backend와의 연동을 테스트합니다.
"""

import requests
import json
import sys

AI_API_BASE_URL = "http://localhost:5000"

def print_section(title):
    """섹션 제목 출력"""
    print("\n" + "=" * 80)
    print(f"🧪 {title}")
    print("=" * 80)

def test_health_check():
    """헬스체크 테스트"""
    print_section("1. 헬스체크 테스트")
    
    try:
        response = requests.get(f"{AI_API_BASE_URL}/api/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 헬스체크 성공")
            print(f"   상태: {data.get('status')}")
            print(f"   요트 개수: {data.get('yachtCount')}")
            print(f"   버전: {data.get('version')}")
            return True
        else:
            print(f"❌ 헬스체크 실패: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 연결 실패: {e}")
        print("💡 Python AI 서버가 실행 중인지 확인하세요:")
        print("   python chatbot_unified.py --mode api --port 5000")
        return False

def test_yacht_analyze(yacht_name="J/70"):
    """요트 이름으로 부품 조회 테스트"""
    print_section(f"2. 요트 이름으로 부품 조회 테스트: {yacht_name}")
    
    try:
        response = requests.get(
            f"{AI_API_BASE_URL}/api/yacht/analyze",
            params={"yacht_name": yacht_name},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                print("✅ 요트 분석 성공")
                print(f"   요트 ID: {data.get('yachtId')}")
                print(f"   요트 이름: {data.get('yachtName')}")
                print(f"   부품 개수: {data.get('totalParts')}")
                
                parts = data.get('parts', [])
                if parts:
                    print(f"\n   📦 부품 샘플 (처음 3개):")
                    for i, part in enumerate(parts[:3], 1):
                        print(f"      {i}. {part.get('name')} ({part.get('manufacturer')} {part.get('model')})")
                        print(f"         정비 주기: {part.get('interval')}개월")
                
                return True
            else:
                print(f"❌ 요트 분석 실패: {data.get('error')}")
                return False
        else:
            print(f"❌ HTTP 오류: {response.status_code}")
            print(f"   응답: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 요청 실패: {e}")
        return False

def test_pdf_analyze(pdf_path=None):
    """PDF 파일 분석 테스트"""
    print_section("3. PDF 파일 분석 테스트")
    
    if not pdf_path:
        print("⚠️ PDF 파일 경로가 제공되지 않았습니다. 테스트를 건너뜁니다.")
        print("💡 PDF 테스트를 하려면 다음과 같이 실행하세요:")
        print("   python test_ai_integration.py --pdf-path data/yachtpdf/owners_manual.pdf")
        return None
    
    import os
    if not os.path.exists(pdf_path):
        print(f"❌ 파일을 찾을 수 없습니다: {pdf_path}")
        return False
    
    try:
        with open(pdf_path, 'rb') as f:
            files = {'file': (os.path.basename(pdf_path), f, 'application/pdf')}
            response = requests.post(
                f"{AI_API_BASE_URL}/api/yacht/analyze-pdf",
                files=files,
                timeout=60  # PDF 분석은 시간이 오래 걸릴 수 있음
            )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                print("✅ PDF 분석 성공")
                print(f"   요트 ID: {data.get('yachtId')}")
                print(f"   요트 이름: {data.get('yachtName')}")
                print(f"   부품 개수: {data.get('totalParts')}")
                
                doc_info = data.get('documentInfo', {})
                if doc_info:
                    print(f"\n   📄 문서 정보:")
                    print(f"      파일명: {doc_info.get('fileName')}")
                    print(f"      제조사: {doc_info.get('manufacturer')}")
                    print(f"      모델: {doc_info.get('model')}")
                    print(f"      연도: {doc_info.get('year')}")
                
                parts = data.get('parts', [])
                if parts:
                    print(f"\n   📦 부품 샘플 (처음 3개):")
                    for i, part in enumerate(parts[:3], 1):
                        print(f"      {i}. {part.get('name')} ({part.get('manufacturer')} {part.get('model')})")
                        print(f"         정비 주기: {part.get('interval')}개월")
                
                return True
            else:
                print(f"❌ PDF 분석 실패: {data.get('error')}")
                return False
        else:
            print(f"❌ HTTP 오류: {response.status_code}")
            print(f"   응답: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 요청 실패: {e}")
        return False

def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Python AI API 통합 테스트')
    parser.add_argument('--pdf-path', type=str, help='테스트할 PDF 파일 경로')
    parser.add_argument('--yacht-name', type=str, default='J/70', help='테스트할 요트 이름')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("🚀 Python AI API 통합 테스트 시작")
    print("=" * 80)
    print(f"📡 AI API URL: {AI_API_BASE_URL}")
    print()
    
    results = []
    
    # 1. 헬스체크
    health_ok = test_health_check()
    results.append(("헬스체크", health_ok))
    
    if not health_ok:
        print("\n❌ AI 서버에 연결할 수 없습니다. 테스트를 중단합니다.")
        sys.exit(1)
    
    # 2. 요트 이름으로 조회
    yacht_ok = test_yacht_analyze(args.yacht_name)
    results.append(("요트 이름 조회", yacht_ok))
    
    # 3. PDF 분석 (선택사항)
    if args.pdf_path:
        pdf_ok = test_pdf_analyze(args.pdf_path)
        if pdf_ok is not None:
            results.append(("PDF 분석", pdf_ok))
    
    # 결과 요약
    print_section("테스트 결과 요약")
    
    all_passed = True
    for test_name, result in results:
        if result:
            print(f"   ✅ {test_name}: 성공")
        else:
            print(f"   ❌ {test_name}: 실패")
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 모든 테스트 통과!")
        print()
        print("✅ Backend 연동 준비 완료!")
        print("💡 다음 단계:")
        print("   1. Backend 서버 시작: cd backend && ./gradlew bootRun")
        print("   2. Backend API 테스트: curl http://localhost:8080/api/yacht/part-list?name=J/70")
    else:
        print("❌ 일부 테스트 실패")
        print("💡 오류를 확인하고 다시 시도하세요.")
    
    print("=" * 80)

if __name__ == "__main__":
    main()

