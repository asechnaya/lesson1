from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import logging
import ephem
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


class FilterCalc(BaseFilter):
    def filter(self, message):
        return bool(message.text or (message.text.startswith('/') and message.text.length == 1))

filter_calc = FilterCalc()

class FilterWordCalc(BaseFilter):
    def filter(self, message):
        return bool(message.text and message.text.startswith('сколько будет'))

filter_word_calc = FilterWordCalc()

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
    dp.add_handler(MessageHandler(filter_word_calc, word_calc))
    dp.add_handler(MessageHandler(filter_calc, talk_to_me))

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

def whatnumber(number, nsign):
    allsign = number
    for key, value in nsign.items():
        allsign = allsign.replace(key,value)

    allsign += " ="
    return allsign.replace(" ", "")

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
                sign_and_index = getSignAndIndex(cstring)
                print(sign_and_index)
                sign = sign_and_index["sign"]
                index = sign_and_index["index"]

                num1 = float(cstring[:index]) #берет все то, что до индекса (не включительно) 
                                              #https://stackoverflow.com/questions/663171/is-there-a-way-to-substring-a-string-in-python

                num2 = float(cstring[index + 1: -1]) #-1  --убрать равно 
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

def getSignAndIndex(input):
    print(input)
    sign = "+"
    index = -1;

    index = input.find(sign)
    if (index != -1):
        return {"sign":sign, "index": index}

    sign = "-"
    index = input.find(sign)
    if (index != -1):
        return {"sign":sign, "index": index}

    sign = "/"
    index = input.find(sign)
    if (index != -1):
        return {"sign":sign, "index": index}

    sign = "*"
    index = input.find(sign)
    if (index != -1):
        return {"sign":sign, "index": index}

def calculator(bot, update):
    text = 'Вызван /calc' 
    user_text = update.message.text
    print(user_text)
    calcu = calc(user_text)
    update.message.reply_text(calcu)
    
def word_calc(bot, update):  
    text = 'Вызван /wordcalc' 
    user_text = update.message.text
    user_text=user_text.replace("сколько будет","").strip()
    print("111 --"+user_text)
    wnumbers = {
    'один': "1",
    'два': "2",
    'три': "3",
    'четыре': "4",
    'пять': "5",
    'шесть': "6",
    'семь': "7",
    'восемь': '8',
    'девять': '9',
    'плюс': '+',
    'минус': '-',
    'умножить на': '*',
    ' и ': '.',
    'разделить на': '/'}
    word_numbers=whatnumber(user_text, wnumbers)
    print('замена', word_numbers) 
    wn = calc(word_numbers)
    #word_numbers=word_numbers.append("=") 
    if (wn !=0):
        update.message.reply_text(wn)
    else:
        update.message.reply_text('error')    
    

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
    print(keyc_text)
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