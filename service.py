#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import consts as cnst
import model as m
import utils.multithread_utils as mt
from utils import db_utils as db
from utils import service_utils as utils

READY_TO_ENROLL = {}
IN_ADMIN_PANEL = {}
READY_TO_LEAVE = {}
# thread_manager = mt.ThreadManager()
TIMEOUT_THREADS = {}

# thread_manager.run_brdcst_shedule()
# utils.send_message_admins_after_restart()


def admin_message_processing(uid, text):
    if text == cnst.MSG_ADMIN_EXIT:
        utils.del_uid_from_dict(uid, IN_ADMIN_PANEL)
        # mt.send_msg_welcome(uid, utils.get_user_keyboard())

    elif text == cnst.BTN_BROADCAST:
        IN_ADMIN_PANEL[uid] = cnst.BTN_BROADCAST
        # mt.send_message(uid, cnst.MSG_USER_SHORT_INFO.format(all_count, msg_allowed_count))
        # mt.send_message(uid, cnst.MSG_ACCEPT_BROADCAST, cnst.KEYBOARD_CANCEL)

    elif text == cnst.BTN_ADMINS:
        IN_ADMIN_PANEL[uid] = cnst.BTN_ADMINS
        admins = db.get_all_admins()
        msg = cnst.MSG_ADMINS
        for a in admins:
            msg += '🔑 {}, id - {}\n\n'.format(a.name, a.uid)
        msg += cnst.MSG_ADMIN_REMOVING
        mt.send_keyboard_vk_message(uid, msg, cnst.KEYBOARD_CANCEL)

    elif text == cnst.BTN_ADD_ADMIN:
        IN_ADMIN_PANEL[uid] = cnst.BTN_ADD_ADMIN
        mt.send_keyboard_vk_message(uid, cnst.MSG_ADMIN_ADDING, cnst.KEYBOARD_CANCEL)
    #
    # elif text == cnst.BTN_ADD_BROADCAST_BY_TIME:
    #     IN_ADMIN_PANEL[uid] = m.BcstByTime()
    #     mt.send_message(uid, cnst.MSG_ADD_BRDCST_BY_TIME, cnst.KEYBOARD_CANCEL)
    #
    # elif text == cnst.BTN_BROADCAST_BY_TIME:
    #     IN_ADMIN_PANEL[uid] = cnst.BTN_BROADCAST_BY_TIME
    #     brtcst = db.get_bcsts_by_time()
    #     msg = '🔥 Запланированные рассылки 🔥\n\n'
    #     for a in brtcst:
    #         msg += cnst.MSG_PLANNED_BCST.format(a.start_date, a.time, a.repet_days, a.id, a.msg)
    #     msg += 'Для удаления рассылки введите её id.'
    #     mt.send_message(uid, msg, cnst.KEYBOARD_CANCEL)

    elif text == cnst.BTN_QUESTIONS:
        IN_ADMIN_PANEL[uid] = m.QuestMsg()
        msg = utils.get_quest_msgs_as_str()
        mt.send_message(uid, msg)
        mt.send_keyboard_vk_message(uid, cnst.MSG_ACCEPT_QUEST_MSG, cnst.KEYBOARD_CANCEL_AND_MSG_EDIT)

    elif text == cnst.BTN_FIRST_MSG_EDIT:
        IN_ADMIN_PANEL[uid] = cnst.BTN_FIRST_MSG_EDIT
        msg = db.get_first_msg()
        msg += "\n\n Отправьте новое приветственное сообщение для замены. Используйте {} для обращения к пользователю."
        mt.send_keyboard_vk_message(uid, msg, keyboard=cnst.KEYBOARD_CANCEL)

    elif text == cnst.BTN_CANCEL:
        IN_ADMIN_PANEL[uid] = ''
        mt.send_keyboard_vk_message(uid, cnst.MSG_CANCELED_MESSAGE, cnst.KEYBOARD_ADMIN)

    elif 'whatsapp' in text :
        num = text.split(' ')[1]
        if num[0] == '7' and len(num) == 10:
            msg = db.get_first_msg()
            mt.first_send(num, msg)
        else:
            mt.send_message(uid, 'Не верный формат. Необходимо:whatsapp 79999999999')

    elif isinstance(IN_ADMIN_PANEL[uid], m.BcstByTime):
        if IN_ADMIN_PANEL[uid].date_time_is_not_sign():
            bcst = utils.parse_bcst(text)
            IN_ADMIN_PANEL[uid] = bcst
            if bcst is None:
                pass
                # mt.send_message(uid, "Некорректный формат. (22.08.2018 15:22 3)")
            else:
                pass
                # mt.send_message(uid, cnst.MSG_ACCEPT_BROADCAST)
        else:
            IN_ADMIN_PANEL[uid].msg = text
            # mt.send_message(uid, 'Рассылка создана!', cnst.KEYBOARD_ADMIN)
            # thread_manager.add_brcst_thread(IN_ADMIN_PANEL[uid])
            IN_ADMIN_PANEL[uid] = None

    elif isinstance(IN_ADMIN_PANEL[uid], m.QuestMsg):
        try:
            if IN_ADMIN_PANEL[uid].quest is not None:
                int('not int')
            qid = int(text)
            utils.del_question(qid)
            mt.send_keyboard_vk_message(uid, "Удалено", cnst.KEYBOARD_ADMIN)
            IN_ADMIN_PANEL[uid] = ''
        except ValueError:
            qid_str = text.split(' ')[0]
            if utils.isint(qid_str) and \
                            IN_ADMIN_PANEL[uid].quest is None and IN_ADMIN_PANEL[uid].id is None:
                IN_ADMIN_PANEL[uid].id = int(qid_str)
                text = ' '.join(text.split(' ')[1:])
            if IN_ADMIN_PANEL[uid].quest is None:
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
        # mt.emailing_to_all_subs_keyboard(uid, text)
        IN_ADMIN_PANEL.clear()
        IN_ADMIN_PANEL[uid] = ''

    elif IN_ADMIN_PANEL[uid] == cnst.BTN_FIRST_MSG_EDIT:
        db.update_first_msg(text)
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
            # thread_manager.delete_brcst(id)
            # mt.send_message(uid, "Запланированная рассылка удалена", cnst.KEYBOARD_ADMIN)
            IN_ADMIN_PANEL[uid] = ''
        except ValueError:
            msg = cnst.MSG_VALUE_ERROR
            # mt.send_message(uid, msg)
    else:
        pass
        # mt.send_message(uid, cnst.MSG_DEFAULT_ANSWER)


