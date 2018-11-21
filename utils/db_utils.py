#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
import model as m

from main import db


# m.Msgs.__table__.drop(db.engine)
db.create_all()
session = db.session


def get_all_quests():
    q = db.session.query(m.QuestMsg)
    return q.all()


def get_all_admins():
    q = db.session.query(m.Admin)
    return q.all()


def get_all_users():
    q = db.session.query(m.EnrollInfo)
    return q.all()


def get_all_bcsts():
    q = db.session.query(m.BcstByTime)
    return q.all()


def get_first_msg():
    q = db.session.query(m.Msgs)
    return q.all()[0].first_msg


def get_first_msg_answs():
    q = db.session.query(m.Msgs)
    answs = q.all()[0].first_msg_answs
    if answs is not None and len(answs) > 3:
        return answs
    else:
        return ''


def get_congrat_msg():
    q = db.session.query(m.Msgs)
    return q.all()[0].congrat_msg


def get_last_msg():
    q = db.session.query(m.Msgs)
    return q.all()[0].last_msg


def delete_admin(id):
    d = m.Admin.query.filter_by(id=id)
    d.delete()
    session.commit()


def delete_user_by_num(num):
    d = m.EnrollInfo.query.filter_by(number=num)
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
    msg = db.session.query(m.Msgs)
    msg[0].first_msg = text
    session.commit()


def update_first_msg_answs(text):
    msg = db.session.query(m.Msgs)
    msg[0].first_msg_answs = text
    session.commit()


def update_congrat_msg(text):
    msg = db.session.query(m.Msgs)
    msg[0].congrat_msg = text
    session.commit()


def update_last_msg(text):
    msg = db.session.query(m.Msgs)
    msg[0].last_msg = text
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


def update_user(user, uid):
    u = db.session.query(m.EnrollInfo).filter_by(uid=uid).first()
    u.answers = user.answers
    print(user.answers)
    u.uid = user.uid
    print(u)
    session.commit()


def update_admin(name, uid):
    u = db.session.query(m.Admin).filter_by(uid=uid).first()
    u.name = name
    session.commit()


def update_quest(quest_msg, id):
    u = db.session.query(m.QuestMsg).filter_by(id=id).first()
    u.quest = quest_msg.quest
    u.answs = quest_msg.answs
    session.commit()


# update_admin('new name', '480542758')


def is_admin(uid):
    admins = get_all_admins()
    for a in admins:
        if uid == a.uid:
            return True
    return False


def is_new_user(uid):
    d = db.session.query(m.EnrollInfo).filter_by(uid=uid).first()
    return d is None


def is_quest_msg_empty():
    return len(get_all_quests()) < 2


def_admin = m.Admin('Юрий', '259056624')
add_any(def_admin)
f_msg = m.Msgs('Приветственное сообщение', 'Поздравительное сообщнеие!', "Спасибо, что уделили время!")
add_any(f_msg)
# if is_quest_msg_empty():
#     add_any(m.QuestMsg('В каком месяце у вас день рождение? (Введите число от 1 до 12). '
#                        'Или отправьте "Нет", если хотите пропустить вопросы о дне рождении.'))
#     add_any(m.QuestMsg('Какого числа у вас день рождение? (Введите число от 1 до 31)'))


def add_birthday_quests():
    quests = copy.deepcopy(get_all_quests())
    db.session.query(m.QuestMsg).delete()
    db.session.commit()

    add_any(m.QuestMsg('В каком месяце у вас день рождение? (Введите число от 1 до 12). '
                           'Или отправьте "Нет", если хотите пропустить вопросы о дне рождении.'))
    add_any(m.QuestMsg('Какого числа у вас день рождение? (Введите число от 1 до 31)'))
    for q in quests:
        add_any(m.QuestMsg(quest=q.quest, answs=q.answs))
    d = get_all_quests()
    print(d)

add_birthday_quests()