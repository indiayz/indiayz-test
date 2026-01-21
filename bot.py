from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import indiayz
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Indiayz Telegram Bot\n\n"
        "/wiki <topic>\n"
        "/video <url>"
    )

# ---------------- WIKI ----------------
async def wiki(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /wiki <topic>")
        return

    query = " ".join(context.args)

    try:
        data = indiayz.wikipedia_search(query)
        await update.message.reply_text(str(data)[:4000])
    except Exception as e:
        await update.message.reply_text(f"❌ Wiki error\n{e}")

# ---------------- VIDEO ----------------
async def video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /video <url>")
        return

    url = context.args[0]

    try:
        data = indiayz.media_download(url)
        text = "🎥 Media Info\n\n"
        for k, v in data.items():
            text += f"{k}: {v}\n"
        await update.message.reply_text(text[:4000])
    except Exception as e:
        await update.message.reply_text(f"❌ Media error\n{e}")

# ---------------- MAIN ----------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("wiki", wiki))
    app.add_handler(CommandHandler("video", video))

    print("🤖 Indiayz bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
