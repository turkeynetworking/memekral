"""
Database Layer - Connection pooling & lifecycle management
Supports SQLite (dev) and PostgreSQL (prod) via same interface
"""
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import aiosqlite

from config import get_config

logger = logging.getLogger(__name__)

# Global connection - for SQLite simple case. PostgreSQL would use connection pool.
_db: aiosqlite.Connection | None = None


async def init_db() -> None:
    """Initialize database and create tables."""
    global _db
    config = get_config()
    
    if config.DATABASE_URL.startswith("sqlite"):
        path = config.DATABASE_URL.replace("sqlite:///", "")
        _db = await aiosqlite.connect(path)
        _db.row_factory = aiosqlite.Row  # Dict-like access
        await _create_tables(_db)
        logger.info("Database initialized (SQLite)")
    else:
        # PostgreSQL: use asyncpg when needed
        raise NotImplementedError("PostgreSQL support: add asyncpg, implement pool")


async def _create_tables(db: aiosqlite.Connection) -> None:
    """Create schema - migrations would go in separate files for larger apps."""
    await db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            referrer_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (referrer_id) REFERENCES users(telegram_id)
        );
        CREATE TABLE IF NOT EXISTS referrals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            referrer_id INTEGER NOT NULL,
            referred_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(referrer_id, referred_id),
            FOREIGN KEY (referrer_id) REFERENCES users(telegram_id),
            FOREIGN KEY (referred_id) REFERENCES users(telegram_id)
        );
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            amount_stars INTEGER NOT NULL,
            payload TEXT,
            telegram_payment_charge_id TEXT,
            provider_payment_charge_id TEXT,
            status TEXT DEFAULT 'completed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (telegram_id) REFERENCES users(telegram_id)
        );
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE NOT NULL,
            init_data TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (telegram_id) REFERENCES users(telegram_id)
        );
        CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);
        CREATE INDEX IF NOT EXISTS idx_referrals_referrer ON referrals(referrer_id);
        CREATE INDEX IF NOT EXISTS idx_transactions_telegram ON transactions(telegram_id);
    """)


async def get_db() -> aiosqlite.Connection:
    """Get database connection. Call after init_db()."""
    if _db is None:
        await init_db()
    assert _db is not None
    return _db


@asynccontextmanager
async def get_cursor() -> AsyncGenerator[aiosqlite.Cursor, None]:
    """Context manager for cursor - ensures proper commit/rollback."""
    db = await get_db()
    async with db.cursor() as cursor:
        try:
            yield cursor
            await db.commit()
        except Exception:
            await db.rollback()
            raise


async def close_db() -> None:
    """Graceful shutdown - close connections."""
    global _db
    if _db:
        await _db.close()
        _db = None
        logger.info("Database connection closed")
