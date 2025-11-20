# 🔧 PDF 경로 감지 기능 개선

작업 경로 외의 다른 경로에 있는 PDF도 인식하도록 개선했습니다.

---

## ✅ 개선 사항

### 1. **절대 경로 지원**
- Windows 절대 경로: `C:\Users\user\Documents\file.pdf`
- 공백 포함 경로: `C:\Users\user\Documents\Sun Odyssey 380 Owners manual.pdf`
- UNC 경로: `\\server\share\file.pdf`

### 2. **상대 경로 지원**
- 현재 작업 디렉토리 기준: `data/yachtpdf/file.pdf`
- 자동으로 절대 경로로 변환

### 3. **다양한 입력 형식 지원**
- 따옴표 포함: `"C:\path\to\file.pdf"`
- 따옴표 없음: `C:\path\to\file.pdf`
- 메시지 중간에 경로: `이 파일 업로드: "C:\path\to\file.pdf"`

---

## 🧪 테스트 결과

```
입력: "C:\Users\user\Documents\Sun Odyssey 380 Owners manual.pdf"
✅ 감지됨: C:\Users\user\Documents\Sun Odyssey 380 Owners manual.pdf
   파일 존재: ✅

입력: C:\Users\user\Documents\Sun Odyssey 380 Owners manual.pdf
✅ 감지됨: C:\Users\user\Documents\Sun Odyssey 380 Owners manual.pdf
   파일 존재: ✅

입력: data/yachtpdf/j70-user-manual.pdf
✅ 감지됨: C:\Users\user\Documents\Yacht2\chat-bot\data\yachtpdf\j70-user-manual.pdf
   파일 존재: ✅
```

---

## 📝 사용 예시

### 절대 경로
```
👤 You: "C:\Users\user\Documents\Sun Odyssey 380 Owners manual.pdf"
🤖 AI: 📄 문서를 분석 중입니다...
```

### 상대 경로
```
👤 You: data/yachtpdf/j70-user-manual.pdf
🤖 AI: 📄 문서를 분석 중입니다...
```

### 따옴표 없이
```
👤 You: C:\Users\user\Documents\file.pdf
🤖 AI: 📄 문서를 분석 중입니다...
```

---

## 🔍 경로 감지 로직

1. **따옴표로 감싸진 경로** 우선 확인
2. **Windows 절대 경로** 패턴 매칭
3. **UNC 경로** 패턴 매칭
4. **상대 경로** 패턴 매칭
5. **메시지 전체**가 경로인지 확인

모든 경우에서 파일 존재 여부를 확인하여 실제 파일만 처리합니다.

---

**수정일**: 2025-01-19

