"""
캐시 관리 모듈
"""

from datetime import datetime, timedelta
from typing import Any, Optional, Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class CacheManager:
    """캐시 데이터를 관리하는 클래스"""

    def __init__(self, cache_duration: timedelta):
        """
        Args:
            cache_duration: 캐시 유효 시간
        """
        self._cache: Dict[str, Tuple[Any, datetime]] = {}
        self._cache_duration = cache_duration

    def get(self, key: str) -> Optional[Any]:
        """
        캐시에서 데이터를 가져옵니다.

        Args:
            key: 캐시 키

        Returns:
            캐시된 데이터 또는 None
        """
        if key in self._cache:
            data, timestamp = self._cache[key]
            if datetime.now() - timestamp < self._cache_duration:
                logger.info(f"캐시 히트: {key}")
                return data
            else:
                del self._cache[key]
                logger.info(f"캐시 만료: {key}")
        return None

    def set(self, key: str, data: Any) -> None:
        """
        데이터를 캐시에 저장합니다.

        Args:
            key: 캐시 키
            data: 저장할 데이터
        """
        self._cache[key] = (data, datetime.now())
        logger.info(f"캐시 저장: {key}")

    def clear(self) -> None:
        """모든 캐시를 삭제합니다."""
        self._cache.clear()
        logger.info("캐시 전체 삭제")

    def remove(self, key: str) -> bool:
        """
        특정 캐시 항목을 삭제합니다.

        Args:
            key: 삭제할 캐시 키

        Returns:
            삭제 성공 여부
        """
        if key in self._cache:
            del self._cache[key]
            logger.info(f"캐시 삭제: {key}")
            return True
        return False

    def get_cache_info(self) -> Dict[str, Any]:
        """
        캐시 상태 정보를 반환합니다.

        Returns:
            캐시 상태 정보 딕셔너리
        """
        return {
            "total_items": len(self._cache),
            "cache_duration_minutes": self._cache_duration.total_seconds() / 60,
            "keys": list(self._cache.keys())
        }
