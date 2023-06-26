from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes
import datetime
import httpx
import json
import os


def getdaid():
    url = "https://oma.ocard.co:456/device/auth"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Host": "oma.ocard.co:456",
        "User-Agent": "Hit Fm/1.11.35 (iPhone; iOS 17.0; Scale/3.00)",
        "Upload-Incomplete": "?0",
        "Upload-Draft-Interop-Version": "3",
    }

    data = {
        "app_id": "tw.com.olis.HitFM",
        "app_key": "bizr1ye6y1ybfjvw9n8q2fk5yf6yhc45",
        "app_secret": "v3w9enfcor03aw0jvk9xd72onmy4y3m5",
        "app_version": "1.11.35",
        "device_id": "",
        "device_name": "iPhone",
        "launch": "1",
        "os": "iOS",
        "os_version": "17.0",
        "platform": "mobile",
        "sdk_version": "1.0.0"
    }
    data = json.loads(httpx.post(url, headers=headers, data=data).text)
    if "data" in data and "daid" in data["data"]:
        return data["data"]["daid"]


def geturl():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    url = "https://oma.ocard.co:456/radio/basic_data"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Host": "oma.ocard.co:456",
        "User-Agent": "Hit Fm/1.11.35 (iPhone; iOS 17.0; Scale/3.00)",
        "Upload-Incomplete": "?0",
        "Upload-Draft-Interop-Version": "3",
        "token": "test"
    }

    data = {
        "daid": getdaid(),
        "update": current_time
    }

    data = json.loads(httpx.post(url, headers=headers, data=data).text)

    if "data" in data and "media" in data["data"]:
        media_sources = data["data"]["media"]
        source_urls = [source["source"] for source in media_sources]
        source_text = "\n\n".join(source_urls)
        return source_text
    else:
        return "data.media.source not found"


async def get_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(geturl())


def main() -> None:
    token = os.environ.get("TG_TOKEN")
    if not token:
        with open("tg_token.txt", "r") as file:
            token = file.read().strip()
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("get", get_handler))
    application.run_polling()


if __name__ == "__main__":
    main()
