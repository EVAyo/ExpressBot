#!/usr/bin/python
# coding:utf-8


import telebot
import logging
import kuaidi100
import json
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.


# start - 输入快递单号来查询
# help - 帮助
# list - 查看我的查询历史
# delete - 删除某个单号
# quickdel - 回复某条查询消息来快速删除


@bot.message_handler(commands=['start'])
def bot_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, 'Send me your ExpressID directly.')


@bot.message_handler(commands=['help'])
def bot_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id,
                     "Hi there.\nI'm a bot that could help you tracking your Express. Feel free to contact "
                     "@BennyThink .")


@bot.message_handler(commands=['list'])
def bot_list(message):
    all_info = kuaidi100.list_query(message.chat.username)
    for i in all_info:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, i[0] + '\n' + i[1] + ' ' + i[2] + '\n')


@bot.message_handler(commands=['delete'])
def bot_delete(message):
    if message.text == '/delete':
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, 'Please append your ExpressID to delete command, i.e. \n/delete 123456789')
    else:
        msg = kuaidi100.delete(message.text[8:])
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['quickdel'])
def bot_quick_delete(message):
    s = message.reply_to_message.text
    msg = kuaidi100.delete(s.split()[0])
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, msg)


@bot.message_handler()
def track_express(message):
    bot.send_chat_action(message.chat.id, 'typing')
    r = kuaidi100.recv(message.text, message.chat.username, message.chat.id)
    bot.send_message(message.chat.id, r)


@bot.message_handler()
def cron(code, un, chat_id):
    # bot.send_chat_action(message.chat.id, 'typing')
    r = kuaidi100.recv(code, un, chat_id)
    # There is not messageid, so not this line.
    # bot.reply_to(c, r)
    bot.send_message(chat_id, r)


if __name__ == '__main__':
    bot.polling()
