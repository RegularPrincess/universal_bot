#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

import requests

import consts as cnst
import model as m
import utils.multithread_utils as mt
import time
import copy
from utils import db_utils as db
from utils import service_utils as utils

READY_TO_ENROLL = {}
IN_ADMIN_PANEL = {}
READY_TO_LEAVE = {}
thread_manager = mt.ThreadManager()
TIMEOUT_THREADS = {}

thread_manager.run_brdcst_shedule()
# utils.send_message_admins_after_restart()


def admin_message_processing(uid, text, link=None):
    if text == cnst.BTN_BROADCAST:
        IN_ADMIN_PANEL[uid] = cnst.BTN_BROADCAST
        # mt.send_message(uid, cnst.MSG_USER_SHORT_INFO.format(all_count, msg_allowed_count))
        mt.send_keyboard_vk_message(uid, cnst.MSG_ACCEPT_BROADCAST, cnst.KEYBOARD_CANCEL)

    elif text == cnst.BTN_SUBS:
        pg = mt.ThreadSubs(uid)
        pg.start()

    elif text == cnst.BTN_ADMINS:
        IN_ADMIN_PANEL[uid] = cnst.BTN_ADMINS
        admins = db.get_all_admins()
        msg = cnst.MSG_ADMINS
        for a in admins:
            msg += '🔑 {}, id - {}\n\n'.format(a.name, a.uid)
        msg += cnst.MSG_ADMIN_REMOVING
        mt.send_keyboard_vk_message(uid, msg, cnst.KEYBOARD_CANCEL)

    elif text == cnst.BTN_BROADCAST_BY_FILE:
        IN_ADMIN_PANEL[uid] = cnst.BTN_BROADCAST_BY_FILE
        mt.send_keyboard_vk_message(uid, cnst.MSG_ACCEPT_BROADCAST_BY_FILE, cnst.KEYBOARD_CANCEL)

    elif text == cnst.BTN_ADD_ADMIN:
        IN_ADMIN_PANEL[uid] = cnst.BTN_ADD_ADMIN
        mt.send_keyboard_vk_message(uid, cnst.MSG_ADMIN_ADDING, cnst.KEYBOARD_CANCEL)

    elif text == cnst.BTN_BROADCASTS:
        mt.send_keyboard_vk_message(uid, 'Меню рассылок:', cnst.KEYBOARD_BROADCASTS)

    elif text == cnst.BTN_ADD_BROADCAST_BY_TIME:
        IN_ADMIN_PANEL[uid] = m.BcstByTime()
        mt.send_keyboard_vk_message(uid, cnst.MSG_ADD_BRDCST_BY_TIME, cnst.KEYBOARD_CANCEL)

    elif text == cnst.BTN_BROADCAST_BY_TIME:
        IN_ADMIN_PANEL[uid] = cnst.BTN_BROADCAST_BY_TIME
        brtcsts = db.get_all_bcsts()
        msg = '🔥 Запланированные рассылки 🔥\n\n'
        for a in brtcsts:
            msg += cnst.MSG_PLANNED_BCST.format(a.start_date, a.time, a.repet_days, a.id, a.msg)
        msg += 'Для удаления рассылки введите её id.'
        mt.send_keyboard_vk_message(uid, msg, cnst.KEYBOARD_CANCEL)

    elif text == cnst.BTN_QUESTIONS:
        IN_ADMIN_PANEL[uid] = m.QuestMsg()
        msg = utils.get_quest_msgs_as_str()
        mt.send_message(uid, msg)
        mt.send_keyboard_vk_message(uid, cnst.MSG_ACCEPT_QUEST_MSG, cnst.KEYBOARD_CANCEL_AND_MSG_EDIT)

    elif text == cnst.BTN_FIRST_MSG_EDIT:
        IN_ADMIN_PANEL[uid] = cnst.BTN_FIRST_MSG_EDIT
        msg = db.get_first_msg()
        msg += "\n\n Отправьте новое приветственное сообщение для замены."
        mt.send_keyboard_vk_message(uid, msg, keyboard=cnst.KEYBOARD_CANCEL)

    elif text == cnst.BTN_EDIT_LAST_MSG:
        IN_ADMIN_PANEL[uid] = cnst.BTN_EDIT_LAST_MSG
        msg = db.get_last_msg()
        msg += "\n\n Отправьте новое завершающее сообщение для замены."
        mt.send_keyboard_vk_message(uid, msg, keyboard=cnst.KEYBOARD_CANCEL)

    elif text == cnst.BTN_CONGRATULATION_EDIT:
        IN_ADMIN_PANEL[uid] = cnst.BTN_CONGRATULATION_EDIT
        msg = db.get_congrat_msg()
        msg += "\n\n Отправьте новое поздравительное сообщение для замены."
        mt.send_keyboard_vk_message(uid, msg, keyboard=cnst.KEYBOARD_CANCEL)

    elif text == cnst.BTN_CANCEL:
        IN_ADMIN_PANEL[uid] = ''
        mt.send_keyboard_vk_message(uid, cnst.MSG_CANCELED_MESSAGE, cnst.KEYBOARD_ADMIN)

    elif text in cnst.ADMIN_KEY_WORDS:
        IN_ADMIN_PANEL[uid] = ''
        mt.send_keyboard_vk_message(uid, cnst.MSG_ADMIN_PANEL, cnst.KEYBOARD_ADMIN)

    elif 'whatsapp' in text:
        num = text.split(' ')[1]
        if num[0] == '7' and len(num) == 11:
            start_conwersation_wapp(num)
            mt.send_message(uid, 'Сообщение отправлено через whatsapp')
        else:
            mt.send_message(uid, 'Не верный формат. Необходимо:whatsapp 79999999999')

    elif 'del' in text:
        num = text.split(' ')[1]
        if num[0] == '7' and len(num) == 11:
            db.delete_user_by_num(num)
            mt.send_message(uid, 'Пользователь удален')
        else:
            mt.send_message(uid, 'Не верный формат. Необходимо:del 79999999999')

    elif isinstance(IN_ADMIN_PANEL[uid], m.BcstByTime):
        if IN_ADMIN_PANEL[uid].date_time_is_not_sign():
            bcst = utils.parse_bcst(text)
            IN_ADMIN_PANEL[uid] = bcst
            if bcst is None:
                mt.send_message(uid, "Некорректный формат. (22.08.2018 15:22 3)")
            else:
                mt.send_message(uid, cnst.MSG_ACCEPT_BROADCAST)
        else:
            IN_ADMIN_PANEL[uid].msg = text
            mt.send_keyboard_vk_message(uid, 'Рассылка создана!', cnst.KEYBOARD_ADMIN)
            thread_manager.add_brcst_thread(IN_ADMIN_PANEL[uid])
            IN_ADMIN_PANEL[uid] = None

    elif isinstance(IN_ADMIN_PANEL[uid], m.QuestMsg):
        try:
            if IN_ADMIN_PANEL[uid].quest != '':
                int('not int')
            qid = int(text)
            utils.del_question(qid)
            mt.send_keyboard_vk_message(uid, "Удалено", cnst.KEYBOARD_ADMIN)
            IN_ADMIN_PANEL[uid] = ''
        except ValueError:
            qid_str = text.split(' ')[0]
            if utils.isint(qid_str) and \
                            IN_ADMIN_PANEL[uid].quest == '' and IN_ADMIN_PANEL[uid].id is None:
                IN_ADMIN_PANEL[uid].id = int(qid_str)
                print('id set' + qid_str)
                text = ' '.join(text.split(' ')[1:])
            if IN_ADMIN_PANEL[uid].quest == '':
                IN_ADMIN_PANEL[uid].quest = text
                mt.send_keyboard_vk_message(uid, cnst.MSG_ADDING_ANSWS_VAR, cnst.KEYBOARD_END_AND_CANCELE)
            elif text == cnst.BTN_END:
                utils.add_quest_msg(IN_ADMIN_PANEL[uid].quest, '', IN_ADMIN_PANEL[uid].id)
                mt.send_keyboard_vk_message(uid, "Сохранено", cnst.KEYBOARD_ADMIN)
                IN_ADMIN_PANEL[uid] = ''
            else:
                utils.add_quest_msg(IN_ADMIN_PANEL[uid].quest, text, IN_ADMIN_PANEL[uid].id)
                mt.send_keyboard_vk_message(uid, "Сохранено", cnst.KEYBOARD_ADMIN)
                IN_ADMIN_PANEL[uid] = ''

    elif IN_ADMIN_PANEL[uid] == cnst.BTN_BROADCAST:
        mt.send_msg_all_whatsapp_subs(text)
        IN_ADMIN_PANEL.clear()
        IN_ADMIN_PANEL[uid] = ''
        mt.send_keyboard_vk_message(uid, "Разослано", cnst.KEYBOARD_ADMIN)

    elif IN_ADMIN_PANEL[uid] == cnst.BTN_BROADCAST_BY_FILE:
        send_msg_by_file(text, link)
        IN_ADMIN_PANEL.clear()
        IN_ADMIN_PANEL[uid] = ''
        mt.send_keyboard_vk_message(uid, "Разослано", cnst.KEYBOARD_ADMIN)

    elif IN_ADMIN_PANEL[uid] == cnst.BTN_FIRST_MSG_EDIT:
        db.update_first_msg(text)
        mt.send_keyboard_vk_message(uid, "Сохранено", cnst.KEYBOARD_ADMIN)
        IN_ADMIN_PANEL[uid] = ''

    elif IN_ADMIN_PANEL[uid] == cnst.BTN_EDIT_LAST_MSG:
        db.update_last_msg(text)
        mt.send_keyboard_vk_message(uid, "Сохранено", cnst.KEYBOARD_ADMIN)
        IN_ADMIN_PANEL[uid] = ''

    elif IN_ADMIN_PANEL[uid] == cnst.BTN_CONGRATULATION_EDIT:
        db.update_congrat_msg(text)
        mt.send_keyboard_vk_message(uid, "Сохранено", cnst.KEYBOARD_ADMIN)
        IN_ADMIN_PANEL[uid] = ''

    elif IN_ADMIN_PANEL[uid] == cnst.BTN_ADMINS:
        try:
            admin_id = int(text)
            db.delete_admin(admin_id)
            msg = cnst.MSG_ADMIN_REMOVED
            mt.send_keyboard_vk_message(uid, msg, cnst.KEYBOARD_ADMIN)
            IN_ADMIN_PANEL[uid] = ''
        except ValueError:
            msg = cnst.MSG_VALUE_ERROR
            mt.send_message(uid, msg)

    elif IN_ADMIN_PANEL[uid] == cnst.BTN_ADD_ADMIN:
        try:
            admin_id = int(text)
            admin = m.Admin('None', admin_id)
            db.add_any(admin)
            mt.send_keyboard_vk_message(uid, cnst.MSG_ADMIN_SUCCCES_ADDED, cnst.KEYBOARD_ADMIN)
            IN_ADMIN_PANEL[uid] = ''
        except ValueError:
            msg = cnst.MSG_VALUE_ERROR
            mt.send_message(uid, msg)

    elif IN_ADMIN_PANEL[uid] == cnst.BTN_BROADCAST_BY_TIME:
        try:
            id = int(text)
            thread_manager.delete_brcst(id)
            mt.send_keyboard_vk_message(uid, "Запланированная рассылка удалена", cnst.KEYBOARD_ADMIN)
            IN_ADMIN_PANEL[uid] = ''
        except ValueError:
            msg = cnst.MSG_VALUE_ERROR
            mt.send_message(uid, msg)
    else:
        pass
        # mt.send_message(uid, cnst.MSG_DEFAULT_ANSWER)


