import aiohttp
import logging
from datetime import datetime
import os
from config.config import API_BASE_URL

API_BASE_URL = API_BASE_URL


async def create_worker(
        telegram_id: int,
        username: str = "",
        first_name: str = "",
        last_name: str = "",
        language: str = "uz"
):
    url = f"{API_BASE_URL}/workers/"

    payload = {
        "telegram_id": telegram_id,
        "username": '@' + username or "",
        "first_name": first_name or "",
        "last_name": last_name or "",
        "language": language or "uz"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                response_text = await response.text()
                return response.status, response_text

    except aiohttp.ClientError as e:
        logging.error(f"HTTP so‘rovda xatolik: {e}")
        return 0, None

    except Exception as e:
        logging.exception(f"Kutilmagan xatolik: {e}")
        return 0, None


async def user_exists(telegram_id: int) -> bool:
    url = f"{API_BASE_URL}/workers/{telegram_id}/"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return True  # User mavjud
                elif response.status == 404:
                    return False  # User topilmadi
                else:
                    logging.warning(f"👀 Noma'lum holat: {response.status}")
                    return False
    except aiohttp.ClientError as e:
        logging.error(f"🌐 HTTP so‘rov xatosi: {e}")
        return False
    except Exception as e:
        logging.exception(f"❌ Kutilmagan xatolik: {e}")
        return False


async def get_user_language_by_user_id(user_id: int) -> str:
    url = f"{API_BASE_URL}/workers/{user_id}/"
    headers = {
        'Content-Type': 'application/json',
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                print("Status:", response.status)

                if response.status == 200:
                    data = await response.json()
                    return data.get("language", "Til topilmadi")

                elif response.status == 404:
                    return "❌ Foydalanuvchi topilmadi"

                else:
                    text = await response.text()
                    print("Javob matni:", text)
                    return f"⚠️ Xatolik: status {response.status}"

    except aiohttp.ContentTypeError:
        return "⚠️ Noto‘g‘ri javob formati (JSON emas)"
    except Exception as e:
        return f"❌ Kutilmagan xatolik: {str(e)}"


async def get_location_name(latitude: float, longitude: float) -> str:
    url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json"

    headers = {
        "User-Agent": "TelegramBot/1.0"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("display_name", "Noma'lum joy")
                else:
                    return "Joy nomi aniqlanmadi"
    except Exception as e:
        print(f"Xatolik: {e}")
        return "Xatolik yuz berdi"


async def has_checked_in_today(telegram_id: int) -> bool:
    url = f"{API_BASE_URL}/workers/{telegram_id}/"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    checkins = data.get("checkins", [])
                    today = datetime.now().date()

                    for checkin in checkins:
                        time_str = checkin.get("check_in_time")
                        checkin_date = datetime.fromisoformat(time_str).date()
                        if checkin_date == today:
                            return True
                    return False
                else:
                    return False
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        return False


async def create_checkin(data: dict):
    """
    data['video_file'] — ochiq fayl obyekti (rb mode)
    """
    url = f"{API_BASE_URL}/checkins/"
    headers = {"Accept": "application/json"}

    try:
        async with aiohttp.ClientSession() as session:
            form = aiohttp.FormData()
            form.add_field("telegram_id", str(data["telegram_id"]))
            form.add_field("latitude", str(data["latitude"]))
            form.add_field("longitude", str(data["longitude"]))
            form.add_field("location_name", data["location_name"])
            form.add_field(
                'video',  # video_file emas, video nomi bilan
                data['video_file'],  # bu esa ochiq fayl obyekti
                filename='video.mp4',
                content_type='video/mp4'
            )

            async with session.post(url, data=form, headers=headers) as resp:
                text = await resp.text()
                if resp.status in (200, 201):
                    logging.info(f"✅ Created checkin (status={resp.status})")
                else:
                    logging.warning(f"⚠️ Checkin failed (status={resp.status}): {text}")
                return resp.status, text

    except Exception as e:
        logging.exception("❌ create_checkin exception")
        return 0, str(e)


async def download_file_from_telegram(bot_token, file_id, save_path):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}"
        try:
            async with session.get(url) as resp:
                if resp.status != 200:
                    logging.error(f"❌ Telegram API'dan fayl ma'lumotlarini olishda xato: {resp.status}")
                    return False
                data = await resp.json()
                if not data.get('ok'):
                    logging.error(f"❌ Telegram API xatosi: {data.get('description')}")
                    return False

                file_path = data['result']['file_path']
                download_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
                async with session.get(download_url) as r:
                    if r.status != 200:
                        logging.error(f"❌ Faylni yuklab olishda xato: {r.status}")
                        return False

                    # Faylni saqlashdan oldin papkani yaratish
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    with open(save_path, 'wb') as f:
                        f.write(await r.read())
                    return True
        except Exception as e:
            logging.error(f"❌ Faylni yuklab olishda xatolik: {e}")
            return False
