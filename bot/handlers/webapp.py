"""
WebApp Handler - Data callbacks from Mini App (Telegram.WebApp.postEvent)
Backend exposes HTTP endpoints for WebApp to fetch data
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes

from bot.services.user_service import UserService
from bot.services.referral_service import ReferralService
from bot.services.payment_service import PaymentService
from bot.services.dex_service import DexService

logger = logging.getLogger(__name__)


# WebApp communicates via Telegram WebApp.initData - validated on backend
# For now, handlers are for future: inline_query, callback_query from WebApp
# Primary data flow: WebApp -> your HTTP API (Flask/FastAPI) -> DB
# Or: WebApp calls bot methods via initData - we'd need a separate API server

def setup_webapp_handlers(app) -> None:
    """Reserved for WebApp-specific bot handlers (e.g. inline, callbacks)."""
    pass
