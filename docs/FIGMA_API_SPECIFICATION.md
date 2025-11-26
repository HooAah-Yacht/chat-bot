# 🎨 피그마 화면 기반 API 응답 형식 문서

> **작성일**: 2025-11-25  
> **기반**: 피그마 디자인 최신 버전  
> **목적**: 프론트엔드-백엔드 API 스펙 정확히 매칭

---

## 📱 **피그마 화면 분석 결과**

### **주요 화면 구성**

1. **요트 등록 화면** (4개 화면)
   - 요트 이름/별칭 입력
   - 요트 선택 (드롭다운)
   - **요트 문서 등록** ⭐ (기존 요트에 매뉴얼 추가)
   
2. **AI 채팅 화면** (3개 화면)
   - 사용자/AI 메시지 (카카오톡 스타일)
   - PDF 파일 업로드
   - 분석 결과 표시

3. **캘린더 화면** (4개 화면)
   - 월별 캘린더 뷰
   - 일정 목록 (색상별 구분)
   - **일정 Dialog** ⭐ ("부품에 대한 일정이 이미 존재합니다")

4. **부품 관리 화면** (6개 화면)
   - 부품 목록
   - 부품 상세/수정

---

## 🎯 **1. 요트 문서 등록 화면**

### **화면 구조 (피그마)**

```
┌─────────────────────────────────────┐
│  요트 선택                           │
│  [드롭다운: Farr 40 ▼]              │
├─────────────────────────────────────┤
│  요트 문서 등록                      │
│  [파일 선택 버튼]                   │
│  선택된 파일: farr40_manual.pdf     │
├─────────────────────────────────────┤
│           [등록하기]                │
└─────────────────────────────────────┘
```

### **API 스펙**

#### **A. 요트 목록 조회**

```http
GET /api/yachts
Host: localhost:5001
```

**Response:**
```json
{
  "success": true,
  "yachts": [
    {
      "id": "farr-40",
      "name": "Farr 40",
      "manufacturer": "Farr Yacht Design",
      "type": "Racing",
      "hasManual": true,
      "partCount": 15
    },
    {
      "id": "j-70",
      "name": "J/70",
      "manufacturer": "J/Boats",
      "type": "Racing",
      "hasManual": true,
      "partCount": 12
    }
  ],
  "totalYachts": 20
}
```

#### **B. 매뉴얼 업로드 (부품 추가)**

```http
POST /api/yacht/{yacht_id}/upload-manual
Host: localhost:5001
Content-Type: multipart/form-data

file: farr40_manual.pdf
```

**Response:**
```json
{
  "success": true,
  "message": "부품 추가 완료!",
  "data": {
    "yachtId": "farr-40",
    "yachtName": "Farr 40",
    "addedParts": 5,
    "skippedParts": 2,
    "totalParts": 20,
    "uploadDate": "2025-11-25T14:30:00Z",
    "parts": [
      {
        "name": "Jib Halyard",
        "manufacturer": "Harken",
        "model": "H-35",
        "interval": 12,
        "latestMaintenanceDate": "2024-10-15"
      }
    ]
  }
}
```

---

## 📅 **2. 캘린더 일정 Dialog**

### **화면 구조 (피그마)**

```
┌─────────────────────────────────────┐
│  부품에 대한 일정이 이미 존재합니다   │
│  일정을 변경하시겠습니까?             │
├──────────────┬──────────────────────┤
│   취소       │        변경          │
├──────────────┴──────────────────────┤
│  하루 종일         [토글: OFF]      │
├─────────────────────────────────────┤
│  시작 날짜                           │
│  2025. 10. 01    15:00              │
├─────────────────────────────────────┤
│  종료 날짜                           │
│  2025. 10. 01    16:00              │
├─────────────────────────────────────┤
│  참조인                              │
│  [텍스트 입력]                       │
├─────────────────────────────────────┤
│           [등록하기]                │
└─────────────────────────────────────┘
```

### **API 스펙**

#### **A. 기존 일정 확인**

