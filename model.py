#!/usr/bin/python
# -*- coding: utf-8 -*-

import consts as cnst
import datetime as dt
from main import db


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    uid = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<Admin %r>' % (self.name)


class QuestMsg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quest = db.Column(db.UnicodeText, index=True)
    answs = db.Column(db.UnicodeText)

    def __repr__(self):
        return '<QuestMsg %r>' % (self.quest)


class BcstByTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DATE)
    time = db.Column(db.TIME)
    repet_days = db.Column(db.INTEGER)
    msg = db.Column(db.UnicodeText)

    def __repr__(self):
        return '<BcstByTime %r>' % (self.msg)


class Msgs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_msg = db.Column(db.UnicodeText)

    def __repr__(self):
        return '<Msgs %r>' % (self.first_msg)


class EnrollInfo:
    def __init__(self, uid):
        self.uid = uid
        self.number = None
        self.answers = []
