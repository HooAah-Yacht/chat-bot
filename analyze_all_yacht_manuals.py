"""
20종 요트 메뉴얼 PDF 전체 분석 스크립트
모든 PDF를 분석하고 결과를 정리합니다.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# UTF-8 인코딩 설정
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# chatbot_unified 모듈 경로 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from chatbot_unified import UnifiedYachtChatbot
    from dotenv import load_dotenv
    load_dotenv()
except ImportError as e:
    print(f"❌ 모듈 import 실패: {e}")
    sys.exit(1)

# 20종 요트 목록
YACHT_LIST = [
    {"name": "FarEast 28", "pdf": "OC15aiiFAREAST28RClassrules-[19458].pdf"},
    {"name": "Farr 40", "pdf": "rulebook.pdf"},
    {"name": "Beneteau 473", "pdf": "Beneteau 473 Owner's Manual_compressed.pdf"},
    {"name": "J/24", "pdf": "J242019CR220319-[24866].pdf"},
    {"name": "Laser", "pdf": "Handbook_2109.pdf"},
    {"name": "Swan 50", "pdf": "ClubSwan50ClassRules07042021-[27210].pdf"},
    {"name": "X-35", "pdf": "X352012CR080412-[12381].pdf"},
    {"name": "Melges 32", "pdf": "M32_CR_2025-03March-30.pdf"},
    {"name": "TP52", "pdf": "TP52_CR20220124.pdf"},
    {"name": "Beneteau First 36", "pdf": "owners_manual.pdf"},
    {"name": "Jeanneau Sun Fast 3300", "pdf": "Sun-Fast-3300-technical-inventory.pdf"},
    {"name": "Dehler 38", "pdf": "press-manual-dehler38.pdf"},
    {"name": "X-Yachts XP 44", "pdf": "Xp44-Brochure_July2018_ONLINE.pdf"},
    {"name": "Hanse 458", "pdf": "Owners-Manual-458-Buch-eng-V8-allg.pdf"},
    {"name": "Beneteau Oceanis 46", "pdf": "14670061006300089_USER_MANUAL_OCEANIS_46.1.pdf"},
    {"name": "Nautor Swan 48", "pdf": "2020_03_31_11_03_39-48 owners manual.pdf"},
    {"name": "Grand Soleil GC 42", "pdf": "GS42LC_Brochure-1.pdf"},
    {"name": "RS21", "pdf": "RS21Riggingguide.pdf"},
    {"name": "J/70", "pdf": "j70-user-manual.pdf"},
    {"name": "Solaris 44", "pdf": "Solaris-44.pdf"},
]


def analyze_all_manuals():
    """모든 요트 메뉴얼 분석"""
    print("="*80)
    print("🚢 20종 요트 메뉴얼 PDF 전체 분석")
    print("="*80)
    print()
    
    # API 키 확인
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY가 설정되지 않았습니다.")
        print("💡 .env 파일에 GEMINI_API_KEY를 설정하세요.")
        return
    
    # 챗봇 초기화
    chatbot = UnifiedYachtChatbot(api_key=api_key, mode="cli")
    
    pdf_dir = Path("data/yachtpdf")
    if not pdf_dir.exists():
        print(f"❌ PDF 디렉토리가 없습니다: {pdf_dir}")
        return
    
    results = []
    success_count = 0
    fail_count = 0
    
    print(f"📚 총 {len(YACHT_LIST)}개의 요트 메뉴얼을 분석합니다.\n")
    
    for i, yacht_info in enumerate(YACHT_LIST, 1):
        yacht_name = yacht_info["name"]
        pdf_filename = yacht_info["pdf"]
        pdf_path = pdf_dir / pdf_filename
        
        print(f"\n{'='*80}")
        print(f"[{i}/{len(YACHT_LIST)}] {yacht_name}")
        print(f"파일: {pdf_filename}")
        print(f"{'='*80}")
        
        result = {
            "yachtName": yacht_name,
            "pdfFile": pdf_filename,
            "pdfPath": str(pdf_path),
            "exists": pdf_path.exists(),
            "timestamp": datetime.now().isoformat(),
            "status": "unknown",
            "error": None,
            "extractedInfo": {
                "yachtName": None,
                "manufacturer": None,
                "dimensions": None,
                "partsCount": 0
            }
        }
        
        if not pdf_path.exists():
            result["status"] = "file_not_found"
            result["error"] = "PDF 파일이 없습니다."
            print(f"❌ 파일 없음: {pdf_path}")
            fail_count += 1
            results.append(result)
            continue
        
        try:
            # PDF 분석 실행
            print(f"📄 분석 시작...")
            response = chatbot.chat(f"요트 등록: {yacht_name}", pdf_file_path=str(pdf_path))
            
            # 응답 확인
            if "오류" in response or "error" in response.lower() or "실패" in response or "추출할 수 없습니다" in response:
                result["status"] = "failed"
                result["error"] = response[:500]  # 처음 500자만
                print(f"❌ 분석 실패")
                print(f"   오류: {response[:200]}")
                fail_count += 1
            else:
                result["status"] = "success"
                print(f"✅ 분석 성공")
                success_count += 1
                
                # 등록 데이터 확인
                registration_data = chatbot.get_registration_data()
                if registration_data:
                    basic_info = registration_data.get("basicInfo", {})
                    result["extractedInfo"]["yachtName"] = basic_info.get("name")
                    result["extractedInfo"]["manufacturer"] = basic_info.get("manufacturer")
                    
                    specs = registration_data.get("specifications", {})
                    dims = specs.get("dimensions", {})
                    if dims:
                        result["extractedInfo"]["dimensions"] = {
                            "loa": dims.get("loa"),
                            "beam": dims.get("beam"),
                            "draft": dims.get("draft")
                        }
                    
                    # 부품 개수 확인
                    parts = registration_data.get("parts", [])
                    if isinstance(parts, list):
                        result["extractedInfo"]["partsCount"] = len(parts)
                    elif isinstance(parts, dict):
                        total = 0
                        for category_parts in parts.values():
                            if isinstance(category_parts, list):
                                total += len(category_parts)
                        result["extractedInfo"]["partsCount"] = total
                
                print(f"   요트명: {result['extractedInfo']['yachtName'] or 'N/A'}")
                print(f"   제조사: {result['extractedInfo']['manufacturer'] or 'N/A'}")
                print(f"   부품 수: {result['extractedInfo']['partsCount']}개")
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            print(f"❌ 예외 발생: {e}")
            import traceback
            traceback.print_exc()
            fail_count += 1
        
        results.append(result)
        print()
    
    # 결과 저장
    output_file = "yacht_manuals_analysis_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "analysisDate": datetime.now().isoformat(),
            "totalYachts": len(YACHT_LIST),
            "successCount": success_count,
            "failCount": fail_count,
            "results": results
        }, f, ensure_ascii=False, indent=2)
    
    # 리포트 생성
    report = generate_report(results, success_count, fail_count)
    print("\n" + "="*80)
    print("📊 분석 결과 리포트")
    print("="*80)
    print(report)
    
    # 리포트 파일로 저장
    report_file = "yacht_manuals_analysis_report.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n💾 결과 저장:")
    print(f"   - JSON: {output_file}")
    print(f"   - 리포트: {report_file}")
    print("\n✅ 전체 분석 완료!")


def generate_report(results, success_count, fail_count):
    """분석 결과 리포트 생성"""
    total = len(results)
    success_rate = (success_count / total * 100) if total > 0 else 0
    
    report = f"""# 20종 요트 메뉴얼 PDF 분석 결과

