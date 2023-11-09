import aiohttp
import asyncio
import logging
import sys
import json
from os import getenv
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hbold

stickerYes = 'CAACAgIAAxkBAAEQJFtlTQMus5jI-9jWcWZNdU_g0oQEhwACAwAD9FX_GIz_XR9Q3aEAATME'
stickerNo = 'CAACAgIAAxkBAAEQJGFlTQNmx9hjgsdL8JENeOBTgH2J_wACAgAD9FX_GGx_83tzh9kbMwQ'

apiUrl = f'http://sanic:{getenv("SANIC_PORT")}/api/'
dp = Dispatcher()
variants = []


async def get_word():
    global apiUrl

    async with aiohttp.ClientSession() as session:
        async with session.get(f'{apiUrl}word/') as response:
            return await response.text()


async def check_word(uuid: str, translation: str):
    global apiUrl

    async with aiohttp.ClientSession() as session:
        async with session.post(f'{apiUrl}check/', json={
            'uuid': uuid,
            'translation': translation
        }) as response:
            return await response.text()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [types.KeyboardButton(text="Поехали!")]
        ]
    )

    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data.startswith('choose_variant:'))
async def choose_variant(callback: types.CallbackQuery):
    global variants, stickerYes, stickerNo

    data = callback.data.split(':')
    uuid = data[1]
    translationNumber = int(data[2])
    translation = variants[translationNumber]

    check_json = await check_word(uuid, translation)
    result = json.loads(check_json)['result']
    sticker = stickerYes if result else stickerNo

    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [types.KeyboardButton(text="Следующее слово!")]
        ]
    )

    await callback.message.answer_sticker(sticker, reply_markup=keyboard)


@dp.message()
async def echo_handler(message: types.Message) -> None:
    global variants

    try:
        word_json = await get_word()
        word_data = json.loads(word_json)['data']
        uuid = word_data['uuid']
        word = word_data['word']
        variants = word_data['variants']
        builder = InlineKeyboardBuilder()
        for (num, variant) in enumerate(variants):
            builder.row(types.InlineKeyboardButton(
                text=variant,
                callback_data=f"choose_variant:{uuid}:{num}"
            ))

        await message.answer(word, reply_markup=builder.as_markup())

    except TypeError:
        await message.answer("Что-то пошло не так..")


async def main() -> None:
    bot = Bot(getenv("TGBOT_TOKEN"), parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
