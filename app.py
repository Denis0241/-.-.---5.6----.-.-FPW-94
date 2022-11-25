import telebot
from config1 import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Приветствую\nДля начала работы введите команду в следующем формате: \n<имя валюты> \
<в какую валюту перевести><количество переводимой валюты>\n(Пример: рубль доллар 1; доллар евро 1)\nУвидеть список \
доступных валют можно с помощью команды: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) > 3:
            raise APIException("Слишком много параметров")
        if len(values) < 3:
            raise APIException("Слишком мало параметров")

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f"Цена {amount} {quote} в {base} равна - {total_base} {base}"
        bot.send_message(message.chat.id, text)


bot.polling()