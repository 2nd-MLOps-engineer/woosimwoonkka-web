# 우심운까 (WoosimWoonkka)

지역, 날씨, 대기질, 시설 정보를 바탕으로 운동 장소를 추천하는 Django 웹 애플리케이션입니다.

## 포함된 기능

- 회원가입·로그인 및 지역 프로필
- 운동 시설 추천
- 날씨·대기질 기반 추천 보조 정보
- 현재 위치 기반 검색
- 카카오 지도 연결
- 운동 기록·레벨·친구 기능
- 시설 운영정보 확인 및 추천 결과 보완

## 실행 방법

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

`.env`에는 실제 API 키를 입력해야 합니다. `.env` 파일은 보안상 Git에 올리지 않습니다.

## 데이터베이스

개발 설정은 `config/settings.py`의 PostgreSQL 설정을 사용합니다. 팀 환경에 맞는 데이터베이스 접속정보를 별도로 설정하세요.

대용량 수집 CSV와 로컬 가상환경은 저장소에 포함하지 않았습니다. 원본 프로젝트의 `frontend/db_backup/`에 있는 CSV가 필요한 경우 팀 내부 저장소나 별도 공유 경로로 전달하세요.

## 주요 경로

```text
config/                 Django 프로젝트 설정
frontend/               웹 기능, 모델, 추천 로직, 템플릿, 정적 파일
frontend/migrations/     데이터베이스 마이그레이션
manage.py               Django 관리 명령
requirements.txt        Python 의존성
```

## 주의사항

- API 키, 비밀번호, `.env` 파일을 커밋하지 마세요.
- `.venv/`, `db.sqlite3`, 대용량 CSV, 생성 결과물은 `.gitignore`로 제외됩니다.
- 운영 배포 전에는 `DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS`, 데이터베이스 접속정보를 환경에 맞게 변경하세요.
