from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import logging
import ephem
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def main():
    updater = Updater("505329679:AAGXnoUdQrGbJpbGCRhAgNJ8Hc6FaHDu2HQ")
    

    dp = updater.dispatcher #принимает входящие сообщения и посылает их куда-то
    dp.add_handler(CommandHandler("start", greet_user))
    #Handler -- обработчик
    dp.add_handler(CommandHandler("planet", planet))
    #планеты ж
    dp.add_handler(CommandHandler("wordcount", word_count))
    #считает слова
    dp.add_handler(CommandHandler("calc", calculator))
    dp.add_handler(CommandHandler("keycalc", calc_keyboard))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    updater.start_polling() #отправь эти данные платформе телеграм
    updater.idle() #Жди, пока тебе телеграм что-то пришлет


def greet_user(bot, update):  #так прописано в пайтон телеграм боте: апдейт -- это "сложный словарь"
    text = 'Вызван /start'
    print(text)
    print(update)
    update.message.reply_text(text)

def what_planet(planet, coord):
    if planet in coord:
       return coord[planet]
    else:
        print('uuuu')

def wordcounts(mystring):
    mystring=mystring.replace("/wordcount","").strip() #стрип удаляет пробелы до и после строки
    if mystring.startswith('"') and mystring.endswith('"'):
        tokens = mystring.split()
        n_tokens = len(tokens)
    else:
        n_tokens = 0
    return n_tokens  

def calc(cstring):
    cstring=cstring.replace("/calc","").strip()
    if ' ' in cstring:
        return "Уберите пробелы, пожалуйста"
    else:
        if cstring.endswith('='):
            try:
                num1 = float(cstring[0])
                num2 = float(cstring[2])  
                print(cstring)
                if '*' in cstring:
                    ans=num1*num2
                elif '+'in cstring:
                    ans=num1+num2
                    print(ans)
                elif '-'in cstring:
                    ans=num1-num2
                elif '/'in cstring:
                    try:
                        ans=num1/num2
                    except ZeroDivisionError:
                        return "Не вводите ноль"
            except (TypeError, ValueError):
                return "вводите числа, все числа, только числа"
        else:
            return 'поставьте равно, пожалуйста'

    return ans


def calculator(bot, update):
    text = 'Вызван /calc' 
    user_text = update.message.text
    print(user_text)
    calcu = calc(user_text)
    update.message.reply_text(calcu)
    


def planet(bot, update):  
    text = 'Вызван /planet' 
    user_text = update.message.text
    print(user_text)
    planets = {
    'mars': ephem.Mars('2016/09/23'),
    'moon': ephem.Moon('2016/09/23'),
    'venus': ephem.Venus('2016/09/23')}
    user_text=user_text.split()
    search_planets=what_planet(user_text[1], planets)
    if search_planets:
        update.message.reply_text(ephem.constellation(search_planets))
    else:
        update.message.reply_text('error')
    
def word_count(bot, update):  
    text = 'Вызван /wordcount' 
    user_text = update.message.text
    print(user_text)
    print(update)
    user_text=user_text
    wc = wordcounts(user_text)
    if (wc !=0):
        update.message.reply_text(wc)
    else:
        update.message.reply_text('error')     
    
keyc_text=''
def talk_to_me(bot, update):
    global keyc_text
    user_text = update.message.text 
    keyc_text+=user_text
    if user_text == "=":
        res_calc = calc(keyc_text)
        keyc_text = ''
        update.message.reply_text(res_calc)

def calc_keyboard(bot, update):
    #reply_markup = telegram.ReplyKeyboardRemove()
    #bot.send_message(chat_id=chat_id, text="I'm back.", reply_markup=reply_markup)
    chat_id = update.message.chat_id
    custom_keyboard = [['1', '2', '3', '+'], 
                       ['4', '5', '6', '-'],
                       ['7', '8', '9', '/'],
                       ['=', '0', '.', '*']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id=chat_id, 
                     text="Custom Keyboard Test", 
                     reply_markup=reply_markup)






main()


#документация по python-telegram-bot (google it!)