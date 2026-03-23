"""
Payment Service - Telegram Stars (XTR) integration
Handles invoices, pre-checkout, successful payment callbacks
"""
import logging
from dataclasses import dataclass
from typing import Optional

from bot.db.database import get_cursor, get_db

logger = logging.getLogger(__name__)


@dataclass
class PaymentRecord:
    id: int
    telegram_id: int
    amount_stars: int
    payload: Optional[str]
    status: str


class PaymentService:
    """Stars payment business logic."""

    @staticmethod
    async def record_payment(
        telegram_id: int,
        amount_stars: int,
        payload: str,
        telegram_payment_charge_id: str,
        provider_payment_charge_id: str,
    ) -> None:
        """Persist successful payment."""
        async with get_cursor() as cursor:
            await cursor.execute(
                """
                INSERT INTO transactions (telegram_id, amount_stars, payload, telegram_payment_charge_id, provider_payment_charge_id, status)
                VALUES (?, ?, ?, ?, ?, 'completed')
                """,
                (telegram_id, amount_stars, payload, telegram_payment_charge_id, provider_payment_charge_id)
            )
        logger.info(f"Payment recorded: {telegram_id} +{amount_stars} Stars")

    @staticmethod
    async def get_balance_stars(telegram_id: int) -> int:
        """Sum of all received Stars for user (wallet balance)."""
        db = await get_db()
        cursor = await db.execute(
            "SELECT COALESCE(SUM(amount_stars), 0) FROM transactions WHERE telegram_id = ? AND status = 'completed'",
            (telegram_id,)
        )
        row = await cursor.fetchone()
        return int(row[0]) if row else 0
