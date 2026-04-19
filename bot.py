import logging
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ─── CONFIG ───────────────────────────────────────────────────────────────────
BOT_TOKEN   = "8640496281:AAGjDMK5sd9pUsv1uYOfQPd8rJguwz_YRoA"
CHANNEL_URL = "https://t.me/mhn_hydra"
ADMIN_URL   = "https://t.me/mahinbhai76"
TOOL_URL    = "https://secret011.netlify.app/"
WELCOME_IMG = "https://i.ibb.co/kgZQMfHL/1000030822.png"
PORT        = 10000
# ──────────────────────────────────────────────────────────────────────────────

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ─── Flask keep-alive ─────────────────────────────────────────────────────────
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Bot is running! ✅"

@flask_app.route("/health")
def health():
    return {"status": "ok"}, 200

def run_flask():
    flask_app.run(host="0.0.0.0", port=PORT)

# ─── Welcome message (HTML - no escaping issues) ──────────────────────────────
WELCOME_TEXT = (
    "🎬 <b>Welcome to TikTok Downloader Bot!</b> 🎬\n\n"
    "Download TikTok videos <b>without watermark</b> — fast, free and easy.\n\n"
    "📌 <b>How to use:</b>\n"
    "Send me any TikTok video link and I will download it for you!\n\n"
    "━━━━━━━━━━━━━━━━━━━━━\n"
    "📢 <b>Channel:</b> <a href='https://t.me/mhn_hydra'>mhn_hydra</a>\n"
    "👤 <b>Admin:</b> <a href='https://t.me/mahinbhai76'>@mahinbhai76</a>\n"
    "━━━━━━━━━━━━━━━━━━━━━\n\n"
    "⬇️ Tap the button below to open the downloader tool!"
)

def build_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀  Open Downloader Tool  🚀", url=TOOL_URL)],
        [
            InlineKeyboardButton("📢 Our Channel", url=CHANNEL_URL),
            InlineKeyboardButton("👤 Admin", url=ADMIN_URL),
        ],
    ])

# ─── Handlers ─────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_photo(
            photo=WELCOME_IMG,
            caption=WELCOME_TEXT,
            parse_mode="HTML",
            reply_markup=build_keyboard(),
        )
        logger.info(f"/start used by {update.message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in /start: {e}")
        await update.message.reply_text(
            "Welcome to TikTok Downloader Bot! 🎬\nSend me a TikTok link to download.",
            reply_markup=build_keyboard(),
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Send me a TikTok video link and I will download it! 🎬")

# ─── Main ─────────────────────────────────────────────────────────────────────
def main() -> None:
    t = threading.Thread(target=run_flask, daemon=True)
    t.start()
    logger.info(f"Flask running on port {PORT}")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    logger.info("Bot polling started...")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()
