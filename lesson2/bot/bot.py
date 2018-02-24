from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import ephem
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def main():
    updater = Updater("505329679:AAHrar4IKIdK8co8j_dfH6QtFAECoP5VbIw")
    

    dp = updater.dispatcher #принимает входящие сообщения и посылает их куда-то
    dp.add_handler(CommandHandler("start", greet_user))
    #Handler -- обработчик
    dp.add_handler(CommandHandler("planet", planet))
    #планеты ж
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

def planet(bot, update):  #так прописано в пайтон телеграм боте: апдейт -- это "сложный словарь"
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
    



def talk_to_me(bot, update):
    user_text = update.message.text 
    print(user_text)
    print(bot)
    update.message.reply_text(user_text[::-1])

main()


#документация по python-telegram-bot (google it!)