#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from threading import Thread

from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from flask import Flask, Response
from flask import json
from flask import request
from flask_sqlalchemy import SQLAlchemy
import os
import telebot
# import telebot.types as types
# from viberbot.api.event_type import EventType
from viberbot.api.messages import TextMessage
from viberbot.api.viber_requests import ViberMessageRequest, ViberConversationStartedRequest
from utils.chat_libs import tglib

import config

token = config.token
confirmation_token = config.confirmation_token
secret_key = config.secret_key
db_name = config.db_name
bot_name = config.bot_name
vk_api_url = config.vk_api_url
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, db_name)
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import service as s
import consts as cnst

'''if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message
        # lets echo back
        viber.send_messages(viber_request.sender.id, [
            message
        ])'''


bot_configuration = BotConfiguration(
    name='Халва Бета',
    avatar='http://viber.com/avatar.jpg',
    auth_token='489dfb600267d384-f945b37ddf43e01c-450da3b3f85de11a'
)
viber = Api(bot_configuration)

tgbot = tglib.tgbot


@tgbot.message_handler(content_types=["text"])
def handle_text(message):
    uid = message.from_user.id
    text = message.text
    print("\nTG uid " + str(uid))
    print("\nTG msg " + text)
    s.message_processing(uid, text, source=cnst.TG)
# tglib.send_mesage(uid, text)
# R = tgbot.send_message('wer', 'text')
# print(R)
# me = tgbot.get_me()
# print(me)


@app.route(rule='/{}/incoming'.format(bot_name), methods=['POST'])
def viberf():
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        print(request.get_data())
        print('Неудачная попытка установить вебхук')
        return Response(status=403)
    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data().decode('utf-8'))
    print(viber_request)
    # if viber_request.event_type == EventType.CONVERSATION_STARTED:
    #     pass
    if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message
        print(message)
        text = message.text
        print(text)
        uid = viber_request.sender.id
        print(uid)
        s.message_processing(uid, text, cnst.VIBER)
    elif isinstance(viber_request, ViberConversationStartedRequest):
        # Запрашивать номер телефона
        uid = viber_request.get_user().get_id()
        print(uid)
        viber.send_messages(uid, [
            TextMessage(text="Welcome!")
        ])
    return Response(status=200)


@app.route(rule='/{}/request.in'.format(bot_name), methods=['POST'])
def whatsapp_new_msg():
    try:
        data = json.loads(request.data)
        for m in data['messages']:
            text = m['body']
            index = m['chatId'].index('@')
            uid = m['chatId'][:index]
            from_me = m['fromMe']
            print(text)
            print(uid)
            if not from_me:
                answer = s.message_processing(uid, text, cnst.WHATSAPP)
            elif '#' in text:
                answer = s.message_processing(uid, text[1:], cnst.WHATSAPP)
            return 'ok'
    except BaseException as e:
        print(e)
        return 'ok'


@app.route(rule='/', methods=['GET'])
def debug():
    # answer = s.message_processing('1111', 'admin', cnst.VK)
    # answer = s.message_processing('1111', 'Администраторы', cnst.VK)
    # s.start_conwersation('79991577222')
    # s.message_processing('79991577222', 'ответ 1', cnst.WHATSAPP)
    # answer = s.message_processing('259056624', 'admin', cnst.VK)
    # answer = s.message_processing('259056624', 'whatsapp 79991577222', cnst.VK)
    return "hello world"


@app.route(rule='/2', methods=['GET'])
def debug2():
    answer = s.message_processing('79991577222', '11', cnst.WHATSAPP)
    return answer


@app.route(rule='/{0}'.format(bot_name), methods=['POST'])
def processing():
    print('Пришел пост запрос')
    try:
        data = json.loads(request.data)
        if 'secret' not in data.keys():
            print('Not vk')
            return 'Not VK.'
        elif not data['secret'] == secret_key:
            print(data['secret'] + "  token не подходит")
            return 'Bad query.'
        if data['type'] == 'confirmation':
            print("Группа привязана!")
            return confirmation_token
        elif data['type'] == 'message_new':
            uid = data['object']['from_id']
            text = data['object']['text']
            attach = data['object']['attachments']
            print(attach)
            link = None
            if len(attach) > 0:
                link = attach[0]['doc']['url']
                print(link)
            answer = s.message_processing(uid, text, cnst.VK, link=link)
            return 'ok'
    except BaseException as e:
        print(e)
        return 'ok'


def main():
    print("Старт")
    port = int(config.port)
    app.run(host='0.0.0.0', port=port, debug=False)


class ThreadSubs(Thread):
    def __init__(self):
        """Инициализация потока"""
        Thread.__init__(self)

    def run(self):
        tgbot.polling(none_stop=True, interval=0)

tg_thread = ThreadSubs()
tg_thread.start()

if __name__ == '__main__':
    main()
