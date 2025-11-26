"""
HooAah Yacht Manual Uploader - 기존 요트에 부품 추가
기존 요트를 선택하고, 새 매뉴얼 PDF를 업로드하여 부품만 추가하는 전용 API

기능:
- 기존 요트 ID로 요트 선택
- PDF 매뉴얼 업로드 및 분석 (부품만 추출)
- 기존 요트 데이터에 부품 추가 (요트 기본 정보는 변경하지 않음)
- Flask API 서버로 실행

사용법:
    # API 서버 모드
    python yacht_manual_uploader.py
    
    # 포트 지정
    python yacht_manual_uploader.py --port 5001
    
    # API 키 지정
    python yacht_manual_uploader.py --api-key YOUR_API_KEY
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

# chatbot_unified.py 임포트
try:
    from chatbot_unified import UnifiedYachtChatbot
except ImportError:
    print("❌ chatbot_unified.py를 찾을 수 없습니다.")
    print("💡 이 파일은 chatbot_unified.py와 같은 디렉토리에 있어야 합니다.")
    sys.exit(1)

# Flask API
try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    from werkzeug.utils import secure_filename
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False
    print("❌ Flask가 설치되지 않았습니다. pip install flask flask-cors")
    sys.exit(1)


class YachtManualUploader:
    """
    기존 요트에 새 매뉴얼(부품) 추가 클래스
    """
    
    def __init__(self, api_key: str = None):
        """
        초기화
        
        Args:
            api_key: Gemini API 키
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        # UnifiedYachtChatbot 인스턴스 생성
        self.chatbot = UnifiedYachtChatbot(api_key=self.api_key, mode="api")
        
        print("✅ Yacht Manual Uploader가 준비되었습니다!")
    
    def get_available_yachts(self) -> List[Dict]:
        """
        등록 가능한 요트 목록 반환 (ID 포함)
        
        Returns:
            요트 목록 (id, name, manufacturer, type)
        """
        yachts = self.chatbot.yacht_data.get('yachts', [])
        yacht_list = []
        
        for yacht in yachts:
            yacht_list.append({
                "id": yacht.get('id', self.chatbot._generate_yacht_id(yacht.get('name', ''))),
                "name": yacht.get('name', ''),
                "manufacturer": yacht.get('manufacturer', ''),
                "type": yacht.get('type', ''),
                "hasManual": bool(yacht.get('manual'))
            })
        
        return yacht_list
    
    def get_yacht_by_id(self, yacht_id: str) -> Optional[Dict]:
        """
        요트 ID로 요트 정보 조회
        
        Args:
            yacht_id: 요트 ID
            
        Returns:
            요트 정보 (없으면 None)
        """
        yachts = self.chatbot.yacht_data.get('yachts', [])
        
        for yacht in yachts:
            current_id = yacht.get('id', self.chatbot._generate_yacht_id(yacht.get('name', '')))
            if current_id == yacht_id:
                return yacht
        
        return None
    
    def upload_manual_for_yacht(self, yacht_id: str, pdf_file_path: str) -> Dict:
        """
        기존 요트에 새 매뉴얼 업로드 및 부품 추가
        
        Args:
            yacht_id: 요트 ID
            pdf_file_path: PDF 파일 경로
            
        Returns:
            업로드 결과 (success, message, parts_added, yacht_info)
        """
        try:
            # 1. 요트 존재 확인
            yacht = self.get_yacht_by_id(yacht_id)
            if not yacht:
                return {
                    "success": False,
                    "error": f"요트 ID '{yacht_id}'를 찾을 수 없습니다.",
                    "yacht_id": yacht_id
                }
            
            yacht_name = yacht.get('name', '')
            
            # 2. PDF 파일 존재 확인
            if not os.path.exists(pdf_file_path):
                return {
                    "success": False,
                    "error": f"파일을 찾을 수 없습니다: {pdf_file_path}",
                    "yacht_id": yacht_id,
                    "yacht_name": yacht_name
                }
            
            # 3. 파일 형식 확인
            if not self.chatbot._is_supported_file(pdf_file_path):
                return {
                    "success": False,
                    "error": "지원되지 않는 파일 형식입니다. PDF, Word, HWP 등만 지원됩니다.",
                    "yacht_id": yacht_id,
                    "yacht_name": yacht_name
                }
            
            print(f"📄 '{yacht_name}'에 매뉴얼 추가 시작: {os.path.basename(pdf_file_path)}")
            
            # 4. 텍스트 추출
            print("📖 텍스트 추출 중...")
            extracted_text = self.chatbot._extract_text_from_file(pdf_file_path)
            
            if not extracted_text or len(extracted_text.strip()) < 100:
                return {
                    "success": False,
                    "error": "파일에서 텍스트를 추출할 수 없습니다.",
                    "yacht_id": yacht_id,
                    "yacht_name": yacht_name
                }
            
            print(f"✅ 텍스트 추출 완료 ({len(extracted_text)} 문자)")
            
            # 5. AI 분석 (부품 추출)
            print("🤖 AI로 부품 분석 중...")
            analysis_result = self.chatbot._analyze_document_directly(pdf_file_path, extracted_text)
            
            if "error" in analysis_result:
                return {
                    "success": False,
                    "error": f"AI 분석 실패: {analysis_result.get('error', '알 수 없는 오류')}",
                    "yacht_id": yacht_id,
                    "yacht_name": yacht_name
                }
            
            print("✅ AI 분석 완료!")
            
            # 6. 부품만 추출
            parts = analysis_result.get('parts', [])
            
            if not parts or len(parts) == 0:
                return {
                    "success": False,
                    "error": "매뉴얼에서 부품 정보를 찾을 수 없습니다.",
                    "yacht_id": yacht_id,
                    "yacht_name": yacht_name,
                    "parts_added": 0
                }
            
            # 7. 기존 요트에 부품 추가 (JSON 파일 업데이트)
            print(f"💾 {len(parts)}개 부품을 '{yacht_name}'에 추가 중...")
            
            manufacturer = yacht.get('manufacturer', '')
            manual_pdf = os.path.basename(pdf_file_path)
            
            # 부품 저장
            self._add_parts_to_existing_yacht(yacht_id, yacht_name, manufacturer, manual_pdf, parts)
            
            print(f"✅ '{yacht_name}'에 {len(parts)}개 부품 추가 완료!")
            
            # 8. 결과 반환
            return {
                "success": True,
                "message": f"'{yacht_name}'에 {len(parts)}개 부품이 추가되었습니다.",
                "yacht_id": yacht_id,
                "yacht_name": yacht_name,
                "manufacturer": manufacturer,
                "manual_file": manual_pdf,
                "parts_added": len(parts),
                "parts": parts[:10],  # 최대 10개만 반환 (미리보기)
                "total_parts": len(parts)
            }
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            
            return {
                "success": False,
                "error": f"부품 추가 중 오류 발생: {str(e)}",
                "yacht_id": yacht_id
            }
    
    def _add_parts_to_existing_yacht(self, yacht_id: str, yacht_name: str, manufacturer: str, manual_pdf: str, parts: List[Dict]):
        """
        기존 요트에 부품만 추가 (요트 기본 정보는 변경하지 않음)
        
        Args:
            yacht_id: 요트 ID
            yacht_name: 요트 이름
            manufacturer: 제조사
            manual_pdf: 매뉴얼 파일명
            parts: 부품 리스트
        """
        try:
            # 1. yacht_parts_database.json 업데이트
            self._update_yacht_parts_database(yacht_id, yacht_name, manufacturer, manual_pdf, parts)
            
            # 2. yacht_parts_app_data.json 업데이트
            self._update_yacht_parts_app_data(yacht_id, yacht_name, manufacturer, parts)
            
            # 3. extracted_yacht_parts.json 업데이트
            self._update_extracted_yacht_parts(yacht_id, yacht_name, manufacturer, parts)
            
            # 4. extracted_yacht_parts_detailed.json 업데이트
            self._update_extracted_yacht_parts_detailed(yacht_id, yacht_name, manufacturer, parts)
            
            # 5. 매뉴얼 업로드 기록 저장 (manual_upload_history.json)
            self._save_manual_upload_history(yacht_id, yacht_name, manual_pdf, parts)
            
            print(f"✅ 부품 데이터가 모든 JSON 파일에 저장되었습니다.")
            
        except Exception as e:
            print(f"⚠️ 부품 저장 중 오류: {e}")
            import traceback
            traceback.print_exc()
    
    def _update_yacht_parts_database(self, yacht_id: str, yacht_name: str, manufacturer: str, manual_pdf: str, parts: List[Dict]):
        """yacht_parts_database.json에 부품 추가 (기존 부품에 병합)"""
        try:
            db_file = 'data/yacht_parts_database.json'
            if os.path.exists(db_file):
                with open(db_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {"yachts": []}
            
            # 요트 찾기
            yacht_entry = None
            for yacht in data.get("yachts", []):
                if yacht.get("id") == yacht_id:
                    yacht_entry = yacht
                    break
            
            if not yacht_entry:
                # 요트가 없으면 생성
                yacht_entry = {
                    "id": yacht_id,
                    "name": yacht_name,
                    "manufacturer": manufacturer,
                    "type": "",
                    "length": None,
                    "officialWebsite": None,
                    "manualPDF": manual_pdf,
                    "parts": {
                        "rigging": {"physicalParts": [], "maintenanceItems": []},
                        "sails": {"physicalParts": [], "maintenanceItems": []},
                        "engine": {"physicalParts": [], "maintenanceItems": []},
                        "hull": {"physicalParts": [], "maintenanceItems": []},
                        "electrical": {"physicalParts": [], "maintenanceItems": []},
                        "plumbing": {"physicalParts": [], "maintenanceItems": []}
                    }
                }
                data["yachts"].append(yacht_entry)
            
            parts_dict = yacht_entry.get("parts", {})
            
            # 부품 추가 (중복 체크)
            for part in parts:
                category = part.get("category", "rigging").lower()
                name = part.get("name", "")
                if not name:
                    continue
                
                # 카테고리 매핑
                if category in ["rigging", "rig"]:
                    cat_key = "rigging"
                elif category in ["sails", "sail"]:
                    cat_key = "sails"
                elif category in ["engine", "motor"]:
                    cat_key = "engine"
                elif category in ["hull", "deck"]:
                    cat_key = "hull"
                elif category in ["electrical", "electric", "electronics"]:
                    cat_key = "electrical"
                elif category in ["plumbing", "water"]:
                    cat_key = "plumbing"
                else:
                    cat_key = "rigging"
                
                if cat_key not in parts_dict:
                    parts_dict[cat_key] = {"physicalParts": [], "maintenanceItems": []}
                
                # 중복 체크 (같은 이름의 부품이 이미 있는지)
                existing_parts = parts_dict[cat_key]["physicalParts"]
                if any(p.get("name") == name for p in existing_parts):
                    print(f"⚠️ 중복 부품 건너뜀: {name}")
                    continue
                
                # 부품 추가
                physical_part = {
                    "id": f"{yacht_id}-{cat_key}-{len(existing_parts) + 1:02d}",
                    "category": category.capitalize(),
                    "name": name,
                    "partNumber": part.get("model", ""),
                    "manufacturer": part.get("manufacturer", ""),
                    "maintenanceInterval": f"{part.get('interval', 12)}개월" if part.get("interval") else "Annual inspection"
                }
                
                parts_dict[cat_key]["physicalParts"].append(physical_part)
            
            with open(db_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ yacht_parts_database.json 업데이트 완료")
            
        except Exception as e:
            print(f"⚠️ yacht_parts_database.json 업데이트 실패: {e}")
    
    def _update_yacht_parts_app_data(self, yacht_id: str, yacht_name: str, manufacturer: str, parts: List[Dict]):
        """yacht_parts_app_data.json에 부품 추가"""
        try:
            file_path = 'data/yacht_parts_app_data.json'
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {"yachts": []}
            
            yacht_entry = None
            for yacht in data.get("yachts", []):
                if yacht.get("id") == yacht_id:
                    yacht_entry = yacht
                    break
            
            if not yacht_entry:
                yacht_entry = {
                    "id": yacht_id,
                    "name": yacht_name,
                    "manufacturer": manufacturer,
                    "parts": []
                }
                data["yachts"].append(yacht_entry)
            
            # 기존 부품 이름 목록
            existing_part_names = {p.get("name", "") for p in yacht_entry.get("parts", [])}
            
            for part in parts:
                name = part.get("name", "")
                if not name or name in existing_part_names:
                    continue
                
                part_entry = {
                    "name": name,
                    "manufacturer": part.get("manufacturer", ""),
                    "model": part.get("model", ""),
                    "category": part.get("category", "rigging"),
                    "maintenanceInterval": part.get("interval", 12)
                }
                
                yacht_entry["parts"].append(part_entry)
                existing_part_names.add(name)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ yacht_parts_app_data.json 업데이트 완료")
            
        except Exception as e:
            print(f"⚠️ yacht_parts_app_data.json 업데이트 실패: {e}")
    
    def _update_extracted_yacht_parts(self, yacht_id: str, yacht_name: str, manufacturer: str, parts: List[Dict]):
        """extracted_yacht_parts.json에 부품 추가"""
        try:
            file_path = 'data/extracted_yacht_parts.json'
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {"yachts": []}
            
            if isinstance(data, list):
                data = {"yachts": data}
            
            yacht_entry = None
            for yacht in data.get("yachts", []):
                if yacht.get("id") == yacht_id:
                    yacht_entry = yacht
                    break
            
            if not yacht_entry:
                yacht_entry = {
                    "id": yacht_id,
                    "name": yacht_name,
                    "manufacturer": manufacturer,
                    "parts": []
                }
                data["yachts"].append(yacht_entry)
            
            existing_part_names = {p.get("name", "") for p in yacht_entry.get("parts", [])}
            
            for part in parts:
                name = part.get("name", "")
                if not name or name in existing_part_names:
                    continue
                
                part_entry = {
                    "name": name,
                    "manufacturer": part.get("manufacturer", ""),
                    "model": part.get("model", ""),
                    "category": part.get("category", "rigging"),
                    "interval": part.get("interval"),
                    "latestMaintenanceDate": part.get("latestMaintenanceDate") or part.get("lastMaintenanceDate") or part.get("servicedOn") or None
                }
                
                yacht_entry["parts"].append(part_entry)
                existing_part_names.add(name)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ extracted_yacht_parts.json 업데이트 완료")
            
        except Exception as e:
            print(f"⚠️ extracted_yacht_parts.json 업데이트 실패: {e}")
    
    def _update_extracted_yacht_parts_detailed(self, yacht_id: str, yacht_name: str, manufacturer: str, parts: List[Dict]):
        """extracted_yacht_parts_detailed.json에 부품 추가"""
        try:
            file_path = 'data/extracted_yacht_parts_detailed.json'
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {"yachts": []}
            
            yacht_entry = None
            for yacht in data.get("yachts", []):
                if yacht.get("id") == yacht_id:
                    yacht_entry = yacht
                    break
            
            if not yacht_entry:
                yacht_entry = {
                    "id": yacht_id,
                    "name": yacht_name,
                    "manufacturer": manufacturer,
                    "parts": {
                        "rigging": [], "sails": [], "engine": [],
                        "hull": [], "electrical": [], "plumbing": []
                    }
                }
                data["yachts"].append(yacht_entry)
            
            parts_dict = yacht_entry.get("parts", {})
            
            for part in parts:
                category = part.get("category", "rigging").lower()
                name = part.get("name", "")
                if not name:
                    continue
                
                if category in ["rigging", "rig"]:
                    cat_key = "rigging"
                elif category in ["sails", "sail"]:
                    cat_key = "sails"
                elif category in ["engine", "motor"]:
                    cat_key = "engine"
                elif category in ["hull", "deck"]:
                    cat_key = "hull"
                elif category in ["electrical", "electric", "electronics"]:
                    cat_key = "electrical"
                elif category in ["plumbing", "water"]:
                    cat_key = "plumbing"
                else:
                    cat_key = "rigging"
                
                if cat_key not in parts_dict:
                    parts_dict[cat_key] = []
                
                # 중복 체크
                if any(p.get("name") == name for p in parts_dict[cat_key]):
                    continue
                
                part_entry = {
                    "name": name,
                    "description": f"{manufacturer} {yacht_name} - {name}",
                    "specifications": [
                        part.get("model", ""),
                        part.get("manufacturer", ""),
                        f"Interval: {part.get('interval', 'N/A')} months" if part.get("interval") else ""
                    ]
                }
                
                parts_dict[cat_key].append(part_entry)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ extracted_yacht_parts_detailed.json 업데이트 완료")
            
        except Exception as e:
            print(f"⚠️ extracted_yacht_parts_detailed.json 업데이트 실패: {e}")
    
    def _save_manual_upload_history(self, yacht_id: str, yacht_name: str, manual_pdf: str, parts: List[Dict]):
        """매뉴얼 업로드 이력 저장"""
        try:
            history_file = 'data/manual_upload_history.json'
            if os.path.exists(history_file):
                with open(history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {
                    "description": "요트 매뉴얼 업로드 이력 (부품 추가)",
                    "totalUploads": 0,
                    "uploads": []
                }
            
            upload_entry = {
                "uploadId": f"{yacht_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "yachtId": yacht_id,
                "yachtName": yacht_name,
                "manualFile": manual_pdf,
                "uploadDate": datetime.now().isoformat(),
                "partsAdded": len(parts),
                "parts": [part.get("name", "") for part in parts[:20]]  # 최대 20개만 저장
            }
            
            data["uploads"].append(upload_entry)
            data["totalUploads"] = len(data["uploads"])
            
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ manual_upload_history.json에 저장됨")
            
        except Exception as e:
            print(f"⚠️ manual_upload_history.json 저장 실패: {e}")


def run_api_server(api_key: str = None, port: int = 5001):
    """API 서버 실행"""
    uploader = YachtManualUploader(api_key=api_key)
    
    app = Flask(__name__)
    CORS(app)
    
    @app.route('/api/yachts', methods=['GET'])
    def get_yachts():
        """
        등록된 요트 목록 조회
        
        Response:
        {
          "success": true,
          "yachts": [
            {
              "id": "farr-40",
              "name": "Farr 40",
              "manufacturer": "Farr Yacht Design",
              "type": "Racing",
              "hasManual": true
            }
          ],
          "totalYachts": 20
        }
        """
        try:
            yachts = uploader.get_available_yachts()
            return jsonify({
                "success": True,
                "yachts": yachts,
                "totalYachts": len(yachts)
            }), 200
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    @app.route('/api/yacht/<yacht_id>', methods=['GET'])
    def get_yacht_info(yacht_id):
        """
        특정 요트 정보 조회
        
        Response:
        {
          "success": true,
          "yacht": {
            "id": "farr-40",
            "name": "Farr 40",
            "manufacturer": "Farr Yacht Design",
            ...
          }
        }
        """
        try:
            yacht = uploader.get_yacht_by_id(yacht_id)
            if not yacht:
                return jsonify({
                    "success": False,
                    "error": f"요트 ID '{yacht_id}'를 찾을 수 없습니다."
                }), 404
            
            return jsonify({
                "success": True,
                "yacht": yacht
            }), 200
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    @app.route('/api/yacht/<yacht_id>/upload-manual', methods=['POST'])
    def upload_manual(yacht_id):
        """
        기존 요트에 매뉴얼 업로드 (부품 추가)
        
        Request:
        - multipart/form-data
        - file: PDF/Word/HWP 파일
        
        Response:
        {
          "success": true,
          "message": "'Farr 40'에 15개 부품이 추가되었습니다.",
          "yacht_id": "farr-40",
          "yacht_name": "Farr 40",
          "parts_added": 15,
          "parts": [...],
          "total_parts": 15
        }
        """
        try:
            if 'file' not in request.files:
                return jsonify({
                    "success": False,
                    "error": "파일이 필요합니다."
                }), 400
            
            file = request.files['file']
            
            if file.filename == '':
                return jsonify({
                    "success": False,
                    "error": "파일이 선택되지 않았습니다."
                }), 400
            
            # 파일 저장
            upload_folder = 'uploads'
            os.makedirs(upload_folder, exist_ok=True)
            
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            
            # 매뉴얼 업로드 처리
            result = uploader.upload_manual_for_yacht(yacht_id, file_path)
            
            if result.get("success"):
                return jsonify(result), 200
            else:
                return jsonify(result), 400
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({"success": False, "error": str(e)}), 500
    
    @app.route('/api/yacht/<yacht_id>/parts', methods=['GET'])
    def get_yacht_parts(yacht_id):
        """
        특정 요트의 부품 목록 조회
        
        Response:
        {
          "success": true,
          "yacht_id": "farr-40",
          "yacht_name": "Farr 40",
          "parts": [...],
          "total_parts": 45
        }
        """
        try:
            yacht = uploader.get_yacht_by_id(yacht_id)
            if not yacht:
                return jsonify({
                    "success": False,
                    "error": f"요트 ID '{yacht_id}'를 찾을 수 없습니다."
                }), 404
            
            # 부품 데이터 로드
            yacht_name = yacht.get('name', '')
            parts = uploader.chatbot._get_yacht_parts(yacht_name)
            
            return jsonify({
                "success": True,
                "yacht_id": yacht_id,
                "yacht_name": yacht_name,
                "parts": parts,
                "total_parts": len(parts)
            }), 200
            
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """헬스체크"""
        try:
            yachts = uploader.get_available_yachts()
            return jsonify({
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "totalYachts": len(yachts),
                "service": "Yacht Manual Uploader"
            }), 200
        except Exception as e:
            return jsonify({
                "status": "unhealthy",
                "error": str(e)
            }), 500
    
    print("=" * 60)
    print("🌐 HooAah Yacht Manual Uploader API Server")
    print("=" * 60)
    print(f"🚀 서버 시작: http://localhost:{port}")
    print("📡 API 엔드포인트:")
    print("  - GET  /api/yachts - 요트 목록 조회")
    print("  - GET  /api/yacht/<yacht_id> - 특정 요트 정보 조회")
    print("  - POST /api/yacht/<yacht_id>/upload-manual - 매뉴얼 업로드 (부품 추가)")
    print("  - GET  /api/yacht/<yacht_id>/parts - 요트 부품 조회")
    print("  - GET  /api/health - 헬스체크")
    print("=" * 60)
    print()
    print("💡 사용 예시:")
    print("  1. 요트 목록 조회:")
    print("     curl http://localhost:5001/api/yachts")
    print()
    print("  2. 매뉴얼 업로드 (Farr 40):")
    print("     curl -X POST -F 'file=@manual.pdf' http://localhost:5001/api/yacht/farr-40/upload-manual")
    print()
    print("=" * 60)
    print()
    
    app.run(host='0.0.0.0', port=port, debug=False)


def main():
    """메인 함수"""
    print("🚀 Yacht Manual Uploader 시작 중...")
    print()
    
    parser = argparse.ArgumentParser(description='HooAah Yacht Manual Uploader - 기존 요트에 부품 추가')
    parser.add_argument('--api-key', type=str, help='Gemini API 키')
    parser.add_argument('--port', type=int, default=5001, help='API 서버 포트 (기본: 5001)')
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ 오류: GEMINI_API_KEY가 설정되지 않았습니다.")
        print("💡 .env 파일에 GEMINI_API_KEY를 설정하거나 --api-key 옵션을 사용하세요.")
        sys.exit(1)
    
    run_api_server(api_key=api_key, port=args.port)


if __name__ == "__main__":
    main()


