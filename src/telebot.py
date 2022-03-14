from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Hello! Hello! Hello! \nps Annoy-o-Tron")


@dp.message_handler()
async def echo_message(message: types.Message):
    response = "Hello! Hello! Hello!"
    await bot.send_message(message.from_user.id, response, reply_to_message_id=message.message_id)


if __name__ == '__main__':
    executor.start_polling(dp)
