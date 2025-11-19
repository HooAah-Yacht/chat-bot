"""
HooAah Yacht Document Analyzer - Gemini API 기반 문서 분석
요트 매뉴얼, 부품 정보 등 문서를 분석하여 구조화된 데이터 추출
"""

import os
import json
import google.generativeai as genai
from pathlib import Path
from typing import Dict, List, Optional
import base64

# PDF 텍스트 추출을 위한 라이브러리
try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False
    try:
        import pdfplumber
        HAS_PDFPLUMBER = True
    except ImportError:
        HAS_PDFPLUMBER = False

class YachtDocumentAnalyzer:
    def __init__(self, api_key: str = None):
        """
        Gemini API 기반 요트 문서 분석기 초기화
        
        Args:
            api_key: Gemini API 키 (없으면 환경변수에서 가져옴)
        """
        # API 키 설정
        if api_key is None:
            api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다.")
        
        # Gemini API 설정
        genai.configure(api_key=api_key)
        
        # 모델 초기화 - Gemini 2.5 Flash 사용 (2025년 6월 출시, 2026년 6월까지 지원)
        # 참고: https://ai.google.dev/gemini-api/docs/deprecations?hl=ko
        try:
            # Gemini 2.5 Flash 모델 사용 (최신 안정 모델)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            print("✅ Gemini 2.5 Flash 모델 사용")
        except Exception as e:
            print(f"⚠️ Gemini 2.5 Flash 모델 초기화 실패: {e}")
            # Fallback: gemini-pro 사용
            try:
                self.model = genai.GenerativeModel('gemini-pro')
                print("✅ gemini-pro 모델 사용 (fallback)")
            except Exception as e2:
                print(f"❌ 모델 초기화 실패: {e2}")
                raise
        
        print("✅ HooAah Yacht Document Analyzer가 준비되었습니다!")
    
    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        PDF에서 텍스트 추출
        
        Args:
            pdf_path: PDF 파일 경로
            
        Returns:
            추출된 텍스트
        """
        text = ""
        
        if HAS_PYPDF2:
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                return text
            except Exception as e:
                print(f"⚠️ PyPDF2로 텍스트 추출 실패: {e}")
        
        if HAS_PDFPLUMBER:
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                return text
            except Exception as e:
                print(f"⚠️ pdfplumber로 텍스트 추출 실패: {e}")
        
        # 텍스트 추출 실패
        return ""
    
    def analyze_pdf(self, pdf_path: str, use_file_upload: bool = False) -> Dict:
        """
        PDF 문서 분석
        
        Args:
            pdf_path: PDF 파일 경로
            use_file_upload: True면 파일 업로드 방식, False면 텍스트 추출 방식
            
        Returns:
            분석 결과 딕셔너리
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {pdf_path}")
        
        print(f"\n📄 문서 분석 시작: {os.path.basename(pdf_path)}")
        
        try:
            # 방법 1: 파일 업로드 방식 (gemini-1.5-pro만 지원)
            if use_file_upload:
                try:
                    pdf_file = genai.upload_file(path=pdf_path)
                    print(f"✅ 파일 업로드 완료")
                    
                    # 분석 프롬프트
                    prompt = """이 PDF 문서는 요트 매뉴얼 또는 부품 정보 문서입니다.

다음 정보를 추출하여 JSON 형식으로 반환해주세요:

1. **문서 기본 정보:**
   - 문서 제목
   - 요트 모델명 (있는 경우)
   - 제조사 (있는 경우)
   - 문서 유형 (매뉴얼, 부품 목록, 기술 사양서 등)

2. **요트 스펙 정보 (있는 경우):**
   - 전장 (LOA)
   - 폭 (Beam)
   - 흘수 (Draft)
   - 배수량 (Displacement)
   - 마스트 높이
   - 엔진 정보 (타입, 출력, 모델)
   - 돛 면적

3. **부품 정보 (있는 경우):**
   - 부품명 (name)
   - 제조사 (manufacturer)
   - 모델명 (model)
   - 정비 주기 (interval, 단위: 개월)
   - 부품 카테고리 (Rigging, Sails, Engine, Hull 등)

4. **정비 정보 (있는 경우):**
   - 정비 항목
   - 정비 주기
   - 정비 방법

5. **문서 형식 평가:**
   - 텍스트 추출 가능 여부
   - 이미지/표 추출 가능 여부
   - 분석 가능 여부 (가능/불가능)
   - 불가능한 경우 이유

**응답 형식:**
```json
{
  "documentInfo": {
    "title": "...",
    "yachtModel": "...",
    "manufacturer": "...",
    "documentType": "..."
  },
  "yachtSpecs": {
    "dimensions": {...},
    "engine": {...},
    "sailArea": {...}
  },
  "parts": [
    {
      "name": "...",
      "manufacturer": "...",
      "model": "...",
      "interval": 12,
      "category": "..."
    }
  ],
  "maintenance": [...],
  "analysisResult": {
    "canExtractText": true/false,
    "canExtractImages": true/false,
    "canAnalyze": true/false,
    "reason": "..."
  }
}
```

JSON 형식으로만 응답해주세요. 다른 설명은 필요 없습니다."""

                    # Gemini API 호출
                    print("🤖 AI 분석 중...")
                    response = self.model.generate_content([pdf_file, prompt])
                    
                    # 응답 파싱
                    result_text = response.text
                    
                    # JSON 추출 (마크다운 코드 블록 제거)
                    if "```json" in result_text:
                        json_start = result_text.find("```json") + 7
                        json_end = result_text.find("```", json_start)
                        result_text = result_text[json_start:json_end].strip()
                    elif "```" in result_text:
                        json_start = result_text.find("```") + 3
                        json_end = result_text.find("```", json_start)
                        result_text = result_text[json_start:json_end].strip()
                    
                    # JSON 파싱
                    try:
                        result = json.loads(result_text)
                    except json.JSONDecodeError:
                        # JSON 파싱 실패 시 텍스트 그대로 반환
                        result = {
                            "rawResponse": result_text,
                            "error": "JSON 파싱 실패"
                        }
                    
                    # 파일 정보 추가
                    result["fileInfo"] = {
                        "fileName": os.path.basename(pdf_path),
                        "filePath": pdf_path,
                        "fileSize": os.path.getsize(pdf_path)
                    }
                    
                    print("✅ 분석 완료!")
                    return result
                except Exception as upload_error:
                    print(f"⚠️ 파일 업로드 실패, 텍스트 추출 방식으로 전환: {upload_error}")
                    use_file_upload = False
            
            # 방법 2: 텍스트 추출 방식 (fallback)
            if not use_file_upload:
                # PDF에서 텍스트 추출
                print("📝 PDF에서 텍스트 추출 중...")
                extracted_text = self._extract_text_from_pdf(pdf_path)
                
                if not extracted_text or len(extracted_text.strip()) < 100:
                    return {
                        "error": "PDF에서 텍스트를 추출할 수 없습니다. 스캔된 이미지 PDF일 수 있습니다.",
                        "fileInfo": {
                            "fileName": os.path.basename(pdf_path),
                            "filePath": pdf_path,
                            "fileSize": os.path.getsize(pdf_path)
                        },
                        "analysisResult": {
                            "canExtractText": False,
                            "canExtractImages": False,
                            "canAnalyze": False,
                            "reason": "텍스트 추출 실패 - 스캔된 이미지 PDF일 가능성"
                        }
                    }
                
                print(f"✅ 텍스트 추출 완료 ({len(extracted_text)} 문자)")
                
                # 텍스트가 너무 길면 앞부분만 사용 (토큰 제한 고려)
                if len(extracted_text) > 30000:
                    extracted_text = extracted_text[:30000] + "\n\n[... 텍스트가 너무 길어 일부만 분석합니다 ...]"
                
                # 분석 프롬프트
                prompt = f"""다음은 요트 매뉴얼 또는 부품 정보 문서에서 추출한 텍스트입니다:

{extracted_text}

위 텍스트를 분석하여 다음 정보를 추출하여 JSON 형식으로 반환해주세요:

1. **문서 기본 정보:**
   - 문서 제목
   - 요트 모델명 (있는 경우)
   - 제조사 (있는 경우)
   - 문서 유형 (매뉴얼, 부품 목록, 기술 사양서 등)

2. **요트 스펙 정보 (있는 경우):**
   - 전장 (LOA)
   - 폭 (Beam)
   - 흘수 (Draft)
   - 배수량 (Displacement)
   - 마스트 높이
   - 엔진 정보 (타입, 출력, 모델)
   - 돛 면적

3. **부품 정보 (있는 경우):**
   - 부품명 (name)
   - 제조사 (manufacturer)
   - 모델명 (model)
   - 정비 주기 (interval, 단위: 개월)
   - 부품 카테고리 (Rigging, Sails, Engine, Hull 등)

4. **정비 정보 (있는 경우):**
   - 정비 항목
   - 정비 주기
   - 정비 방법

5. **문서 형식 평가:**
   - 텍스트 추출 가능 여부
   - 분석 가능 여부 (가능/불가능)
   - 불가능한 경우 이유

**응답 형식:**
```json
{{
  "documentInfo": {{
    "title": "...",
    "yachtModel": "...",
    "manufacturer": "...",
    "documentType": "..."
  }},
  "yachtSpecs": {{
    "dimensions": {{}},
    "engine": {{}},
    "sailArea": {{}}
  }},
  "parts": [
    {{
      "name": "...",
      "manufacturer": "...",
      "model": "...",
      "interval": 12,
      "category": "..."
    }}
  ],
  "maintenance": [],
  "analysisResult": {{
    "canExtractText": true/false,
    "canAnalyze": true/false,
    "reason": "..."
  }}
}}
```

JSON 형식으로만 응답해주세요. 다른 설명은 필요 없습니다."""

                # Gemini API 호출
                print("🤖 AI 분석 중...")
                response = self.model.generate_content(prompt)
                
                # 응답 파싱
                result_text = response.text
                
                # JSON 추출 (마크다운 코드 블록 제거)
                if "```json" in result_text:
                    json_start = result_text.find("```json") + 7
                    json_end = result_text.find("```", json_start)
                    result_text = result_text[json_start:json_end].strip()
                elif "```" in result_text:
                    json_start = result_text.find("```") + 3
                    json_end = result_text.find("```", json_start)
                    result_text = result_text[json_start:json_end].strip()
                
                # JSON 파싱
                try:
                    result = json.loads(result_text)
                except json.JSONDecodeError:
                    # JSON 파싱 실패 시 텍스트 그대로 반환
                    result = {
                        "rawResponse": result_text,
                        "error": "JSON 파싱 실패",
                        "extractedTextLength": len(extracted_text)
                    }
                
                # 파일 정보 추가
                result["fileInfo"] = {
                    "fileName": os.path.basename(pdf_path),
                    "filePath": pdf_path,
                    "fileSize": os.path.getsize(pdf_path)
                }
                
                print("✅ 분석 완료!")
                return result
            
        except Exception as e:
            error_result = {
                "error": str(e),
                "fileInfo": {
                    "fileName": os.path.basename(pdf_path),
                    "filePath": pdf_path
                },
                "analysisResult": {
                    "canAnalyze": False,
                    "reason": f"오류 발생: {str(e)}"
                }
            }
            print(f"❌ 분석 실패: {e}")
            return error_result
    
    def analyze_multiple_pdfs(self, pdf_directory: str) -> List[Dict]:
        """
        여러 PDF 파일 일괄 분석
        
        Args:
            pdf_directory: PDF 파일이 있는 디렉토리 경로
            
        Returns:
            분석 결과 리스트
        """
        pdf_dir = Path(pdf_directory)
        if not pdf_dir.exists():
            raise FileNotFoundError(f"디렉토리를 찾을 수 없습니다: {pdf_directory}")
        
        pdf_files = list(pdf_dir.glob("*.pdf"))
        
        if not pdf_files:
            print(f"⚠️ {pdf_directory}에 PDF 파일이 없습니다.")
            return []
        
        print(f"\n📚 총 {len(pdf_files)}개의 PDF 파일을 분석합니다.\n")
        
        results = []
        for i, pdf_file in enumerate(pdf_files, 1):
            print(f"\n[{i}/{len(pdf_files)}] {pdf_file.name}")
            print("=" * 60)
            
            try:
                result = self.analyze_pdf(str(pdf_file))
                results.append(result)
            except Exception as e:
                print(f"❌ {pdf_file.name} 분석 실패: {e}")
                results.append({
                    "error": str(e),
                    "fileInfo": {
                        "fileName": pdf_file.name,
                        "filePath": str(pdf_file)
                    }
                })
        
        return results
    
    def save_results(self, results: List[Dict], output_file: str = "document_analysis_results.json"):
        """
        분석 결과 저장
        
        Args:
            results: 분석 결과 리스트
            output_file: 출력 파일 경로
        """
        output_path = Path(output_file)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 분석 결과가 {output_path}에 저장되었습니다.")
    
    def generate_summary_report(self, results: List[Dict]) -> str:
        """
        분석 결과 요약 보고서 생성
        
        Args:
            results: 분석 결과 리스트
            
        Returns:
            마크다운 형식의 요약 보고서
        """
        report = "# 📊 요트 문서 분석 결과 요약\n\n"
        report += f"**분석 일시**: {Path().cwd()}\n"
        report += f"**총 문서 수**: {len(results)}\n\n"
        
        # 성공/실패 통계
        success_count = sum(1 for r in results if "error" not in r)
        fail_count = len(results) - success_count
        
        report += "## 📈 통계\n\n"
        report += f"- ✅ 분석 성공: {success_count}개\n"
        report += f"- ❌ 분석 실패: {fail_count}개\n\n"
        
        # 문서 형식별 분류
        report += "## 📄 문서 형식별 분류\n\n"
        
        analyzable = []
        not_analyzable = []
        
        for result in results:
            if "error" in result:
                not_analyzable.append(result)
                continue
            
            analysis_result = result.get("analysisResult", {})
            can_analyze = analysis_result.get("canAnalyze", False)
            
            if can_analyze:
                analyzable.append(result)
            else:
                not_analyzable.append(result)
        
        report += f"### ✅ 분석 가능한 문서 ({len(analyzable)}개)\n\n"
        for result in analyzable:
            file_name = result.get("fileInfo", {}).get("fileName", "Unknown")
            doc_type = result.get("documentInfo", {}).get("documentType", "Unknown")
            report += f"- **{file_name}** ({doc_type})\n"
        
        report += f"\n### ❌ 분석 불가능한 문서 ({len(not_analyzable)}개)\n\n"
        for result in not_analyzable:
            file_name = result.get("fileInfo", {}).get("fileName", "Unknown")
            reason = result.get("analysisResult", {}).get("reason", "알 수 없음")
            if "error" in result:
                reason = result["error"]
            report += f"- **{file_name}**: {reason}\n"
        
        # 상세 결과
        report += "\n## 📋 상세 분석 결과\n\n"
        
        for i, result in enumerate(results, 1):
            file_name = result.get("fileInfo", {}).get("fileName", "Unknown")
            report += f"### {i}. {file_name}\n\n"
            
            if "error" in result:
                report += f"**오류**: {result['error']}\n\n"
                continue
            
            # 문서 정보
            doc_info = result.get("documentInfo", {})
            if doc_info:
                report += "**문서 정보:**\n"
                report += f"- 제목: {doc_info.get('title', 'N/A')}\n"
                report += f"- 요트 모델: {doc_info.get('yachtModel', 'N/A')}\n"
                report += f"- 제조사: {doc_info.get('manufacturer', 'N/A')}\n"
                report += f"- 문서 유형: {doc_info.get('documentType', 'N/A')}\n\n"
            
            # 부품 정보
            parts = result.get("parts", [])
            if parts:
                report += f"**부품 정보 ({len(parts)}개):**\n"
                for part in parts[:5]:  # 최대 5개만 표시
                    report += f"- {part.get('name', 'N/A')} ({part.get('manufacturer', 'N/A')})\n"
                if len(parts) > 5:
                    report += f"- ... 외 {len(parts) - 5}개\n"
                report += "\n"
            
            # 분석 결과
            analysis_result = result.get("analysisResult", {})
            if analysis_result:
                report += "**분석 결과:**\n"
                report += f"- 텍스트 추출: {'가능' if analysis_result.get('canExtractText') else '불가능'}\n"
                report += f"- 이미지 추출: {'가능' if analysis_result.get('canExtractImages') else '불가능'}\n"
                report += f"- 분석 가능: {'가능' if analysis_result.get('canAnalyze') else '불가능'}\n"
                if not analysis_result.get('canAnalyze'):
                    report += f"- 이유: {analysis_result.get('reason', 'N/A')}\n"
                report += "\n"
            
            report += "---\n\n"
        
        return report


