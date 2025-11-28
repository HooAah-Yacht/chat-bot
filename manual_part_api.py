#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
부품 수동 등록 API 서버
피그마 "요트 등록하기" 화면 지원

기능:
1. 수동 부품 등록 (장비명, 제조사명, 모델명, 최근 정비일, 정비 주기)
2. PDF 업로드 및 부품 추출
3. 백엔드 MySQL DB에 직접 저장

사용법:
    python manual_part_api.py --port 5002
    
엔드포인트:
    POST /api/part/manual - 수동 부품 등록
    POST /api/part/upload-pdf - PDF 업로드 및 자동 추출
    GET /api/part/list?yachtId={id} - 요트의 부품 목록 조회
"""

import sys
import os
from datetime import datetime
from typing import List, Dict, Optional

# Windows 콘솔 인코딩
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# Flask
from flask import Flask, request, jsonify
from flask_cors import CORS

# Gemini AI (부품 추출용)
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False
    print("⚠️ google-generativeai 없음. PDF 추출 기능 비활성화")

# PDF 처리
try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False

# MySQL 연결 (선택사항 - 백엔드 API 대신 직접 DB 접근 시)
try:
    import mysql.connector
    HAS_MYSQL = True
except ImportError:
    HAS_MYSQL = False
    print("⚠️ mysql-connector-python 없음. pip install mysql-connector-python")

# HTTP 요청 (백엔드 API 호출용)
import requests


class ManualPartService:
    """수동 부품 등록 서비스"""
    
    def __init__(self, backend_url: str = "http://localhost:8080", api_key: str = None):
        self.backend_url = backend_url
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        # Gemini 초기화
        if HAS_GEMINI and self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            print("✅ Gemini AI 준비 완료")
        else:
            self.model = None
            print("⚠️ Gemini AI 비활성화 (PDF 자동 추출 불가)")
        
        print(f"✅ 백엔드 URL: {self.backend_url}")
    
    def register_manual_part(self, yacht_id: int, part_data: Dict) -> Dict:
        """
        수동 부품 등록
        
        Args:
            yacht_id: 요트 ID
            part_data: {
                "name": "장비명",
                "manufacturer": "제조사명",
                "model": "모델명",
                "lastRepair": "2025-11-28",  # ISO 8601
                "interval": 12
            }
        
        Returns:
            {"success": True, "partId": 123}
        """
        try:
            # 백엔드 API 호출
            response = requests.post(
                f"{self.backend_url}/api/part",
                json={
                    "yachtId": yacht_id,
                    "name": part_data.get("name"),
                    "manufacturer": part_data.get("manufacturer", ""),
                    "model": part_data.get("model", ""),
                    "interval": part_data.get("interval", 12),
                    "lastRepair": part_data.get("lastRepair", datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z"))
                },
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "partId": response.json().get("id"),
                    "message": "부품이 등록되었습니다."
                }
            else:
                return {
                    "success": False,
                    "error": f"백엔드 오류: {response.status_code}",
                    "details": response.text
                }
        
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "백엔드 서버에 연결할 수 없습니다. localhost:8080이 실행 중인지 확인하세요."
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def extract_parts_from_pdf(self, pdf_path: str) -> Dict:
        """
        PDF에서 부품 정보 추출 (Gemini AI 사용)
        
        Returns:
            {
                "success": True,
                "parts": [
                    {
                        "name": "Engine",
                        "manufacturer": "YANMAR",
                        "model": "3GM30",
                        "interval": 12
                    }
                ]
            }
        """
        if not self.model:
            return {
                "success": False,
                "error": "Gemini API가 설정되지 않았습니다."
            }
        
        try:
            # PDF 텍스트 추출
            text = self._extract_text_from_pdf(pdf_path)
            
            if not text or len(text.strip()) < 100:
                return {
                    "success": False,
                    "error": "PDF에서 텍스트를 추출할 수 없습니다."
                }
            
            # AI 분석 프롬프트 (간단 버전)
            prompt = f"""다음은 요트 매뉴얼에서 추출한 텍스트입니다:

{text[:10000]}

---

## 작업: 부품 목록만 간단히 추출

아래 JSON 형식으로만 응답하세요:

```json
{{
  "parts": [
    {{
      "name": "부품명",
      "manufacturer": "제조사 (있다면)",
      "model": "모델명 (있다면)",
      "interval": 12,
      "category": "Engine/Rigging/Deck/Electrical/Other"
    }}
  ]
}}
```