## 📊 전체 통계

- **총 요트 수**: {total}개
- **분석 성공**: {success_count}개 ({success_rate:.1f}%)
- **분석 실패**: {fail_count}개 ({(100-success_rate):.1f}%)

## ✅ 분석 성공한 요트

"""
    
    success_results = [r for r in results if r["status"] == "success"]
    for result in success_results:
        report += f"### {result['yachtName']}\n"
        report += f"- **PDF 파일**: {result['pdfFile']}\n"
        if result["extractedInfo"]["yachtName"]:
            report += f"- **추출된 요트명**: {result['extractedInfo']['yachtName']}\n"
        if result["extractedInfo"]["manufacturer"]:
            report += f"- **제조사**: {result['extractedInfo']['manufacturer']}\n"
        if result["extractedInfo"]["dimensions"]:
            dims = result["extractedInfo"]["dimensions"]
            report += f"- **치수**: "
            dim_parts = []
            if dims.get("loa"):
                dim_parts.append(f"LOA: {dims['loa']}")
            if dims.get("beam"):
                dim_parts.append(f"Beam: {dims['beam']}")
            if dims.get("draft"):
                dim_parts.append(f"Draft: {dims['draft']}")
            report += ", ".join(dim_parts) + "\n"
        report += f"- **추출된 부품 수**: {result['extractedInfo']['partsCount']}개\n"
        report += "\n"
    
    # 실패한 요트
    failed_results = [r for r in results if r["status"] in ["failed", "error", "file_not_found"]]
    if failed_results:
        report += "## ❌ 분석 실패한 요트\n\n"
        for result in failed_results:
            report += f"### {result['yachtName']}\n"
            report += f"- **PDF 파일**: {result['pdfFile']}\n"
            report += f"- **상태**: {result['status']}\n"
            if result["error"]:
                error_msg = result["error"][:200] if len(result["error"]) > 200 else result["error"]
                report += f"- **오류**: {error_msg}\n"
            report += "\n"
    
    # 문서 형식별 통계
    report += "## 📋 문서 형식별 분석 결과\n\n"
    report += "| 문서 유형 | 성공 | 실패 | 성공률 |\n"
    report += "|----------|------|------|--------|\n"
    
    # 카테고리 분류
    categories = {}
    for result in results:
        pdf_name = result["pdfFile"].lower()
        if "rule" in pdf_name or "class" in pdf_name:
            category = "클래스 규칙서"
        elif "owner" in pdf_name or "manual" in pdf_name:
            category = "오너스 매뉴얼"
        elif "brochure" in pdf_name or "press" in pdf_name:
            category = "브로셔"
        elif "handbook" in pdf_name:
            category = "핸드북"
        elif "technical" in pdf_name or "inventory" in pdf_name:
            category = "기술 문서"
        else:
            category = "기타"
        
        if category not in categories:
            categories[category] = {"success": 0, "fail": 0}
        
        if result["status"] == "success":
            categories[category]["success"] += 1
        else:
            categories[category]["fail"] += 1
    
    for category, stats in sorted(categories.items()):
        total = stats["success"] + stats["fail"]
        rate = (stats["success"] / total * 100) if total > 0 else 0
        report += f"| {category} | {stats['success']} | {stats['fail']} | {rate:.1f}% |\n"
    
    return report


if __name__ == "__main__":
    analyze_all_manuals()

