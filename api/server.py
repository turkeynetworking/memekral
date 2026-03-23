"""
MEMEKRAL API Server - FastAPI
WebApp backend: wallet, referrals, dex proxy
"""
import logging
import os
from typing import Optional

from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import get_config
from api.auth import validate_init_data
from bot.db.database import init_db, get_db
from bot.services.payment_service import PaymentService
from bot.services.referral_service import ReferralService
from bot.services.dex_service import DexService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MEMEKRAL API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production to Telegram origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Auth dependency ---
async def get_telegram_user(x_telegram_init_data: Optional[str] = Header(None)) -> int:
    """Validate initData and return telegram user id."""
    if not x_telegram_init_data:
        raise HTTPException(401, "Missing X-Telegram-Init-Data")
    data = validate_init_data(x_telegram_init_data)
    if not data:
        raise HTTPException(401, "Invalid init data")
    user = data.get("user")
    if not user:
        raise HTTPException(401, "No user in init data")
    uid = user.get("id")
    if uid is None:
        raise HTTPException(401, "Invalid user")
    return int(uid)


# --- Response models ---
class WalletResponse(BaseModel):
    balance_stars: int


class ReferralStatsResponse(BaseModel):
    total_referrals: int
    level_1: int


class DexSearchResponse(BaseModel):
    pairs: list


# --- Routes ---
@app.on_event("startup")
async def startup():
    await init_db()


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.get("/api/wallet", response_model=WalletResponse)
async def get_wallet(telegram_id: int = Depends(get_telegram_user)):
    balance = await PaymentService.get_balance_stars(telegram_id)
    return WalletResponse(balance_stars=balance)


@app.get("/api/referrals", response_model=ReferralStatsResponse)
async def get_referrals(telegram_id: int = Depends(get_telegram_user)):
    stats = await ReferralService.get_stats(telegram_id)
    return ReferralStatsResponse(
        total_referrals=stats.total_referrals,
        level_1=stats.level_1,
    )


@app.get("/api/dex/search", response_model=DexSearchResponse)
async def dex_search(q: str = "", limit: int = 15):
    """Proxy Dexscreener search - no auth required (public data)."""
    pairs = await DexService.search(q or "solana", limit=limit)
    return DexSearchResponse(pairs=pairs)


@app.get("/api/dex/trending", response_model=DexSearchResponse)
async def dex_trending(limit: int = 20):
    """Community takeovers - trending memecoins."""
    data = await DexService.get_community_takeovers(limit=limit)
    return DexSearchResponse(pairs=data)


def run():
    import uvicorn
    config = get_config()
    uvicorn.run(
        "api.server:app",
        host="0.0.0.0",
        port=int(os.getenv("API_PORT", "8000")),
        reload=config.DEBUG,
    )


if __name__ == "__main__":
    run()