def message_processing(uid, text, source, link=None):

    if db.is_admin(str(uid)) and source == cnst.VK:
        admin_message_processing(uid, text, link=link)
        return 'ok'

    if uid not in READY_TO_ENROLL and source == cnst.WHATSAPP:
        start_conwersation_wapp(uid, welcome_only=True)

    if uid not in READY_TO_ENROLL and source == cnst.VIBER:
        quests = copy.deepcopy(db.get_all_quests())
        user = m.EnrollInfo(number=None, uid=uid, msgr=cnst.VIBER)
        READY_TO_ENROLL[uid] = m.EnrollObj(enroll_info=m.EnrollInfo(
            user.number, user.uid, user.id, [], user.msgr), quests=quests)
        msg = db.get_first_msg()
        print(msg)
        mt.send_message(uid, msg=msg, msgr=cnst.VIBER)
        time.sleep(1)
        mt.RequestNumberViber(uid, 'Нам необходим ваш номер телефона')
        return 'ok'

    # Обработка ввода данных пользователя
    if uid in READY_TO_ENROLL:

        # Блок для viber, где нельзя получить номер
        if source == cnst.VIBER and READY_TO_ENROLL[uid].ei.number is None:
            if utils.is_number_valid(text):
                READY_TO_ENROLL[uid].ei.number = text
            else:
                mt.send_message(uid, "Поделитесь номером, нажав на кнопку, пожалуйста.")
                return 'ok'

        # блок для ватсапп, где нет кнопок и варианты цифрами
        if source == cnst.WHATSAPP and READY_TO_ENROLL[uid].last_variants is not None:
            if utils.isint(text) and int(text) <= len(READY_TO_ENROLL[uid].last_variants):
                index = int(text) - 1
                text = READY_TO_ENROLL[uid].last_variants[index]
                READY_TO_ENROLL[uid].last_variants = None
            else:
                mt.send_message(uid, 'Введите цифру варианта!', msgr=READY_TO_ENROLL[uid].ei.msgr)
                return
        #

        READY_TO_ENROLL[uid].ei.answers.append(text)
        if len(READY_TO_ENROLL[uid].qsts) > 0:
            q = READY_TO_ENROLL[uid].qsts.pop(0)
            READY_TO_ENROLL[uid].last_variants = q.answs
            mt.send_quest(uid, q, msgr=READY_TO_ENROLL[uid].ei.msgr)
        else:
            print('sending last msg by ' + text + '\n')
            mt.send_last_msge(uid, READY_TO_ENROLL[uid].ei.msgr)
            db.update_user(uid, READY_TO_ENROLL[uid].ei)
            del READY_TO_ENROLL[uid]

    # Вход для админа
    elif text.lower() in cnst.ADMIN_KEY_WORDS and not_ready_to_enroll(uid):
        if db.is_admin(str(uid)) and source == cnst.VK:
            IN_ADMIN_PANEL[uid] = ''
            mt.send_keyboard_vk_message(uid, cnst.MSG_ADMIN_PANEL, cnst.KEYBOARD_ADMIN)
        elif source != cnst.VK:
            mt.send_message(uid, "Зайдите в меню администратора через ВК")
        elif not db.is_admin(uid):
            mt.send_message(uid, "Вы не админ")
    elif text.lower() == "clearme":
        pass
        # mt.send_message(uid, "clear", keyboard=cnst.EMPTY_KEYBOARD)
    else:
        pass
    return 'ok'


