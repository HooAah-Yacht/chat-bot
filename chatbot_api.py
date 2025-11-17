"""
HooAah Yacht AI Chatbot API Server
Flutter 앱과 통합을 위한 RESTful API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot_gemini import YachtAIChatbot
import os
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)  # Flutter 앱에서 접근 가능하도록 CORS 설정

# 세션별 챗봇 인스턴스 저장
chatbot_sessions = {}

# Gemini API 키 (환경변수에서 가져오기)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def get_or_create_chatbot(session_id: str) -> YachtAIChatbot:
    """세션 ID로 챗봇 인스턴스 가져오기 또는 생성"""
    if session_id not in chatbot_sessions:
        chatbot_sessions[session_id] = YachtAIChatbot(api_key=GEMINI_API_KEY)
    return chatbot_sessions[session_id]


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    채팅 메시지 전송 API
    
    Request Body:
    {
        "message": "사용자 메시지",
        "session_id": "세션 ID (선택사항)"
    }
    
    Response:
    {
        "success": true,
        "response": "AI 응답",
        "session_id": "세션 ID",
        "timestamp": "2024-11-17T10:30:00"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "success": False,
                "error": "메시지가 필요합니다."
            }), 400
        
        user_message = data['message']
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        # 챗봇 인스턴스 가져오기
        chatbot = get_or_create_chatbot(session_id)
        
        # AI 응답 생성
        ai_response = chatbot.chat(user_message)
        
        return jsonify({
            "success": True,
            "response": ai_response,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/chat/history', methods=['GET'])
def get_history():
    """
    대화 기록 조회 API
    
    Query Parameters:
    - session_id: 세션 ID
    
    Response:
    {
        "success": true,
        "history": [
            {
                "role": "user",
                "content": "메시지",
                "timestamp": "2024-11-17T10:30:00"
            },
            ...
        ]
    }
    """
    try:
        session_id = request.args.get('session_id')
        
        if not session_id:
            return jsonify({
                "success": False,
                "error": "session_id가 필요합니다."
            }), 400
        
        if session_id not in chatbot_sessions:
            return jsonify({
                "success": True,
                "history": []
            })
        
        chatbot = chatbot_sessions[session_id]
        history = chatbot.get_history()
        
        return jsonify({
            "success": True,
            "history": history
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/chat/clear', methods=['POST'])
def clear_history():
    """
    대화 기록 초기화 API
    
    Request Body:
    {
        "session_id": "세션 ID"
    }
    
    Response:
    {
        "success": true,
        "message": "대화 기록이 초기화되었습니다."
    }
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if not session_id:
            return jsonify({
                "success": False,
                "error": "session_id가 필요합니다."
            }), 400
        
        if session_id in chatbot_sessions:
            chatbot_sessions[session_id].clear_history()
        
        return jsonify({
            "success": True,
            "message": "대화 기록이 초기화되었습니다."
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/yachts', methods=['GET'])
def get_yachts():
    """
    요트 목록 조회 API
    
    Response:
    {
        "success": true,
        "yachts": [
            {
                "id": "fareast-28",
                "name": "FarEast 28",
                "type": "One-Design Racing",
                "manufacturer": "FarEast Yachts"
            },
            ...
        ]
    }
    """
    try:
        # 임시 챗봇 인스턴스로 데이터 가져오기
        temp_chatbot = YachtAIChatbot(api_key=GEMINI_API_KEY)
        yachts = temp_chatbot.yacht_data.get('yachts', [])
        
        # 간단한 정보만 추출
        yacht_list = [
            {
                "id": yacht.get('id'),
                "name": yacht.get('name'),
                "type": yacht.get('type'),
                "manufacturer": yacht.get('manufacturer')
            }
            for yacht in yachts
        ]
        
        return jsonify({
            "success": True,
            "yachts": yacht_list,
            "total": len(yacht_list)
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/yacht/<yacht_id>', methods=['GET'])
def get_yacht_detail(yacht_id):
    """
    요트 상세 정보 조회 API
    
    Response:
    {
        "success": true,
        "yacht": {
            "id": "fareast-28",
            "name": "FarEast 28",
            "dimensions": {...},
            "sailArea": {...},
            ...
        }
    }
    """
    try:
        temp_chatbot = YachtAIChatbot(api_key=GEMINI_API_KEY)
        yachts = temp_chatbot.yacht_data.get('yachts', [])
        
        yacht = next((y for y in yachts if y.get('id') == yacht_id), None)
        
        if not yacht:
            return jsonify({
                "success": False,
                "error": "요트를 찾을 수 없습니다."
            }), 404
        
        return jsonify({
            "success": True,
            "yacht": yacht
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """서버 상태 확인"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_sessions": len(chatbot_sessions)
    })


@app.route('/', methods=['GET'])
def index():
    """API 정보"""
    return jsonify({
        "name": "HooAah Yacht AI Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/chat": "채팅 메시지 전송",
            "GET /api/chat/history": "대화 기록 조회",
            "POST /api/chat/clear": "대화 기록 초기화",
            "GET /api/yachts": "요트 목록 조회",
            "GET /api/yacht/<id>": "요트 상세 정보 조회",
            "GET /api/health": "서버 상태 확인"
        }
    })


if __name__ == '__main__':
    print("=" * 60)
    print("🛥️  HooAah Yacht AI Chatbot API Server")
    print("=" * 60)
    print()
    
    if not GEMINI_API_KEY:
        print("⚠️  경고: GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")
        print("   export GEMINI_API_KEY='your-api-key' 로 설정해주세요.")
        print()
    
    print("🚀 서버 시작: http://localhost:5000")
    print("📡 API 문서: http://localhost:5000")
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=True)

