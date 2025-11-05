"""
쿠팡 웹 스크래핑 모듈
"""

import time
import logging
from typing import List, Dict, Any, Optional
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class CoupangScraper:
    """쿠팡 웹사이트 스크래핑을 담당하는 클래스"""

    def __init__(self, base_url: str, search_url: str, headers: Dict[str, str],
                 timeout: int, request_delay: float, selectors: Dict[str, str]):
        """
        Args:
            base_url: 쿠팡 기본 URL
            search_url: 검색 URL
            headers: HTTP 헤더
            timeout: 요청 타임아웃 (초)
            request_delay: 요청 간 딜레이 (초)
            selectors: HTML 셀렉터 딕셔너리
        """
        self.base_url = base_url
        self.search_url = search_url
        self.headers = headers
        self.timeout = timeout
        self.request_delay = request_delay
        self.selectors = selectors

    def search_products(self, keyword: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        쿠팡에서 제품을 검색합니다.

        Args:
            keyword: 검색 키워드
            max_results: 최대 결과 수

        Returns:
            제품 정보 리스트
        """
        try:
            logger.info(f"쿠팡 검색 시작: {keyword}")

            params = {"q": keyword}
            response = requests.get(
                self.search_url,
                params=params,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            product_list = soup.select(self.selectors['product_list'])

            if not product_list:
                logger.warning(f"검색 결과 없음: {keyword}")
                return [{
                    "message": "검색 결과가 없습니다.",
                    "keyword": keyword,
                    "suggestion": "다른 키워드로 검색해보세요."
                }]

            products = []
            for product in product_list[:max_results]:
                try:
                    product_info = self._parse_product(product)
                    if product_info:
                        products.append(product_info)
                except Exception as e:
                    logger.error(f"상품 파싱 오류: {e}")
                    continue

            logger.info(f"검색 완료: {keyword}, {len(products)}개 제품")
            return products

        except requests.Timeout:
            error_msg = {"error": "요청 시간 초과. 네트워크 연결을 확인해주세요."}
            logger.error(f"타임아웃: {keyword}")
            return [error_msg]
        except requests.RequestException as e:
            error_msg = {"error": f"네트워크 오류: {str(e)}"}
            logger.error(f"네트워크 오류: {e}")
            return [error_msg]
        except Exception as e:
            error_msg = {"error": f"예상치 못한 오류: {str(e)}"}
            logger.error(f"예상치 못한 오류: {e}")
            return [error_msg]

    def _parse_product(self, product) -> Optional[Dict[str, Any]]:
        """
        제품 요소를 파싱합니다.

        Args:
            product: BeautifulSoup 제품 요소

        Returns:
            제품 정보 딕셔너리
        """
        name_elem = product.select_one(self.selectors['name'])
        name = name_elem.text.strip() if name_elem else "정보 없음"

        price_elem = product.select_one(self.selectors['price'])
        price = price_elem.text.strip() if price_elem else "가격 정보 없음"

        rating_elem = product.select_one(self.selectors['rating'])
        rating = rating_elem.text.strip() if rating_elem else "평점 없음"

        review_elem = product.select_one(self.selectors['review_count'])
        review_count = review_elem.text.strip() if review_elem else "(0)"

        link_elem = product.select_one(self.selectors['product_link'])
        product_link = ""
        if link_elem and link_elem.get('href'):
            href = link_elem['href']
            product_link = f"{self.base_url}{href}" if href.startswith('/') else href

        rocket_elem = product.select_one(self.selectors['rocket_badge'])
        is_rocket = "로켓배송" if rocket_elem else "일반배송"

        discount_elem = product.select_one(self.selectors['discount'])
        discount = discount_elem.text.strip() if discount_elem else ""

        return {
            "name": name,
            "price": price,
            "rating": rating,
            "review_count": review_count,
            "delivery": is_rocket,
            "discount": discount,
            "link": product_link
        }

    def wait_between_requests(self) -> None:
        """요청 간 딜레이를 적용합니다."""
        time.sleep(self.request_delay)