def message_processing(uid, text, source):

    if uid in IN_ADMIN_PANEL:
        admin_message_processing(uid, text)
        return 'ok'

    # Обработка ввода данных пользователя
    elif uid in READY_TO_ENROLL:
        if len(READY_TO_ENROLL[uid].qsts) > 0:
            if len(READY_TO_ENROLL[uid].qsts) == 1:
                mt.send_message(uid, "Еще нет вопросов")
                pass
            # Конец опроса
            else:
                READY_TO_ENROLL[uid].ei.answers += '; ' + text
                q = READY_TO_ENROLL[uid].qsts.pop(0)
                msg = q.quest
                if len(q.answs) > 0:
                    answrs = q.answs.split('; ')
                    mt.send_message_keyboard(uid, msg, answrs, msgr=READY_TO_ENROLL[uid].ei.msgr)
                else:
                    mt.send_message(uid, msg, msgr=READY_TO_ENROLL[uid].ei.msgr)

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


# message_processing('259056624', 'Admin', cnst.VK)


def start_conwersation(number):
    user = m.EnrollInfo(number=number, uid=number, msgr=cnst.WHATSAPP)
    READY_TO_ENROLL[number] = m.EnrollObj(user, db.get_all_quests())
    db.add_any(user)
    msg = db.get_first_msg()
    mt.send_message(number, msg, cnst.WHATSAPP)