def not_ready_to_enroll(uid):
    return uid not in READY_TO_ENROLL


def start_conwersation_wapp(number, welcome_only=False):
    user = m.EnrollInfo(number=number, uid=number, msgr=cnst.WHATSAPP)
    msg = db.get_first_msg()
    mt.send_message(number, msg, cnst.WHATSAPP)
    time.sleep(1)
    quests = copy.deepcopy(db.get_all_quests())
    READY_TO_ENROLL[number] = m.EnrollObj(m.EnrollInfo(
        user.number, user.uid, user.id, '', user.msgr), quests)

    if len(quests) > 0:
        q = quests.pop(0)
        msg = q.quest
        if q.answs is not None and len(q.answs) > 0:
            answrs = q.answs.split('; ')
            READY_TO_ENROLL[number].last_variants = answrs
            mt.send_message_keyboard(number, msg, answrs, msgr=READY_TO_ENROLL[number].ei.msgr)
        else:
            READY_TO_ENROLL[number].last_variants = None
            mt.send_message(number, msg, msgr=READY_TO_ENROLL[number].ei.msgr)


def send_msg_by_file(text, link):   
    r = requests.get(link, allow_redirects=True)
    file = open('subs_num.txt', 'wb')
    file.write(r.content)
    file.close()
    with open("subs_num.txt") as file:
        array = [row.strip() for row in file]
        for num in array:
            start_conwersation_wapp(num, welcome_only=True)