```http
GET /api/calendars?partId=123
Host: localhost:8080
Authorization: Bearer {JWT_TOKEN}
```

**Response (일정 있음):**
```json
{
  "statusCode": 200,
  "message": "success",
  "data": [
    {
      "id": 456,
      "partId": 123,
      "startDate": "2025-10-01T15:00:00+09:00",
      "endDate": "2025-10-01T16:00:00+09:00",
      "content": "메인 할야드 정비 - 참조인: 김철수"
    }
  ]
}
```

**Response (일정 없음):**
```json
{
  "statusCode": 200,
  "message": "success",
  "data": []
}
```

#### **B. 일정 생성**

```http
POST /api/calendars
Host: localhost:8080
Authorization: Bearer {JWT_TOKEN}
Content-Type: application/json

{
  "partId": 123,
  "startDate": "2025-10-01T15:00:00+09:00",
  "endDate": "2025-10-01T16:00:00+09:00",
  "content": "메인 할야드 정비 - 참조인: 김철수"
}
```

**Response:**
```json
{
  "statusCode": 201,
  "message": "success",
  "data": {
    "id": 456,
    "partId": 123,
    "startDate": "2025-10-01T15:00:00+09:00",
    "endDate": "2025-10-01T16:00:00+09:00",
    "content": "메인 할야드 정비 - 참조인: 김철수"
  }
}
```

#### **C. 일정 수정**

```http
PUT /api/calendars/456
Host: localhost:8080
Authorization: Bearer {JWT_TOKEN}
Content-Type: application/json

{
  "startDate": "2025-10-15T09:00:00+09:00",
  "endDate": "2025-10-15T11:00:00+09:00",
  "content": "메인 할야드 정비 - 참조인: 이영희"
}
```

**Response:**
```json
{
  "statusCode": 200,
  "message": "success",
  "data": {
    "id": 456,
    "partId": 123,
    "startDate": "2025-10-15T09:00:00+09:00",
    "endDate": "2025-10-15T11:00:00+09:00",
    "content": "메인 할야드 정비 - 참조인: 이영희"
  }
}
```

---

## 🔔 **3. FCM 알림**

### **알림 수신 형식 (피그마 기준)**

#### **A. 정비 알림 (1주일 전, 1일 전)**

```json
{
  "notification": {
    "title": "HooAah",
    "body": "⚠️ 정비 일정 알림\n\n요트: Farr 40\n부품: Main Halyard\n정비 예정일: 2025-10-15 (1주일 후)\n\n앱에서 확인해주세요!"
  },
  "data": {
    "type": "maintenance",
    "yachtId": "1",
    "partId": "123",
    "calendarId": "456",
    "route": "/calendar"
  }
}
```

#### **B. 참조인 초대 알림**

```json
{
  "notification": {
    "title": "HooAah",
    "body": "🎉 요트 초대 알림\n\n김철수님이 요트 'Farr 40'에 참조인으로 초대했습니다!\n\n앱에서 확인해주세요."
  },
  "data": {
    "type": "invitation",
    "yachtId": "1",
    "inviterId": "5",
    "route": "/yacht/1"
  }
}
```

---

## 💡 **4. 프론트엔드 구현 가이드**

### **A. 요트 문서 등록 화면 로직**

