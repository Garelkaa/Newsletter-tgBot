import imp
import logging
from aiogram import Bot, Dispatcher, executor,types
from db import Database
logging.basicConfig(level=logging.INFO)

bot = Bot(token='' #bot token) 
dp = Dispatcher(bot)
db = Database('database.db')

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == 'private':
            if not db.user_exists(message.from_user.id):
                db.add_user(message.from_user.id)
            await bot.send_message(message.from_user.id, "Добро пожаловать!") 

@dp.message_handler(commands=['newsletter'])
async def sendall(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id == 626452615:
            text = message.text[12:]
            users = db.get_users()
            for row in users:
                try:
                    await bot.send_message(row[0], text)
                    if int(row[1]) != 1:
                        db.set_active(row[0], 1)
                except:
                    db.set_active(row[0], 0)
            await bot.send_message(message.from_user.id, "Успех")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates= True)
