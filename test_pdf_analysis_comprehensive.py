"""
요트 문서 PDF 분석 기능 종합 테스트
다양한 문서 형식에 대한 분석 성공/실패 여부를 테스트하고 결과를 정리합니다.
"""

import os
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# chatbot_unified 모듈 경로 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from chatbot_unified import UnifiedYachtChatbot
    from dotenv import load_dotenv
    load_dotenv()
except ImportError as e:
    print(f"❌ 모듈 import 실패: {e}")
    print("💡 chatbot_unified.py가 같은 디렉토리에 있는지 확인하세요.")
    sys.exit(1)


class PDFAnalysisTester:
    """PDF 분석 기능 테스터"""
    
    def __init__(self, api_key: str = None):
        """테스터 초기화"""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            print("❌ GEMINI_API_KEY가 설정되지 않았습니다.")
            sys.exit(1)
        
        self.chatbot = UnifiedYachtChatbot(api_key=self.api_key, mode="cli")
        self.results = []
        self.pdf_dir = Path("data/yachtpdf")
        
    def test_pdf(self, pdf_path: Path) -> Dict:
        """단일 PDF 파일 테스트"""
        print(f"\n{'='*80}")
        print(f"📄 테스트 중: {pdf_path.name}")
        print(f"{'='*80}")
        
        result = {
            "fileName": pdf_path.name,
            "filePath": str(pdf_path),
            "fileSize": pdf_path.stat().st_size if pdf_path.exists() else 0,
            "timestamp": datetime.now().isoformat(),
            "status": "unknown",
            "error": None,
            "analysisResult": None,
            "extractedInfo": {
                "yachtName": None,
                "manufacturer": None,
                "dimensions": None,
                "partsCount": 0,
                "textLength": 0
            }
        }
        
        try:
            # PDF 분석 실행
            response = self.chatbot.chat(f"PDF 분석: {pdf_path}", pdf_file_path=str(pdf_path))
            
            # 응답에서 정보 추출
            if "오류" in response or "error" in response.lower() or "실패" in response:
                result["status"] = "failed"
                result["error"] = response
                print(f"❌ 분석 실패: {response[:200]}")
            else:
                result["status"] = "success"
                result["analysisResult"] = response[:1000]  # 처음 1000자만 저장
                
                # 등록 데이터 확인
                registration_data = self.chatbot.get_registration_data()
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
                
                print(f"✅ 분석 성공")
                print(f"   요트명: {result['extractedInfo']['yachtName'] or 'N/A'}")
                print(f"   제조사: {result['extractedInfo']['manufacturer'] or 'N/A'}")
                
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            print(f"❌ 예외 발생: {e}")
            import traceback
            traceback.print_exc()
        
        self.results.append(result)
        return result
    
    def categorize_pdf(self, pdf_path: Path) -> str:
        """PDF 파일을 카테고리별로 분류"""
        filename_lower = pdf_path.name.lower()
        
        # 카테고리 분류
        if "rule" in filename_lower or "class" in filename_lower:
            return "클래스 규칙서"
        elif "owner" in filename_lower or "manual" in filename_lower:
            return "오너스 매뉴얼"
        elif "brochure" in filename_lower or "press" in filename_lower:
            return "브로셔/프레스 자료"
        elif "handbook" in filename_lower:
            return "핸드북"
        elif "technical" in filename_lower or "inventory" in filename_lower:
            return "기술 문서"
        elif "rigging" in filename_lower:
            return "리깅 가이드"
        elif any(kr in filename_lower for kr in ["정비", "후아", "풀리"]):
            return "한글 문서"
        else:
            return "기타"
    
    def test_all_pdfs(self) -> List[Dict]:
        """모든 PDF 파일 테스트"""
        if not self.pdf_dir.exists():
            print(f"❌ PDF 디렉토리가 없습니다: {self.pdf_dir}")
            return []
        
        pdf_files = list(self.pdf_dir.glob("*.pdf"))
        print(f"\n📚 총 {len(pdf_files)}개의 PDF 파일을 테스트합니다.\n")
        
        for pdf_path in sorted(pdf_files):
            self.test_pdf(pdf_path)
        
        return self.results
    
    def generate_report(self) -> str:
        """테스트 결과 리포트 생성"""
        if not self.results:
            return "테스트 결과가 없습니다."
        
        # 통계 계산
        total = len(self.results)
        success = sum(1 for r in self.results if r["status"] == "success")
        failed = sum(1 for r in self.results if r["status"] == "failed")
        errors = sum(1 for r in self.results if r["status"] == "error")
        
        # 카테고리별 통계
        categories = {}
        for result in self.results:
            pdf_path = Path(result["filePath"])
            category = self.categorize_pdf(pdf_path)
            if category not in categories:
                categories[category] = {"total": 0, "success": 0, "failed": 0, "error": 0}
            categories[category]["total"] += 1
            if result["status"] == "success":
                categories[category]["success"] += 1
            elif result["status"] == "failed":
                categories[category]["failed"] += 1
            else:
                categories[category]["error"] += 1
        
        # 리포트 생성
        report = f"""# 요트 문서 PDF 분석 기능 테스트 결과

## 📊 전체 통계

- **총 테스트 파일 수**: {total}개
- **성공**: {success}개 ({success/total*100:.1f}%)
- **실패**: {failed}개 ({failed/total*100:.1f}%)
- **오류**: {errors}개 ({errors/total*100:.1f}%)

## 📁 카테고리별 통계

"""
        
        for category, stats in sorted(categories.items()):
            success_rate = stats["success"] / stats["total"] * 100 if stats["total"] > 0 else 0
            report += f"### {category}\n"
            report += f"- 총 {stats['total']}개 파일\n"
            report += f"- 성공: {stats['success']}개 ({success_rate:.1f}%)\n"
            report += f"- 실패: {stats['failed']}개\n"
            report += f"- 오류: {stats['error']}개\n\n"
        
        # 성공한 문서
        report += "## ✅ 분석 성공한 문서\n\n"
        success_results = [r for r in self.results if r["status"] == "success"]
        for result in success_results:
            pdf_path = Path(result["filePath"])
            category = self.categorize_pdf(pdf_path)
            report += f"### {result['fileName']}\n"
            report += f"- **카테고리**: {category}\n"
            report += f"- **파일 크기**: {result['fileSize']:,} bytes\n"
            if result["extractedInfo"]["yachtName"]:
                report += f"- **추출된 요트명**: {result['extractedInfo']['yachtName']}\n"
            if result["extractedInfo"]["manufacturer"]:
                report += f"- **추출된 제조사**: {result['extractedInfo']['manufacturer']}\n"
            report += "\n"
        
        # 실패한 문서
        failed_results = [r for r in self.results if r["status"] in ["failed", "error"]]
        if failed_results:
            report += "## ❌ 분석 실패한 문서\n\n"
            for result in failed_results:
                pdf_path = Path(result["filePath"])
                category = self.categorize_pdf(pdf_path)
                report += f"### {result['fileName']}\n"
                report += f"- **카테고리**: {category}\n"
                report += f"- **파일 크기**: {result['fileSize']:,} bytes\n"
                report += f"- **상태**: {result['status']}\n"
                if result["error"]:
                    error_msg = result["error"][:200] if len(result["error"]) > 200 else result["error"]
                    report += f"- **오류 메시지**: {error_msg}\n"
                report += "\n"
        
        # 문서 형식별 작동 여부 요약
        report += "## 📋 문서 형식별 작동 여부 요약\n\n"
        report += "| 문서 형식 | 작동 여부 | 비고 |\n"
        report += "|----------|----------|------|\n"
        
        format_status = {}
        for result in self.results:
            pdf_path = Path(result["filePath"])
            category = self.categorize_pdf(pdf_path)
            if category not in format_status:
                format_status[category] = {"works": 0, "fails": 0}
            if result["status"] == "success":
                format_status[category]["works"] += 1
            else:
                format_status[category]["fails"] += 1
        
        for category, status in sorted(format_status.items()):
            works = status["works"]
            fails = status["fails"]
            total = works + fails
            if works > 0 and fails == 0:
                status_text = "✅ 완벽 작동"
            elif works > fails:
                status_text = "⚠️ 대부분 작동"
            elif works == fails:
                status_text = "⚠️ 부분 작동"
            else:
                status_text = "❌ 작동 안 함"
            
            report += f"| {category} | {status_text} | 성공 {works}/{total} |\n"
        
        # 개선 사항
        report += "\n## 🔧 개선 필요 사항\n\n"
        
        # 텍스트 추출 실패 분석
        text_extraction_fails = [r for r in self.results if "텍스트를 추출할 수 없습니다" in str(r.get("error", ""))]
        if text_extraction_fails:
            report += "### 텍스트 추출 실패\n"
            report += "다음 문서들은 텍스트 추출에 실패했습니다 (스캔된 이미지 PDF일 가능성):\n\n"
            for result in text_extraction_fails:
                report += f"- {result['fileName']}\n"
            report += "\n**해결 방안**: OCR 기능 추가 필요\n\n"
        
        # 분석 실패 사례
        analysis_fails = [r for r in self.results if r["status"] == "failed" and "텍스트를 추출할 수 없습니다" not in str(r.get("error", ""))]
        if analysis_fails:
            report += "### 분석 실패 (텍스트는 추출됨)\n"
            report += "다음 문서들은 텍스트는 추출되었지만 분석에 실패했습니다:\n\n"
            for result in analysis_fails:
                report += f"- {result['fileName']}: {result.get('error', '알 수 없는 오류')[:100]}\n"
            report += "\n**해결 방안**: 프롬프트 개선 또는 문서 형식별 맞춤 분석 로직 필요\n\n"
        
        return report
    
    def save_results(self, output_file: str = "pdf_analysis_test_results.json"):
        """테스트 결과를 JSON 파일로 저장"""
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                "testDate": datetime.now().isoformat(),
                "totalFiles": len(self.results),
                "results": self.results
            }, f, ensure_ascii=False, indent=2)
        print(f"\n💾 테스트 결과 저장: {output_path}")


def main():
    """메인 함수"""
    print("="*80)
    print("🚢 요트 문서 PDF 분석 기능 종합 테스트")
    print("="*80)
    
    tester = PDFAnalysisTester()
    
    # 모든 PDF 테스트
    tester.test_all_pdfs()
    
    # 결과 저장
    tester.save_results()
    
    # 리포트 생성 및 출력
    report = tester.generate_report()
    print("\n" + "="*80)
    print("📊 테스트 리포트")
    print("="*80)
    print(report)
    
    # 리포트 파일로 저장
    report_file = "pdf_analysis_test_report.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n💾 리포트 저장: {report_file}")
    print("\n✅ 테스트 완료!")


if __name__ == "__main__":
    main()

