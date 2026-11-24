# 스킬 사전

여러 공개 저장소의 에이전트 스킬을 분야와 목적별로 찾아보는 한국어 사전입니다. 첫 화면에서 여러 사전을 함께 검색하거나, 집합별 사전을 HTML 한 파일로 열 수 있습니다.

## 사전 만들기

`skills/skill-dictionary` 폴더를 에이전트의 스킬 경로에 복사하고 “이 저장소의 스킬로 한국어 사전을 만들어줘”라고 요청합니다. 항목을 직접 편집하려면 `catalogs/`의 JSON을 참고하세요. 원래 스킬과 저자 사례의 출처는 개별 항목에서 확인할 수 있습니다.

## 사이트 빌드

Python 3.10 이상에서 저장소 루트의 `python3 build.py`를 실행하면 `public/index.html`과 집합별 HTML이 생성됩니다. Cloudflare Pages의 빌드 명령은 `python3 build.py`, 출력 디렉터리는 `public`입니다. 집합을 추가할 때는 `catalogs/`에 고유한 id가 있는 JSON 파일을 넣고 다시 빌드합니다.

## 수록 분야와 선정 근거

각 카탈로그의 `field`가 홈의 분야 제목이 됩니다. 여러 분야를 다루는 모음은 대표 분야에 한 번 싣고, 전체 검색에서는 분야 이름과 스킬 용도를 함께 찾을 수 있습니다. 일부만 선별한 사전은 수록 범위를 카탈로그에 기록합니다.

2026년 11월 24일 GitHub Trending의 전체 언어 목록에서 확인한 후보입니다. 순위는 조회 당시의 위치이며 링크에서는 현재 목록이 열립니다.

| 분야 | 발견한 저장소 | 확인한 목록 |
|---|---|---|
| 개발 과정과 협업 | [Superpowers](https://github.com/obra/superpowers) | [일간 2위](https://github.com/trending?since=daily) |
| 문서와 콘텐츠 | [Anthropic Skills](https://github.com/anthropics/skills) | [월간 5위](https://github.com/trending?since=monthly) |
| 데이터와 리서치 | [last30days](https://github.com/mvanhorn/last30days-skill) | [주간 5위](https://github.com/trending?since=weekly) |
| 영상과 시각화 | [Diagram Design](https://github.com/cathrynlavery/diagram-design), [FFmpeg Skill](https://github.com/kajisho5/ffmpeg-skill) | [일간 9위](https://github.com/trending?since=daily), [주간 13위](https://github.com/trending?since=weekly) |
| 마케팅과 검색 최적화 | [Claude SEO](https://github.com/AgriciDaniel/claude-seo) | [월간 13위](https://github.com/trending?since=monthly) |

디자인 분야의 [Jakub Krehel](https://github.com/jakubkrehel/skills)은 요청받은 모음으로 선정했습니다. [Addy Osmani](https://github.com/addyosmani/agent-skills)와 [Vercel Labs](https://github.com/vercel-labs/agent-skills)는 앞서 선정한 인기 모음입니다. 각 스킬의 상세 화면에서 조사한 버전의 원문을 열 수 있습니다.
