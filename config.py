"""
MEMEKRAL - Centralized Configuration
Environment-based config for dev/staging/prod parity
"""
import os
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Optional


@dataclass(frozen=True)
class Config:
    """Immutable config - prevents accidental overrides."""
    # Telegram
    BOT_TOKEN: str = field(default_factory=lambda: os.getenv("BOT_TOKEN", ""))
    WEBAPP_URL: str = field(default_factory=lambda: os.getenv("WEBAPP_URL", "https://your-domain.com"))
    WEBHOOK_URL: Optional[str] = field(default_factory=lambda: os.getenv("WEBHOOK_URL") or None)
    
    # App
    ENV: str = field(default_factory=lambda: os.getenv("ENV", "development"))
    DEBUG: bool = field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")
    
    # Database
    DATABASE_URL: str = field(default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///memekral.db"))
    
    # Dexscreener API
    DEXSCREENER_BASE_URL: str = field(default_factory=lambda: os.getenv("DEXSCREENER_URL", "https://api.dexscreener.com"))
    
    # Payment (Telegram Stars)
    STAR_PRICE_MULTIPLIER: int = 1  # 1 Star = 0.013 USD
    PAYMENT_PROVIDER_TOKEN: str = field(default_factory=lambda: os.getenv("PAYMENT_PROVIDER_TOKEN", ""))
    
    @property
    def is_production(self) -> bool:
        return self.ENV == "production"
    
    @property
    def use_webhook(self) -> bool:
        """Webhook scales better than polling for production."""
        return bool(self.WEBHOOK_URL) and self.is_production


@lru_cache(maxsize=1)
def get_config() -> Config:
    """Singleton config - load once, reuse everywhere."""
    return Config()
