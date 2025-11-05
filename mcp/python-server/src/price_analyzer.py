"""
가격 분석 모듈
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class PriceAnalyzer:
    """제품 가격 분석을 담당하는 클래스"""

    @staticmethod
    def extract_price_number(price_str: str) -> int:
        """
        가격 문자열에서 숫자를 추출합니다.

        Args:
            price_str: 가격 문자열 (예: "1,234,567원")

        Returns:
            숫자 가격 (예: 1234567)
        """
        try:
            cleaned = price_str.replace(",", "").replace("원", "").strip()
            return int(cleaned)
        except (ValueError, AttributeError):
            return 0

    def compare_prices(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        제품들의 가격을 비교 분석합니다.

        Args:
            products: 제품 정보 리스트

        Returns:
            가격 분석 결과
        """
        if not products or products[0].get("error") or products[0].get("message"):
            return {"error": "유효한 제품 정보가 없습니다."}

        prices = []
        valid_items = []

        for item in products:
            price_num = self.extract_price_number(item.get("price", "0"))
            if price_num > 0:
                prices.append(price_num)
                item["price_numeric"] = price_num
                valid_items.append(item)

        if not prices:
            return {"message": "유효한 가격 정보를 찾을 수 없습니다."}

        return {
            "lowest_price": f"{min(prices):,}원",
            "highest_price": f"{max(prices):,}원",
            "average_price": f"{sum(prices) // len(prices):,}원",
            "price_range": f"{max(prices) - min(prices):,}원",
            "item_count": len(prices),
            "sample_items": valid_items[:3]
        }

    def filter_by_budget(self, products: List[Dict[str, Any]], budget: int,
                        budget_multiplier: float = 1.2) -> Dict[str, Any]:
        """
        예산에 따라 제품을 필터링합니다.

        Args:
            products: 제품 정보 리스트
            budget: 예산 (원)
            budget_multiplier: 예산 초과 허용 배율

        Returns:
            예산별 필터링 결과
        """
        if not products or products[0].get("error") or products[0].get("message"):
            return {"error": "유효한 제품 정보가 없습니다."}

        within_budget = []
        above_budget = []

        for phone in products:
            if phone.get("error") or phone.get("message"):
                continue

            price_num = self.extract_price_number(phone.get("price", "0"))

            if price_num == 0:
                continue

            phone["price_numeric"] = price_num

            if price_num <= budget:
                within_budget.append(phone)
            else:
                above_budget.append(phone)

        # 가격 순으로 정렬
        within_budget.sort(key=lambda x: x.get("price_numeric", 0), reverse=True)
        above_budget.sort(key=lambda x: x.get("price_numeric", 0))

        result = {
            "within_budget_count": len(within_budget),
            "recommendations": within_budget
        }

        # 예산을 약간 초과하는 옵션도 제공
        if above_budget:
            close_above = [p for p in above_budget if p["price_numeric"] <= budget * budget_multiplier]
            if close_above:
                result["slightly_above_budget"] = close_above

        return result
