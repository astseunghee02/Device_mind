DCR 📱 (Final Architecture)
독자적인 알고리즘, 실시간 시장 분석, 그리고 당신의 선택을 더한 초개인화 스마트폰 추천

💡 프로젝트 개요
DeviceMind for Mobile은 사용자의 실제 스마트폰 사용 데이터를 분석하고, MCP(Model Context Protocol)로 수집한 실시간 시장 정보와 사용자가 직접 선택한 필터 조건을 결합하여 최적의 스마트폰을 추천하는 상호작용형 지능형 추천 시스템입니다.

이 프로젝트의 핵심은 **자동 분석(Implicit Data)**과 **직접 선택(Explicit Data)**의 결합입니다. AI가 사용자의 숨겨진 니즈를 데이터로 파악하고, 사용자는 가격, 성능 등 자신의 명확한 기준을 직접 설정합니다. 이 두 가지를 모두 반영한 하이브리드 추천 엔진을 통해, 타의 추종을 불허하는 개인화 추천 경험을 제공합니다.

✨ 주요 기능
📱 온디바이스 데이터 수집: 스크린 타임, 배터리, 앱 사용 목록 등 핵심 데이터를 안전하게 수집합니다.

👤 독자적인 사용자 프로파일링: 수집된 데이터를 규칙 기반 알고리즘으로 분석하여 사용자의 명확한 프로필을 생성합니다.

🌐 MCP 기반 실시간 시장 데이터 연동: 독립된 MCP 서버가 최신 스마트폰의 스펙, 가격, 크기, 무게 데이터를 실시간으로 수집하고 제공합니다.

🎛️ 사용자 맞춤형 추천 필터: 추천받기 전, 사용자가 원하는 가격대, 성능 수준, 기기 크기 등 구체적인 조건을 직접 설정할 수 있습니다.

⚖️ 하이브리드 추천 엔진: 사용자의 명시적 필터로 후보군을 추린 뒤, 묵시적 데이터(사용 습관) 기반의 가중치 알고리즘으로 최종 순위를 매기는 정교한 2단계 추천 로직을 사용합니다.

🤖 자연어 분석 리포트: 최종 추천 결과를 LLM이 자연스러운 언어로 가공하여, 설득력 있는 설명과 함께 제공합니다.

🏗️ 시스템 아키텍처
백엔드의 추천 엔진은 **'필터링'**과 **'랭킹'**의 2단계로 작동합니다.

Plaintext

[📱 Mobile App]
 - Sends user logs AND user-selected filters (price, performance, etc.)
   ↓
[🧠 AI Logic Server (MCP Client)]
  1. [User Profiling Algorithm] creates User Profile from logs.
  2. [MCP Request] to Market Data Server to get ALL latest phones.
     ↓
   [🌐 Market Data MCP Server]
     3. Scrapes web for real-time phone specs, prices, etc.
     4. Returns a full, structured list of phones.
     ↑
[🧠 AI Logic Server (MCP Client)]
  5. [Filtering Engine] selects candidate phones based on user's explicit filters.
  6. [Ranking Engine] runs the custom matching algorithm on the filtered candidates to create the final ranked list.
  7. [LLM Layer] explains the result in natural language.
     ↓
[📱 Mobile App]
  8. Displays the final recommendation that matches the user's criteria.
🛠️ 기술 스택 (Tech Stack)
컴포넌트	기술
📱 모바일 앱	<img src="https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white"> or <img src="https://img.shields.io/badge/React%20Native-61DAFB?style=for-the-badge&logo=react&logoColor=black">
🧠 AI 로직 서버 (MCP 클라이언트)	<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"> (Flask/FastAPI), Custom Algorithm Logic
🌐 시장 데이터 서버 (MCP 서버)	<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white">, <img src="https://img.shields.io/badge/Beautiful%20Soup-4A7E9D?style=for-the-badge&logo=python&logoColor=white">
🤖 AI 언어 모델	<img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white"> or <img src="https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white">

Sheets로 내보내기
🚀 개발 로드맵 (Development Roadmap)
👤 1단계: 사용자 프로파일링 알고리즘 개발

🌐 2단계: 시장 데이터 MCP 서버 구축 (가격, 스펙, 크기, 무게 데이터 포함)

⚖️ 3단계: 2단계 추천 엔진(필터링+랭킹) 구현

🎨 4단계: 모바일 앱에 필터 선택 UI 추가

🤖 5단계: LLM 설명 레이어 연동 및 최종 통합

⚙️ 시작하기 (Getting Started)
프로젝트는 두 개의 백엔드 서버와 하나의 모바일 앱으로 구성됩니다. 각 컴포넌트는 별도의 터미널에서 실행해야 합니다.

1. 시장 데이터 MCP 서버 실행
Bash

cd backend/mcp_server/
pip install -r requirements.txt
uvicorn main:app --reload
2. AI 로직 서버 실행
Bash

cd backend/logic_server/
pip install -r requirements.txt
python app.py
3. 모바일 앱 실행
Bash

cd mobile_app/
# (Flutter)
flutter pub get && flutter run
📄 라이선스 (License)
이 프로젝트는 MIT License를 따릅니다.
