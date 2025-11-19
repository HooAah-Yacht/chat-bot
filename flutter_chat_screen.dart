// HooAah Yacht AI Chat Screen - Figma 디자인 기반 UI
// 이 파일을 frontend/lib/screens/ 폴더에 복사하세요

import 'package:flutter/material.dart';
import '../services/flutter_integration.dart'; // 위에서 만든 파일

class YachtAIChatScreen extends StatefulWidget {
  const YachtAIChatScreen({Key? key}) : super(key: key);

  @override
  State<YachtAIChatScreen> createState() => _YachtAIChatScreenState();
}

class _YachtAIChatScreenState extends State<YachtAIChatScreen> {
  final YachtAIChatService _chatService = YachtAIChatService(
    baseUrl: 'http://localhost:5000', // 실제 서버 URL로 변경
  );

  final TextEditingController _messageController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final List<ChatMessage> _messages = [];
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  @override
  void dispose() {
    _messageController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  /// 대화 기록 로드
  Future<void> _loadHistory() async {
    try {
      final history = await _chatService.getHistory();
      setState(() {
        _messages.addAll(history);
      });
      _scrollToBottom();
    } catch (e) {
      print('기록 로드 실패: $e');
    }
  }

  /// 메시지 전송
  Future<void> _sendMessage() async {
    final text = _messageController.text.trim();
    if (text.isEmpty) return;

    // 사용자 메시지 추가
    final userMessage = ChatMessage(
      role: 'user',
      content: text,
      timestamp: DateTime.now(),
    );

    setState(() {
      _messages.add(userMessage);
      _isLoading = true;
    });

    _messageController.clear();
    _scrollToBottom();

    try {
      // AI 응답 받기
      final aiResponse = await _chatService.sendMessage(text);
      
      setState(() {
        _messages.add(aiResponse);
        _isLoading = false;
      });
      
      _scrollToBottom();
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      
      // 오류 메시지 표시
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('메시지 전송 실패: $e'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  /// 스크롤을 맨 아래로
  void _scrollToBottom() {
    Future.delayed(const Duration(milliseconds: 100), () {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  /// 대화 초기화
  Future<void> _clearChat() async {
    final confirm = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('대화 초기화'),
        content: const Text('모든 대화 내용을 삭제하시겠습니까?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('취소'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('삭제', style: TextStyle(color: Colors.red)),
          ),
        ],
      ),
    );

    if (confirm == true) {
      try {
        await _chatService.clearHistory();
        setState(() {
          _messages.clear();
        });
        
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('대화가 초기화되었습니다')),
        );
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('초기화 실패: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white, // HooAah 디자인 시스템 - 흰색 배경
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        leading: Padding(
          padding: const EdgeInsets.only(left: 24),
          child: IconButton(
            icon: const Icon(
              Icons.arrow_back_ios,
              color: Colors.black,
            ),
            padding: EdgeInsets.zero,
            constraints: const BoxConstraints(),
            onPressed: () => Navigator.pop(context),
          ),
        ),
        leadingWidth: 56,
        title: const Text(
          'AI',
          style: TextStyle(
            color: Colors.black,
            fontSize: 20,
            letterSpacing: -0.5,
          ),
        ),
        centerTitle: true,
        actions: [
          IconButton(
            icon: const Icon(Icons.delete_outline, color: Colors.black),
            onPressed: _clearChat,
            tooltip: '대화 초기화',
            padding: const EdgeInsets.only(right: 24),
          ),
        ],
      ),
      body: Column(
        children: [
          // 메시지 리스트
          Expanded(
            child: _messages.isEmpty
                ? _buildEmptyState()
                : ListView.builder(
                    controller: _scrollController,
                    padding: const EdgeInsets.symmetric(
                      horizontal: 24,
                      vertical: 16,
                    ),
                    itemCount: _messages.length,
                    itemBuilder: (context, index) {
                      return _buildMessageBubble(_messages[index]);
                    },
                  ),
          ),

          // 로딩 인디케이터
          if (_isLoading)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
              child: Row(
                children: [
                  Container(
                    width: 40,
                    height: 40,
                    decoration: BoxDecoration(
                      color: const Color(0xFF2B4184).withOpacity(0.1),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: const Icon(
                      Icons.sailing,
                      color: Color(0xFF2B4184),
                      size: 24,
                    ),
                  ),
                  const SizedBox(width: 12),
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 20,
                      vertical: 16,
                    ),
                    decoration: BoxDecoration(
                      color: const Color(0xFFF5F5F5),
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(
                        color: const Color(0xFFE0E0E0),
                        width: 1,
                      ),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        SizedBox(
                          width: 16,
                          height: 16,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            valueColor: const AlwaysStoppedAnimation<Color>(
                              Color(0xFF2B4184),
                            ),
                          ),
                        ),
                        const SizedBox(width: 12),
                        const Text(
                          '답변 생성 중...',
                          style: TextStyle(
                            color: Colors.black,
                            fontSize: 16,
                            letterSpacing: -0.5,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),

          // 입력 영역
          _buildInputArea(),
        ],
      ),
    );
  }

  /// 빈 상태 위젯
  Widget _buildEmptyState() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 80,
              height: 80,
              decoration: BoxDecoration(
                color: const Color(0xFF2B4184).withOpacity(0.1),
                borderRadius: BorderRadius.circular(40),
              ),
              child: const Icon(
                Icons.sailing,
                size: 40,
                color: Color(0xFF2B4184),
              ),
            ),
            const SizedBox(height: 24),
            const Text(
              'HooAah Yacht AI',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.black,
                letterSpacing: -0.5,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              '요트에 대해 무엇이든 물어보세요!',
              style: TextStyle(
                fontSize: 16,
                color: Colors.grey[600],
                letterSpacing: -0.5,
              ),
            ),
            const SizedBox(height: 32),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              alignment: WrapAlignment.center,
              children: [
                _buildSuggestionChip('Farr 40 크기 알려줘'),
                _buildSuggestionChip('레이싱 요트 추천해줘'),
                _buildSuggestionChip('정비 주기는?'),
              ],
            ),
          ],
        ),
      ),
    );
  }

  /// 추천 질문 칩
  Widget _buildSuggestionChip(String text) {
    return ActionChip(
      label: Text(
        text,
        style: const TextStyle(
          fontSize: 14,
          letterSpacing: -0.5,
          color: Colors.black,
        ),
      ),
      onPressed: () {
        _messageController.text = text;
        _sendMessage();
      },
      backgroundColor: Colors.white,
      side: const BorderSide(
        color: Color(0xFF47546F),
        width: 1,
      ),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
      ),
    );
  }

  /// 메시지 버블
  Widget _buildMessageBubble(ChatMessage message) {
    final isUser = message.isUser;
    
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Row(
        mainAxisAlignment:
            isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (!isUser) ...[
            // AI 아바타
            Container(
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                color: const Color(0xFF2B4184).withOpacity(0.1),
                borderRadius: BorderRadius.circular(20),
              ),
              child: const Icon(
                Icons.sailing,
                color: Color(0xFF2B4184),
                size: 24,
              ),
            ),
            const SizedBox(width: 12),
          ],
          
          // 메시지 내용
          Flexible(
            child: Column(
              crossAxisAlignment:
                  isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 20,
                    vertical: 16,
                  ),
                  decoration: BoxDecoration(
                    color: isUser
                        ? const Color(0xFF2B4184) // HooAah 액센트 컬러
                        : const Color(0xFFF5F5F5), // 연한 회색 배경
                    borderRadius: BorderRadius.circular(16),
                    border: isUser
                        ? null
                        : Border.all(
                            color: const Color(0xFFE0E0E0),
                            width: 1,
                          ),
                  ),
                  child: Text(
                    message.content,
                    style: TextStyle(
                      fontSize: 16,
                      letterSpacing: -0.5,
                      color: isUser ? Colors.white : Colors.black,
                      height: 1.5,
                    ),
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  _formatTime(message.timestamp),
                  style: TextStyle(
                    fontSize: 12,
                    letterSpacing: -0.5,
                    color: Colors.grey[600],
                  ),
                ),
              ],
            ),
          ),
          
          if (isUser) ...[
            const SizedBox(width: 12),
            // 사용자 아바타 (선택사항)
            Container(
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                color: const Color(0xFF2B4184).withOpacity(0.1),
                borderRadius: BorderRadius.circular(20),
              ),
              child: const Icon(
                Icons.person,
                color: Color(0xFF2B4184),
                size: 24,
              ),
            ),
          ],
        ],
      ),
    );
  }

  /// 입력 영역
  Widget _buildInputArea() {
    return Container(
      decoration: const BoxDecoration(
        color: Colors.white,
        border: Border(
          top: BorderSide(
            color: Color(0xFFB0B8C1),
            width: 1,
          ),
        ),
      ),
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
      child: SafeArea(
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            Expanded(
              child: Container(
                constraints: const BoxConstraints(
                  maxHeight: 120,
                ),
                padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(
                    color: const Color(0xFF47546F),
                    width: 1,
                  ),
                ),
                child: TextField(
                  controller: _messageController,
                  decoration: const InputDecoration(
                    hintText: '메시지를 입력하세요',
                    hintStyle: TextStyle(
                      color: Color(0xFF47546F),
                      fontSize: 16,
                      letterSpacing: -0.5,
                    ),
                    border: InputBorder.none,
                  ),
                  style: const TextStyle(
                    fontSize: 16,
                    letterSpacing: -0.5,
                  ),
                  maxLines: null,
                  textInputAction: TextInputAction.send,
                  onSubmitted: (_) => _sendMessage(),
                ),
              ),
            ),
            const SizedBox(width: 12),
            Container(
              width: 48,
              height: 48,
              decoration: BoxDecoration(
                color: const Color(0xFF2B4184),
                borderRadius: BorderRadius.circular(16),
              ),
              child: IconButton(
                icon: const Icon(Icons.send, color: Colors.white),
                onPressed: _sendMessage,
                padding: EdgeInsets.zero,
              ),
            ),
          ],
        ),
      ),
    );
  }

  /// 시간 포맷팅
  String _formatTime(DateTime time) {
    final now = DateTime.now();
    final diff = now.difference(time);

    if (diff.inMinutes < 1) {
      return '방금';
    } else if (diff.inHours < 1) {
      return '${diff.inMinutes}분 전';
    } else if (diff.inDays < 1) {
      return '${time.hour}:${time.minute.toString().padLeft(2, '0')}';
    } else {
      return '${time.month}/${time.day}';
    }
  }
}

