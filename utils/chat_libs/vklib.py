# #!/usr/bin/python
# # -*- coding: utf-8 -*-

import json

import copy
import requests
import config
import logging as log
import consts as cnst


api_ver = config.api_ver


def send_message(user_id, text):
    """
    Send VK message
    """
    data = {
        'message': text,
        'user_id': user_id,
        'access_token': config.token,
        'v': api_ver
    }
    r = requests.post(config.vk_api_url + 'messages.send', data=data)
    print(r)


def send_message_simple_keyboard(user_id, text, keyboard):
    k = get_keyboard_from_list(keyboard)
    data = {
        'message': text,
        'user_id': user_id,
        'access_token': config.token,
        'keyboard': json.dumps(k, ensure_ascii=False),
        'v': api_ver
    }
    res = requests.post(config.vk_api_url + 'messages.send', data=data)
    print(res)


def send_message_keyboard(user_id, text, keyboard):
    data = {
        'message': text,
        'user_id': user_id,
        'access_token': config.token,
        'keyboard': json.dumps(keyboard, ensure_ascii=False),
        'v': api_ver
    }
    res = requests.post(config.vk_api_url + 'messages.send', data=data)
    print(res)


def send_message_much(user_ids, text):
    """
    Отправить сообщения многим пользователям за один запрос
    """
    d = str(user_ids).strip('[]').replace(' ', '')
    print(d)
    data = {
        'message': text,
        'user_ids': d,
        'access_token': config.token,
        'v': api_ver
    }
    answ = requests.post(config.vk_api_url + 'messages.send', data=data)
    print(answ)


def get_messages_upload_server(peer_id):
    """
    Получить сервер ВК для загрузки фото в ЛС
    """
    data = {
        'peer_id': peer_id,
        'access_token': config.token,
        'v': api_ver
    }
    res = requests.post(config.vk_api_url + 'photos.getMessagesUploadServer', data=data)
    return res.json()


def save_messages_photo(photo, server, hash):
    """
    Сохраняет фотографию после успешной загрузки на URI
    """
    data = {
        'photo': photo,
        'server': server,
        'hash': hash,
        'access_token': config.token,
        'v': api_ver
    }
    res = requests.post(config.vk_api_url + 'photos.saveMessagesPhoto', data=data)
    return res.json()


def send_message_with_photo(user_id, text, photo):
    """
    Отправить сообщение с фото
    :param photo: строка вида photoOWNERID_PHOTOID
    """
    data = {
        'message': text,
        'user_id': user_id,
        'attachment': photo,
        'access_token': config.token,
        'v': api_ver
    }
    res = requests.post(config.vk_api_url + 'messages.send', data=data)
    print(res.text)


def get_keyboard_from_list(list):
    keyboard = copy.deepcopy(cnst.keyboard_pattern.copy())
    c = 0
    for i in list:
        if c == 7:
            break
        one_btns = copy.deepcopy(cnst.one_button_pattern)
        one_btns[0]['action']['label'] = i
        j = {"button": 'K'}
        one_btns[0]['action']['payload'] = json.dumps(j)
        keyboard['buttons'].append(one_btns)
        c += 1
    return keyboard
