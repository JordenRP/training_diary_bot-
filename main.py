from telegram import Update
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove

from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import CallbackContext
from telegram.ext import ConversationHandler
 
from db import Db 

db = Db('test')

EXERCISE_NAME, WEIGTH, REP, NAME  = range(4)

def start_conversation (update: Update, context: CallbackContext) -> int:
    button = [[KeyboardButton('Заврешить тренеровку')]]

    update.message.reply_text(
        'Введите название упражнения', 
        reply_markup = ReplyKeyboardMarkup(button, resize_keyboard = True)
    )

    return EXERCISE_NAME

def exercise_name(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    button = [[KeyboardButton('Заврешить тренеровку')]]

    if(text != 'Повторить упражение'):
        db.create_field()   
        db.save_name(text)
        update.message.reply_text('Введите вес снаряда')
    else:
        print('ads')
        update.message.reply_text(
            'Введите вес снаряда',
            reply_markup = ReplyKeyboardMarkup(button, resize_keyboard=True)   
        )

    return WEIGTH

def weight(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    db.save_weight(text)

    update.message.reply_text('Введите количестов повторений')

    return REP

def rep(update: Update, context: CallbackContext) -> int:
    button = [
                [
                    KeyboardButton('Повторить упражение')
                ], 
                [
                    KeyboardButton('Следующее упражнение')
                ],
                [
                    KeyboardButton('Заврешить тренеровку')
                ] 
            ]

    text = update.message.text
    db.save_rep(text)

    update.message.reply_text(
        'Повторение было учтено', 
        reply_markup = ReplyKeyboardMarkup(button, resize_keyboard = True)
    )

    return EXERCISE_NAME

def cancel(update: Update, context: CallbackContext) -> int:
    button = [[KeyboardButton("Добавить упражнение")], [KeyboardButton("Начать тренеровку")]]

    update.message.reply_text(
        'Тренеровка завершена',
        reply_markup = ReplyKeyboardMarkup(button, resize_keyboard = True)
    )

    return ConversationHandler.END

def cancel_2(update: Update, context: CallbackContext) -> int:
    button = [[KeyboardButton("Добавить упражнение")], [KeyboardButton("Начать тренеровку")]]
    update.message.reply_text(
        'Начнем тренеровку', 
        reply_markup = ReplyKeyboardMarkup(button, resize_keyboard=True)
    )

    return ConversationHandler.END

def init_train(update: Update, context: CallbackContext):
    button = [[KeyboardButton("Добавить упражнение")], [KeyboardButton("Начать тренеровку")]]

    update.effective_message.reply_text(
        'Начнем тренеровку' ,
        reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True)
    )

def start_conversation_2(update: Update, context: CallbackContext):
    button = [[KeyboardButton("Вернутся в главное меню")]]

    update.message.reply_text(
        'Введите название упражнения',
        reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True)
    )

    return NAME

def name(update: Update, context: CallbackContext):
    print(update.message.text)
    
    update.message.reply_text(
        'Введите название упражнения',
    )

    return NAME

def repeat_exe(update: Update, context: CallbackContext):
    button = [[KeyboardButton('Завершить тренеровку')]]

    update.message.reply_text(
        'Введите вес снаряда',
        reply_markup = ReplyKeyboardMarkup(button, resize_keyboard=True)
    )

    return WEIGTH

def next_exe(update: Update, context: CallbackContext):
    button = [[KeyboardButton('Завершить тренеровку')]]

    update.message.reply_text(
        'Введите название упражнения',
        reply_markup = ReplyKeyboardMarkup(button, resize_keyboard=True)
    )

    return EXERCISE_NAME


def main ():
    updater = Updater(
        token='1422044333:AAF6NYIjczwBBPApDAioqbXmR9ydSh6HvHw'
    )

    conversation = ConversationHandler(
        entry_points=[MessageHandler(Filters.text('Начать тренеровку'),  start_conversation)],
        states={
            EXERCISE_NAME: [MessageHandler(Filters.regex('^\w+$'), exercise_name)],
            WEIGTH: [MessageHandler(Filters.regex('^\d+$'), weight)],
            REP: [MessageHandler(Filters.regex('^\d+$'), rep)]
        },
        fallbacks=[
                MessageHandler(Filters.text('Заврешить тренеровку'), cancel),
                MessageHandler(Filters.text('Повторить упражение'), repeat_exe),
                MessageHandler(Filters.text('Следующее упражнение'), next_exe),
            ]
    )

    conversation_2 = ConversationHandler(
        entry_points=[MessageHandler(Filters.text('Добавить упражнение'), start_conversation_2)],
        states={
            NAME: [MessageHandler(Filters.regex('^\w+$'), name)],
        },
        fallbacks=[MessageHandler(Filters.text('Вернутся в главное меню'), cancel_2)]
    )

    dispatcher = updater.dispatcher

    dispatcher.add_handler(conversation)
    dispatcher.add_handler(conversation_2)
    dispatcher.add_handler(CommandHandler('start', init_train))

    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()