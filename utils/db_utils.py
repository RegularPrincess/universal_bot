#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
import model as m

from main import db

db.create_all()
session = db.session


def get_all_quests():
    q = session.query(m.QuestMsg)
    return q.all()


def get_all_admins():
    q = session.query(m.Admin)
    return q.all()


def get_all_users():
    q = session.query(m.EnrollInfo)
    return q.all()


def get_all_bcsts():
    q = session.query(m.BcstByTime)
    return q.all()


def get_first_msg():
    q = session.query(m.Msgs)
    return q.all()[0].first_msg


def get_congrat_msg():
    q = session.query(m.Msgs)
    return q.all()[0].congrat_msg


def delete_admin(id):
    d = m.Admin.query.filter_by(id=id)
    d.delete()
    session.commit()


def delete_quest(id):
    d = m.QuestMsg.query.filter_by(id=id)
    d.delete()
    session.commit()


def delete_brdcst(id):
    d = m.BcstByTime.query.filter_by(id=id)
    d.delete()
    session.commit()


def update_first_msg(text):
    msg = session.query(m.Msgs)
    msg[0].first_msg = text
    session.commit()


def update_congrat_msg(text):
    msg = session.query(m.Msgs)
    msg[0].congrat_msg = text
    session.commit()


def add_any(obj):
    try:
        db.session.add(obj)
        db.session.commit()
    except sqlalchemy.exc.InvalidRequestError as e:
        db.session.rollback()
        print(e)
    except BaseException as e:
        db.session.rollback()
        print(e)


def is_admin(uid):
    admins = get_all_admins()
    for a in admins:
        if uid == a.uid:
            return True
    return False


def is_new_user(uid):
    d = session.query(m.EnrollInfo).filter_by(uid=uid).first()
    return d is None


def is_quest_msg_empty():
    return len(get_all_quests()) < 2


def_admin = m.Admin('Юрий', '259056624')
add_any(def_admin)
f_msg = m.Msgs('Приветственное сообщение', 'Поздравительное сообщнеие!')
add_any(f_msg)
if is_quest_msg_empty():
    add_any(m.QuestMsg('В каком месяце у вас день рождение? (Введите число от 1 до 12)'))
    add_any(m.QuestMsg('Какого числа у вас день рождение? (Введите число от 1 до 31)'))
