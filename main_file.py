from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, BotCommand, KeyboardButton, ChatAction, ReplyKeyboardRemove, \
    InlineKeyboardButton, InlineKeyboardMarkup

# Ob-havo qismi
import requests
import datetime
from bs4 import BeautifulSoup as BS

def info_command(update, context):
    update.message.reply_text(text="Ushbu bot sizga ob-havo haqida ma'lumot beradi!")

def user_command(update, context):
    message = update.message.text
    update.message.reply_chat_action(action=ChatAction.TYPING)
    buttons = [
        [KeyboardButton(text="Viloyatlar")],
    ]
    update.message.reply_text(
        text=f"{update.message.from_user.first_name}, viloyatlar bo'limiga o'ting 👇\n",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
    )

def message_handler(update, context):
    message = update.message.text

    if message == "Viloyatlar":
        buttons = [
            [KeyboardButton(text="Qashqadaryo")],
            [KeyboardButton(text="Samarqand"), KeyboardButton(text="Jizzax")],
            [KeyboardButton(text="Buxoro"), KeyboardButton(text="Surxondaryo")],
            [KeyboardButton(text="Toshkent"), KeyboardButton(text="Sirdaryo")],
            [KeyboardButton(text="Farg'ona"), KeyboardButton(text="Andijon")],
            [KeyboardButton(text="Namangan"), KeyboardButton(text="Navoiy")],
            [KeyboardButton(text="Qoraqalpog'iston"), KeyboardButton(text="Xorazm")],
            [KeyboardButton(text="🔙 Ortga")],
        ]
        update.message.reply_chat_action(action=ChatAction.TYPING)
        update.message.reply_text(
            text="Viloyatlardan birini tanlang 👉",
            reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        )

    viloyat = ["Qashqadaryo", "Samarqand", "Buxoro", "Toshkent", "Surxondaryo", "Jizzax", "Farg'ona", "Namangan",
               "Sirdaryo", "Andijon", "Navoiy", "Xorazm", "Qoraqalpog'iston"]

    vil = ["карши", "самарканд", "бухара", "ташкент", "термез", "джизак", "фергана", "наманган", "сырдарья",
           "андижан", "навои", "ургенч", "нукус"]

    date = datetime.datetime.now()
    now = date.strftime("%Y-%m-%d %H:%M")
    date_add = datetime.datetime(5, 00, 00)

    for i in range(len(viloyat)):
        button = [[InlineKeyboardButton(text="Viloyatlar 👉", callback_data="viloyat")],
                 [InlineKeyboardButton(text="Kanalga a'zo bo'ling 😊", url="https://t.me/eralidev_blog")],]
        if viloyat[i] == message:
            region = requests.get(f'https://sinoptik.ua/погода-{vil[i]}')
            html_t = BS(region.content, 'html.parser')

            for el in html_t.select('#content'):
                min = el.select('.temperature .min')[0].text
                max = el.select('.temperature .max')[0].text
                t_min = min[4:]
                t_max = max[5:]

            update.message.reply_chat_action(action=ChatAction.TYPING)
            msg = update.message.reply_text(
                text="🕔",
                reply_markup=ReplyKeyboardRemove()
            )
            context.bot.delete_message(chat_id=update.message.chat_id, message_id=msg.message_id)
            update.message.reply_photo(
                photo="https://www.unews.uz/uploads/05-2021/ICqHlPPzsxgAmOCBbVaAp1INUMhSs8CB0gR8kkIb.jpeg",
                caption=f"✅ {viloyat[i]} viloyati uchun ob-havo ma'lumoti:\n\n"
                        f"⛅ Past harorat: {t_min}\n"
                        f"🌞 Yuqori harorat: {t_max}\n"
                        f"⏰ Vaqt: {now+date_add}",
                reply_markup=InlineKeyboardMarkup(button)
            )

    if message == "🔙 Ortga":
        message = update.message.text
        buttons = [
            [KeyboardButton(text="Viloyatlar")],
        ]
        update.message.reply_text(
            text="Viloyatlar bo'limiga o'ting 👇",
            reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        )


def inline_handler(update, context):
    query = update.callback_query
    if query.data == "viloyat":
        buttons = [
            [KeyboardButton(text="Qashqadaryo")],
            [KeyboardButton(text="Samarqand"), KeyboardButton(text="Jizzax")],
            [KeyboardButton(text="Buxoro"), KeyboardButton(text="Surxondaryo")],
            [KeyboardButton(text="Toshkent"), KeyboardButton(text="Sirdaryo")],
            [KeyboardButton(text="Farg'ona"), KeyboardButton(text="Andijon")],
            [KeyboardButton(text="Namangan"), KeyboardButton(text="Navoiy")],
            [KeyboardButton(text="Qoraqalpog'iston"), KeyboardButton(text="Xorazm")],
            [KeyboardButton(text="🔙 Ortga")],
        ]

        context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        query.message.reply_text(
            text="Viloyatlardan birini tanlang 👉",
            reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        )
