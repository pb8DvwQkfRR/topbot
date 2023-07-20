import logging
import os

from telegram import Update, InputMediaPhoto
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes

import get_hitfm
import jsweather


async def get_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(get_hitfm.hitfm_geturl())


async def jsweather_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    weather_text, weather_postfix, weather_img_list = jsweather.jsweather_getall()
    media_group = []
    for i, image_url in enumerate(weather_img_list):
        caption = weather_text + weather_postfix if i == 0 else None
        media_group.append(
            InputMediaPhoto(
                media=image_url,
                caption=caption,
                parse_mode=ParseMode.HTML,
            )
        )
    await update.message.reply_media_group(media=media_group)


def main() -> None:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.ERROR)
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
