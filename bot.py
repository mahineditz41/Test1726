import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ─── CONFIG ───────────────────────────────────────────────────────────────────
BOT_TOKEN   = "8640496281:AAGjDMK5sd9pUsv1uYOfQPd8rJguwz_YRoA"
CHANNEL_URL = "https://t.me/mhn_hydra"
ADMIN_URL   = "https://t.me/mahinbhai76"
TOOL_URL    = "https://secret011.netlify.app/"
WELCOME_IMG = "https://i.ibb.co/kgZQMfHL/1000030822.png"
# ──────────────────────────────────────────────────────────────────────────────

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

WELCOME_TEXT = (
    "🎬 *Welcome to TikTok Downloader Bot!* 🎬\n\n"
    "Download TikTok videos *without watermark* — fast, free, and easy\\.\n\n"
    "📌 *How to use:*\n"
    "Simply send me any TikTok video link and I'll get it ready for download\\!\n\n"
    "━━━━━━━━━━━━━━━━━━━━━\n"
    "📢 *Channel:* [mhn\\_hydra](https://t.me/mhn_hydra)\n"
    "👤 *Admin:* [@mahinbhai76](https://t.me/mahinbhai76)\n"
    "━━━━━━━━━━━━━━━━━━━━━\n\n"
    "⬇️ Tap the button below to open the downloader tool\\!"
)


def build_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        # Row 1 — big single button
        [InlineKeyboardButton("🚀  Open Downloader Tool  🚀", url=TOOL_URL)],
        # Row 2 — two side-by-side buttons
        [
            InlineKeyboardButton("📢 Our Channel", url=CHANNEL_URL),
            InlineKeyboardButton("👤 Admin",       url=ADMIN_URL),
        ],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the welcome photo + message when /start is issued."""
    await update.message.reply_photo(
        photo=WELCOME_IMG,
        caption=WELCOME_TEXT,
        parse_mode="MarkdownV2",
        reply_markup=build_keyboard(),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Send me a TikTok video link and I'll download it for you\\! 🎬",
        parse_mode="MarkdownV2",
    )


def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help",  help_command))

    logger.info("Bot is running…  Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
