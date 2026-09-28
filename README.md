# 우심운까 · WoosimWoonkka

> 오늘 어디서 운동할지 고민하는 순간부터 운동을 마치고 나만의 방을 꾸미는 순간까지

지역, 날씨, 대기질, 운동 취향을 연결해 오늘 운동하기 좋은 장소를 추천하고 운동 기록을 이어가는 웹 서비스입니다. 이번 단위 프로젝트에서는 웹 서비스와 분리된 공공데이터 수집·전처리·품질검증·적재·스케줄링 파이프라인을 함께 정리했습니다.

## 웹사이트와 저장소

| 항목 | 주소 |
| --- | --- |
| 서비스 URL | [https://hkjfduhalihufsduahufahoiuw.onrender.com/](https://hkjfduhalihufsduahufahoiuw.onrender.com/) |
| 로컬 서비스 | [http://127.0.0.1:8000/](http://127.0.0.1:8000/) |
| 제출 저장소 | [mlo-02-p1-team3](https://github.com/encore-ai-campus/mlo-02-p1-team3) |
| 웹 서비스 원본 | [woosimwoonkka-web](https://github.com/2nd-MLOps-engineer/woosimwoonkka-web) |
| 데이터·백엔드 원본 | [hkjfduhalihufsduahufahoiuw](https://github.com/2nd-MLOps-engineer/hkjfduhalihufsduahufahoiuw) |

> 현재 배포 서비스는 이 저장소가 아닌 별도 배포 설정에서 운영됩니다. 이 저장소는 프로젝트 문서와 평가 설명을 보관합니다.

## 목차

- [1. 팀 소개](#1-팀-소개)
- [2. 프로젝트 개요](#2-프로젝트-개요)
- [3. 기술 스택](#3-기술-스택)
- [4. WBS](#4-wbs)
- [5. 요구사항 명세서](#5-요구사항-명세서)
- [6. ERD](#6-erd)
- [7. 주요 프로시저](#7-주요-프로시저)
- [8. 수행 결과](#8-수행-결과)
- [9. 자동 학습 데이터 파이프라인 평가 증빙](#9-자동-학습-데이터-파이프라인-평가-증빙)
- [10. 실행 방법](#10-실행-방법)
- [11. 한 줄 회고](#11-한-줄-회고)

## 1. 팀 소개

### 팀명

**MOTIVE**

### 팀원

| 팀원 | 역할 | 담당 업무 | GitHub |
| --- | --- | --- | --- |
| 신경호 | 프론트엔드 · 발표자료 | 서비스 화면 구현, 사용자 인터페이스 구성, 발표자료 준비 | [Shinkyeongho](https://github.com/Shinkyeongho) |
| 류지예 | 프론트엔드 · 발표자료 | 서비스 화면 구현, 사용자 경험 구성, 발표자료 준비 | [callijee22-ship-it](https://github.com/callijee22-ship-it) |
| 백선영 | 데이터 수집 · 데이터베이스 파이프라인 | 공공데이터 수집, 전처리, 품질검증, 데이터 파이프라인 구축 | [baikAnalyst](https://github.com/baikAnalyst) |
| 김형준 | 백엔드 · 프로젝트 전반 | Django 백엔드, 기능 연동, 배포 설정 및 프로젝트 전반 | [kimhyounjun](https://github.com/kimhyounjun) |

## 2. 프로젝트 개요

### 프로젝트명

**우심운까: 공공데이터 기반 운동 장소 추천 서비스와 자동 학습 데이터 파이프라인**

### 프로젝트 소개

사용자가 지역과 운동 종목을 선택하면 체육시설 정보, 날씨, 대기질을 조합해 운동 장소를 추천합니다. 운동 후에는 칼로리를 기록하고 누적 운동량에 따라 나만의 운동방을 꾸밀 수 있습니다.

서비스에 필요한 데이터는 다음 흐름으로 다룹니다.

```text
공공데이터 API·웹 공개 정보
        ↓
수집기: 원본 응답 보존
        ↓
전처리: 필드 표준화·타입 변환
        ↓
품질검증: 행 수·식별자·NULL 변화 확인
        ↓
PostgreSQL 적재
        ↓
Django 추천 API와 화면
```

### 프로젝트 필요성

운동을 시작하려면 주변 시설, 운영시간, 날씨, 대기질을 각각 찾아야 합니다. 데이터가 여러 출처에 흩어져 있고 형식도 달라 수작업으로 관리하면 추천 결과가 오래되거나, 전처리 중 값이 사라져도 발견하기 어렵습니다. 따라서 서비스 기능과 데이터 파이프라인을 분리하고, 원본과 정제 결과를 추적할 수 있는 구조가 필요합니다.

### 프로젝트 목표

1. 지역·운동 종목·환경 조건을 반영한 운동 장소 추천 서비스 구현
2. 체육시설·기상·대기질 데이터를 반복 수집할 수 있는 실행 흐름 구성
3. 수집 원본, 정제 결과, 품질검증 결과, 적재 건수를 평가자가 확인할 수 있도록 기록
4. 실패한 API 요청과 누락·형식 오류를 로그로 남기고 재실행 가능한 구조 제공

## 3. 기술 스택

| 구분 | 기술 | 사용 목적 |
| --- | --- | --- |
| Frontend | HTML, CSS, Vanilla JavaScript, Django Templates | 운동방·추천·친구·프로필 화면 |
| Backend | Python, Django, Gunicorn | 페이지, 세션, 회원, 추천 API |
| Database | PostgreSQL, PostGIS | 회원·운동량·시설·위치 데이터 |
| Data pipeline | Python, requests, BeautifulSoup4, pyproj | API 수집, 공개 정보 확인, 좌표 변환 |
| Scheduling | APScheduler 또는 cron | 주기적 수집 실행 |
| Quality | row count, key uniqueness, NULL transition, type validation | 전처리 손실 확인 |
| Deployment | Render 설정(`render.yaml`), WhiteNoise | 웹 배포 설정과 정적 파일 제공 |
| Collaboration | GitHub, Notion | 코드·문서·발표자료 협업 |

현재 추천 로직은 학습 모델이 아닌 규칙 기반 점수 계산입니다. README에서 “자동 학습 데이터 파이프라인”은 이번 단위 프로젝트의 수집·전처리·적재 자동화 범위를 의미하며, 학습 모델 자체를 구현했다고 주장하지 않습니다.

## 4. WBS

| 단계 | 작업 | 산출물 | 담당 |
| --- | --- | --- | --- |
| 1 | 요구사항·데이터 출처 확인 | 요구사항 명세서, API 목록 | 전원 |
| 2 | 원천 데이터 수집 | API 응답 JSON, CSV 원천 | 백선영 |
| 3 | 전처리·표준화 | 정제 CSV/JSON, 컬럼 매핑 | 백선영 |
| 4 | 품질검증 | 검증 리포트, 오류 로그 | 백선영·김형준 |
| 5 | DB 적재 | PostgreSQL 테이블, 적재 건수 | 백선영·김형준 |
| 6 | 추천 서비스 연동 | Django 추천 API, 추천 화면 | 김형준·신경호·류지예 |
| 7 | 화면·사용자 흐름 구현 | 운동방, 추천, 기록, 친구 화면 | 신경호·류지예 |
| 8 | 스케줄·실행 기록 | APScheduler/cron 설정, 로그 | 백선영·김형준 |
| 9 | 통합 테스트·시연 | 캡처, 테스트 결과, 발표자료 | 전원 |

## 5. 요구사항 명세서

| ID | 구분 | 요구사항 | 검증 방법 |
| --- | --- | --- | --- |
| FR-01 | 수집 | 체육시설 API에서 지역별 시설 데이터를 수집한다 | `frontend/collector.py` 실행 및 수집 건수 확인 |
| FR-02 | 수집 | 기상청·에어코리아 데이터를 수집한다 | 원본 JSON과 요청 시각 확인 |
| FR-03 | 전처리 | 시설명·주소·좌표·유형 필드를 표준 컬럼으로 변환한다 | 정제 CSV 컬럼과 샘플 행 확인 |
| FR-04 | 검증 | 행 수, 필수 식별자, 타입 오류, NULL 변화를 기록한다 | `docs/assessment/data-quality.md` 및 로그 확인 |
| FR-05 | 적재 | 검증을 통과한 정제 데이터를 PostgreSQL에 적재한다 | 적재 전후 건수와 DB 조회 결과 확인 |
| FR-06 | 자동화 | 수집부터 적재까지 설정된 주기로 반복 실행한다 | 스케줄 설정과 실행 로그 확인 |
| FR-07 | 추천 | 지역·운동 종목·거리·환경 조건으로 후보를 정렬한다 | 추천 API 응답 및 화면 시연 |
| FR-08 | 예외 | API 오류·좌표 누락·운영정보 확인 불가를 실패 또는 확인 필요로 남긴다 | 오류 로그와 리포트 확인 |
| NFR-01 | 보안 | API 키와 DB 비밀번호를 환경변수로 관리한다 | `.env.example`과 배포 환경변수 확인 |
| NFR-02 | 재현성 | 같은 명령으로 로컬 수집과 검증을 재실행할 수 있다 | 실행 방법 재현 테스트 |

## 6. ERD

웹 서비스의 핵심 엔터티는 다음과 같습니다.

```mermaid
erDiagram
    MEMBER ||--o| WORKOUT_PROGRESS : has
    MEMBER ||--o{ FRIENDSHIP : creates
    MEMBER ||--o{ FRIEND_REQUEST : sends
    MEMBER ||--o{ FRIEND_NOTE : writes
    MEMBER ||--o{ SITE_VISIT : records
    MEMBER { int id PK; string name; string nickname UK; string password_hash; string address; string friend_code UK; json room_state; json room_layout }
    WORKOUT_PROGRESS { int id PK; int member_id FK; int total_calories; json entries }
    FRIENDSHIP { int id PK; int member_id FK; int friend_id FK }
    FRIEND_REQUEST { int id PK; int requester_id FK; int recipient_id FK; string status }
    FRIEND_NOTE { int id PK; int author_id FK; text text }
    SITE_VISIT { int id PK; string visitor_key; date visited_on }
```

파이프라인 데이터는 서비스 테이블과 분리해 `raw` 원본과 `processed` 정제 데이터로 관리하는 것을 기준으로 합니다. 현재 코드의 DB 우선 추천은 `processed.facility`, `facility_processed`, `processed.weather_ultra_ncst`, `processed.air_quality`가 존재하면 우선 조회하고, 없을 때 외부 API 또는 백업 CSV로 보완합니다.

## 7. 주요 프로시저

### 7.1 수집·전처리·적재

```text
1. 지역과 실행 시각을 확인한다
2. 체육시설·기상·대기질 API를 호출하고 재시도한다
3. API 원문을 output/raw에 저장한다
4. 시설 필드를 표준 이름과 문자열·좌표 형식으로 변환한다
5. 필수 키·행 수·중복·NULL 변화를 검증한다
6. 검증 통과 결과만 PostgreSQL에 적재한다
7. 수집·정제·적재 건수와 오류를 JSON Lines 로그에 기록한다
```

실제 서비스 추천 흐름은 `사용자 지역 또는 현재 위치 → 시설 후보 조회 → 운동 종목 필터 → 거리·날씨·대기질 점수 계산 → 운영정보 확인 → 추천 카드와 지도 링크 → 운동량 기록`입니다. 현재 이동시간은 실제 대중교통 경로가 아닌 거리 기반 추정값입니다.

### 7.2 실패 및 예외 처리

- API 502·503·504와 네트워크 오류는 최대 3회 재시도합니다.
- 응답이 JSON이 아니면 오류 응답 일부와 요청 URL을 로그에 남깁니다.
- 좌표가 없거나 운영정보를 확인할 수 없는 시설은 삭제하지 않고 `확인 필요`로 남깁니다.
- 위치 권한을 거부하면 사용자가 직접 선택한 지역으로 대체합니다.
- API 키는 `.env`에서 읽고 저장소에 커밋하지 않습니다.

## 8. 수행 결과

| 화면 | 설명 |
| --- | --- |
| HOME | 누적 운동량, 운동방, 오늘의 추천 진입 |
| MOVE | 지역·운동 종목·이동 조건 입력 |
| RESULT | 시설·거리·추천 이유·운영정보 확인 |
| DIARY | 날짜별 운동 기록 확인 |
| FRIEND | 친구 조회와 운동 한마디 |
| PROFILE | 운동 지역·종목·캐릭터 설정 |

### 테스트 및 시연 순서

1. 로컬 서버를 실행하고 시작 화면을 엽니다.
2. 게스트 체험 또는 회원가입으로 운동방에 들어갑니다.
3. 지역과 운동 종목을 선택해 추천을 요청합니다.
4. 추천 카드의 거리·환경 정보와 지도 링크를 확인합니다.
5. 운동 칼로리를 기록하고 운동방 보상 변화를 확인합니다.
6. 파이프라인 명령을 실행해 `output/`과 `logs/`의 건수를 확인합니다.

실제 테스트 건수와 평균 응답시간은 실행 환경과 API 응답에 따라 달라지므로 실행 후 로그에 기록된 값을 발표자료에 옮겨 적습니다. 임의의 성공률이나 응답시간은 기재하지 않았습니다.

## 9. 자동 학습 데이터 파이프라인 평가 증빙

### 평가 유의사항

- 팀별 주제와 사용한 프레임워크·라이브러리는 서로 다를 수 있으므로, 구현 방식의 차이는 점수에 반영하지 않고 산출물과 실행 결과(로그·캡처·시연)로 평가합니다.
- 공모전용으로 기존에 구축한 웹 서비스 코드는 평가 대상에서 제외하고, 이번 단위 프로젝트에서 구현한 수집·전처리·적재·스케줄링 부분만 평가합니다.
- README에 실행 방법, 스케줄 설정, 로그 위치, 적재 결과(수집·적재 건수)를 기재하여 평가 근거로 제출합니다.

### Repository Description

권장 Repository Description은 다음과 같습니다.

```text
공공데이터 기반 운동 장소 추천 서비스의 자동 학습 데이터 파이프라인
```

Repository 이름에는 프로젝트명을 넣지 않고, 프로젝트 설명은 GitHub Repository Description에 작성합니다. 프로젝트명이 확정되지 않은 경우 임시 설명을 작성한 뒤 확정 후 수정합니다.

### 필수 산출물

1. 데이터 수집·전처리 파이프라인 명세서
2. 기초 데이터셋과 품질검증 결과
3. 웹 크롤링 또는 API 수집 코드
4. 파이프라인 스케줄링 코드와 실행 로그

### 평가 범위

- 기존 웹 서비스 화면과 기존 공모전용 코드는 서비스 시연 참고 자료입니다.
- 이번 단위 프로젝트의 평가 대상은 수집, 전처리, 적재, 스케줄링, 로그, 적재 결과입니다.
- 팀별 프레임워크·라이브러리가 달라도 구현 방식보다 실행 결과와 증빙을 기준으로 확인합니다.

### 데이터 출처와 활용

| 출처 | 주요 데이터 | 서비스 활용 | 결과 위치 |
| --- | --- | --- | --- |
| 전국체육시설 API | 시설명, 유형, 주소, 좌표, 운영정보 | 운동시설 후보와 거리 계산 | `output/facilities.csv`, DB |
| 기상청 API | 기온, 습도, 강수, 풍속 | 실외 운동 적합도 | `output/raw/weather.json`, DB |
| 에어코리아 API | PM10, PM2.5, 측정소, 측정시각 | 실내·실외 우선순위 | `output/raw/air.json`, DB |
| 공개 시설 페이지 | 휴무·운영시간 문구 | 추천 카드의 운영정보 보완 | `output/facility_enrichment/` |

### 품질검증 기준

| 검사 | 기준 | 실패 시 조치 |
| --- | --- | --- |
| Row count | 원본·정제·적재 건수 차이를 기록 | 차이 원인을 리포트에 기록 |
| Key uniqueness | 시설 식별자 또는 시설명·주소 조합 중복 확인 | 중복 행 격리 |
| Required fields | 시설명·주소·지역 필수 | 누락 건은 적재 전 분리 |
| Type validation | 위도·경도·수치·일시 형식 확인 | 원본 보존 후 오류 로그 기록 |
| NULL transition | 원본 값이 전처리 후 NULL이 되었는지 확인 | 변환 규칙 또는 원본 값 검토 |
| API status | HTTP·응답 구조·요청 시각 기록 | 재시도 후 실패 로그 저장 |

검증 기준과 실행 결과는 이 README의 평가 증빙 항목과 실행 로그를 기준으로 정리합니다.

### 스케줄 설정

```bash
python pipeline/run_pipeline.py --region "서울특별시 강남구" --limit 50
python pipeline/scheduler.py --region "서울특별시 강남구" --interval-hours 6
```

운영 환경에서는 API 호출량과 제공기관 이용정책을 확인한 뒤 주기를 조정합니다. 스케줄러는 실행마다 동일한 파이프라인을 호출하고 이전 실행의 로그와 결과 파일을 덮어쓰지 않습니다.

### 로그와 적재 결과

| 항목 | 위치 |
| --- | --- |
| 원본 API 응답 | `output/raw/*.json` |
| 정제 결과 | `output/facilities_normalized.json`, `output/facilities.csv` |
| 시설 보완 리포트 | `output/facility_enrichment/report_*.json`, `report_*.csv` |
| 파이프라인 실행 로그 | `logs/pipeline-YYYYMMDD.jsonl` |
| 품질검증 설명 | `docs/assessment/data-quality.md` |

실행 로그 한 줄에는 `run_id`, `started_at`, `finished_at`, `region`, `collected_count`, `normalized_count`, `loaded_count`, `quality_status`, `errors`를 기록합니다. DB 적재를 사용하지 않은 실행은 `loaded_count: 0`, `load_status: skipped`로 명확히 표시합니다.

## 10. 실행 방법

### 설치

```bash
git clone https://github.com/encore-ai-campus/mlo-02-p1-team3.git
cd mlo-02-p1-team3
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

`.env.example`을 `.env`로 복사하고 공공데이터 API 키와 DB 설정을 입력합니다.

```bash
cp .env.example .env
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

브라우저에서 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)을 엽니다.

### 수집기 단독 실행

```bash
python frontend/collector.py --region "서울특별시 강남구" --limit 50
python frontend/collector.py --region "서울특별시 강남구" --limit 50 --enrich-web
```

### 평가용 파이프라인 실행

```bash
python pipeline/run_pipeline.py --region "서울특별시 강남구" --limit 50
python pipeline/run_pipeline.py --region "서울특별시 강남구" --limit 50 --load-db
```

실행 후 로그에서 수집·정제·적재 건수를 확인합니다.

## 11. 한 줄 회고

**신경호** — 사용자가 데이터의 출처와 추천 이유를 화면에서 이해하도록 만드는 일이 중요하다는 것을 배웠습니다.

**류지예** — 기능을 많이 넣는 것보다 사용자가 다음 행동으로 자연스럽게 이어지는 흐름을 다듬는 일이 중요했습니다.

**백선영** — 행 수만 맞는 것으로는 데이터 품질을 보장할 수 없어 원본과 변환 전후 값을 함께 추적해야 한다는 것을 배웠습니다.

**김형준** — 화면 기능과 데이터 파이프라인을 분리하면서도 실행 결과가 하나의 사용자 경험으로 이어지도록 설계하는 과정을 경험했습니다.

## 라이선스와 주의사항

- API 키, DB 비밀번호, 개인 위치정보를 저장소에 커밋하지 않습니다.
- 공개 웹 페이지 확인은 `robots.txt`와 제공기관 정책을 준수합니다.
- 화면 캡처의 시설·운영정보·추천 점수는 실행 시점의 결과와 다를 수 있습니다.
