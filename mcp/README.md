# MCP 서버 프로젝트

이 프로젝트는 Model Context Protocol (MCP) 서버 구현을 포함하고 있습니다.

## 📁 프로젝트 구조

```
mcp/
├── python-server/          # Python MCP 서버 (쿠팡 휴대폰 가격 검색)
│   ├── src/               # 소스 코드
│   │   ├── server.py      # 메인 서버
│   │   ├── scraper.py     # 웹 스크래핑
│   │   ├── cache_manager.py  # 캐시 관리
│   │   └── price_analyzer.py # 가격 분석
│   ├── config/            # 설정 파일
│   │   └── settings.py    # 서버 설정
│   ├── tests/             # 테스트 코드
│   ├── logs/              # 로그 파일
│   ├── requirements.txt   # Python 의존성
│   └── .gitignore        # Git 무시 파일
│
├── typescript-server/      # TypeScript MCP 서버 템플릿
│   ├── src/
│   │   └── index.ts
│   ├── package.json
│   └── tsconfig.json
│
├── README.md              # 이 파일
└── QUICKSTART.md          # 빠른 시작 가이드
```

## 🚀 빠른 시작

### Python 서버 (쿠팡 휴대폰 가격 검색)

1. **의존성 설치**
```bash
cd python-server
pip install -r requirements.txt
```

2. **서버 실행 테스트**
```bash
python src/server.py
```

3. **Claude Desktop 설정**

#### macOS
```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

#### Windows
```bash
notepad %APPDATA%\Claude\claude_desktop_config.json
```

설정 내용:
```json
{
  "mcpServers": {
    "coupang-phones": {
      "command": "python3",
      "args": [
        "/절대/경로/mcp/python-server/src/server.py"
      ]
    }
  }
}
```

4. **Claude Desktop 재시작**

자세한 내용은 [QUICKSTART.md](QUICKSTART.md)를 참조하세요.

## 📚 Python 서버 기능

### 1. search_phones
휴대폰을 검색합니다.
- **입력**: keyword (검색어), max_results (최대 결과 수)
- **출력**: 상품명, 가격, 평점, 리뷰 수, 배송 정보, 링크, 할인율

### 2. compare_phone_prices
여러 모델의 가격을 비교합니다.
- **입력**: phone_models (모델명 리스트)
- **출력**: 최저가, 최고가, 평균가, 가격 범위

### 3. recommend_phones
예산에 맞는 휴대폰을 추천합니다.
- **입력**: budget (예산), category (카테고리)
- **출력**: 예산 내 추천 제품 목록

## 🔧 개선 사항 (v2.0)

### 아키텍처
- ✅ 클래스 기반 설계로 전환
- ✅ 모듈별 책임 분리 (Scraper, CacheManager, PriceAnalyzer)
- ✅ 설정 파일 분리 (config/settings.py)

### 코드 품질
- ✅ 타입 힌팅 추가
- ✅ 에러 처리 개선
- ✅ 로깅 강화
- ✅ 코드 재사용성 향상

### 유지보수성
- ✅ 명확한 폴더 구조
- ✅ 모듈화된 코드
- ✅ 설정 파일로 쉬운 커스터마이징
- ✅ .gitignore 추가

## ⚙️ 설정 커스터마이징

`python-server/config/settings.py`에서 다음을 변경할 수 있습니다:

```python
# 캐시 설정
CACHE_DURATION = timedelta(minutes=30)  # 캐시 유효 시간

# HTTP 요청 설정
REQUEST_TIMEOUT = 10  # 타임아웃 (초)
REQUEST_DELAY = 1.5   # 요청 간 딜레이 (초)

# 로깅 설정
LOG_LEVEL = 'INFO'    # DEBUG, INFO, WARNING, ERROR

# 검색 설정
DEFAULT_MAX_RESULTS = 10
MAX_RESULTS_LIMIT = 20
```

## 🧪 테스트

```bash
cd python-server
python -m pytest tests/
```

## 📝 로그 확인

로그는 `python-server/logs/coupang_mcp_server.log`에 저장됩니다.

```bash
# 로그 보기
cat python-server/logs/coupang_mcp_server.log

# 실시간 로그 모니터링
tail -f python-server/logs/coupang_mcp_server.log
```

## ⚠️ 주의사항

### 법적 고려사항
- 이 도구는 **개인 학습 목적**으로만 사용하세요
- 상업적 사용 금지
- 쿠팡의 이용약관을 확인하고 준수하세요
- 과도한 요청으로 서버에 부담을 주지 마세요

### 기술적 제한
- 웹사이트 구조가 변경되면 작동하지 않을 수 있습니다
- 로그인이 필요한 정보는 접근할 수 없습니다
- 캐시는 설정된 시간 동안만 유효합니다

## 🤝 기여

개선 사항이나 버그를 발견하면 이슈를 등록하거나 PR을 보내주세요.

## 📄 라이선스

MIT License

## 📞 문제 해결

문제가 발생하면:
1. 로그 파일 확인
2. Python 버전 확인 (3.8 이상 권장)
3. 의존성 패키지 재설치
4. [QUICKSTART.md](QUICKSTART.md)의 문제 해결 섹션 참조

## 🔗 참고 자료

- [MCP 공식 문서](https://modelcontextprotocol.io/)
- [Claude Desktop](https://claude.ai/)
- [BeautifulSoup 문서](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