```dart
class YachtManualUploadScreen extends StatefulWidget {
  @override
  _YachtManualUploadScreenState createState() => _YachtManualUploadScreenState();
}

class _YachtManualUploadScreenState extends State<YachtManualUploadScreen> {
  String? selectedYachtId;
  File? selectedFile;
  List<Yacht> yachts = [];
  bool isLoading = false;

  @override
  void initState() {
    super.initState();
    _loadYachts();
  }

  // 요트 목록 로드
  Future<void> _loadYachts() async {
    final response = await http.get(
      Uri.parse('http://localhost:5001/api/yachts'),
    );
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      setState(() {
        yachts = (data['yachts'] as List)
            .map((json) => Yacht.fromJson(json))
            .toList();
      });
    }
  }

  // 파일 선택
  Future<void> _pickFile() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf'],
    );
    
    if (result != null) {
      setState(() {
        selectedFile = File(result.files.single.path!);
      });
    }
  }

  // 매뉴얼 업로드
  Future<void> _uploadManual() async {
    if (selectedYachtId == null || selectedFile == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('요트와 파일을 선택해주세요')),
      );
      return;
    }

    setState(() {
      isLoading = true;
    });

    try {
      final request = http.MultipartRequest(
        'POST',
        Uri.parse('http://localhost:5001/api/yacht/$selectedYachtId/upload-manual'),
      );

      request.files.add(
        await http.MultipartFile.fromPath('file', selectedFile!.path),
      );

      final streamedResponse = await request.send();
      final response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              '${data['data']['addedParts']}개 부품 추가 완료!'
            ),
          ),
        );

        Navigator.pop(context);
      } else {
        throw Exception('업로드 실패');
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('오류: $e')),
      );
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('요트 문서 등록')),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // 요트 선택
            DropdownButtonFormField<String>(
              value: selectedYachtId,
              decoration: InputDecoration(labelText: '요트 선택'),
              items: yachts.map((yacht) {
                return DropdownMenuItem(
                  value: yacht.id,
                  child: Text(yacht.name),
                );
              }).toList(),
              onChanged: (value) {
                setState(() {
                  selectedYachtId = value;
                });
              },
            ),
            SizedBox(height: 20),
            
            // 파일 선택
            Text('요트 문서 등록', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            SizedBox(height: 10),
            ElevatedButton.icon(
              onPressed: _pickFile,
              icon: Icon(Icons.upload_file),
              label: Text('파일 선택'),
            ),
            if (selectedFile != null)
              Padding(
                padding: EdgeInsets.only(top: 8),
                child: Text('선택된 파일: ${selectedFile!.path.split('/').last}'),
              ),
            
            Spacer(),
            
            // 등록 버튼
            ElevatedButton(
              onPressed: isLoading ? null : _uploadManual,
              style: ElevatedButton.styleFrom(
                padding: EdgeInsets.symmetric(vertical: 16),
                backgroundColor: Color(0xFF2B4184),
              ),
              child: isLoading
                  ? CircularProgressIndicator(color: Colors.white)
                  : Text('등록하기', style: TextStyle(fontSize: 16)),
            ),
          ],
        ),
      ),
    );
  }
}
```

---

### **B. 캘린더 일정 Dialog 로직**

```dart
Future<void> showCalendarDialog(BuildContext context, int partId) async {
  // 1. 기존 일정 확인
  final existingEvents = await _checkExistingCalendar(partId);
  
  if (existingEvents.isNotEmpty) {
    // 2. 일정이 이미 있으면 확인 Dialog
    final shouldUpdate = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('부품에 대한 일정이 이미 존재합니다'),
        content: Text('일정을 변경하시겠습니까?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: Text('취소'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            child: Text('변경'),
          ),
        ],
      ),
    );
    
    if (shouldUpdate != true) return;
  }
  
  // 3. 일정 입력 Dialog
  final calendarData = await showDialog<Map<String, dynamic>>(
    context: context,
    builder: (context) => CalendarInputDialog(
      existingEvent: existingEvents.isNotEmpty ? existingEvents.first : null,
    ),
  );
  
  if (calendarData == null) return;
  
  // 4. API 호출 (생성 or 수정)
  if (existingEvents.isEmpty) {
    await _createCalendar(partId, calendarData);
  } else {
    await _updateCalendar(existingEvents.first.id, calendarData);
  }
}

// 기존 일정 확인
Future<List<CalendarEvent>> _checkExistingCalendar(int partId) async {
  final response = await http.get(
    Uri.parse('http://localhost:8080/api/calendars?partId=$partId'),
    headers: {'Authorization': 'Bearer $jwtToken'},
  );
  
  if (response.statusCode == 200) {
    final data = json.decode(response.body);
    return (data['data'] as List)
        .map((json) => CalendarEvent.fromJson(json))
        .toList();
  }
  
  return [];
}

// 일정 생성
Future<void> _createCalendar(int partId, Map<String, dynamic> data) async {
  final response = await http.post(
    Uri.parse('http://localhost:8080/api/calendars'),
    headers: {
      'Authorization': 'Bearer $jwtToken',
      'Content-Type': 'application/json',
    },
    body: json.encode({
      'partId': partId,
      ...data,
    }),
  );
  
  if (response.statusCode == 201) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('일정이 등록되었습니다')),
    );
  }
}

// 일정 수정
Future<void> _updateCalendar(int calendarId, Map<String, dynamic> data) async {
  final response = await http.put(
    Uri.parse('http://localhost:8080/api/calendars/$calendarId'),
    headers: {
      'Authorization': 'Bearer $jwtToken',
      'Content-Type': 'application/json',
    },
    body: json.encode(data),
  );
  
  if (response.statusCode == 200) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('일정이 수정되었습니다')),
    );
  }
}
```

