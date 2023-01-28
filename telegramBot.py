from telegram.ext import Updater, CommandHandler
def printId(update, context):
    print(update.message.chat.id)

if __name__ == '__main__':
    updater = Updater("5345322467:AAHxdqp9vzOUZU4CQCHFTfdnrgb0ucCb_Cs")
    # updater.bot.send_message(chat_id=1615520772, text="a")
    updater.dispatcher.add_handler(CommandHandler("start", printId))
    updater.start_polling()
def runBot():
    pass