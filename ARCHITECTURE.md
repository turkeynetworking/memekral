# MEMEKRAL - Scalable Backend Architecture

## Genel Yapı

```
MEMEKRAL/
├── config.py              # Merkezi konfig (env-based, immutable)
├── bot.py                 # Giriş noktası (legacy)
├── run_api.py             # API sunucusu
├── bot/
│   ├── main.py            # Application factory, lifecycle
│   ├── handlers/          # Telegram event handlers (thin layer)
│   │   ├── start.py
│   │   ├── payment.py
│   │   └── webapp.py
│   ├── services/          # İş mantığı (business logic)
│   │   ├── user_service.py
│   │   ├── referral_service.py
│   │   ├── payment_service.py
│   │   └── dex_service.py
│   └── db/
│       └── database.py    # DB bağlantısı, migrations
├── api/
│   ├── server.py          # FastAPI - WebApp backend
│   └── auth.py            # initData doğrulama
└── webapp/
    └── index.html         # Telegram Mini App (frontend)
```

## Katmanlar

| Katman | Sorumluluk | Ölçeklenebilirlik |
|--------|------------|-------------------|
| **Handlers** | Telegram event'lerini karşıla, service'e yönlendir | Her handler bağımsız modül |
| **Services** | İş kuralları, DB erişimi, harici API'ler | Stateless, test edilebilir |
| **DB** | Bağlantı havuzu, şema | SQLite → PostgreSQL geçişi kolay |
| **API** | WebApp için REST, initData auth | FastAPI workers ile horizontal scaling |

## Scaling Stratejisi

1. **Bot**: Polling (dev) → Webhook (prod, tek instance) → Çoklu webhook worker
2. **API**: Uvicorn workers (`--workers 4`) → Kubernetes/Docker replicas
3. **DB**: SQLite → PostgreSQL + connection pooling (asyncpg)
4. **Cache**: Redis (rate limit, Dexscreener cache) - opsiyonel

## Veri Akışı

```
Telegram User → /start → Handler → UserService → DB
WebApp → fetch(/api/wallet, {headers: {X-Telegram-Init-Data}}) → API → Auth → PaymentService → DB
WebApp → fetch(/api/dex/search?q=...) → API → DexService → Dexscreener
```

## Ortam Değişkenleri

`.env.example` dosyasından kopyala, `.env` oluştur.
