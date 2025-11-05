# 쿠팡 휴대폰 가격 MCP 서버 - 빠른 시작 가이드

## 🚀 5분 안에 시작하기

### 1단계: 파일 위치 확인
프로젝트 구조:
```
mcp/
└── python-server/
    ├── src/
    │   └── server.py       # 메인 서버 파일
    ├── config/
    │   └── settings.py     # 설정 파일
    └── requirements.txt    # 의존성
```

### 2단계: 패키지 설치
터미널에서 다음 명령어를 실행하세요:

```bash
# 폴더로 이동
cd mcp/python-server

# 패키지 설치
pip install -r requirements.txt
```

### 3단계: 서버 테스트
서버가 제대로 작동하는지 확인:

```bash
python src/server.py
```

오류 없이 실행되면 Ctrl+C로 종료하세요.

### 4단계: Claude Desktop 설정

#### macOS 사용자:
```bash
# 설정 파일 열기
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

#### Windows 사용자:
```bash
# 메모장으로 열기
notepad %APPDATA%\Claude\claude_desktop_config.json
```

#### 설정 내용:
```json
{
  "mcpServers": {
    "coupang-phones": {
      "command": "python3",
      "args": [
        "/Users/yourname/Device_ggg/mcp/python-server/src/server.py"
      ]
    }
  }
}
```

**중요**:
- `/Users/yourname/Device_ggg/` 부분을 실제 파일 경로로 변경
- Windows는 `C:\\Users\\yourname\\Device_ggg\\...` 형식 사용
- 경로는 반드시 **절대 경로**여야 함

**절대 경로 찾기:**
```bash
# macOS/Linux
pwd

# Windows (PowerShell)
Get-Location
```

### 5단계: Claude Desktop 재시작
Claude Desktop을 **완전히 종료**하고 다시 시작하세요.

---

## 🎯 사용 예시

Claude Desktop에서 다음과 같이 질문해보세요:

### 기본 검색
```
아이폰 15 프로 가격 정보 좀 찾아줘
```

### 가격 비교
```
아이폰 15와 갤럭시 S24 울트라 가격 비교해줘
```

### 예산 기반 추천
```
80만원 예산으로 살 수 있는 갤럭시 폰 추천해줘
```

### 복합 질문
```
100만원 이하 아이폰 중에서 로켓배송 되는 제품 찾아줘
```

---

## 📊 서버가 제공하는 정보

각 휴대폰에 대해 다음 정보를 제공합니다:
- ✅ 상품명
- 💰 가격
- ⭐ 평점
- 💬 리뷰 수
- 🚚 배송 정보 (로켓배송/일반배송)
- 🔗 상품 링크
- 💸 할인율 (있는 경우)

---

## 🔧 문제 해결

### "서버를 찾을 수 없습니다"
1. 파일 경로가 정확한지 확인
   ```bash
   # macOS/Linux
   ls -l /경로/mcp/python-server/src/server.py

   # Windows
   dir C:\경로\mcp\python-server\src\server.py
   ```

2. Python 경로 확인
   ```bash
   # macOS/Linux
   which python3

   # Windows
   where python
   ```

3. 설정 파일의 command를 실제 Python 경로로 변경

### "패키지를 찾을 수 없습니다"
```bash
# pip 업그레이드
pip install --upgrade pip

# 패키지 재설치
pip install -r requirements.txt --force-reinstall
```

### "검색 결과가 없습니다"
1. 인터넷 연결 확인
2. 다른 키워드로 시도
3. 로그 파일 확인: `python-server/logs/coupang_mcp_server.log`

### ImportError 발생 시
```bash
# Python 버전 확인 (3.8 이상 필요)
python --version

# 가상환경 사용 권장
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows

# 패키지 재설치
pip install -r requirements.txt
```

---

## 📝 로그 확인

서버는 자동으로 로그를 기록합니다:
```bash
# 로그 파일 위치
cat python-server/logs/coupang_mcp_server.log

# 실시간 로그 보기
tail -f python-server/logs/coupang_mcp_server.log
```

---

## ⚙️ 고급 설정

### 캐시 시간 변경
`python-server/config/settings.py` 파일에서:
```python
CACHE_DURATION = timedelta(minutes=30)  # 원하는 시간으로 변경
```

### 최대 결과 수 변경
```python
DEFAULT_MAX_RESULTS = 10  # 기본 결과 수
MAX_RESULTS_LIMIT = 20    # 최대 결과 수
```

### 로깅 레벨 변경
```python
LOG_LEVEL = 'DEBUG'  # 더 자세한 로그
# 'DEBUG', 'INFO', 'WARNING', 'ERROR' 중 선택
```

### 요청 딜레이 조정
```python
REQUEST_DELAY = 1.5  # 요청 간 딜레이 (초)
```

---

## ⚠️ 중요 주의사항

### 법적 고려사항
- 이 도구는 **개인 학습 목적**으로만 사용하세요
- 상업적 사용 금지
- 쿠팡의 이용약관을 확인하세요
- 과도한 요청으로 서버에 부담을 주지 마세요

### 기술적 제한
- 웹사이트 구조가 변경되면 작동하지 않을 수 있음
- 로그인이 필요한 정보는 접근 불가
- 캐시는 설정된 시간 동안만 유효

---

## 💡 사용 팁

1. **구체적인 키워드 사용**: "아이폰" 보다 "아이폰 15 프로 256GB"가 더 정확
2. **가격 비교 시**: 정확한 모델명 사용 (예: "갤럭시 S24 울트라")
3. **예산 설정**: 실제 구매 가능 금액보다 약간 높게 설정
4. **캐시 활용**: 같은 검색은 30분 내에 빠르게 응답

---

## 🧪 서버 테스트 명령어

```bash
# 서버 직접 실행하여 오류 확인
cd mcp/python-server
python src/server.py

# Python 대화형 모드에서 모듈 테스트
python
>>> from src.scraper import CoupangScraper
>>> from config.settings import *
>>> scraper = CoupangScraper(COUPANG_BASE_URL, COUPANG_SEARCH_URL, HEADERS, REQUEST_TIMEOUT, REQUEST_DELAY, SELECTORS)
>>> results = scraper.search_products("아이폰", 5)
>>> print(results)
```

---

## 📞 지원

문제가 발생하면:
1. 로그 파일 확인 (`logs/coupang_mcp_server.log`)
2. 터미널에서 직접 실행하여 에러 메시지 확인
3. Python 버전 확인 (3.8 이상 권장)
4. 패키지 버전 확인 (`pip list`)

---

## 🎉 성공했다면

이제 Claude에게 휴대폰 가격을 물어보세요!
서버가 자동으로 쿠팡을 검색하고 결과를 제공합니다.

즐거운 쇼핑 되세요! 🛍️

---

## 📚 추가 정보

자세한 내용은 [README.md](README.md)를 참조하세요.
