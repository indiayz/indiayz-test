import os
import telebot

from indiayz.wiki import wiki
from indiayz.media import download as media


# ======================
# CONFIG
# ======================
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")


# ======================
# SAFE RESPONSE
# ======================
def safe_text(res):
    if isinstance(res, dict):
        if res.get("success") is False:
            return res.get("error", "Unknown error")
        return res.get("data") or str(res)
    return str(res)


# ======================
# START / HELP
# ======================
@bot.message_handler(commands=["start", "help"])
def start(m):
    bot.reply_to(
        m,
        "👋 <b>Nia Bot</b>\n\n"
        "📘 <b>/wiki topic</b>\n"
        "🎬 <b>Media link bhejo</b>\n\n"
        "Example:\n"
        "<code>/wiki india</code>\n"
        "<code>https://youtube.com/...</code>"
    )


# ======================
# WIKI
# ======================
@bot.message_handler(commands=["wiki"])
def wiki_cmd(m):
    query = m.text.replace("/wiki", "").strip()

    if not query:
        bot.reply_to(m, "❌ Topic likho\nExample: <code>/wiki usa</code>")
        return

    res = wiki(query.title())
    bot.reply_to(m, safe_text(res))


# ======================
# MEDIA
# ======================
@bot.message_handler(func=lambda m: "http" in m.text)
def media_cmd(m):
    try:
        res = media(m.text.strip())
        bot.reply_to(m, safe_text(res))
    except Exception as e:
        bot.reply_to(m, f"❌ Media error:\n<code>{e}</code>")


# ======================
# FALLBACK
# ======================
@bot.message_handler(func=lambda m: True)
def fallback(m):
    bot.reply_to(
        m,
        "❓ Samajh nahi aaya\n\n"
        "Use:\n"
        "📘 /wiki topic\n"
        "🎬 media link"
    )


# ======================
# RUN
# ======================
print("🤖 Bot started")
bot.infinity_polling(skip_pending=True)
