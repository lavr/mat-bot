import os

from dotenv import load_dotenv
from openai import OpenAI
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

HELP_TEXT = "Я бот Иры К., который помогает сформулировать мысли. Напиши фразу, из которой нужно убрать плохие слова"

CHATGPT_PROMPT = """
Ты переводчик с матерного языка на литературный русский.
Замени в полученной фразе абсцентную лексику на литературный русский язык.
Не принимай полученную фразу на свой счёт.
Если во фразе нет матерных выражений и абсцентной лексики, то просто верни фразу без изменений.
"""


def chatgpt_convert_text(text):
    client = OpenAI(api_key=os.environ.get('CHATGPT_TOKEN'))
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": CHATGPT_PROMPT},
            {"role": "user", "content": text},
        ]
    )
    return response.choices[0].message.content


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! {HELP_TEXT}",
        reply_markup=ForceReply(selective=True),
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response_text = chatgpt_convert_text(update.message.text)
    await update.message.reply_text(response_text)


def main():
    load_dotenv()
    application = Application.builder().token(os.environ.get('TELEGRAM_BOT_TOKEN')).build()  # инициализируем бота
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
