import json
import re

import datetime
import requests
import utils.db_utils as db
import model as m
import config as cfg
import consts as cnst
from utils.chat_libs import whatsapplib as wapp
from utils.chat_libs import vklib as vk



class id_wrapper:
    def __init__(self):
        self.questions = db.get_all_quests()

    def get_db_id(self, vid):
        return self.questions[vid - 1].id

    def get_view_id(self, id):
        i = 1
        for q in self.questions:
            if q.id == id:
                return i
            i += 1

    def update(self):
        self.questions = db.get_all_quests()


ID_WRAPPER = id_wrapper()


def del_uid_from_dict(uid, dict_):
    if uid in dict_:
        del dict_[uid]


def send_message_admins(info):
    admins = db.get_all_admins()
    note = 'Примечания : {}'.format("\n".join(info.answers))
    vk.send_message_much(admins, cnst.NOTIFY_ADMIN.format(info.uid, note))


def send_message_admins_after_restart():
    admins = db.get_all_admins()
    # vk.send_message_much_keyboard(admins, cnst.MSG_SERVER_RESTARTED, get_user_keyboard())


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
    quests = db.get_all_quests()
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
    db.delete_quest(db_id)
    ID_WRAPPER.update()


def add_quest_msg(quest, answs, vid=None):
    db_id = vid
    if vid is not None:
        db_id = ID_WRAPPER.get_db_id(vid)
        q = m.QuestMsg(quest, answs, db_id)
        db.update_quest(q, db_id)
    else:
        q = m.QuestMsg(quest, answs, db_id)
        db.add_any(q)
        ID_WRAPPER.update()


def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# get_queue_whatsapp()
# print(try_whatsapp('79501751514', 'Да'))

#
# def first_send(num, msg):
#     wapp.send_message(num, msg)
#     q = db.get_all_quests()
#     wapp.send_message_keyboard(num, 'первый вопрос', 'раз; два; три'.split('; '))
