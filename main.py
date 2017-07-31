import telebot
import constants
import sys
import time
import unicodedata
bot = telebot.TeleBot(constants.token)
#bot.send_message(265004005, "Hello, my dear friend!!!")
#last_updates = bot.get_updates()[-1]
#message_from_user = last_updates.message
#print(message_from_user)
print("Messages".center(50, '~'))

def log_info(message, answer):
    from _datetime import datetime
    print(datetime.now())
    str_message = "Message from {0} {1},id = {2},\nText of message: {3}".format(message.from_user.first_name,
                                                                             message.from_user.last_name,
                                                                             str(message.from_user.id), message.text)
    print(str_message)
    print("Text of answer: ", answer)
    print("~" * 50, "\n")

def download_doc(message, doc_name):
    directory = './documents'
    doc_name = str(doc_name)
    doc = open(directory + '/' + doc_name + '.pdf', 'rb')
    bot.send_chat_action(message.from_user.id, 'upload_document')
    bot.send_document(message.from_user.id, doc)
    log_info(message, 'Result: '+str(bot.send_chat_action(message.from_user.id, 'upload_document')))
    doc.close()

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/start', '/stop')
    user_markup.row('pictures', 'documents')
    user_markup.row('audio', 'stickers', 'location')
    bot.send_message(message.from_user.id, 'Welcome', reply_markup=user_markup)

@bot.message_handler(commands=['stop'])
def handle_stop(message):
    bot.send_message(message.from_user.id, 'Bye...', reply_markup=telebot.types.ReplyKeyboardRemove())

@bot.message_handler(content_types=['text'])
def handle_command(message):
    if message.text =="Привет" or  message.text =="Здравствуйте" or message.text =="Hello" or message.text =="Hi":
        answer = "Hello"
        bot.send_message(message.from_user.id, answer)
        log_info(message, answer)

    elif message.text =="Пока" or  message.text =="До свидания" or message.text =="Bye" or message.text =="See you again":
        answer = "See you again"
        bot.send_message(message.from_user.id, answer)
        log_info(message, answer)

    elif message.text == "documents":
        # all_documents_in_directory = os.listdir(directory)
        doc_user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        doc_user_markup.row('/start', '/stop')
        doc_user_markup.row('Booking')
        doc_user_markup.row('Train: Moscow to St. Petersburg', 'Train: St. Petersburg to Moscow')
        bot.send_message(message.from_user.id, 'Set of documents:', reply_markup=doc_user_markup)
        # for file in all_documents_in_directory:
    elif message.text == "Booking":
        download_doc(message, message.text)
    elif message.text == 'Train: Moscow to St. Petersburg':
        download_doc(message, message.text)
    elif message.text == 'Train: St. Petersburg to Moscow':
        download_doc(message, message.text)
    else:
        answer = "I don't understand what you wrote"+'\U0001F614'
        bot.send_message(message.from_user.id, answer)
        log_info(message, answer)


def main_loop():
    bot.polling(none_stop=True, interval=0)
    while 1:
        time.sleep(3)


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
sys.exit(0)
