import requests
import asyncio

FOLDER_ID = 111111 # Тут, номер вашей заявки
URL = f"https://passportzu.kdmid.ru/Petition/GetPetitionStatus?folderId={FOLDER_ID}"
CHECK_INTERVAL = 60  # 1 минута (86400 - 24ч)
LAST_STATUS = None


def get_status():
    r = requests.get(URL, timeout=10)
    r.raise_for_status()
    return r.json().get("StatusText")


async def check_status_loop(notify_callback):
    global LAST_STATUS
    while True:
        try:
            status = get_status()
            if LAST_STATUS is None:
                LAST_STATUS = status
            elif status != LAST_STATUS:
                if LAST_STATUS == "Статус заявления: дело в обработке.":
                    await notify_callback(f"⚡ Новый статус заявления: {status}")
                LAST_STATUS = status
        except Exception as e:
            print("Ошибка при проверке статуса:", e)

        await asyncio.sleep(CHECK_INTERVAL)
