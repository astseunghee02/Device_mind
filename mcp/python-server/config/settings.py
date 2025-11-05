"""
쿠팡 휴대폰 가격 MCP 서버 설정
"""

from datetime import timedelta
from typing import Dict

# 캐시 설정
CACHE_DURATION = timedelta(minutes=30)

# HTTP 요청 설정
REQUEST_TIMEOUT = 10  # 초
REQUEST_DELAY = 1.5  # 요청 간 딜레이 (초)

# HTTP 헤더
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}

# 쿠팡 검색 URL
COUPANG_SEARCH_URL = "https://www.coupang.com/np/search"
COUPANG_BASE_URL = "https://www.coupang.com"

# HTML 셀렉터
SELECTORS = {
    'product_list': 'li.search-product',
    'name': 'div.name',
    'price': 'strong.price-value',
    'rating': 'em.rating',
    'review_count': 'span.rating-total-count',
    'product_link': 'a.search-product-link',
    'rocket_badge': 'span.badge.rocket',
    'discount': 'span.discount-percentage',
}

# 검색 설정
DEFAULT_MAX_RESULTS = 10
MAX_RESULTS_LIMIT = 20
MIN_RESULTS = 1

# 추천 설정
RECOMMENDATION_LIMIT = 10
SLIGHTLY_ABOVE_BUDGET_LIMIT = 3
BUDGET_MULTIPLIER = 1.2  # 예산의 120%까지 "약간 초과" 범주

# 가격 비교 설정
COMPARISON_SAMPLE_SIZE = 5
COMPARISON_TOP_ITEMS = 3

# 검색 키워드 맵
SEARCH_KEYWORDS: Dict[str, str] = {
    "아이폰": "아이폰",
    "갤럭시": "갤럭시",
    "전체": "스마트폰"
}

# 로깅 설정
LOG_FILE = 'logs/coupang_mcp_server.log'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'

# 최소 예산
MIN_BUDGET = 500000  # 50만원
