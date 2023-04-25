import telebot


speech = [
    """
    Это простой бот для игры в сапера.
    Используйте:
    /help - для помощи
    /play - для игры
    """,
    """
    Тут будет инструкция к игре. Потом.
    """,
    """
    Начали играть
    """,
    """
    Прекратили играть
    """
]


token = open("token.txt").read()
bot = telebot.TeleBot(token)

users = {}

@bot.message_handler(commands=["start", "начало", "начинай", "стартуй"])
def start(message):
    bot.send_message(message.chat.id, speech[0])

@bot.message_handler(commands=["help", "помоги"])
def help(message):
    bot.send_message(message.chat.id, speech[1])

@bot.message_handler(commands=["play"])
def play(message):
    chat_id = message.chat.id
    users[chat_id] = True
    bot.send_message(chat_id, speech[2])

@bot.message_handler(commands=["stop"])
def stop(message):
    chat_id = message.chat.id
    users[chat_id] = False
    bot.send_message(message.chat.id, speech[3])

@bot.message_handler(func=lambda message: True)
def msger(message):
    chat_id = message.chat.id
    if chat_id not in users or not users[chat_id]:
        bot.send_message(chat_id, "Игра сейчас не начата")
    else:
        try:
            row, clmn = map(int, message.text.split())
            print(row, clmn)
        except ValueError:
            bot.send_message(chat_id, "Введите два числа (через пробел!!!)")
        



bot.polling()