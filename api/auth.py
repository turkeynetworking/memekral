"""
Telegram WebApp initData validation
Ensures requests come from legitimate Mini App
"""
import hashlib
import hmac
import json
import logging
from typing import Optional
from urllib.parse import parse_qsl

from config import get_config

logger = logging.getLogger(__name__)


def validate_init_data(init_data: str) -> Optional[dict]:
    """
    Validate Telegram WebApp initData.
    https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
    """
    if not init_data:
        return None
    config = get_config()
    # secret_key = HMAC_SHA256(bot_token, "WebAppData")
    secret = hmac.new(
        config.BOT_TOKEN.encode(),
        b"WebAppData",
        hashlib.sha256
    ).digest()
    parsed = dict(parse_qsl(init_data))
    hash_val = parsed.pop("hash", None)
    if not hash_val:
        return None
    data_check = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
    expected = hmac.new(secret, data_check.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, hash_val):
        return None
    # Check auth_date (optional: reject if too old, e.g. > 1 hour)
    try:
        auth_date = int(parsed.get("auth_date", 0))
        import time as _time
        if auth_date < (int(_time.time()) - 86400):  # 24h max
            return None
        user_str = parsed.get("user")
        if user_str:
            return {"user": json.loads(user_str), "auth_date": auth_date}
        return parsed
    except Exception:
        return None
