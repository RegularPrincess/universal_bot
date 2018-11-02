import time
from multiprocessing import Process
from threading import Thread

from datetime import datetime, timedelta

import requests

from utils import db_utils as db
import consts as cnst
import utils.chat_libs.vklib as vk
import utils.chat_libs.whatsapplib as wapp
import utils.service_utils as utils


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


class ThreadDropUserAfterTime(Thread):
    def __init__(self, redy_to_enroll):
        """Инициализация потока"""
        Thread.__init__(self)
        self.redy_to_enroll = redy_to_enroll

    def run(self):
        print('run\n')
        while True:
            keys_to_remove = []
            for key in self.redy_to_enroll.keys():
                print(key)
                self.redy_to_enroll[key].minut_to_drop -= 1
                if self.redy_to_enroll[key].minut_to_drop <= 0:
                    keys_to_remove.append(key)
            for k in keys_to_remove:
                del self.redy_to_enroll[k]
            time.sleep(60)


def send_message(uid, msg, msgr=cnst.VK):
    # keyboard - list buttons
    if msgr == cnst.VK:
        p = Process(target=vk.send_message, args=(uid, msg))
        p.start()
    elif msgr == cnst.WHATSAPP:
        p = Process(target=wapp.send_message, args=(uid, msg))
        p.start()
    else:
        pass


def send_message_keyboard(uid, msg, keyboard, msgr=cnst.VK):
    # keyboard - list buttons
    if msgr == cnst.VK:
        p = Process(target=vk.send_message_simple_keyboard, args=(uid, msg, keyboard))
        p.start()
    elif msgr == cnst.WHATSAPP:
        p = Process(target=wapp.send_message_keyboard, args=(uid, msg, keyboard))
        p.start()
    else:
        pass


def send_keyboard_vk_message(uid, msg, keyboard):
    p = Process(target=vk.send_message_keyboard, args=(uid, msg, keyboard))
    p.start()


def send_msg_all_whatsapp_subs(msg):
    p = Process(target=_send_msg_all_whatsapp_subs, args=(msg,))
    p.start()

def send_msg_welcome(uid, out=cnst.WHATSAPP):

    if out == cnst.WHATSAPP:
        pass
        # отправить приветствие через ватсапп
    elif out == cnst.TG:
        pass
        # отправить приветствие через телеграмм
    elif out == cnst.SMS:
        pass
        # отправить приветствие через SMS


def send_msg_to_admins(info):
    proc = Process(target=utils.send_message_admins, args=(info,))
    proc.start()


def _send_msg_all_whatsapp_subs(msg):
    users = db.get_all_users()
    for u in users:
        wapp.send_message(u.number, msg)


def send_msg_by_file(text, link):
    return None