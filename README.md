# 스킬 사전

pstack과 Matt Pocock의 에이전트 스킬을 목적별로 찾아보는 한국어 사전입니다. 첫 화면에서 여러 사전을 함께 검색하거나, 집합별 사전을 HTML 한 파일로 열 수 있습니다.

## 사전 만들기

`skills/skill-dictionary` 폴더를 에이전트의 스킬 경로에 복사하고 “이 저장소의 스킬로 한국어 사전을 만들어줘”라고 요청합니다. 항목을 직접 편집하려면 `catalogs/`의 JSON을 참고하세요. 원래 스킬과 저자 사례의 출처는 개별 항목에서 확인할 수 있습니다.

## 사이트 빌드

Python 3.10 이상에서 저장소 루트의 `python3 build.py`를 실행하면 `public/index.html`과 집합별 HTML이 생성됩니다. Cloudflare Pages의 빌드 명령은 `python3 build.py`, 출력 디렉터리는 `public`입니다. 집합을 추가할 때는 `catalogs/`에 고유한 id가 있는 JSON 파일을 넣고 다시 빌드합니다.