def admins_to_admin_menu():
    admins = db.get_all_admins()
    for a in admins:
        IN_ADMIN_PANEL[a.uid] = ''

admins_to_admin_menu()
# IN_ADMIN_PANEL['259056624'] = cnst.BTN_BROADCAST_BY_FILE

# message_processing('259056624', '', cnst.VK, link='https://vk.com/doc259056624_478912520?hash=207dee4cb744dbf03d&dl=GI2TSMBVGY3DENA:1540288896:debfd5a95c7d878fc4&api=1&no_preview=1')

# message_processing('259056624', 'del 79991577222', cnst.VK)


# message_processing('259056624', cnst.BTN_QUESTIONS, cnst.VK)
# message_processing('259056624', '1 wert', cnst.VK)

#
# message_processing('259056624', 'whatsapp 79991577222', cnst.VK)
# message_processing('70000000000', '3r56g', cnst.WHATSAPP)
# message_processing('79991577222', '222222', cnst.WHATSAPP)
# message_processing('79991577222', '2', cnst.WHATSAPP)


# if READY_TO_ENROLL[uid].need_birthday and not utils.isint(text):
#     # пропускаем вопрос о др
#     READY_TO_ENROLL[uid].ei.answers += text + '; '
#     q = READY_TO_ENROLL[uid].qsts.pop(0)
#     READY_TO_ENROLL[uid].need_birthday = False
#     if len(READY_TO_ENROLL[uid].qsts) > 0:
#         q = READY_TO_ENROLL[uid].qsts.pop(0)
#         msg = q.quest
#     else:
#         last_msg = db.get_last_msg()
#         mt.send_message(uid, last_msg, msgr=READY_TO_ENROLL[uid].ei.msgr)
#         mt.send_msg_to_admins(READY_TO_ENROLL[uid].ei)
#         db.update_user(READY_TO_ENROLL[uid].ei, uid)
#         READY_TO_ENROLL[uid].last_variants = None
#         utils.del_uid_from_dict(uid, READY_TO_ENROLL)
#         return
# else:
#     if not READY_TO_ENROLL[uid].skip_next_answ:
#         READY_TO_ENROLL[uid].ei.answers += text + '; '
#         READY_TO_ENROLL[uid].skip_next_answ = False
#     q = READY_TO_ENROLL[uid].qsts.pop(0)
#     msg = q.quest
# if q.answs is not None and len(q.answs) > 0:
#     answrs = q.answs.split('; ')
#     READY_TO_ENROLL[uid].last_variants = answrs
#     mt.send_message_keyboard(uid, msg, answrs, msgr=READY_TO_ENROLL[uid].ei.msgr)
# else:
#     READY_TO_ENROLL[uid].last_variants = None
#     mt.send_message(uid, msg, msgr=READY_TO_ENROLL[uid].ei.msgr)
# else:
# READY_TO_ENROLL[uid].ei.answers += text
# try:
#     answs = READY_TO_ENROLL[uid].ei.answers.split('; ')
#     if datetime.today().month > int(answs[1]) and \
#                     datetime.today().day > int(answs[0]):
#         y = str(datetime.today().year + 1)
#     else:
#         y = str(datetime.today().year + 1)
#     dmy = answs[1] + '.' + answs[0] + '.' + y
#     obj = m.BcstByTime()
#     obj.start_date = datetime.strptime(dmy, '%d.%m.%Y').date()
#     obj.time = datetime.strptime('10:00', '%H:%M').time()
#     obj.repet_days = 365
#     obj.msg = db.get_congrat_msg()
#     thread_manager.add_brcst_thread(obj)
# except BaseException as e:
#     print(e.with_traceback(e.__traceback__))
#     print(e)
#     print(e.__traceback__)
# finally:
#     print('Пользователь закончил опрос')
#     msg = db.get_last_msg()
#     mt.send_message(uid, msg, msgr=READY_TO_ENROLL[uid].ei.msgr)
#     mt.send_msg_to_admins(READY_TO_ENROLL[uid].ei)
#     db.update_user(READY_TO_ENROLL[uid].ei, uid)
#     READY_TO_ENROLL[uid].last_variants = None
#     utils.del_uid_from_dict(uid, READY_TO_ENROLL)



