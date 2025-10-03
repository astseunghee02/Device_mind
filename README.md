# Device_mind

DeviceMind 🤖
AI가 알려주는 당신만을 위한 디지털 기기 파트너

💡 프로젝트 개요
DeviceMind는 사용자의 실제 기기 사용 데이터를 수집하고 AI로 분석하여, 최적의 교체 시점을 예측하고 개인의 사용 성향에 딱 맞는 새로운 기기를 추천해주는 지능형 기기 관리 시스템입니다. "내 노트북, 언제 바꿔야 할까?", "나한테 가장 잘 맞는 스마트폰은 뭘까?" 와 같은 고민을 데이터 기반의 객관적인 분석으로 해결합니다.

더 이상 막연한 감이나 광고성 리뷰에 의존하지 마세요. DeviceMind가 당신의 디지털 라이프를 위한 최고의 파트너가 되어 드립니다.

✨ 주요 기능
💻 실시간 기기 데이터 수집: CPU, 메모리 사용률, 배터리 상태 등 현재 기기의 핵심 데이터를 자동으로 수집합니다.

🧠 AI 기반 사용자 프로파일링: 수집된 데이터를 LLM(거대 언어 모델)이 분석하여 '영상 편집 전문가', '캐주얼 웹서핑 유저' 등 사용자의 숨겨진 성향을 파악합니다.

🔔 최적의 교체 타이밍 예측: 성능 저하, 배터리 수명 사이클 등을 종합적으로 분석하여 기기 교체가 필요한 최적의 시점을 알려줍니다.

🤖 초개인화 기기 추천: 사용자의 프로필과 최신 시장 데이터를 결합하여, 수많은 기기 중 나에게 가장 적합한 모델을 추천합니다.

💬 대화형 챗봇 인터페이스: 간단한 질문과 답변을 통해 내 기기 상태를 진단받고 새로운 기기를 추천받을 수 있습니다.

🛠️ 기술 스택 (Tech Stack)
이 프로젝트는 특정 클라우드에 종속되지 않는 범용적인 오픈소스 기술을 중심으로 구성되었습니다.

구분	기술
Data Agent	<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"> psutil
Backend API	<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white">
AI Engine	<img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white"> <img src="https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white">
Database	<img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white"> or <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white">
Frontend	<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white">

Sheets로 내보내기
🏗️ 시스템 아키텍처
Plaintext

[사용자 PC: Python Agent 실행]
      ↓ (device_log.json 생성)
[Streamlit UI: 파일 업로드 및 질문 입력]
      ↓ (HTTP POST 요청)
[Flask API 서버]
      ↓ (분석 요청)
[범용 LLM API: 성향/상태 분석] ←→ [Web Search API: 시장 데이터]
      ↓ (분석 결과)
[Flask API 서버]
      ↓ (HTTP 응답)
[Streamlit UI: 결과 표시]
🚀 시작하기 (Getting Started)
1. 프로젝트 클론
Bash

git clone https://github.com/your-username/DeviceMind.git
cd DeviceMind
2. 가상 환경 설정 및 라이브러리 설치
Bash

# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화 (Windows)
.\venv\Scripts\activate

# 가상 환경 활성화 (macOS/Linux)
source venv/bin/activate

# 필요한 라이브러리 설치
pip install -r requirements.txt
requirements.txt 예시

flask
psutil
openai
streamlit
requests
3. API 키 설정
프로젝트 루트 디렉토리에 .env 파일을 생성하고 사용하려는 LLM의 API 키를 입력하세요.

# .env
OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
▶️ 사용 방법 (Usage)
데이터 수집 에이전트 실행
사용자의 기기에서 아래 명령어를 실행하여 device_log.json 파일을 생성합니다. (주기적인 실행을 위해 OS 스케줄러에 등록하는 것을 권장합니다.)

Bash

python device_agent.py
백엔드 서버 실행
새 터미널을 열고 아래 명령어를 실행하여 API 서버를 시작합니다.

Bash

python app.py
프론트엔드 UI 실행
또 다른 터미널을 열고 아래 명령어를 실행하여 Streamlit 웹 앱을 시작합니다.

Bash

streamlit run ui.py
웹 브라우저에서 UI가 열리면, 생성된 device_log.json 파일을 업로드하고 AI에게 질문을 시작하세요!

✨ 데모 예시
사용자: "내 노트북 바꿔야 할까요?"

DeviceMind UI:

🔍 AI 분석 결과
사용자 프로필: 영상 편집 및 다중 작업을 주로 하는 파워 유저

현재 기기 상태: RAM 점유율이 평균 89%로 지속적인 성능 저하가 감지됩니다.

✅ AI 추천
교체를 권장합니다. 현재 사용 패턴을 고려할 때, M2 Pro 기반 MacBook 또는 Surface Laptop Studio를 추천합니다. 두 모델 모두 고사양 영상 편집 작업에 탁월한 성능을 제공합니다.

🗺️ 향후 확장 계획 (Roadmap)
[ ] 전공별/직무별 (개발자, 디자이너 등) 특화 추천 기능 추가

[ ] 기업 및 학교를 위한 IT 자산 관리 솔루션으로 확장

[ ] 디지털 웰빙(과사용 경고, 기기 수명 관리) 서비스 연동

📄 라이선스 (License)
이 프로젝트는 MIT License를 따릅니다.
