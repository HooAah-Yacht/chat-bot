#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
부품 선택 API 서버
PDF에서 추출된 부품을 사용자가 선택할 수 있도록 지원

기능:
1. PDF 업로드 → 모든 부품 추출 (트리 구조)
2. 부품 미리보기 (카테고리별 그룹화)
3. 선택된 부품만 백엔드에 등록

사용법:
    python parts_selector_api.py --port 5001
"""

import sys
import os
import json
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

# Windows 콘솔 인코딩
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# chatbot_unified 임포트
try:
    from chatbot_unified import UnifiedYachtChatbot
    HAS_CHATBOT = True
except ImportError:
    HAS_CHATBOT = False
    print("❌ chatbot_unified.py를 찾을 수 없습니다.")

# Flask 임포트
try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    from werkzeug.utils import secure_filename
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False
    print("❌ Flask를 설치하세요: pip install flask flask-cors")


class PartsSelectionService:
    """부품 선택 서비스 클래스"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY가 필요합니다.")
        
        # Chatbot 인스턴스
        self.chatbot = UnifiedYachtChatbot(api_key=self.api_key, mode="api")
        
        # 세션별 추출 결과 캐시
        self.extraction_cache = {}
        
        print("✅ 부품 선택 서비스 준비 완료")
    
    def extract_parts_with_tree(self, file_path: str, extracted_text: str) -> Dict:
        """
        PDF에서 부품을 트리 구조로 추출
        
        Returns:
            {
                "documentInfo": {...},
                "categories": [
                    {
                        "id": "cat-engine",
                        "name": "Engine",
                        "importance": "high",
                        "parts": [
                            {
                                "id": "part-001",
                                "name": "Engine Block",
                                "manufacturer": "YANMAR",
                                "model": "3GM30",
                                "interval": 12,
                                "importance": "high",
                                "subParts": [
                                    {
                                        "id": "part-001-01",
                                        "name": "Sea Water Pump",
                                        "parentId": "part-001",
                                        ...
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        """
        if len(extracted_text) > 30000:
            extracted_text = extracted_text[:30000] + "\n\n[... 텍스트 일부만 분석 ...]"
        
        prompt = f"""다음은 요트 또는 부품 매뉴얼에서 추출한 텍스트입니다:

{extracted_text}

---

## 📋 작업 지시사항: 부품 트리 구조 추출

**목적: 부품을 계층 구조(트리)로 추출하여 사용자가 선택할 수 있도록 함**

**1. 카테고리 분류 (최상위):**
- Engine (엔진 관련)
- Rigging (돛/마스트 관련)
- Deck (갑판 장비)
- Electrical (전기 시스템)
- Plumbing (배관 시스템)
- Hull (선체)
- Safety (안전 장비)
- Other (기타)

**2. 부품 계층 구조:**
```
카테고리
  ├─ 메인 부품 (예: Engine Block)
  │   ├─ 하위 부품 1 (예: Sea Water Pump)
  │   ├─ 하위 부품 2 (예: Fuel Filter)
  │   └─ 하위 부품 3 (예: Oil Filter)
  ├─ 메인 부품 2
  └─ ...
```

**3. ID 생성 규칙:**
- 카테고리: `cat-{{category}}` (예: cat-engine)
- 메인 부품: `part-{{번호}}` (예: part-001)
- 하위 부품: `part-{{메인번호}}-{{하위번호}}` (예: part-001-01)
- 하위의 하위: `part-{{메인}}-{{하위}}-{{하위하위}}` (예: part-001-01-01)

**4. 중요도 판단:**
- high: 핵심 부품 (엔진, 키, 돛, 마스트 등)
- medium: 중요 하위 부품 (펌프, 필터, 배터리 등)
- low: 소모품 (볼트, 개스킷, 씰 등)

**5. 응답 형식 (JSON):**

```json
{{
  "documentInfo": {{
    "title": "문서 제목",
    "yachtModel": "요트 모델명 (있다면)",
    "manufacturer": "제조사",
    "documentType": "Parts Manual / Service Manual / Owner's Manual"
  }},
  "categories": [
    {{
      "id": "cat-engine",
      "name": "Engine",
      "displayName": "엔진",
      "importance": "high",
      "partsCount": 15,
      "parts": [
        {{
          "id": "part-001",
          "name": "Engine Block",
          "displayName": "엔진 블록",
          "manufacturer": "YANMAR",
          "model": "3GM30",
          "interval": 12,
          "importance": "high",
          "hasSubParts": true,
          "subParts": [
            {{
              "id": "part-001-01",
              "parentId": "part-001",
              "name": "Sea Water Pump",
              "displayName": "해수 펌프",
              "manufacturer": "YANMAR",
              "model": "...",
              "interval": 6,
              "importance": "medium",
              "hasSubParts": false,
              "subParts": []
            }},
            {{
              "id": "part-001-02",
              "parentId": "part-001",
              "name": "Fuel Filter",
              "displayName": "연료 여과기",
              "interval": 3,
              "importance": "medium"
            }}
          ]
        }}
      ]
    }}
  ],
  "totalCategories": 5,
  "totalParts": 59,
  "summary": {{
    "high": 5,
    "medium": 20,
    "low": 34
  }}
}}
```

**6. 중요 규칙:**
- 모든 부품을 빠짐없이 추출 (개수 제한 없음)
- 계층 구조를 명확히 표현 (parentId 필수)
- displayName은 한글로 (사용자가 이해하기 쉽게)
- 불확실한 정보는 null
- JSON 형식으로만 응답

**응답:**
"""
        
        try:
            print("🤖 부품 트리 구조 추출 중...")
            response = self.chatbot.model.generate_content(prompt)
            result_text = response.text
            
            # JSON 추출
            if "```json" in result_text:
                json_start = result_text.find("```json") + 7
                json_end = result_text.find("```", json_start)
                result_text = result_text[json_start:json_end].strip()
            elif "```" in result_text:
                json_start = result_text.find("```") + 3
                json_end = result_text.find("```", json_start)
                result_text = result_text[json_start:json_end].strip()
            
            result = json.loads(result_text)
            result["fileInfo"] = {
                "fileName": os.path.basename(file_path),
                "filePath": file_path
            }
            
            # 통계 계산
            total_parts = self._count_all_parts(result.get('categories', []))
            result["totalParts"] = total_parts
            
            print(f"✅ {result.get('totalCategories', 0)}개 카테고리, {total_parts}개 부품 발견!")
            return result
            
        except Exception as e:
            print(f"❌ 부품 트리 추출 실패: {e}")
            import traceback
            traceback.print_exc()
            return {"error": str(e)}
    
    def _count_all_parts(self, categories: List[Dict]) -> int:
        """모든 부품 개수 계산 (하위 부품 포함)"""
        count = 0
        for category in categories:
            for part in category.get('parts', []):
                count += 1  # 메인 부품
                count += self._count_sub_parts(part.get('subParts', []))
        return count
    
    def _count_sub_parts(self, sub_parts: List[Dict]) -> int:
        """하위 부품 재귀 카운트"""
        count = len(sub_parts)
        for sub in sub_parts:
            count += self._count_sub_parts(sub.get('subParts', []))
        return count
    
    def flatten_selected_parts(self, categories: List[Dict], selected_ids: List[str]) -> List[Dict]:
        """
        선택된 ID에 해당하는 부품만 평탄화하여 반환
        (백엔드 등록용)
        """
        selected_parts = []
        
        for category in categories:
            for part in category.get('parts', []):
                # 메인 부품 체크
                if part['id'] in selected_ids:
                    selected_parts.append(self._flatten_part(part, category['name']))
                
                # 하위 부품 재귀 체크
                self._collect_selected_sub_parts(
                    part.get('subParts', []),
                    selected_ids,
                    selected_parts,
                    category['name']
                )
        
        return selected_parts
    
    def _flatten_part(self, part: Dict, category: str) -> Dict:
        """부품을 평탄화 (백엔드 DTO 형식)"""
        return {
            "id": part.get('id'),
            "name": part.get('name'),
            "displayName": part.get('displayName'),
            "manufacturer": part.get('manufacturer'),
            "model": part.get('model'),
            "interval": part.get('interval'),
            "category": category,
            "importance": part.get('importance'),
            "parentId": part.get('parentId')
        }
    
    def _collect_selected_sub_parts(self, sub_parts: List[Dict], selected_ids: List[str], 
                                    result: List[Dict], category: str):
        """하위 부품 재귀 수집"""
        for sub in sub_parts:
            if sub['id'] in selected_ids:
                result.append(self._flatten_part(sub, category))
            
            if 'subParts' in sub and sub['subParts']:
                self._collect_selected_sub_parts(
                    sub['subParts'],
                    selected_ids,
                    result,
                    category
                )


