import os
import telebot
from indiayz import wiki, media

# ======================
# CONFIG
# ======================
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Heroku config var
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")


# ======================
# SAFE RESPONSE HANDLER
# ======================
def safe_text(res):
    """
    indiayz kabhi dict return karta hai
    kabhi string
    ye function dono ko safely handle karega
    """
    if isinstance(res, dict):
        if res.get("success") is False:
            return res.get("error", "Unknown error")
        return res.get("data") or str(res)
    return str(res)


# ======================
# COMMANDS
# ======================
@bot.message_handler(commands=["start", "help"])
def start(m):
    bot.reply_to(
        m,
        "👋 <b>Nia Bot</b>\n\n"
        "📘 <b>/wiki topic</b> – Wikipedia search\n"
        "🎬 <b>Media link bhejo</b> – video download info\n\n"
        "Example:\n"
        "<code>/wiki usa</code>\n"
        "<code>https://youtube.com/...</code>"
    )


@bot.message_handler(commands=["wiki"])
def wiki_cmd(m):
    query = m.text.replace("/wiki", "").strip()

    if not query:
        bot.reply_to(m, "❌ Topic likho\nExample: <code>/wiki india</code>")
        return

    query = query.title()  # usa → Usa
    res = wiki(query)
    bot.reply_to(m, safe_text(res))


# ======================
# MEDIA HANDLER
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
        "🎬 koi media link"
    )


# ======================
# START BOT
# ======================
print("🤖 Bot started...")
bot.infinity_polling(skip_pending=True)
