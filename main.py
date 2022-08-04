from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, BotCommand, KeyboardButton, ChatAction
from main_file import inline_handler, message_handler, info_command, user_command

from DatabaseDB import weatherdb

db = weatherdb.weather_db
TOKEN = weatherdb.TOKEN
ADMIN_ID = weatherdb.ADMIN_ID

counter = 0

def start_command(update, context):  # botni ishga tushrish funksiyasi
    global counter
    message = update.message.text
    update.message.reply_chat_action(action=ChatAction.TYPING)

    user = update.message.from_user
    db_user = db.get_user_by_chat_id(user.id)

    if not db_user:
        db.create_user(user.id)
        buttons = [
            [KeyboardButton(text="Viloyatlar")],
        ]
        update.message.reply_text(
            text=f"Salom {update.message.from_user.first_name}, Ob-havo ma'lumotlari bilan tanishing!\n"
                 "Buning uchun viloyatlar bo'limiga o'ting 👇",
            reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        )

        if user.id:
            counter += 1
            context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"👤 New user:\n\n"
                     f"First name: {user['first_name']}\n"
                     f"Last name: {user['last_name']}\n"
                     f"Username: {user['username']}\n"
                     f"ID: {user['id']}\n"
                     f"Bot: {user['is_bot']}\n\n"
                     f"👤 Botda ro'yxatdan o'tgan odamlar {counter} ta bo'ldi."
            )
    else:
        user_command(update, context)

    # command_list = [
    #     BotCommand(command="start", description="botni ishga tushirish"),
    #     BotCommand(command="info", description="bot haqida ma'lumot"),
    # ]
    # context.bot.set_my_commands(commands=command_list)


def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("info", info_command))
    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    dispatcher.add_handler(CallbackQueryHandler(inline_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
