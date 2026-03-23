"""
Dex Service - Dexscreener API client
Memecoin analysis, rate-limited (60 req/min), cache-ready for scaling
"""
import logging
from typing import Any, Dict, List

import aiohttp

logger = logging.getLogger(__name__)

BASE_URL = "https://api.dexscreener.com"


class DexService:
    """Dexscreener API - search, token pairs, community takeovers."""

    @staticmethod
    async def search(query: str, limit: int = 15) -> List[Dict[str, Any]]:
        """Search tokens by name/symbol/address. GET /latest/dex/search?q="""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{BASE_URL}/latest/dex/search", params={"q": query}) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return (data.get("pairs") or [])[:limit]
            except Exception as e:
                logger.warning(f"Dexscreener search error: {e}")
        return []

    @staticmethod
    async def get_token_pairs(chain_id: str, token_address: str) -> List[Dict[str, Any]]:
        """Get all pairs for a token. GET /token-pairs/v1/{chainId}/{tokenAddress}"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"{BASE_URL}/token-pairs/v1/{chain_id}/{token_address}"
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("pairs", [])
            except Exception as e:
                logger.warning(f"Dexscreener token-pairs error: {e}")
        return []

    @staticmethod
    async def get_community_takeovers(limit: int = 20) -> List[Dict[str, Any]]:
        """Latest token community takeovers - trending memecoins. Rate: 60/min."""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{BASE_URL}/community-takeovers/latest/v1") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return (data if isinstance(data, list) else [])[:limit]
            except Exception as e:
                logger.warning(f"Dexscreener community-takeovers error: {e}")
        return []
