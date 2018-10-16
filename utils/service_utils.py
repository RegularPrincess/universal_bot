import json
import os
import re

import datetime

import copy
import requests

import utils.vklib as vk
import utils.db_utils as db
import model as m
import consts as cnst
import config as cfg


def get_user_keyboard():
    k = cnst.KEYBOARD_USER
    k["buttons"][0][0]["action"]["label"] = db.get_first_btn()
    k["buttons"][0][0]["color"] = db.get_color_btn()
    return k


def get_user_enroll_btn():
    k = cnst.enroll_btn
    k[0]["action"]["label"] = db.get_first_btn()
    k[0]["color"] = db.get_color_btn()
    return k



class id_wrapper:
    def __init__(self):
        self.questions = db.get_quest_msgs()

    def get_db_id(self, vid):
        return self.questions[vid - 1].id

    def get_view_id(self, id):
        i = 1
        for q in self.questions:
            if q.id == id:
                return i
            i += 1

    def update(self):
        self.questions = db.get_quest_msgs()


ID_WRAPPER = id_wrapper()


def del_uid_from_dict(uid, dict_):
    if uid in dict_:
        del dict_[uid]


def send_message_admins(info):
    admins = db.get_list_bot_admins()
    note = 'Примечания : {}'.format("\n".join(info.answers))
    vk.send_message_much(admins, cnst.NOTIFY_ADMIN.format(info.uid, info.name, info.email, info.number, note))


def send_message_admins_after_restart():
    admins = db.get_list_bot_admins()
    vk.send_message_much_keyboard(admins, cnst.MSG_SERVER_RESTARTED, get_user_keyboard())


def is_number_valid(number):
    match = re.fullmatch('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,9}', number)
    if match:
        return True
    else:
        return False


def is_email_valid(email):
    match = re.fullmatch('[\w.-]+@\w+\.\w+', email)
    if match:
        return True
    else:
        return False


def parse_bcst(text):
    try:
        obj = m.BcstByTime()
        text_arr = text.split(' ', maxsplit=3)
        obj.start_date = datetime.datetime.strptime(text_arr[0], '%d.%m.%Y').date()
        obj.time = datetime.datetime.strptime(text_arr[1], '%H:%M').time()
        obj.repet_days = int(text_arr[2])
        return obj
    except BaseException:
        return None


def get_keyboard_from_list(list, def_btn=get_user_enroll_btn()):
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
    keyboard['buttons'].append(def_btn)
    return keyboard


def send_data_to_uon(data, uid):
    today = datetime.datetime.today()
    t = today.time()
    date_str = '{} {}:{}:{}'.format(today.date(), t.hour + cfg.time_zone_from_msk, t.minute, t.second)
    note = 'Примечания : {}'.format("\n".join(data.answers))
    payload = {
        'r_dat': date_str,
        'r_u_id': cfg.default_uon_admin_id,
        'u_name': data.name,
        'source': 'Бот вконтакте',
        'u_phone': data.number,
        'u_email': data.email,
        'u_social_vk': ('id' + str(uid)),
        'u_note': note
    }
    print(payload)
    url = 'https://api.u-on.ru/{}/lead/create.json'.format(cfg.uon_key)
    response = requests.post(url, data=payload)
    print(response)
    print(response.text)


def get_quest_msgs_as_str():
    quests = db.get_quest_msgs()
    str = ''
    if len(quests) == 0:
        str = '<Еще нет ни одного вопроса кроме вопросов о телефоне и email, которые есть всегда>'
    for q in quests:
        if len(q.answs) > 0:
            str += '(ID-{}) {} \n(Варианты ответа: {})\n\n'.format(ID_WRAPPER.get_view_id(q.id), q.quest, q.answs)
        else:
            str += '(ID-{}) {} \n\n'.format(ID_WRAPPER.get_view_id(q.id), q.quest)
    return str


def del_question(vid):
    db_id = ID_WRAPPER.get_db_id(vid)
    db.delete_quest_msg(db_id)
    ID_WRAPPER.update()


def add_quest_msg(quest, answs, vid=None):
    db_id = vid
    if vid is not None:
        db_id = ID_WRAPPER.get_db_id(vid)
    db.add_quest_msg(quest, answs, db_id)
    ID_WRAPPER.update()


def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def send_welcome_msg(uid, uname, keyboard):
    if uname is None:
        uname = vk.get_user_name(uid)
    msg = db.get_first_msg()
    vk.send_message_keyboard(uid, msg.format(uname), keyboard)


def emailing_to_all_subs_keyboard(uid, text):
    """
    Разослать текст всем подписчикам, кому возможно группы
    """
    count = 0
    arr = []
    users = db.get_bot_followers()
    for u in users:
        if u.is_msging_allowed():
            arr.append(u.uid)
            count += 1
        if len(arr) == 100:
            vk.send_message_much_keyboard(arr, text, get_user_keyboard())
            arr = []
    vk.send_message_much_keyboard(arr, text, get_user_keyboard())
    vk.send_message_keyboard(uid, cnst.MSG_BROADCAST_COMPLETED.format(count), cnst.KEYBOARD_ADMIN)
    return count