---

### **C. FCM 알림 처리**

```dart
class FcmService {
  final FirebaseMessaging _firebaseMessaging = FirebaseMessaging.instance;

  Future<void> initialize() async {
    // 1. 권한 요청
    await _firebaseMessaging.requestPermission();
    
    // 2. FCM 토큰 획득
    final token = await _firebaseMessaging.getToken();
    print('FCM Token: $token');
    
    // 3. 백엔드에 토큰 등록
    if (token != null) {
      await _registerFcmToken(token);
    }
    
    // 4. 토큰 갱신 감지
    _firebaseMessaging.onTokenRefresh.listen(_registerFcmToken);
    
    // 5. 포그라운드 알림 수신
    FirebaseMessaging.onMessage.listen((RemoteMessage message) {
      print('포그라운드 알림: ${message.notification?.title}');
      _showLocalNotification(message);
    });
    
    // 6. 백그라운드 알림 클릭
    FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) {
      print('백그라운드 알림 클릭');
      _handleNotificationTap(message);
    });
  }

  // FCM 토큰 등록
  Future<void> _registerFcmToken(String token) async {
    try {
      final response = await http.put(
        Uri.parse('http://localhost:8080/api/user/fcm-token'),
        headers: {
          'Authorization': 'Bearer $jwtToken',
          'Content-Type': 'application/json',
        },
        body: json.encode({'fcmToken': token}),
      );
      
      if (response.statusCode == 200) {
        print('FCM 토큰 등록 성공');
      }
    } catch (e) {
      print('FCM 토큰 등록 실패: $e');
    }
  }

  // 알림 탭 처리 (라우팅)
  void _handleNotificationTap(RemoteMessage message) {
    final data = message.data;
    final type = data['type'];
    
    if (type == 'maintenance') {
      // 캘린더 화면으로 이동
      navigatorKey.currentState?.pushNamed(
        '/calendar',
        arguments: {'calendarId': data['calendarId']},
      );
    } else if (type == 'invitation') {
      // 요트 상세 화면으로 이동
      navigatorKey.currentState?.pushNamed(
        '/yacht/${data['yachtId']}',
      );
    }
  }
}
```

---

## 📊 **요약 테이블**

| 화면 | API 엔드포인트 | 메서드 | 포트 |
|------|----------------|--------|------|
| 요트 목록 조회 | `/api/yachts` | GET | 5001 |
| 매뉴얼 업로드 | `/api/yacht/{id}/upload-manual` | POST | 5001 |
| 기존 일정 확인 | `/api/calendars?partId={id}` | GET | 8080 |
| 일정 생성 | `/api/calendars` | POST | 8080 |
| 일정 수정 | `/api/calendars/{id}` | PUT | 8080 |
| FCM 토큰 등록 | `/api/user/fcm-token` | PUT | 8080 |

---

**최종 업데이트**: 2025-11-25  
**기반 피그마**: 최신 버전

