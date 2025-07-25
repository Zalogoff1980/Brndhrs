import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
from strategy import get_rsi

TOKEN = "8308663481:AAGBLxEKXnbYzFZ-PATtfV_-hhyVJ0AfieU"

trading = {
    "active": False,
    "step": 0,
    "sequence": [1, 2.5, 6],
    "balance": 10000
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    trading["active"] = True
    trading["step"] = 0
    await update.message.reply_text("✅ Торговля запущена (демо, RSI + Мартингейл)")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    trading["active"] = False
    await update.message.reply_text("⛔️ Торговля остановлена")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = f"""📊 Статус:
— Активно: {'Да' if trading['active'] else 'Нет'}
— Шаг: {trading['step'] + 1}
— Ставка: {trading['sequence'][trading['step']]} $
— Баланс (виртуальный): {trading['balance']} $
"""
    await update.message.reply_text(msg)

async def trade_loop():
    while True:
        if trading["active"]:
            rsi = get_rsi()
            print(f"RSI: {rsi}")

            if rsi is None:
                await asyncio.sleep(60)
                continue

            if rsi < 30 or rsi > 70:
                bet = trading["sequence"][trading["step"]]
                print(f"📈 Ставка: {bet}$ по RSI {rsi}")

                win = True if trading["step"] < 2 else False  # эмуляция результата

                if win:
                    trading["balance"] += bet * 0.8
                    trading["step"] = 0
                else:
                    trading["balance"] -= bet
                    trading["step"] = min(trading["step"] + 1, 2)

        await asyncio.sleep(60)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("status", status))

    loop = asyncio.get_event_loop()
    loop.create_task(trade_loop())
    app.run_polling()
