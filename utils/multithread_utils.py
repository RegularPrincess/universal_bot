import time
from multiprocessing import Process
from threading import Thread

from datetime import datetime, timedelta

from utils import db_utils as db
import consts as cnst
import utils.chat_libs.vklib as vk
import utils.chat_libs.whatsapplib as wapp
import utils.chat_libs.viberlib as vib
import utils.service_utils as utils
import model as m


class ThreadManager:
    def __init__(self):
        self.bcst_threads = []

    def run_brdcst_shedule(self):
        bcsts = db.get_all_bcsts()
        self.bcst_threads = []
        for b in bcsts:
            self.bcst_threads.append(ThreadBrdcst(b))
        for bt in self.bcst_threads:
            bt.start()

    def add_brcst_thread(self, bcst):
        db.add_any(bcst)
        self.run_brdcst_shedule()

    def delete_brcst(self, id):
        db.delete_brdcst(id)
        self.run_brdcst_shedule()


class ThreadBrdcst(Thread):
    def __init__(self, bcst):
        """Инициализация потока"""
        Thread.__init__(self)
        self.bcst = bcst

    def run(self):
        day = self.bcst.start_date
        time_ = self.bcst.time
        plane = datetime.combine(day, time_)
        wait_time = 0
        while True:
            now = datetime.today()
            while plane < now:
                plane += timedelta(days=self.bcst.repet_days)
            if plane >= now:
                wait_time = (plane - now).total_seconds()
            time.sleep(wait_time)
            send_msg_all_whatsapp_subs(self.bcst.msg)
            time.sleep(61)


class _ThreadSendDataByTimeout(Thread):
    def __init__(self, info, uid):
        Thread.__init__(self)
        self.info = info
        self.uid = uid
        self._time = 900
        self.is_stopped = False

    def run(self):
        while self._time > 0 and not self.is_stopped:
            time.sleep(2)
            self._time -= 2
            print(self._time)
        if not self.is_stopped:
            self.info.answers.append('Пользователь не завершил процедуру.')
            utils.send_message_admins(self.info)
            utils.send_data_to_uon(self.info, self.uid)

    def stop(self):
        self.is_stopped = True


class ThreadSubs(Thread):
    def __init__(self, uid):
        """Инициализация потока"""
        Thread.__init__(self)
        self.uid = uid

    def run(self):
        vk_doc_link = utils.make_subs_file(self.uid)
        vk.send_message_doc(self.uid, cnst.MSG_SUBS, vk_doc_link)


class SendMsg(Thread):
    def __init__(self, uid, msg, answs, msgr):
        """answs - list of answers"""
        Thread.__init__(self)
        self.uid = uid
        self.msg = msg
        self.msgr = msgr
        self.answs = answs

    def run(self):
        if self.msgr == cnst.VK:
            if self.answs is None or self.answs == '':
                vk.send_message(self.uid, self.msg)
            else:
                vk.send_message_keyboard(self.uid, self.msg, self.answs)
        elif self.msgr == cnst.WHATSAPP:
            if self.answs is None or self.answs == '':
                wapp.send_message(self.uid, self.msg)
            else:
                wapp.send_message_keyboard(self.uid, self.msg, self.answs)
        elif self.msgr == cnst.VIBER:
            if self.answs is None or self.answs == '':
                vib.send_message(self.uid, self.msg)
            else:
                print('answs: ' + self.answs + '\n')
                vib.send_message_keyboard(self.uid, self.msg, self.answs)


class RequestNumberViber(Thread):
    def __init__(self, uid, msg):
        """answs - list of answers"""
        Thread.__init__(self)
        self.uid = uid
        self.msg = msg

    def run(self):
        vib.send_message_request_number(self.uid, self.msg)


def send_message_keyboard(uid, msg, keyboard, msgr=cnst.VK):
    s = SendMsg(uid, msg, keyboard, msgr)
    s.start()


def send_message(uid, msg, msgr=cnst.VK):
    s = SendMsg(uid, msg, answs=None, msgr=msgr)
    s.start()


def send_msg_welcome(uid, msgr=cnst.WHATSAPP):
    msg = db.get_first_msg()
    s = SendMsg(uid, msg, answs=None, msgr=msgr)
    s.start()


def send_last_msge(uid, msgr=cnst.WHATSAPP):
    msg = db.get_last_msg()
    s = SendMsg(uid, msg, answs=None, msgr=msgr)
    s.start()


def send_msg_to_admins(info):
    proc = Process(target=utils.send_message_admins, args=(info,))
    proc.start()


def send_quest(uid, quest, msgr):
    s = SendMsg(uid, quest.quest, quest.answs, msgr)
    s.start()


def _send_msg_all_whatsapp_subs(msg):
    users = db.get_all_users()
    for u in users:
        wapp.send_message(u.number, msg)


def send_msg_all_whatsapp_subs(msg):
    p = Process(target=_send_msg_all_whatsapp_subs, args=(msg,))
    p.start()


def send_keyboard_vk_message(uid, msg, keyboard):
    p = Process(target=vk.send_message_keyboard, args=(uid, msg, keyboard))
    p.start()


def request_user_number_viber(uid, text):
    p = RequestNumberViber(uid, text)
    p.start()