"""
MEMEKRAL Bot - Application factory & entry point
Scalable: handlers are modular, services are injectable
"""
import asyncio
import logging
import sys

from telegram.ext import ApplicationBuilder

from config import get_config
from bot.db.database import init_db, close_db
from bot.handlers import setup_start_handlers, setup_payment_handlers, setup_webapp_handlers

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


def create_app():
    """Application factory - build bot with all handlers."""
    config = get_config()
    if not config.BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable is required")

    app = (
        ApplicationBuilder()
        .token(config.BOT_TOKEN)
        .post_init(_on_startup)
        .post_shutdown(_on_shutdown)
        .build()
    )

    setup_start_handlers(app)
    setup_payment_handlers(app)
    setup_webapp_handlers(app)

    return app


async def _on_startup(app) -> None:
    await init_db()
    logger.info("Bot started")


async def _on_shutdown(app) -> None:
    await close_db()
    logger.info("Bot shutdown complete")


def run():
    """Run bot - polling (dev) or webhook (prod)."""
    config = get_config()
    app = create_app()

    if config.use_webhook:
        # Production: use webhook for better scalability
        # Requires: HTTPS, public URL, uvicorn/gunicorn for webhook endpoint
        logger.info("Webhook mode - use run_webhook.py with proper setup")
        sys.exit(1)

    app.run_polling(allowed_updates=["message", "pre_checkout_query"])


if __name__ == "__main__":
    run()
