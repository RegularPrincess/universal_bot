#!/usr/bin/python
# -*- coding: utf-8 -*-

from main import db


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    uid = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<Admin %r>' % (self.name)

    def __init__(self, name, uid, id=None):
        if id is not None: self.id = id
        self.name = name
        self.uid = uid


class QuestMsg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quest = db.Column(db.UnicodeText, index=True)
    answs = db.Column(db.UnicodeText)

    def __init__(self, quest='', answs='', id=None):
        self.id = id
        self.quest = quest
        self.answs = answs

    def __repr__(self):
        return '<QuestMsg %r>' % (self.quest)


class BcstByTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DATE)
    time = db.Column(db.TIME)
    repet_days = db.Column(db.INTEGER)
    msg = db.Column(db.UnicodeText)
    target = db.Column(db.UnicodeText)

    def __repr__(self):
        return '<BcstByTime %r>' % (self.msg)

    def date_time_is_not_sign(self):
        return self.start_date is None


class Msgs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    congrat_msg = db.Column(db.UnicodeText)
    first_msg = db.Column(db.UnicodeText)
    first_msg_answs = db.Column(db.UnicodeText)
    last_msg = db.Column(db.UnicodeText)
    unic = db.Column(db.INTEGER, unique=True, default=1)

    def __init__(self, first_msg, congrat_msg, last_msg, first_msg_answs='0'):
        self.first_msg = first_msg
        self.congrat_msg = congrat_msg
        self.last_msg = last_msg
        self.first_msg_answs = first_msg_answs


    def __repr__(self):
        return '<Msgs %r>' % (self.first_msg)


class EnrollInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(50))
    number = db.Column(db.String(20))
    answers = db.Column(db.TEXT)
    msgr = db.Column(db.INTEGER)

    def __init__(self, number, uid=None, id=None, answers='', msgr=None):
        self.id = id
        self.uid = uid
        self.number = number
        self.answers = answers
        self.msgr = msgr

    def __repr__(self):
        return '<EnrollInfo %r>' % (self.number)


class EnrollObj:
    def __init__(self, enroll_info, quests, need_birthday=True, first_time=False):
        self.ei = enroll_info
        self.qsts = quests
        self.last_variants = None
        self.need_birthday = need_birthday
        self.skip_next_answ = False
        self.minut_to_drop = 29
        self.first_time = first_time