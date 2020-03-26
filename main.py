from bot.bot import Bot
from bot.handler import MessageHandler, HelpCommandHandler, CommandHandler, Filter
import time

TOKEN = ""# it's a secret

bot = Bot(token=TOKEN)

channels_to_send = []
message = ''


def post_cb(bot, event):
    global message
    message = event.text[10:]
    if message != '':
        bot.send_text(chat_id=event.from_chat, text="Принял сообщение. Теперь проверьте список рассылки /show_channels\nИ запустите рассылку /time *задержка в с*")
    else:
        bot.send_text(chat_id=event.from_chat, text="Напиши сообщение побольше")

def add_channel(bot, event):
    global channels_to_send
    channel = event.text[13:]
    if channel not in channels_to_send and channel != '':
        channels_to_send.append(channel)
        bot.send_text(chat_id=event.from_chat, text="Channel added")
    elif channel in channels_to_send:
        bot.send_text(chat_id=event.from_chat, text="Такой канал уже есть, я его помню")
    elif channel == '':
        bot.send_text(chat_id=event.from_chat, text="Попробуй использовать другой nick/stamp/id")

def delete_channel(bot, event):
    global channels_to_send
    channel = event.text[16:]
    if channel in channels_to_send:
        for i in range(len(channels_to_send)):
            if channels_to_send[i] == channel:
                channels_to_send.pop(i)
                bot.send_text(chat_id=event.from_chat, text="Channel deleted")
                break
    else:
        bot.send_text(chat_id=event.from_chat, text="Нет такого канала(( Попробуй еще раз")


def show_channels(bot, event):
    global channels_to_send
    if len(channels_to_send) > 0:
        res = ''
        for i in channels_to_send:
            res += i + '\n'
        bot.send_text(chat_id=event.from_chat, text=res)
    else:
        bot.send_text(chat_id=event.from_chat, text='Пока что в рассылке ни одного канала((')

def time_cb(bot, event):
    global channels_to_send, message
    time_ = event.text[6:]
    try:
        if message != '' and len(channels_to_send) > 0:
            time.sleep(float(time_))
            for i in channels_to_send:
                bot.send_text(chat_id=i, text=message)
        elif message == '':
            bot.send_text(chat_id=event.from_chat, text='Нечего отправлять(( Попробуй еще раз')
        elif len(channels_to_send) == 0:
            bot.send_text(chat_id=event.from_chat, text='Некому отправлять(( Попробуй еще раз')
    except:
        bot.send_text(chat_id=event.from_chat, text='Вы ввели недопустимое значение времени(( Попробуй еще раз')


def helps(bot, event):
    bot.send_text(chat_id=event.from_chat, text='Привет. Я- простой бот для рассылки.\n'
                                                'Я умею:\n'
                                                '/new_post *Текст сообщения* - данная команда поможет тебе задать текст для рассылки\n'
                                                '/add_channel *id/username/etc..* - эта команда добавит пользователя для рассылки\n'
                                                '/delete_channel *id/username/etc..* - эта команда удалит пользователя из рассылки\n'
                                                '/show_channels - покажет каналы для расслыки\n'
                                                '/time *n* поможет запустить рассылку через n секунд')

bot.dispatcher.add_handler(MessageHandler(filters=Filter.regexp("/new_post*"), callback=post_cb))
bot.dispatcher.add_handler(MessageHandler(filters=Filter.regexp("/add_channel*"), callback=add_channel))
bot.dispatcher.add_handler(MessageHandler(filters=Filter.regexp("/delete_channel*"), callback=delete_channel))
bot.dispatcher.add_handler(MessageHandler(filters=Filter.regexp("/time*"), callback=time_cb))
bot.dispatcher.add_handler(CommandHandler(command="show_channels", callback=show_channels))
bot.dispatcher.add_handler(HelpCommandHandler(callback=helps))
bot.start_polling()
bot.idle()
