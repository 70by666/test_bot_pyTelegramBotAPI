import telebot
import os
import random
from telebot import types
from dotenv import load_dotenv, find_dotenv
from parvk import get_wall_posts
from mee import delete1


load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.getenv("TOKEN"))
white_users = [1047484838]


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    help = types.KeyboardButton("/help")
    markup.add(help)
    mess = f"Салам, {message.from_user.first_name}"
    bot.send_message(message.chat.id, mess)
    st = open("sticker.webp", "rb")
    bot.send_sticker(message.chat.id, st, reply_markup=markup)


@bot.message_handler(commands=["mem"])
def mem(message):
    try:
        img_list = os.listdir("data/memi/")
        img_path = random.choice(img_list)
        bot.send_photo(
            message.chat.id, photo=open(
                f"data/memi/{img_path}", "rb"))
    except Exception:
        bot.send_message(message.chat.id, "файлы не загружены")


@bot.message_handler(commands=["cat"])
def mem(message):
    try:
        img_list = os.listdir("data/cats/")
        img_path = random.choice(img_list)
        bot.send_photo(
            message.chat.id, photo=open(
                f"data/cats/{img_path}", "rb"))
    except Exception:
        bot.send_message(message.chat.id, "файлы не загружены")


@bot.message_handler(commands=["video"])
def mem(message):
    try:
        v_list = os.listdir("data/video/")
        v_path = random.choice(v_list)
        bot.send_video(
            message.chat.id, video=open(
                f"data/video/{v_path}", "rb"))
    except Exception:
        bot.send_message(message.chat.id, "файлы не загружены")


@bot.message_handler(commands=["update"])
def update(message):
    if message.from_user.id in white_users:
        bot.send_message(
            message.chat.id,
            "отправь мне короткий адрес сообщества(пример vk.com/group_name, мне нужно только group_name):")
        bot.register_next_step_handler(message, name)
    else:
        bot.send_message(message.chat.id, "нет доступа")


def name(message):
    if not message.text.isdigit():
        bot.send_message(
            message.chat.id,
            f"проверяю {message.text}, ожидайте ответа")
        o = get_wall_posts(message.text)
        bot.send_message(message.chat.id, f"{o}")
    else:
        bot.send_message(message.chat.id, "вы ввели что-то не так")
        bot.register_next_step_handler(message, name)


@bot.message_handler(commands=["delete"])
def delete(message):
    if message.from_user.id in white_users:
        bot.send_message(message.chat.id, "начинаю удалять")
        delete1()
        bot.send_message(
            message.chat.id,
            "файлы удалены, чтобы загрузить новые: /update")
    else:
        bot.send_message(message.chat.id, "нет доступа")


@bot.message_handler(commands=["help"])
def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mem = types.KeyboardButton("/mem")
    start = types.KeyboardButton("/start")
    weather = types.KeyboardButton("/weather")
    update = types.KeyboardButton("/update")
    mem2 = types.KeyboardButton("/mem2")
    cat = types.KeyboardButton("/cat")
    cat2 = types.KeyboardButton("/cat2")
    video = types.KeyboardButton("/video")
    delete = types.KeyboardButton("/delete")
    markup.add(start, mem, cat, video, update, delete)  # weather, mem2, cat2)
    bot.send_message(
        message.chat.id,
        "список доступный команд\n/mem - случайный мем с котом\n/cat - случайная картинка с котом\n"
        "/video - случайное видео\n/update - обновить мемы(добавить новые)\n/delete удалить все загруженные картинки и видео\n"
        "/weather - погода(не работает)\n/mem2 - мемы по порядку(не работает)\n/cat2 - картинки с котом по порядку(не работает)",
        reply_markup=markup)


@bot.message_handler()
def get_user_text(message):
    if message.text == "ты нефор":
        bot.send_message(message.chat.id, "Такие вещи не говори, да!")
    elif message.text == "id" or message.text == "ид":
        bot.send_message(message.chat.id, f"Ладно ID: {message.from_user.id}")
    else:
        bot.send_message(
            message.chat.id,
            "чо, если хочешь кинуть мем на оценку, это должна быть картинка, логично же")


@bot.message_handler(content_types=["photo"])
def get_user_photo(message):
    o = random.randint(1, 5)
    if o < 3:
        bot.send_message(message.chat.id, f"Не розстраюйся! {o}/5")
        video = open("videoplayback.mp4", "rb")
        bot.send_video(message.chat.id, video)
        bot.send_message(
            message.chat.id,
            "мем отличный, просто я случайно выставляю оценки xd")
    elif o == 5:
        bot.send_message(message.chat.id, f"МЕМ СУПЕР, ОДИН ИЗ ЛУЧШИХ: {o}/5")
    else:
        bot.send_message(message.chat.id, f"мне нравится, хороший мем: {o}/5")


@bot.message_handler(content_types=["sticker"])
def get_user_sticker(message):
    bot.send_message(message.chat.id, "крутой стикер")


bot.polling(non_stop=True)
