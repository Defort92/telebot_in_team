from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from collections import deque
from json import dump, load

from config import TOKEN, DATABASE
from messages_text import *
from work_with_picture import make_picture

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
companions = deque()

with open(DATABASE) as file:
    chat_rooms = load(file)

old_id = []
for user in list(chat_rooms.keys()):
    chat_rooms[int(user)] = chat_rooms[user]
    old_id.append(user)

for id_ in old_id:
    chat_rooms.pop(id_)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(WELCOME)


@dp.message_handler(commands=['find_companion'])
async def process_find_command(message: types.Message):
    user_id = message.from_user.id

    if user_id in chat_rooms:
        await message.reply(HAVE_COMPANION_YET)
        return

    # Если нет собеседников ожидающих партнера или там лежит наш же айдишник
    if len(companions) == 0 or companions[0] == user_id:
        answer = WAIT_FOR_COMPANION
        companions.append(user_id)  # Добавили в очередь пользователя, который ищет собеседника
    else:
        answer = HAVE_COMPANION
        companion = companions.pop()  # Достаем собеседника из очереди
        chat_rooms[user_id] = companion  # Создаем пару айдишник пользователя: его себеседник
        chat_rooms[companion] = user_id  # И наоборот
        with open(DATABASE, "w") as file_:
            dump(chat_rooms, file_)
        await bot.send_message(companion, HAVE_COMPANION)

    await message.reply(answer)


@dp.message_handler(commands=['stop_communication'])
async def process_stop_command(message: types.Message):
    user_id = message.from_user.id
    if user_id not in chat_rooms:
        await message.reply(NO_COMPANION_YET)
    else:
        await bot.send_message(chat_rooms[user_id], STOP_COM_FOR_COMPANION)
        await bot.send_message(user_id, STOP_COM_FOR_ME)
        chat_rooms.pop(chat_rooms[user_id])
        chat_rooms.pop(user_id)

        with open(DATABASE, "w") as file_:
            dump(chat_rooms, file_)


@dp.message_handler(commands=['speak_by_picture'])
async def process_picture_command(message: types.Message):
    user_id = message.from_user.id
    if user_id not in chat_rooms:
        await message.reply(NO_COMPANION)
        return

    args = message.get_args().split()
    if len(args) < 2:
        await message.reply(INCORRECT_COMMAND_PICTURE)
        return
    link = args[0]
    text = ' '.join(args[1:])
    picture, result = make_picture(link, text)
    if picture is None:
        await message.reply(result)
    else:
        await message.reply(PICTURE_DONE)
        await bot.send_photo(chat_id=chat_rooms[message.from_user.id], photo=picture)


@dp.message_handler()
async def process_message(message: types.Message):
    user_id = message.from_user.id
    if user_id in chat_rooms:
        await bot.send_message(chat_rooms[user_id], message.text)
    else:
        await message.reply(NO_COMPANION)


if __name__ == '__main__':
    executor.start_polling(dp)
