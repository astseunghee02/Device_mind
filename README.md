DeviceMind for Mobile 📱 (Final Architecture)
독자적인 알고리즘, 실시간 시장 분석, 그리고 당신의 선택을 더한 초개인화 스마트폰 추천

💡 프로젝트 개요
DeviceMind for Mobile은 사용자의 실제 스마트폰 사용 데이터를 분석하고, MCP(Model Context Protocol)로 수집한 실시간 시장 정보와 사용자가 직접 선택한 필터 조건을 결합하여 최적의 스마트폰을 추천하는 상호작용형 지능형 추천 시스템입니다.

✨ 주요 기능
📱 **온디바이스 데이터 수집 (구현 완료)**: 사용자의 개입 없이 핵심 데이터를 안전하게 수집합니다.
- **상세 배터리 성능**: 단순 잔량뿐만 아니라, 건강 상태, 온도, 전압, 충전 상태 등 종합적인 성능 지표를 수집합니다.
- **기간별 앱 사용 기록**: 일간, 주간, 월간 등 원하는 기간을 선택하여 앱 사용 시간 통계를 동적으로 수집합니다.

📸 **AI 기반 외관 상태 분석 (뼈대 구현)**: 휴대폰 외관 사진을 분석하여 흠집, 파손 등을 감지하고 중고 등급(S,A,B,C)을 자동으로 판정합니다.

👤 **독자적인 사용자 프로파일링**: 수집된 데이터를 규칙 기반 알고리즘으로 분석하여 사용자의 명확한 프로필을 생성합니다.

🌐 **MCP 기반 실시간 시장 데이터 연동**: 독립된 MCP 서버가 최신 스마트폰의 스펙, 가격, 크기, 무게 데이터를 실시간으로 수집하고 제공합니다.

🎛️ **사용자 맞춤형 추천 필터**: 추천받기 전, 사용자가 원하는 가격대, 성능 수준, 기기 크기 등 구체적인 조건을 직접 설정할 수 있습니다.

⚖️ **하이브리드 추천 엔진**: 사용자의 명시적 필터로 후보군을 추린 뒤, 묵시적 데이터(사용 습관) 기반의 가중치 알고리즘으로 최종 순위를 매기는 정교한 2단계 추천 로직을 사용합니다.

🤖 **자연어 분석 리포트**: 최종 추천 결과를 LLM이 자연스러운 언어로 가공하여, 설득력 있는 설명과 함께 제공합니다.

🏗️ 시스템 아키텍처
이 시스템은 여러 마이크로서비스가 상호작용하는 구조로 설계되었습니다.

```plaintext
[📱 Mobile App]
 | - Sends user logs & filters -> [🧠 AI Logic Server]
 | - Uploads phone photo -> [👁️ Vision Server]
   ↓
[🧠 AI Logic Server (Handles Profiling & Recommendations)]
 | - Requests market data -> [🌐 Market Data Server]
 | - Stores user data -> [☁️ External DB (MongoDB)]
   ↓
[👁️ Vision Server (Handles Image Analysis)]
 | - Analyzes image with OpenCV -> returns grade {A, B, C}
   ↓
[🌐 Market Data Server (Scrapes Web)]
   ↓
[☁️ External DB (MongoDB Atlas)]
```

🛠️ 기술 스택 (Tech Stack)
| 컴포넌트 | 기술 |
|---|---|
| 📱 모바일 앱 | <img src="https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white"> |
| 🧠 AI 로직 서버 | <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">, <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white">, <img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white"> (Motor) |
| 👁️ 비전 서버 | <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">, <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white">, <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white"> |
| 🌐 시장 데이터 서버 | <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white">, <img src="https://img.shields.io/badge/Beautiful%20Soup-4A7E9D?style=for-the-badge&logo=python&logoColor=white"> |
| 🤖 AI 언어 모델 | <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white"> or <img src="https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white"> |

🚀 개발 로드맵 (Development Roadmap)
- **✅ 1단계: 사용자 프로파일링 알고리즘 개발**
  - ✅ **온디바이스 데이터 수집 기능 구현**
  - ✅ **외부 데이터베이스(MongoDB) 연동**
  - 🔲 수집된 데이터를 기반으로 사용자 프로필 생성 로직 개발

- **🔲 2단계: 시장 데이터 MCP 서버 구축**

- **🔲 3단계: 2단계 추천 엔진(필터링+랭킹) 구현**

- **🔲 4단계: 모바일 앱에 필터 선택 UI 추가**

- **🔲 5단계: LLM 설명 레이어 연동 및 최종 통합**

- **🔲 6단계: AI 외관 상태 분석 기능 개발**
  - ✅ **비전 서버 기본 뼈대 구현**
  - 🔲 모바일 앱에 사진 업로드 UI 및 로직 구현
  - 🔲 OpenCV 기반 상세 분석 및 등급 분류 로직 구현

⚙️ 시작하기 (Getting Started)
프로젝트는 세 개의 백엔드 서버와 하나의 모바일 앱으로 구성됩니다. 각 컴포넌트는 별도의 터미널에서 실행해야 합니다.

**1. 시장 데이터 MCP 서버 실행**
```bash
cd backend/mcp_server/
pip install -r requirements.txt
uvicorn main:app --reload
```

**2. AI 로직 서버 실행**
```bash
cd backend/logic_server/
pip install -r requirements.txt
# .env 파일에 DATABASE_URL을 설정했는지 확인하세요.
uvicorn app:app --reload
```

**3. 비전 서버 실행 (신규)**
```bash
cd backend/vision_server/
pip install -r requirements.txt
# 다른 서버와 포트가 겹치지 않도록 8001번 포트를 사용합니다.
uvicorn main:app --port 8001 --reload
```

**4. 모바일 앱 실행**
```bash
cd mobile_app/
flutter pub get && flutter run
```

📄 라이선스 (License)
이 프로젝트는 MIT License를 따릅니다.