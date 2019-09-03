#!/usr/bin/python3

import sys
import os
sys.path.insert(0, os.environ['HOME'] + '/.myconfig/telegram_bot/')
import misc
import telebot
import re
import logging
import shelve
from telebot import types
from random import choice
from string import ascii_letters

import threading
mutex = threading.Lock()

from telebot import apihelper
apihelper.proxy = {'https': 'socks5://116405641:EgwmiTnv@orbtl.s5.opennetwork.cc:999'}

if not os.path.exists(os.getcwd() + '/temp'):
    os.makedirs(os.getcwd() + '/temp')

token = misc.token
bot = telebot.TeleBot(token)
whitelist = misc.whitelist
admin = misc.admin
userlist = []
keyword = misc.keyword

#  bot.config['api_key'] = token
print(bot.get_me())
os.system("rm -r ./temp/*")
mutex.acquire()
with shelve.open("db") as states:
    #  print("db:")
    for key in states:
        userlist.append(key)
    #  for state in states.items():
        #  print(state)
mutex.release()
print(userlist)

def log(message, answer):
    rows, columns = os.popen('stty size', 'r').read().split()
    print("\n")
    print('_' * int(columns))
    from datetime import datetime
    print(datetime.now())
    print("mes from {0} {1}. (id = {2}) \ntext: {3}".format(message.from_user.first_name,
        message.from_user.last_name,
        str(message.from_user.id),
            message.text))
    print(answer)

def youtube_url_validation(url):
    youtube_regex = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return youtube_regex_match.group(6)

    return youtube_regex_match

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "go away")
    answer = "command"
    log(message, answer)

@bot.message_handler(content_types=["text"])
@bot.edited_message_handler(content_types=["text"])
def handle_text(message):
    answer = "who are you"

    if str(message.from_user.id) not in userlist:
        if message.text in keyword:
            log(message, answer)
            mutex.acquire()
            with shelve.open("db") as states:
                states[str(message.from_user.id)] = "1"
            print("add user in db")
            mutex.release()
            userlist.append(str(message.from_user.id))
            bot.send_message(message.from_user.id, "congratz")
        else:
            log(message, answer)
    else:
        #  url = re.search("(?P<url>https?://[^\s]+)", message.text).group("url")
        youtube_link = youtube_url_validation(message.text)
        if youtube_link:
            answer = "url correct"
            log(message, answer)

            namedir = (''.join(choice(ascii_letters) for i in range(12)))
            mutex.acquire()
            with shelve.open("db") as states:
                speed = states.get(str(message.from_user.id), "1")
            mutex.release()
            os.system("./road.sh {0} {1} {2}".format(youtube_link, namedir, speed))

            directory = "./temp/{0}".format(namedir)
            all_files_in_direcotry = os.listdir(directory)
            #  print(all_files_in_direcotry)

            for file in all_files_in_direcotry:
                audio = open(directory + '/' + file, 'rb')
                bot.send_chat_action(message.from_user.id, 'upload_audio')
                bot.send_audio(message.from_user.id, audio)
                audio.close()

            os.system("rm -r ./temp/{0}".format(namedir))

        elif message.text in [ "settings", "Settings" ]:
            answer = "in settings"
            log(message, answer)
            key = types.InlineKeyboardMarkup()
            but1 = types.InlineKeyboardButton(text="1", callback_data="speed1")
            but2 = types.InlineKeyboardButton(text="1.25", callback_data="speed1.25")
            but3 = types.InlineKeyboardButton(text="1.5", callback_data="speed1.5")
            but4 = types.InlineKeyboardButton(text="1.75", callback_data="speed1.75")
            but5 = types.InlineKeyboardButton(text="2", callback_data="speed2")
            key.add(but1, but2, but3, but4, but5)
            bot.send_message(message.from_user.id, "select speed:", reply_markup=key)


        elif str(message.from_user.id) == admin:
            answer = "(admin)"
            if message.text in [ "temp", "Temp" ]:
                log(message, answer)
                bot.send_message(message.from_user.id,\
                        os.popen('cat /sys/devices/virtual/thermal/thermal_zone0/temp').read())

            elif message.text in [ "users", "Users" ]:
                log(message, answer)
                bot.send_message(message.from_user.id, userlist)

            else:
                log(message, answer)
                bot.send_message(message.from_user.id, "wat&")

        else:
            answer = "url not correct"
            log(message, answer)
            bot.send_message(message.from_user.id, "give me correct youtube url link")


@bot.callback_query_handler(func=lambda c:True)
def inline(c):
    if c.data == "speed1":
        mutex.acquire()
        with shelve.open("db") as states:
            #  print(states[str(c.from_user.id)])
            states[str(c.from_user.id)] = "1"
        mutex.release()
        bot.send_message(c.from_user.id, "select speed: 1")

    elif c.data == "speed1.25":
        mutex.acquire()
        with shelve.open("db") as states:
            states[str(c.from_user.id)] = "1.25"
        mutex.release()
        bot.send_message(c.from_user.id, "select speed: 1.25")

    elif c.data == "speed1.5":
        mutex.acquire()
        with shelve.open("db") as states:
            states[str(c.from_user.id)] = "1.5"
        mutex.release()
        bot.send_message(c.from_user.id, "select speed: 1.5")

    elif c.data == "speed1.75":
        mutex.acquire()
        with shelve.open("db") as states:
            states[str(c.from_user.id)] = "1.75"
        mutex.release()
        bot.send_message(c.from_user.id, "select speed: 1.75")

    elif c.data == "speed2":
        mutex.acquire()
        with shelve.open("db") as states:
            states[str(c.from_user.id)] = "2"
        mutex.release()
        bot.send_message(c.from_user.id, "select speed: 2")

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=5)

