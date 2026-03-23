"""
User Service - Business logic for user management
Single responsibility, testable, injectable
"""
import logging
from dataclasses import dataclass
from typing import Optional

from bot.db.database import get_cursor

logger = logging.getLogger(__name__)


@dataclass
class User:
    telegram_id: int
    username: Optional[str]
    referrer_id: Optional[int]
    created_at: Optional[str] = None


class UserService:
    """Handles user CRUD and session validation."""

    @staticmethod
    async def get_or_create(telegram_id: int, username: Optional[str] = None, referrer_id: Optional[int] = None) -> User:
        """Idempotent user registration."""
        async with get_cursor() as cursor:
            await cursor.execute(
                "SELECT telegram_id, username, referrer_id, created_at FROM users WHERE telegram_id = ?",
                (telegram_id,)
            )
            row = await cursor.fetchone()
            if row:
                return User(telegram_id=row[0], username=row[1], referrer_id=row[2], created_at=row[3])

            await cursor.execute(
                "INSERT INTO users (telegram_id, username, referrer_id) VALUES (?, ?, ?)",
                (telegram_id, username, referrer_id)
            )
            logger.info(f"New user registered: {telegram_id}")
            return User(telegram_id=telegram_id, username=username, referrer_id=referrer_id)

    @staticmethod
    async def get(telegram_id: int) -> Optional[User]:
        """Fetch user by telegram_id."""
        from bot.db.database import get_db
        db = await get_db()
        cursor = await db.execute(
            "SELECT telegram_id, username, referrer_id, created_at FROM users WHERE telegram_id = ?",
            (telegram_id,)
        )
        row = await cursor.fetchone()
        if not row:
            return None
        return User(telegram_id=row[0], username=row[1], referrer_id=row[2], created_at=row[3])

    @staticmethod
    async def save_webapp_session(telegram_id: int, init_data: str) -> None:
        """Persist WebApp initData for server-side validation."""
        async with get_cursor() as cursor:
            await cursor.execute(
                """
                INSERT INTO user_sessions (telegram_id, init_data, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(telegram_id) DO UPDATE SET init_data = excluded.init_data, updated_at = CURRENT_TIMESTAMP
                """,
                (telegram_id, init_data)
            )
