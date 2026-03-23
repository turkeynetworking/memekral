"""
Start Handler - /start, WebApp button, referral deep link
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes, CommandHandler

from config import get_config
from bot.services.user_service import UserService
from bot.services.referral_service import ReferralService

logger = logging.getLogger(__name__)


def _parse_start_args(text: str | None) -> int | None:
    """Extract referrer_id from /start ref_12345"""
    if not text or not text.strip():
        return None
    parts = text.strip().split()
    if len(parts) < 2:
        return None
    ref = parts[1]
    if ref.startswith("ref_"):
        try:
            return int(ref[4:])
        except ValueError:
            return None
    return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start - register user, show WebApp button."""
    if not update.message:
        return
    user = update.effective_user
    if not user:
        return

    referrer_id = _parse_start_args(update.message.text)
    await UserService.get_or_create(
        telegram_id=user.id,
        username=user.username,
        referrer_id=referrer_id,
    )
    if referrer_id and referrer_id != user.id:
        await ReferralService.add_referral(referrer_id, user.id)

    config = get_config()
    keyboard = [[
        InlineKeyboardButton("👑 KRALI BAŞLAT", web_app=WebAppInfo(url=config.WEBAPP_URL))
    ]]
    await update.message.reply_text(
        "👑 Kral hoş geldin! Piyasayı süpürmeye hazır mısın?",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


def setup_start_handlers(app) -> None:
    """Register start handlers."""
    app.add_handler(CommandHandler("start", start))
