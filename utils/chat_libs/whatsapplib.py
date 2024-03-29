# #!/usr/bin/python
# # -*- coding: utf-8 -*-

import json
import requests
import config
import logging as log


api_ver = config.api_ver


def send_message(user_id, text):
    # text += "\n\n(Вы можете отправить # для прекращения общения и остановки рассылки)"
    payload = {
        "phone": user_id,
        "body": text
    }
    print(payload)
    url = 'https://eu21.chat-api.com/instance13769/message?token=8xfrmb4v0c29qea2'
    response = requests.post(url, data=payload)
    print(response)
    print(response.text)
    data = json.loads(response.text)
    try:
        return data['sent']
    except BaseException as e:
        print(e)
        return False


def send_message_keyboard(user_id, text, keyboard):
    text += get_keyboard_from_list(keyboard)
    # text += "\n\n(Вы можете отправить # для прекращения общения и остановки рассылки)"
    payload = {
        "phone": user_id,
        "body": text
    }
    print(payload)
    url = 'https://eu21.chat-api.com/instance13769/message?token=8xfrmb4v0c29qea2'
    response = requests.post(url, data=payload)
    print(response)
    print(response.text)
    data = json.loads(response.text)
    try:
        return data['sent']
    except BaseException as e:
        print(e)
        return False


def get_queue_whatsapp():
    url = 'https://eu21.chat-api.com/instance13769/showMessagesQueue?token=8xfrmb4v0c29qea2'
    response = requests.get(url)
    print(response)
    print(response.text)
    data = json.loads(response.text)
    print(data)


def get_keyboard_from_list(list_btns):
    k = '\n'
    i = 1
    for b in list_btns:
        k += str(i) + ' - ' + b + '\n'
        i += 1
    return k


def stop_broadcasting():
    url = 'https://eu21.chat-api.com/instance13769/clearMessagesQueue?token=8xfrmb4v0c29qea2'
    response = requests.get(url)
    print(response)
    print(response.text)
    data = json.loads(response.text)
    return data['message']
#
# def send_message_much(user_ids, text):
#     """
#     Отправить сообщения многим пользователям за один запрос
#     """
#     d = str(user_ids).strip('[]').replace(' ', '')
#     print(d)
#     data = {
#         'message': text,
#         'user_ids': d,
#         'access_token': config.token,
#         'v': api_ver
#     }
#     answ = requests.post(config.vk_api_url + 'messages.send', data=data)
#     print(answ)
