from telegram import Update

from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import CallbackContext
from telegram.ext import ConversationHandler
 
from db import Db 

db = Db('test')

EXERCISE_NAME, WEIGTH, REP  = range(3)

def start (update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Введите название упражнения')

    return EXERCISE_NAME

def exercise_name(update: Update, context: CallbackContext) -> int:
    text = update.message.text

    db.create_field()
    db.save_name(text)

    update.message.reply_text('Введите вес снаряда')

    return WEIGTH

def weight(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    db.save_weight(text)

    update.message.reply_text('Введите количестов повторений')

    return REP

def rep(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    db.save_rep(text)

    update.message.reply_text('Повторение было учтено\nВведите название упражнения')

    return EXERCISE_NAME

def canel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Тренеровка завершена')

    return ConversationHandler.END
 

def main ():
    updater = Updater(
        token='1422044333:AAF6NYIjczwBBPApDAioqbXmR9ydSh6HvHw'
    )

    conversation = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            EXERCISE_NAME: [MessageHandler(Filters.regex('^\w+$'), exercise_name)],
            WEIGTH: [MessageHandler(Filters.regex('^\d+$'), weight)],
            REP: [MessageHandler(Filters.regex('^\d+$'), rep)]
        },
        fallbacks=[CommandHandler('cancel', canel)]
    )

    dispatcher = updater.dispatcher

    dispatcher.add_handler(conversation)

    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()