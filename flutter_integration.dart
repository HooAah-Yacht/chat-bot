// HooAah Yacht AI Chatbot - Flutter Integration
// 이 파일을 frontend/lib/services/ 폴더에 복사하세요

import 'dart:convert';
import 'package:http/http.dart' as http;

/// 채팅 메시지 모델
class ChatMessage {
  final String role; // 'user' or 'assistant'
  final String content;
  final DateTime timestamp;

  ChatMessage({
    required this.role,
    required this.content,
    required this.timestamp,
  });

  factory ChatMessage.fromJson(Map<String, dynamic> json) {
    return ChatMessage(
      role: json['role'],
      content: json['content'],
      timestamp: DateTime.parse(json['timestamp']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'role': role,
      'content': content,
      'timestamp': timestamp.toIso8601String(),
    };
  }

  bool get isUser => role == 'user';
  bool get isAssistant => role == 'assistant';
}

/// AI 챗봇 서비스
class YachtAIChatService {
  final String baseUrl;
  String? sessionId;

  YachtAIChatService({
    this.baseUrl = 'http://localhost:5000', // 실제 서버 URL로 변경
  });

  /// 메시지 전송
  Future<ChatMessage> sendMessage(String message) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/chat'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'message': message,
          'session_id': sessionId,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(utf8.decode(response.bodyBytes));
        
        if (data['success']) {
          // 세션 ID 저장
          sessionId = data['session_id'];
          
          // AI 응답을 ChatMessage로 변환
          return ChatMessage(
            role: 'assistant',
            content: data['response'],
            timestamp: DateTime.parse(data['timestamp']),
          );
        } else {
          throw Exception(data['error'] ?? '응답 생성 실패');
        }
      } else {
        throw Exception('서버 오류: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('메시지 전송 실패: $e');
    }
  }

  /// 대화 기록 조회
  Future<List<ChatMessage>> getHistory() async {
    if (sessionId == null) {
      return [];
    }

    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/chat/history?session_id=$sessionId'),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(utf8.decode(response.bodyBytes));
        
        if (data['success']) {
          final List<dynamic> historyJson = data['history'];
          return historyJson
              .map((json) => ChatMessage.fromJson(json))
              .toList();
        } else {
          throw Exception(data['error'] ?? '기록 조회 실패');
        }
      } else {
        throw Exception('서버 오류: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('기록 조회 실패: $e');
    }
  }

  /// 대화 기록 초기화
  Future<void> clearHistory() async {
    if (sessionId == null) {
      return;
    }

    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/chat/clear'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'session_id': sessionId}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(utf8.decode(response.bodyBytes));
        
        if (!data['success']) {
          throw Exception(data['error'] ?? '초기화 실패');
        }
      } else {
        throw Exception('서버 오류: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('초기화 실패: $e');
    }
  }

  /// 새 세션 시작
  void startNewSession() {
    sessionId = null;
  }
}

/// 사용 예시:
/// 
/// ```dart
/// // 1. 서비스 초기화
/// final chatService = YachtAIChatService(
///   baseUrl: 'http://your-server-url:5000',
/// );
/// 
/// // 2. 메시지 전송
/// try {
///   final aiResponse = await chatService.sendMessage('Farr 40 크기 알려줘');
///   print('AI: ${aiResponse.content}');
/// } catch (e) {
///   print('오류: $e');
/// }
/// 
/// // 3. 대화 기록 조회
/// final history = await chatService.getHistory();
/// for (var msg in history) {
///   print('${msg.role}: ${msg.content}');
/// }
/// 
/// // 4. 대화 초기화
/// await chatService.clearHistory();
/// ```

