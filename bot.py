import telebot
from config import keys, TOKEN, symbols
from extensions import API_GET, APIException


bot = telebot.TeleBot(TOKEN)

#приветствие
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате: \n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты> \n Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

#Доступные данные
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

# чтение запроса пользователя и конверт валют
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise APIException('Слишком много параметров.')
        if len(values) < 3:
            raise APIException('Недостаточно параметров.')

        quote, base, amount = values
        total_base = API_GET.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {symbols[keys[quote]]} ({quote}) в {base} - {total_base} {symbols[keys[base]]}'
        bot.send_message(message.chat.id, text)


bot.polling()
