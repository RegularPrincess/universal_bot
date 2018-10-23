#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask import json
from flask import request
from flask_sqlalchemy import SQLAlchemy
import os

import config

token = config.token
confirmation_token = config.confirmation_token
secret_key = config.secret_key
group_id = config.group_id
admin_id = config.admin_id
admin_name = config.admin_name
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
            if len(attach) > 0:
                link = attach[0]['doc']
            answer = s.message_processing(uid, text, cnst.VK, link=link)
            return 'ok'
    except BaseException as e:
        print(e)
        return 'ok'


def main():
    print("Старт")
    port = int(config.port)
    app.run(host='0.0.0.0', port=port, debug=False)


if __name__ == '__main__':
    main()
