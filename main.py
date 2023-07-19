import logging
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import get_hitfm
import jsweather


async def get_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(get_hitfm.hitfm_geturl())


async def jsweather_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(jsweather.jsweather_getall())


def main() -> None:
    token = os.environ.get("TG_TOKEN")
    try:
        if not token:
            with open("tg_token.txt", "r") as file:
                token = file.read().strip()
    except FileNotFoundError:
        logging.error("tg_token.txt not found")
        exit(1)
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("get", get_handler))
    application.add_handler(CommandHandler("jsweather", jsweather_handler))
    application.run_polling()


if __name__ == "__main__":
    main()
