
import os

from telebot import TeleBot
import api
from binance import error
import database
from models import User
TOKEN = os.environ['TELEGRAM_TOKEN']
bot = TeleBot(TOKEN)

users = {}


@bot.message_handler(commands=["start"])
def say_hello(message):
    uid = message.from_user.id
    print(uid)
    bot.send_message(uid, "Hello new user!")
    bot.send_message(uid, "your available commands\n -> /register"  )


@bot.message_handler(commands=["info"])
def get_info(message):
    uid = message.from_user.id
    result = database.get_user(uid)
    if result is not None:
        bot.send_message(uid, f"Hi, your info:\nID=> {result[0]}\nAPI_KEY=> {result[1]}\nSECRET_KEY=> {result[2]}")

    else:
        bot.send_message(uid, "\n Register first", )

@bot.message_handler(commands=["reg", "register", "r"])
def register(message):
    uid = message.from_user.id

    if database.get_user(uid) is None:
        users[uid] = User(uid)
        bot.send_message(uid, "Enter your api_key:")
        bot.register_next_step_handler(message, enter_api_key)
    else:
        bot.send_message(uid, "You already registered!")
        bot.send_message(uid, "your available commands\n -> /info\n -> /mypositions")

def enter_api_key(message):
    uid = message.from_user.id
    users[uid].api_key = message.text
    bot.send_message(uid, "Enter your secret_key:")
    bot.register_next_step_handler(message, enter_secret_key)


def enter_secret_key(message):
    uid = message.from_user.id
    users[uid].secret_key = message.text
    try:
        api.connection(users[uid].api_key,users[uid].secret_key).account()
    except error.ClientError:
        bot.send_message(uid, 'Your keys inavaild, Try again :) ')
    else:
        users[uid].save_to_database()
        bot.send_message(uid, "Done!")
        bot.send_message(uid, "your available commands\n -> /info\n -> /mypositions")


@bot.message_handler(commands=["mypositions"])
def check_position(message):
    uid = message.from_user.id
    user_info = database.get_user(uid)
    print('ok')
    con = api.connection(user_info[1], user_info[2])
    # open orders

    all_coins = con.get_position_risk(symbol = 'BTCUSDT')
    print(all_coins)
    msg = ''

    for order in all_coins:
        if float(order['positionAmt'])== 0 :
            msg += f'Instrument: {order["symbol"]}\n' \
                   f'Your profit: {order["unRealizedProfit"]}\n' \
                   f'Liquidation Price: {order["liquidationPrice"]}\n' \
                   f'Entry position price: {order["entryPrice"]}'
    bot.send_message(uid, msg)
    print(msg)


bot.infinity_polling()
# ( )