- 중요한 부품만 추출 (최대 20개)
- 불확실한 정보는 null
- JSON만 응답
"""
            
            print("🤖 AI 분석 중...")
            response = self.model.generate_content(prompt)
            result_text = response.text
            
            # JSON 추출
            import json
            if "```json" in result_text:
                json_start = result_text.find("```json") + 7
                json_end = result_text.find("```", json_start)
                result_text = result_text[json_start:json_end].strip()
            elif "```" in result_text:
                json_start = result_text.find("```") + 3
                json_end = result_text.find("```", json_start)
                result_text = result_text[json_start:json_end].strip()
            
            result = json.loads(result_text)
            
            return {
                "success": True,
                "parts": result.get("parts", []),
                "count": len(result.get("parts", []))
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """PDF에서 텍스트 추출"""
        if not HAS_PYPDF2:
            return ""
        
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages[:10]:  # 최대 10페이지
                    text += page.extract_text() or ""
            return text
        except Exception as e:
            print(f"❌ PDF 추출 오류: {e}")
            return ""
    
    def get_parts_list(self, yacht_id: int) -> Dict:
        """요트의 부품 목록 조회"""
        try:
            response = requests.get(
                f"{self.backend_url}/api/part/yacht/{yacht_id}",
                timeout=10
            )
            
            if response.status_code == 200:
                parts = response.json()
                return {
                    "success": True,
                    "parts": parts,
                    "count": len(parts)
                }
            else:
                return {
                    "success": False,
                    "error": f"조회 실패: {response.status_code}"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


def create_app(backend_url: str = "http://localhost:8080", api_key: str = None, port: int = 5002):
    """Flask 앱 생성"""
    app = Flask(__name__)
    CORS(app)
    
    service = ManualPartService(backend_url=backend_url, api_key=api_key)
    
    @app.route('/api/part/manual', methods=['POST'])
    def register_manual_part():
        """
        수동 부품 등록
        
        Request (JSON):
        {
            "yachtId": 123,
            "name": "장비명",
            "manufacturer": "제조사명",
            "model": "모델명",
            "lastRepair": "2025-11-28",
            "interval": 12
        }
        """
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({"success": False, "error": "JSON 데이터가 필요합니다."}), 400
            
            yacht_id = data.get('yachtId')
            if not yacht_id:
                return jsonify({"success": False, "error": "yachtId가 필요합니다."}), 400
            
            name = data.get('name')
            if not name:
                return jsonify({"success": False, "error": "부품명(name)이 필요합니다."}), 400
            
            # 백엔드에 등록
            result = service.register_manual_part(yacht_id, data)
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 500
        
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    @app.route('/api/part/upload-pdf', methods=['POST'])
    def upload_pdf():
        """
        PDF 업로드 및 부품 자동 추출
        
        Request:
        - multipart/form-data
        - file: PDF 파일
        - yachtId: 요트 ID
        """
        try:
            if 'file' not in request.files:
                return jsonify({"success": False, "error": "파일이 필요합니다."}), 400
            
            file = request.files['file']
            yacht_id = request.form.get('yachtId')
            
            if not yacht_id:
                return jsonify({"success": False, "error": "yachtId가 필요합니다."}), 400
            
            if file.filename == '':
                return jsonify({"success": False, "error": "파일명이 비어있습니다."}), 400
            
            # 파일 저장
            upload_folder = 'uploads'
            os.makedirs(upload_folder, exist_ok=True)
            
            file_path = os.path.join(upload_folder, file.filename)
            file.save(file_path)
            
            # 부품 추출
            result = service.extract_parts_from_pdf(file_path)
            
            if result['success']:
                return jsonify({
                    "success": True,
                    "parts": result['parts'],
                    "count": result['count'],
                    "message": f"{result['count']}개 부품이 추출되었습니다. 등록할 부품을 선택하세요."
                }), 200
            else:
                return jsonify(result), 500
        
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    @app.route('/api/part/list', methods=['GET'])
    def get_parts_list():
        """
        요트의 부품 목록 조회
        
        Query:
        - yachtId: 요트 ID
        """
        try:
            yacht_id = request.args.get('yachtId')
            
            if not yacht_id:
                return jsonify({"success": False, "error": "yachtId가 필요합니다."}), 400
            
            result = service.get_parts_list(int(yacht_id))
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 500
        
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({
            "success": True,
            "service": "Manual Part API",
            "status": "running",
            "backend": service.backend_url,
            "aiEnabled": service.model is not None
        }), 200
    
    # 서버 시작 메시지
    print("=" * 60)
    print("🛠️  수동 부품 등록 API 서버")
    print("=" * 60)
    print(f"🚀 서버: http://localhost:{port}")
    print(f"🔗 백엔드: {backend_url}")
    print()
    print("📡 엔드포인트:")
    print("  - POST /api/part/manual")
    print("      수동 부품 등록 (장비명, 제조사, 모델, 정비일, 주기)")
    print()
    print("  - POST /api/part/upload-pdf")
    print("      PDF 업로드 및 자동 추출")
    print()
    print("  - GET /api/part/list?yachtId={id}")
    print("      요트의 부품 목록 조회")
    print()
    print("  - GET /api/health")
    print("      서버 상태 확인")
    print("=" * 60)
    print()
    
    app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='수동 부품 등록 API')
    parser.add_argument('--port', type=int, default=5002, help='포트 (기본: 5002)')
    parser.add_argument('--backend', type=str, default='http://localhost:8080', help='백엔드 URL')
    parser.add_argument('--api-key', type=str, help='Gemini API 키 (PDF 추출용)')
    
    args = parser.parse_args()
    
    create_app(
        backend_url=args.backend,
        api_key=args.api_key or os.getenv('GEMINI_API_KEY'),
        port=args.port
    )
