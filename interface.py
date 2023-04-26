import telebot
import main as GAME


speech = [
    """
    Это простой бот для игры в сапера.
    Используйте:
    /help - для помощи
    /play - для игры
    """,
    """
    Инструкция к игре.
    Здесь все предельно просто: При вводе команды /play бот создаст вам игру. 
    Размер игрового поля - 10х10, количество мин на поле - 7шт. 
    После начала игры бот будет запрашивать координаты в формате "x y", например: 1 1, 8 4, и так далее.
    Координаты - целые числа от 1 до 10.
    В будущем бот будет дорабатываться
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
    if chat_id in users:
        bot.send_message(chat_id, "Игра уже начата")
    else:
        game = GAME.GamePole()
        users[chat_id] = game
        bot.send_message(chat_id,
            f"```\n{users[chat_id].show()}\n```\nВведите координаты ячейки",
            parse_mode="Markdown")

@bot.message_handler(commands=["stop"])
def stop(message):
    chat_id = message.chat.id
    if chat_id not in users:
        bot.send_message(chat_id, "Игра не начата")
    else:
        bot.send_message(chat_id, "Вы хотите закончить игру?")
        bot.register_next_step_handler(message, lambda msg: finisher(msg))
def finisher(msg):
    chat_id = msg.chat.id
    if msg.text.lower()[:3:] in ["да", "ага", "ну", "+", "yes", "даа", "есс"]:
        bot.send_message(chat_id,
            f"```\n{users[chat_id].gameover()}\n```\nИгра окончена",
            parse_mode="Markdown")
        users.pop(chat_id)

@bot.message_handler(func=lambda message: True)
def msger(message):
    chat_id = message.chat.id
    if chat_id not in users:
        bot.reply_to(message, "Держите в курсе.")
    else:
        try:
            row, clmn = map(int, message.text.split())
            rs = users[chat_id].open(row-1, clmn-1)
            if "уже открыта" in rs[0]:
                bot.send_message(chat_id, "Введите координаты неоткрытой ячейки")
            elif "подорвались" in rs[0]:
                bot.send_message(chat_id,
                    f"```\n{users[chat_id].gameover()}\n```\nВы подорвались на мине.\nИгра окончена",
                    parse_mode="Markdown")
                users.pop(chat_id)
            elif "все ячейки" in rs[0]:
                bot.send_message(chat_id,
                    f"```\n{users[chat_id].gameover()}\n```\nВы открыли все ячейки.\nИгра окончена",
                    parse_mode="Markdown")
                users.pop(chat_id)
            else:
                bot.send_message(chat_id,
                    f"```\n{users[chat_id].show()}\n```\nВведите координаты ячейки",
                    parse_mode="Markdown")
        except ValueError:
            bot.send_message(chat_id, "Соблюдайте формат!")
        except IndexError:
            bot.send_message(chat_id, "Требуется ввести правильные координаты")

bot.polling()