import time
from multiprocessing import Process
from threading import Thread

import consts as cnst
import utils.chat_libs.vklib as vk
import utils.chat_libs.whatsapplib as wapp
import utils.service_utils as su
import utils.service_utils as us


# class ThreadManager:
#     def __init__(self):
#         self.bcst_threads = []
#
#     def run_brdcst_shedule(self):
#         bcst = db.get_bcsts_by_time()
#         self.bcst_threads = []
#         for b in bcst:
#             self.bcst_threads.append(ThreadBrdcst(b))
#         for bt in self.bcst_threads:
#             bt.start()
#
#     def add_brcst_thread(self, bcst):
#         db.add_bcst(bcst)
#         self.run_brdcst_shedule()
#
#     def delete_brcst(self, id):
#         db.delete_bcst(id)
#         self.run_brdcst_shedule()
#
#
# class ThreadBrdcst(Thread):
#     def __init__(self, bcst):
#         """Инициализация потока"""
#         Thread.__init__(self)
#         self.bcst = bcst
#
#     def run(self):
#         day = self.bcst.start_date
#         time_ = self.bcst.time
#         plane = datetime.combine(day, time_)
#         wait_time = 0
#         while True:
#             now = datetime.today()
#             while plane < now:
#                 plane += timedelta(days=self.bcst.repet_days)
#             if plane >= now:
#                 wait_time = (plane - now).total_seconds()
#             time.sleep(wait_time)
#             us.emailing_to_all_subs_keyboard(self.bcst.msg)
#             time.sleep(61)


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
            us.send_message_admins(self.info)
            us.send_data_to_uon(self.info, self.uid)

    def stop(self):
        self.is_stopped = True


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
    proc = Process(target=su.send_message_admins, args=(info,))
    proc.start()


def first_send(num, msg):
    proc = Process(target=su.first_send, args=(num, msg))
    proc.start()