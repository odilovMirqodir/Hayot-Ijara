from aiogram.types import InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton


async def language_button() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🇺🇿 Uzbek"),
            ],
            [
                KeyboardButton(text="🇷🇺 Русский"),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Tilni tanlang / Выберите язык"
    )
    return keyboard


async def registration(language: str) -> ReplyKeyboardMarkup:
    if language == 'uz':
        register_text = "Ro'yxatdan o'tish"
    else:
        register_text = "Регистрация"

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=register_text)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Tilni tanlang / Выберите язык"
    )
    return keyboard


async def request_location_keyboard(language: str) -> ReplyKeyboardMarkup:
    if language == "ru":
        button_text = "📍 Отправить локацию"
        placeholder = "Пожалуйста, отправьте вашу геолокацию"
    else:
        button_text = "📍 Joylashuvni yuborish"
        placeholder = "Iltimos, joylashuvingizni yuboring"

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=button_text, request_location=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=placeholder
    )
    return keyboard
