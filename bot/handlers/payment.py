"""
Payment Handler - Telegram Stars (XTR), pre_checkout, successful_payment
"""
import logging
from telegram import Update, LabeledPrice
from telegram.ext import ContextTypes, PreCheckoutQueryHandler, MessageHandler, filters

from config import get_config
from bot.services.payment_service import PaymentService

logger = logging.getLogger(__name__)


async def pre_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Approve pre-checkout - validate payload, amount before charging."""
    query = update.pre_checkout_query
    if not query:
        return
    # Optional: validate payload, amount, user here
    await query.answer(ok=True)


async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Persist payment, credit user wallet."""
    msg = update.message
    if not msg or not msg.successful_payment:
        return
    pay = msg.successful_payment
    await PaymentService.record_payment(
        telegram_id=msg.from_user.id if msg.from_user else 0,
        amount_stars=pay.total_amount,
        payload=pay.invoice_payload or "",
        telegram_payment_charge_id=pay.telegram_payment_charge_id,
        provider_payment_charge_id=pay.provider_payment_charge_id,
    )
    await msg.reply_text(f"✅ {pay.total_amount} ⭐ Stars cüzdanına eklendi!")


async def send_stars_invoice(
    chat_id: int,
    title: str,
    description: str,
    payload: str,
    amount_stars: int,
    bot,
) -> bool:
    """Send Stars invoice. Requires PAYMENT_PROVIDER_TOKEN from @BotFather."""
    config = get_config()
    if not config.PAYMENT_PROVIDER_TOKEN:
        logger.warning("PAYMENT_PROVIDER_TOKEN not set - Stars disabled")
        return False
    prices = [LabeledPrice(label="XTR Stars", amount=amount_stars)]
    await bot.send_invoice(
        chat_id=chat_id,
        title=title,
        description=description,
        payload=payload,
        provider_token=config.PAYMENT_PROVIDER_TOKEN,
        currency="XTR",  # Telegram Stars
        prices=prices,
    )
    return True


def setup_payment_handlers(app) -> None:
    """Register payment handlers."""
    app.add_handler(PreCheckoutQueryHandler(pre_checkout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
