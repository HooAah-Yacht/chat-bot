로컬에서 챗봇 실행 안내

요트 데이터 파일: `YachtList01.json` — 이 파일을 `chatbot.py`가 있는 동일한 폴더에 두세요.

필수: Python 3.8+

기본 사용법 (Windows cmd.exe)

- 폴더로 이동한 뒤 대화형 실행

  ```cmd
  cd C:\Users\user\Documents\요트앱\front\front
  python chatbot.py
  ```

- 한 번만 질문하고 종료

  ```cmd
  python chatbot.py --question "(모델명)의 길이는 얼마인가요?"
  ```

- 모델 목록 보기

  ```cmd
  python chatbot.py --list
  ```

- JSON 경로 및 요트 개수 확인 (검증용)
  ```cmd
  python chatbot.py --info
  ```

대화 예시

```
C:\Users\user\Documents\요트앱\front\front>python chatbot.py
요트 상태 질문 챗봇입니다. '종료'를 입력하면 종료됩니다.
질문을 입력하세요: Laser (ILCA 7 / Standard) 크기를 알고 싶어.
챗봇: 'Laser (ILCA 7 / Standard)'의 크기 정보는 아래와 같습니다:
- LOA(전장): 4.23 m (13.83 ft)
- LWL(수선간장): 3.81 m (12.5 ft)
- Beam(폭): 1.39 m (4.56 ft)
- Draft(흘수): 0.787 m (2.58 ft)
질문을 입력하세요: Melges 32 크기를 알고 싶어.
챗봇: 'Melges 32'의 크기 정보는 아래와 같습니다:
- LOA(전장): 9.7 m (31.83 ft)
- LWL(수선간장): 8.69 m (28.5 ft)
- Beam(폭): 3.0 m (9.83 ft)
- Draft(흘수): 2.13 m (7.0 ft)
질문을 입력하세요: Jeanneau Sun Fast 3300 크기를 알고 싶어.
챗봇: 'Jeanneau Sun Fast 3300'의 크기 정보는 아래와 같습니다:
- LOA(전장): 9.99 m (32.76 ft)
- LWL(수선간장): 9.2 m (30.18 ft)
- Beam(폭): 3.35 m (10.99 ft)
- Draft(흘수): 2.2 m (7.22 ft)
질문을 입력하세요: 종료
챗봇을 종료합니다.

C:\Users\user\Documents\요트앱\front\front>
```

메모 및 팁

- 모델명 매칭: 괄호, 슬래시, 구두점 등(예: "Laser (ILCA 7 / Standard)")을 포함한 입력도 자동으로 정규화하여 매칭합니다. 따라서 사용자는 모델명을 자연스럽게 입력하시면 됩니다.
- 잘못된 명령(오타): Windows에서 `pyton` 같은 오타를 입력하면 인식되지 않습니다. `python` 또는 `py`를 사용하세요.
- Python이 설치되어 있지 않거나 PATH에 없다면 아래로 확인하세요:
  ```cmd
  python --version
  py -3 --version
  ```
  설치되어 있지 않다면 Python.org 또는 Microsoft Store에서 설치하시고 설치 시 "Add Python to PATH" 옵션을 체크하세요.

문제 해결

- FileNotFoundError: `YachtList01.json` 파일이 없다는 에러가 뜨면 `chatbot.py`와 동일한 폴더에 `YachtList01.json`을 두거나, 파일 경로를 확인하세요.
- 챗봇이 잘못된 요트를 찾거나 다른 요트를 응답하면 모델명 표기(공백, 약어 등)를 확인해 보시고, 필요하면 `--list`로 모델 목록을 확인한 뒤 동일하게 입력하세요.

추가 도움

원하시면 제가 예시 질문(단발)으로 실행해 출력 결과를 보여드리거나, 간단한 유닛 테스트 파일을 추가해 자동 검증을 구성해 드릴 수 있습니다. 어떤 걸 도와드릴까요?
