# 우심운까 AI 챗봇

## 구현 내용

- 모든 로그인/게스트 앱 화면 우측 하단에 미니 캐릭터 AI 코치 표시
- 남/여 캐릭터 설정에 따라 챗봇 미니어처 캐릭터도 자동 변경
- OpenAI Responses API를 Django 서버에서 호출
- API 키는 브라우저에 노출하지 않음
- 로그인 회원의 닉네임, 주소, 누적 운동량과 최근 운동 기록을 필요한 범위에서 AI 컨텍스트로 사용
- 추천/주변 시설/날씨/대기질 관련 질문은 기존 `recommendation_service.make_recommendations()` 결과를 최대 3개까지 AI에 함께 제공
- 추천 결과가 있을 때 채팅창에 시설 카드 표시
- 최근 대화는 Django 세션에만 저장하며 새로 시작 버튼으로 초기화
- 통증/부상 등 의료성 질문은 진단 대신 안전 안내를 하도록 시스템 프롬프트에 제한 적용

## 필요한 환경변수

`.env.example`을 참고해 서버 환경변수에 다음 값을 설정합니다.

```env
OPENAI_API_KEY=sk-...
OPENAI_CHAT_MODEL=gpt-5.6-luna
OPENAI_CHAT_MAX_OUTPUT_TOKENS=700
```

기존에 `GPT_API_KEY`라는 이름으로 키를 관리했다면 코드가 fallback으로 인식하지만, 운영에서는 표준 이름인 `OPENAI_API_KEY` 사용을 권장합니다.

## 설치

macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

가상환경 폴더 자체를 다른 운영체제로 복사하지 말고 각 PC에서 새로 생성하세요.

## 주요 파일

- `frontend/chatbot_service.py`: OpenAI 호출, 사용자/추천 컨텍스트 구성
- `frontend/chatbot_views.py`: Django JSON API
- `frontend/static/assets/js/chatbot.js`: 챗봇 UI 동작
- `frontend/static/assets/css/chatbot.css`: 미니 캐릭터 챗봇 디자인
- `frontend/templates/frontend/base.html`: 모든 앱 화면에 챗봇 삽입
- `frontend/urls.py`: 챗봇 API 라우트

## 빠른 확인

```bash
python manage.py check
python manage.py runserver
```

로그인 또는 게스트 체험으로 앱에 들어간 뒤 우측 하단의 `우심이에게 물어봐!` 캐릭터 버튼을 누르면 됩니다.