def create_app(api_key: str = None, port: int = 5001):
    """Flask 앱 생성 및 실행"""
    if not HAS_FLASK:
        print("❌ Flask가 설치되지 않았습니다.")
        return None
    
    app = Flask(__name__)
    CORS(app)
    
    # 서비스 초기화
    try:
        service = PartsSelectionService(api_key=api_key)
    except ValueError as e:
        print(f"❌ 초기화 실패: {e}")
        return None
    
    # 세션 관리
    sessions = {}
    
    @app.route('/api/parts/upload-and-extract', methods=['POST'])
    def upload_and_extract():
        """
        PDF 업로드 및 부품 트리 추출
        
        Request:
        - multipart/form-data
        - file: PDF 파일
        - session_id: 세션 ID (선택)
        
        Response:
        - 카테고리별 부품 트리 구조
        """
        try:
            if 'file' not in request.files:
                return jsonify({"success": False, "error": "파일이 필요합니다."}), 400
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({"success": False, "error": "파일명이 비어있습니다."}), 400
            
            if not file.filename.lower().endswith('.pdf'):
                return jsonify({"success": False, "error": "PDF 파일만 가능합니다."}), 400
            
            # 파일 저장
            upload_folder = 'uploads'
            os.makedirs(upload_folder, exist_ok=True)
            
            if secure_filename:
                filename = secure_filename(file.filename)
            else:
                filename = file.filename.replace(' ', '_')
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            
            # 세션 ID
            session_id = request.form.get('session_id', f"session-{datetime.now().timestamp()}")
            
            # 텍스트 추출
            print(f"📄 파일: {filename}")
            extracted_text = service.chatbot._extract_text_from_file(file_path)
            
            if not extracted_text or len(extracted_text.strip()) < 100:
                return jsonify({
                    "success": False,
                    "error": "텍스트 추출 실패"
                }), 400
            
            # 부품 트리 추출
            result = service.extract_parts_with_tree(file_path, extracted_text)
            
            if "error" in result:
                return jsonify({
                    "success": False,
                    "error": result['error']
                }), 500
            
            # 세션에 저장
            sessions[session_id] = {
                "filePath": file_path,
                "fileName": filename,
                "extractionResult": result,
                "timestamp": datetime.now().isoformat()
            }
            
            return jsonify({
                "success": True,
                "sessionId": session_id,
                "fileName": filename,
                "documentInfo": result.get('documentInfo', {}),
                "categories": result.get('categories', []),
                "totalCategories": result.get('totalCategories', 0),
                "totalParts": result.get('totalParts', 0),
                "summary": result.get('summary', {}),
                "message": f"{result.get('totalParts', 0)}개 부품이 발견되었습니다."
            }), 200
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({"success": False, "error": str(e)}), 500
    
    @app.route('/api/parts/register-selected', methods=['POST'])
    def register_selected():
        """
        선택된 부품만 등록
        
        Request (JSON):
        {
            "sessionId": "session-xxx",
            "selectedPartIds": ["part-001", "part-001-01", "part-002"],
            "yachtInfo": {
                "name": "요트명",
                "nickName": "별명"
            }
        }
        
        Response:
        - 선택된 부품 목록 (백엔드 등록 형식)
        """
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({"success": False, "error": "JSON 데이터 필요"}), 400
            
            session_id = data.get('sessionId')
            selected_ids = data.get('selectedPartIds', [])
            yacht_info = data.get('yachtInfo', {})
            
            if not session_id or session_id not in sessions:
                return jsonify({"success": False, "error": "세션을 찾을 수 없습니다."}), 404
            
            if not selected_ids:
                return jsonify({"success": False, "error": "선택된 부품이 없습니다."}), 400
            
            # 세션 데이터 가져오기
            session_data = sessions[session_id]
            extraction_result = session_data['extractionResult']
            
            # 선택된 부품 평탄화
            selected_parts = service.flatten_selected_parts(
                extraction_result.get('categories', []),
                selected_ids
            )
            
            # 백엔드 등록 형식으로 변환
            payload = {
                "yacht": {
                    "name": yacht_info.get('name', extraction_result.get('documentInfo', {}).get('yachtModel', 'Unknown')),
                    "nickName": yacht_info.get('nickName', '')
                },
                "partList": [
                    {
                        "name": part['name'],
                        "manufacturer": part.get('manufacturer', ''),
                        "model": part.get('model', ''),
                        "interval": part.get('interval', 12),
                        "lastRepair": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
                    }
                    for part in selected_parts
                ]
            }
            
            return jsonify({
                "success": True,
                "selectedCount": len(selected_ids),
                "registeredCount": len(selected_parts),
                "yacht": payload['yacht'],
                "parts": selected_parts,
                "backendPayload": payload,
                "message": f"{len(selected_parts)}개 부품이 준비되었습니다."
            }), 200
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({"success": False, "error": str(e)}), 500
    
    @app.route('/api/parts/session/<session_id>', methods=['GET'])
    def get_session(session_id):
        """세션 데이터 조회"""
        if session_id not in sessions:
            return jsonify({"success": False, "error": "세션 없음"}), 404
        
        session_data = sessions[session_id]
        return jsonify({
            "success": True,
            "sessionId": session_id,
            "fileName": session_data['fileName'],
            "timestamp": session_data['timestamp'],
            "extractionResult": session_data['extractionResult']
        }), 200
    
    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({
            "success": True,
            "service": "Parts Selection API",
            "status": "running",
            "activeSessions": len(sessions)
        }), 200
    
    # 서버 시작
    print("=" * 60)
    print("🌐 부품 선택 API 서버")
    print("=" * 60)
    print(f"🚀 서버: http://localhost:{port}")
    print()
    print("📡 엔드포인트:")
    print("  - POST /api/parts/upload-and-extract")
    print("      PDF 업로드 및 부품 트리 추출")
    print()
    print("  - POST /api/parts/register-selected")
    print("      선택된 부품만 등록 (백엔드 형식)")
    print()
    print("  - GET /api/parts/session/<session_id>")
    print("      세션 데이터 조회")
    print()
    print("  - GET /api/health")
    print("      서버 상태 확인")
    print("=" * 60)
    print()
    
    app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='부품 선택 API 서버')
    parser.add_argument('--port', type=int, default=5001, help='포트 (기본: 5001)')
    parser.add_argument('--api-key', type=str, help='Gemini API 키')
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ GEMINI_API_KEY가 필요합니다.")
        print("   export GEMINI_API_KEY=your_key  (또는 .env 파일)")
        exit(1)
    
    create_app(api_key=api_key, port=args.port)
