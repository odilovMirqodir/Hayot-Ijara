async def commandstart_text(first_name: str) -> str:
    message = (
        f"*Assalomu alaykum, {first_name}!* 👋\n\n"
        "Tilni tanlang:\n\n"
        "🇺🇿 *O'zbek tili* — /uzbek\n"
        "🇷🇺 *Русский язык* — /russian\n\n"
        "_Iltimos, davom etish uchun tilni tanlang._"
    )
    return message


async def select_language(language):
    return "uz" if language == '🇺🇿 Uzbek' else 'ru'


async def registration_text(language: str) -> str:
    if language == "uz":
        return "Iltimos, ro'yxatdan o'tish uchun quyidagi tugmani bosing 👇"
    else:
        return "Пожалуйста, нажмите кнопку ниже, чтобы зарегистрироваться 👇"


async def location_text(language: str) -> str:
    if language == "uz":
        return "*📍 Iltimos, joylashuvingizni yuboring:*"
    else:
        return "*📍 Пожалуйста, отправьте вашу геолокацию:*"


async def video_text(language):
    if language == 'uz':
        return f"✅ Joylashuvingiz qabul qilindi.\n"f"Endi videoni yuboring."
    else:
        return f"✅ Ваше местоположение принято.\n"f"Теперь отправьте видео."


async def check_registration_text(language):
    if language == 'uz':
        return f"✅ Siz bugun ro'yxatdan o'tgansiz."
    else:
        return f"✅ Вы зарегистрировались сегодня."


async def no_video_text(language):
    if language == 'uz':
        return f"❗️Video yuborilmagan. Video yuboring"
    else:
        return f"❗️Видео не отправлено. Отправить видео"


async def video_greater_10(language):
    if language == 'uz':
        return f"⚠️ Video 10 soniyadan oshmasligi kerak. Qaytadan yuboring."
    else:
        return f"⚠️ Видео должно быть не длиннее 10 секунд. Пожалуйста, отправьте повторно."


async def video_error_text(language):
    if language == 'uz':
        return f"❌ Videoni yuklab olishda xatolik. Qaytadan urinib ko‘ring."
    else:
        return f"❌ Ошибка загрузки видео. Попробуйте еще раз."


async def checking_success_text(language):
    if language == 'uz':
        return f"✅ Check-in muvaffaqiyatli amalga oshirildi."
    else:
        return f"✅ Регистрация прошла успешно."

async def not_working_text(language):
    if language =="uz":
        return f"❌ Worker topilmadi. Ro‘yxatdan o‘ting."
    else:
        return f"❌ Работник не найден. Зарегистрируйтесь."