def main():
    """메인 함수 - 테스트 실행"""
    print("=" * 60)
    print("🛥️  HooAah Yacht Document Analyzer")
    print("=" * 60)
    print()
    
    # API 키 설정
    api_key = "AIzaSyBhPZDNBTEqYu8ahBIVpK2B1h_CAKgo7JI"
    
    try:
        # 분석기 초기화
        analyzer = YachtDocumentAnalyzer(api_key=api_key)
        
        # PDF 디렉토리 경로
        pdf_directory = "data/yachtpdf"
        
        # 여러 PDF 분석
        results = analyzer.analyze_multiple_pdfs(pdf_directory)
        
        # 결과 저장
        analyzer.save_results(results, "document_analysis_results.json")
        
        # 요약 보고서 생성
        report = analyzer.generate_summary_report(results)
        
        # 보고서 저장
        with open("document_analysis_report.md", "w", encoding="utf-8") as f:
            f.write(report)
        
        print("\n" + "=" * 60)
        print("📊 요약 보고서:")
        print("=" * 60)
        print(report)
        
        print("\n✅ 모든 분석이 완료되었습니다!")
        print("📁 결과 파일:")
        print("  - document_analysis_results.json (상세 결과)")
        print("  - document_analysis_report.md (요약 보고서)")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

