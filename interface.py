speech = [
    """
    Это простой бот для игры в сапера.
    Используйте:
    /help - для помощи
    /play - для игры
    """,
    """
    Тут будет помощь. Потом.
    """,
    """
    Сыграем?
    """,
    """
    Прекратили играть
    """
]


import telebot

token = open("token.txt").read()

bot = telebot.TeleBot(token)
fl_play:bool = False

@bot.message_handler(commands=["start", "начало", "начинай", "стартуй"])
def start(message):
    bot.send_message(message.chat.id, speech[0])

@bot.message_handler(commands=["help", "помоги"])
def help(message):
    bot.send_message(message.chat.id, speech[1])

@bot.message_handler(commands=["play"])
def play(message):
    global fl_play
    fl_play = True
    bot.send_message(message.chat.id, speech[2])

@bot.message_handler(commands=["stop"])
def stop(message):
    global fl_play
    fl_play = False

@bot.message_handler(func=lambda message: True)
def msger(message):
    if fl_play:
        bot.send_message(message.chat.id, "Игра сейчас начата")
    else:
        bot.send_message(message.chat.id, "Игра сейчас не начата")


bot.polling()