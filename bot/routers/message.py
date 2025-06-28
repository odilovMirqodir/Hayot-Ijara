from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import CommandStart
from buttons.buttons import *
from text.text import *
from api.api import *
from states.state import Form
from aiogram import types
from config.config import TOKEN

message_router = Router(name=__name__)


@message_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_id = message.from_user.id
    user_exist = await user_exists(user_id)
    first_name = message.from_user.first_name or "Foydalanuvchi"
    language = await get_user_language_by_user_id(user_id)
    if user_exist:
        await message.answer(await registration_text(language), parse_mode='markdown',
                             reply_markup=await registration(language))
    else:
        await message.answer(
            await commandstart_text(first_name),
            reply_markup=await language_button(),
            parse_mode='Markdown'
        )


@message_router.message(lambda message: message.text in ['🇺🇿 Uzbek', '🇷🇺 Русский'])
async def language_reaction(message: Message):
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    user_id = message.from_user.id
    language_message_text = message.text
    return_language = await select_language(language_message_text)
    await create_worker(user_id, username, first_name, last_name, return_language)
    language = await get_user_language_by_user_id(user_id)
    await message.answer(await registration_text(language), parse_mode='markdown',
                         reply_markup=await registration(language))


@message_router.message(lambda message: message.text in ["Ro'yxatdan o'tish", 'Регистрация'])
async def registration_reaction(message: Message, state: FSMContext):
    user_id = message.from_user.id
    language = await get_user_language_by_user_id(user_id)
    if await has_checked_in_today(user_id):
        await message.answer(await check_registration_text(language))
        return

    language = await get_user_language_by_user_id(user_id)
    await message.answer(
        await location_text(language),
        reply_markup=await request_location_keyboard(language),
        parse_mode='markdown'
    )
    await state.set_state(Form.location_data)


@message_router.message(lambda message: message.location is not None)
async def handle_location(message: Message, state: FSMContext):
    user_id = message.from_user.id
    latitude = message.location.latitude
    longitude = message.location.longitude
    location_name = await get_location_name(latitude, longitude)
    language = await get_user_language_by_user_id(user_id)
    # ✅ Ma'lumotni dict holida saqlaymiz
    await state.update_data(location_data={
        "latitude": latitude,
        "longitude": longitude,
        "location_name": location_name
    })

    await message.answer(await video_text(language),
                         reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Form.video)


@message_router.message(Form.video)
async def handle_video(message: Message, state: FSMContext):
    user_id = message.from_user.id
    language = await get_user_language_by_user_id(user_id)
    data = await state.get_data()
    loc = data.get("location_data", {})
    latitude = loc.get("latitude")
    longitude = loc.get("longitude")
    location_name = loc.get("location_name", "Nomaʼlum")
    user_id = message.from_user.id

    # Video yoki video_note ni aniqlash
    video = message.video or message.video_note
    if not video:
        return await message.answer(await no_video_text(language))

    # Uzunlikni tekshirish
    if video.duration and video.duration > 10:
        return await message.answer(await video_greater_10(language))

    # Yuklab olish
    save_path = f"videos/{video.file_id}.mp4"
    success = await download_file_from_telegram(TOKEN, video.file_id, save_path)
    if not success:
        return await message.answer(await video_error_text(language))

    # Faylni ochib yuborish
    with open(save_path, "rb") as video_file:
        checkin_data = {
            "telegram_id": user_id,
            "latitude": latitude,
            "longitude": longitude,
            "location_name": location_name,
            "video_file": video_file
        }
        status, resp_text = await create_checkin(checkin_data)

    # Vaqtinchalik o‘chirish
    if os.path.exists(save_path):
        os.remove(save_path)

    # Javobni qayta ishlash
    if status in (200, 201):
        await message.answer(await checking_success_text(language), reply_markup=await registration(language))
    elif status == 404:
        await message.answer(await not_working_text(language))
    else:
        await message.answer(f"❌{status}")

    await state.clear()
