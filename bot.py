import os
import asyncio
import requests
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

LOG_FILE = "checker.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, "a", "utf-8")
    ]
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TG_BOT_TOKEN")
CHAT_ID = int(os.getenv("TG_CHAT_ID"))

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

FOLDER_ID = "11111" # Тут, номер вашей заявки
URL = f"https://passportzu.kdmid.ru/Petition/GetPetitionStatus?folderId={FOLDER_ID}"

last_status = None

async def check_status():
    global last_status
    try:
        r = requests.get(URL, timeout=10)
        r.raise_for_status()

        data = r.json()
        status_text = data.get("StatusText", "").strip()

        logger.info(f"Текущий статус: {status_text}")

        if status_text and status_text != last_status:
            await bot.send_message(CHAT_ID, f"🔔 Новый статус: {status_text}")
            logger.info(f"Отправлено уведомление: {status_text}")
            last_status = status_text

    except Exception as e:
        logger.error(f"Ошибка запроса: {e}")

async def main():
    logger.info("Бот запущен и начал проверку...")
    while True:
        await check_status()
        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(main())
