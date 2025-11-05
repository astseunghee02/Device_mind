#!/usr/bin/env python3
"""
쿠팡 휴대폰 가격 정보 MCP 서버
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Any, List

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.settings import (
    CACHE_DURATION, HEADERS, COUPANG_SEARCH_URL, COUPANG_BASE_URL,
    SELECTORS, DEFAULT_MAX_RESULTS, MAX_RESULTS_LIMIT, MIN_RESULTS,
    REQUEST_TIMEOUT, REQUEST_DELAY, SEARCH_KEYWORDS, LOG_FILE,
    LOG_FORMAT, LOG_LEVEL, MIN_BUDGET, RECOMMENDATION_LIMIT,
    SLIGHTLY_ABOVE_BUDGET_LIMIT, BUDGET_MULTIPLIER, COMPARISON_SAMPLE_SIZE
)
from src.cache_manager import CacheManager
from src.scraper import CoupangScraper
from src.price_analyzer import PriceAnalyzer

# 로깅 설정
log_file_path = project_root / LOG_FILE
log_file_path.parent.mkdir(exist_ok=True)

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    filename=str(log_file_path)
)
logger = logging.getLogger(__name__)


class CoupangPhonePriceServer:
    """쿠팡 휴대폰 가격 MCP 서버"""

    def __init__(self):
        """서버 초기화"""
        self.server = Server("coupang-phone-price-server")
        self.cache_manager = CacheManager(CACHE_DURATION)
        self.scraper = CoupangScraper(
            base_url=COUPANG_BASE_URL,
            search_url=COUPANG_SEARCH_URL,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
            request_delay=REQUEST_DELAY,
            selectors=SELECTORS
        )
        self.price_analyzer = PriceAnalyzer()

        self._setup_handlers()
        logger.info("서버 초기화 완료")

    def _setup_handlers(self) -> None:
        """핸들러 설정"""
        self.server.list_tools()(self.list_tools)
        self.server.call_tool()(self.call_tool)

    async def list_tools(self) -> List[Tool]:
        """사용 가능한 도구 목록"""
        return [
            Tool(
                name="search_phones",
                description="쿠팡에서 휴대폰을 검색합니다. 브랜드, 모델명, 특징 등으로 검색 가능합니다.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "keyword": {
                            "type": "string",
                            "description": "검색 키워드 (예: '아이폰 15 프로', '갤럭시 S24', '플립폰')"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": f"최대 결과 수 ({MIN_RESULTS}-{MAX_RESULTS_LIMIT}, 기본값: {DEFAULT_MAX_RESULTS})",
                            "minimum": MIN_RESULTS,
                            "maximum": MAX_RESULTS_LIMIT,
                            "default": DEFAULT_MAX_RESULTS
                        }
                    },
                    "required": ["keyword"]
                }
            ),
            Tool(
                name="compare_phone_prices",
                description="여러 휴대폰 모델의 가격을 비교 분석합니다. 최저가, 최고가, 평균가를 제공합니다.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "phone_models": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "비교할 모델명 리스트",
                            "minItems": 2,
                            "maxItems": 5
                        }
                    },
                    "required": ["phone_models"]
                }
            ),
            Tool(
                name="recommend_phones",
                description="예산과 선호 카테고리에 맞는 최적의 휴대폰을 추천합니다.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "budget": {
                            "type": "integer",
                            "description": "예산 (원)",
                            "minimum": MIN_BUDGET
                        },
                        "category": {
                            "type": "string",
                            "description": "선호 브랜드",
                            "enum": list(SEARCH_KEYWORDS.keys()),
                            "default": "전체"
                        }
                    },
                    "required": ["budget"]
                }
            )
        ]

    async def call_tool(self, name: str, arguments: Any) -> List[TextContent]:
        """도구 호출 처리"""
        try:
            if name == "search_phones":
                result = await self._handle_search_phones(arguments)
            elif name == "compare_phone_prices":
                result = await self._handle_compare_prices(arguments)
            elif name == "recommend_phones":
                result = await self._handle_recommend_phones(arguments)
            else:
                result = {"error": f"알 수 없는 도구: {name}"}

            return [TextContent(
                type="text",
                text=json.dumps(result, ensure_ascii=False, indent=2)
            )]

        except Exception as e:
            logger.error(f"도구 호출 오류: {name}, {e}")
            return [TextContent(
                type="text",
                text=json.dumps({"error": f"처리 중 오류 발생: {str(e)}"}, ensure_ascii=False)
            )]

    async def _handle_search_phones(self, arguments: dict) -> Any:
        """휴대폰 검색 처리"""
        keyword = arguments.get("keyword")
        max_results = arguments.get("max_results", DEFAULT_MAX_RESULTS)

        if not keyword:
            return {"error": "검색 키워드가 필요합니다."}

        # 캐시 확인
        cache_key = f"search_{keyword}_{max_results}"
        cached_data = self.cache_manager.get(cache_key)
        if cached_data:
            return cached_data

        # 검색 수행
        results = self.scraper.search_products(keyword, max_results)

        # 캐시에 저장
        if results and not results[0].get("error"):
            self.cache_manager.set(cache_key, results)

        return results

    async def _handle_compare_prices(self, arguments: dict) -> Any:
        """가격 비교 처리"""
        phone_models = arguments.get("phone_models", [])

        if not phone_models or len(phone_models) < 2:
            return {"error": "최소 2개 이상의 모델이 필요합니다."}

        logger.info(f"가격 비교 시작: {phone_models}")
        comparison_results = {}

        for model in phone_models:
            # 캐시 또는 검색
            cache_key = f"search_{model}_{COMPARISON_SAMPLE_SIZE}"
            cached_data = self.cache_manager.get(cache_key)

            if cached_data:
                results = cached_data
            else:
                results = self.scraper.search_products(model, max_results=COMPARISON_SAMPLE_SIZE)
                if results and not results[0].get("error"):
                    self.cache_manager.set(cache_key, results)

            # 에러 처리
            if results and results[0].get("error"):
                comparison_results[model] = {"error": results[0].get("error")}
                continue

            if results and results[0].get("message"):
                comparison_results[model] = {"message": results[0].get("message")}
                continue

            # 가격 분석
            analysis = self.price_analyzer.compare_prices(results)
            comparison_results[model] = analysis

            # 요청 간 딜레이
            self.scraper.wait_between_requests()

        logger.info(f"가격 비교 완료: {len(comparison_results)}개 모델")
        return comparison_results

    async def _handle_recommend_phones(self, arguments: dict) -> Any:
        """휴대폰 추천 처리"""
        budget = arguments.get("budget")
        category = arguments.get("category", "전체")

        if not budget or budget < MIN_BUDGET:
            return {"error": f"예산은 {MIN_BUDGET:,}원 이상이어야 합니다."}

        logger.info(f"추천 시작: 예산={budget}, 카테고리={category}")

        keyword = SEARCH_KEYWORDS.get(category, "스마트폰")

        # 캐시 또는 검색
        cache_key = f"search_{keyword}_20"
        cached_data = self.cache_manager.get(cache_key)

        if cached_data:
            all_phones = cached_data
        else:
            all_phones = self.scraper.search_products(keyword, max_results=20)
            if all_phones and not all_phones[0].get("error"):
                self.cache_manager.set(cache_key, all_phones)

        if all_phones and all_phones[0].get("error"):
            return {"error": all_phones[0].get("error")}

        # 예산별 필터링
        filtered = self.price_analyzer.filter_by_budget(
            all_phones,
            budget,
            BUDGET_MULTIPLIER
        )

        result = {
            "budget": f"{budget:,}원",
            "category": category,
            "within_budget_count": filtered.get("within_budget_count", 0),
            "recommendations": filtered.get("recommendations", [])[:RECOMMENDATION_LIMIT]
        }

        if "slightly_above_budget" in filtered:
            result["slightly_above_budget"] = filtered["slightly_above_budget"][:SLIGHTLY_ABOVE_BUDGET_LIMIT]

        logger.info(f"추천 완료: {result['within_budget_count']}개 제품")
        return result

    async def run(self) -> None:
        """서버 실행"""
        logger.info("MCP 서버 시작")
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """메인 함수"""
    server = CoupangPhonePriceServer()
    await server.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("서버 종료")
    except Exception as e:
        logger.error(f"서버 오류: {e}")
        raise
