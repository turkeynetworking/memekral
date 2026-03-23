"""
Referral Service - Network marketing logic
Handles referral tree, stats, commissions
"""
import logging
from dataclasses import dataclass
from typing import List

from bot.db.database import get_cursor, get_db

logger = logging.getLogger(__name__)


@dataclass
class ReferralStats:
    total_referrals: int
    level_1: int
    level_2: int  # Future: multi-level


class ReferralService:
    """Referral/network logic."""

    @staticmethod
    async def add_referral(referrer_id: int, referred_id: int) -> bool:
        """Link referred user to referrer. Returns False if already exists."""
        async with get_cursor() as cursor:
            try:
                await cursor.execute(
                    "INSERT INTO referrals (referrer_id, referred_id) VALUES (?, ?)",
                    (referrer_id, referred_id)
                )
                logger.info(f"Referral: {referrer_id} -> {referred_id}")
                return True
            except Exception:
                return False  # Unique constraint

    @staticmethod
    async def get_stats(telegram_id: int) -> ReferralStats:
        """Get referral counts for user."""
        db = await get_db()
        cursor = await db.execute(
            "SELECT COUNT(*) FROM referrals WHERE referrer_id = ?",
            (telegram_id,)
        )
        row = await cursor.fetchone()
        total = row[0] if row else 0
        return ReferralStats(total_referrals=total, level_1=total, level_2=0)

    @staticmethod
    async def get_referral_list(telegram_id: int, limit: int = 50) -> List[int]:
        """Get list of referred user IDs."""
        db = await get_db()
        cursor = await db.execute(
            "SELECT referred_id FROM referrals WHERE referrer_id = ? ORDER BY created_at DESC LIMIT ?",
            (telegram_id, limit)
        )
        rows = await cursor.fetchall()
        return [r[0] for r in rows] if rows else []
