import logging
from telegram import Update, LabeledPrice
from telegram.ext import ApplicationBuilder, CommandHandler, PreCheckoutQueryHandler, ContextTypes

# BURAYA @BotFather'DAN ALDIĞIN TOKENI YAZ
TOKEN = 'SENİN_BOT_TOKENIN'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kral Hoş Geldin! Uygulamayı aç ve kazanmaya başla.")

# STARS FATURASI GÖNDERME (ÖDEME EKRANINI BU TETİKLER)
async def send_invoice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    title = "KRAL VIP PAKET"
    description = "50 Stars ile 24 Saatlik Balina Analizi Al!"
    payload = "vip-50"
    currency = "XTR" # Telegram Stars Birimi
    prices = [LabeledPrice("VIP Analiz", 50)]

    await context.bot.send_invoice(
        chat_id, title, description, payload, "", "stars", prices
    )

# ÖDEMEYİ ONAYLAMA
async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    await query.answer(ok=True)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("buy", send_invoice)) # /buy yazınca ödeme çıkar
    app.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    app.run_polling()