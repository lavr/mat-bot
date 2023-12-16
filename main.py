import logging
import os

from dotenv import load_dotenv
from telegram import ForceReply, Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from processor.chatgpt import process_text

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

HELP_TEXT = "Я бот Иры К., который помогает сформулировать мысли. Напиши фразу, из которой нужно убрать плохие слова"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! {HELP_TEXT}",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP_TEXT)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response_text = process_text(update.message.text)
    await update.message.reply_text(response_text)


def main() -> None:
    load_dotenv()

    application = Application.builder().token(os.environ.get('TELEGRAM_BOT_TOKEN')).build()  # инициализируем бота
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
