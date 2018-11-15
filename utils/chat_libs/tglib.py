from telethon import TelegramClient, sync
from telethon.tl.functions.channels import InviteToChannelRequest

api_id = 384524
api_hash = '6fd9e886360d69bc24a8076665cdd496'

client = TelegramClient('MYSESSION228', api_id, api_hash).start()
print(client.get_me().stringify())

user = client.get_entity('+79991577222')
channel = client.get_entity('autoinvitetest')

# Add users.
result = client(InviteToChannelRequest(
    channel,
    [user]
))
print(result)
#
# import telebot
# import telebot.types as types
# import utils as u
#
# bot = telebot.TeleBot("645100799:AAHr08yGqhY8PxAjeSJSdPiUZ-D2MgcB3i8")
# USERS = {}
# ADMINS = []
# INADMINMENU = {}
# Questions = []
# Questions.append(u.Question("Введите ваше имя, пожалуйста"))
# Questions.append(u.Question("Выберите город доставки или введите свой вариант",
#                             ["Казань", "Бугульма", "Зеленодольск", "Альметьевск"]))
# Questions.append(u.Question("Уточните улицу и дом"))
# Questions.append(u.Question("Уточните время доставки", ["Утро", "День", "Вечер"]))
#
#
# def send_to_admins(user):
#     for a in ADMINS:
#         msg = "Пользователь прошел опрос. Его ответы: \n"
#         for ans in user.answs:
#             msg += ans + ", "
#         if len(user.answs) < 1:
#             msg += "<Еще нет вопросов>"
#         bot.send_message(a, msg)
#
#
# # Обработчик команд '/start' и '/imadmin'.
# @bot.message_handler(commands=['start'])
# def handle_start_help(message):
#     bot.send_message(message.from_user.id, "Здравствуйте, вас приветствует тестовый бот, "
#                                            "который поможет вам опросить клиентов. ")
#     markup = u.get_keyboard(["Да", "Нет"])
#     bot.send_message(message.from_user.id, "Вам будет задан ряд вопросов, вы готовы?", reply_markup=markup)
#     USERS[message.from_user.id] = u.User()
#
#
# @bot.message_handler(commands=['imadmin'])
# def handle_start_help(message):
#     bot.send_message(message.from_user.id, "Теперь вы админ этого бота и "
#                                            "будете получать информацию о пользователях прошедших опрос"
#                                            "и сможете попасть в меню управления ботом по команде /admin")
#     ADMINS.append(message.from_user.id)
#
#
# @bot.message_handler(commands=['imnotadmin'])
# def handle_start_help(message):
#     bot.send_message(message.from_user.id, "Теперь вы не админ этого бота")
#     ADMINS.remove(message.from_user.id)
#
#
# @bot.message_handler(commands=['admin'])
# def handle_start_help(message):
#     if message.from_user.id in ADMINS:
#         markup = u.get_keyboard(["Существующие вопросы", "Добавить вопрос", "Отмена"])
#         bot.send_message(message.from_user.id, "Меню администратора \n"
#                                                "(Визуальное представление меню, "
#                                                "логика и способы взаимодействия c ботом являются "
#                                                "демо-вариантами и могут быть изменены)", reply_markup=markup)
#     else:
#         bot.send_message(message.from_user.id, "Вы не администратор")
#
#
# @bot.message_handler(content_types=["text"])
# def handle_text(message):
#     uid = message.from_user.id
#     if message.from_user.id not in USERS:
#         USERS[message.from_user.id] = u.User()
#
#     if message.text == "Отмена" and uid in ADMINS:
#
#         if uid in INADMINMENU:
#             if INADMINMENU[uid] != '':
#                 INADMINMENU[uid] = ''
#                 markup = u.get_keyboard(["Существующие вопросы", "Добавить вопрос", "Отмена"])
#                 bot.send_message(message.from_user.id, "Меню администратора \n"
#                                                        "(Визуальное представление меню, "
#                                                        "логика и способы взаимодействия c ботом являются "
#                                                        "демо-вариантами и могут быть изменены)", reply_markup=markup)
#                 return
#
#             bot.send_message(message.from_user.id, "Чтобы начать "
#                                                    "опрос введите команду /start", reply_markup=u.get_keyboard([]))
#         return
#
#     if message.text == "Существующие вопросы" and uid in ADMINS:
#         msg = "Текущие вопросы в боте: \n\n"
#         print(Questions)
#         for i in range(0, len(Questions)):
#             q = Questions[i]
#             msg += "(№ {}) ".format(i)
#             msg += '{} \n Ответы: {}\n\n'.format(q.text, ", ".join(q.answers))
#         msg += "Для удаления вопроса отправьте его номер."
#         INADMINMENU[uid] = "Существующие вопросы"
#         markup = u.get_keyboard(["Отмена"])
#         print(msg)
#         bot.send_message(uid, msg, reply_markup=markup)
#         return
#
#     if message.text == "Добавить вопрос" and uid in ADMINS:
#         INADMINMENU[uid] = "Добавить вопрос"
#         msg = "Для добавления вопроса введите текст нового вопроса, " \
#               "затем в скобках варианты через запятую, если требуется. \n\n" \
#               "Пример: Введите ваш возраст (12 лет, 21 год, 45, более 50-ти)\n\n" \
#               "(строгие требования к написанию вопроса относятся лишь к существующему "\
#                 "прототипу и в дальнейшем ввод вопросов будет упрощен)"
#         markup = u.get_keyboard(["Отмена"])
#         print(msg)
#         bot.send_message(uid, msg, reply_markup=markup)
#         return
#
#     if uid in INADMINMENU:
#         if INADMINMENU[uid] == "Существующие вопросы":
#             if u.isint(message.text):
#                 id = int(message.text)
#                 Questions.remove(Questions[id])
#                 msg = "Вопрос удален"
#                 bot.send_message(uid, msg)
#                 # markup = u.get_keyboard(["/start"])
#                 # bot.send_message(message.from_user.id, "Нажмите на кнопку старт чтоб начать "
#                 #                                        "опрос или введите команду /start", reply_markup=markup)
#                 markup = u.get_keyboard(["Существующие вопросы", "Добавить вопрос", "Отмена"])
#                 bot.send_message(message.from_user.id, "Меню администратора \n"
#                                                        "(Визуальное представление меню, "
#                                                        "логика и способы взаимодействия c ботом являются "
#                                                        "демо-вариантами и могут быть изменены)", reply_markup=markup)
#                 # INADMINMENU[uid] = ""
#                 return
#             else:
#                 msg = "Для удаления вопроса отправьте его номер."
#                 bot.send_message(uid, msg)
#                 return
#         if INADMINMENU[uid] == "Добавить вопрос":
#             try:
#                 t = message.text
#                 tq = t.split(' (')[0]
#                 if len(t.split(' (')) > 1:
#                     ta = t.split(' (')[1][:-1]
#                     ta_arr = ta.split(', ')
#                     if len(ta_arr[0]) > 0:
#                         Questions.append(u.Question(tq, ta_arr))
#                     else:
#                         Questions.append(u.Question(tq))
#                 else:
#                     Questions.append(u.Question(tq))
#                 markup = u.get_keyboard(["/start"])
#                 bot.send_message(uid, "Вопрос добавлен", reply_markup=markup)
#                 INADMINMENU[uid] = ""
#             except Exception:
#                 bot.send_message(uid, "Пожалуйста следуйте требованиям при написании вопроса "
#                                       "(строгие требования относятся лишь к существующему "
#                                       "прототипу и в дальнейшем ввод вопросов будет упрощен)")
#                 return
#
#     if message.text.lower() == "да":
#         if len(Questions) > 0:
#             USERS[message.from_user.id].question = Questions[0]
#             markup = u.get_keyboard(USERS[uid].question.answers)
#             bot.send_message(uid, USERS[uid].question.text, reply_markup=markup)
#         else:
#             markup = u.get_keyboard([])
#             bot.send_message(uid, "В боте еще не заданы вопросы", reply_markup=markup)
#         if len(Questions) > 1:
#             USERS[uid].question = Questions[1]
#             USERS[uid].q_index = 1
#         else:
#             USERS[uid].is_last_quest = True
#         return
#
#     if not USERS[uid].is_last_quest and USERS[message.from_user.id].question is not None:
#         USERS[uid].answs.append(message.text)
#         # if USERS[uid].question is None:
#         #     USERS[uid].question = Questions[0]
#         #     USERS[uid].q_index = 0
#         markup = u.get_keyboard(USERS[uid].question.answers)
#         bot.send_message(uid, USERS[uid].question.text, reply_markup=markup)
#         if len(Questions) > USERS[uid].q_index + 1:
#             USERS[uid].q_index += 1
#             USERS[uid].question = Questions[USERS[uid].q_index]
#         else:
#             USERS[uid].is_last_quest = True
#         return
#
#     if USERS[uid].is_last_quest:
#         # markup = u.get_keyboard(["/start"])
#         markup = types.ReplyKeyboardRemove(selective=False)
#         bot.send_message(message.from_user.id, "Спасибо, за пройденный опрос", reply_markup=u.get_keyboard([]))
#         send_to_admins(USERS[message.from_user.id])
#         USERS[message.from_user.id] = u.User()
#
#     if message.text.lower() == "нет":
#         markup = u.get_keyboard(["/start"])
#         bot.send_message(message.from_user.id, "Нажмите на кнопку старт чтоб начать "
#                                                "опрос или введите команду /start", reply_markup=markup)
#         return
#         #
#         # elif USERS[message.from_user.id].name is None:
#         #     USERS[message.from_user.id].name = message.text
#         #     markup = u.get_keyboard(["Казань", "Бугульма", "Зеленодольск", "Альметьевск"])
#         #     msg = "{}, выберите город доставки или введите свой вариант".format(USERS[message.from_user.id].name)
#         #     bot.send_message(message.from_user.id, msg, reply_markup=markup)
#         #
#         # elif USERS[message.from_user.id].city is None:
#         #     USERS[message.from_user.id].city = message.text
#         #     markup = types.ReplyKeyboardRemove(selective=False)
#         #     bot.send_message(message.from_user.id, "Уточните улицу и дом", reply_markup=markup)
#         #
#         # elif USERS[message.from_user.id].detail is None:
#         #     USERS[message.from_user.id].detail = message.text
#         #     markup = u.get_keyboard(["Пропустить"])
#         #     msg = "Сообщите, пожалуйста, ваш email или вы можете пропустить этот шаг"
#         #     bot.send_message(message.from_user.id, msg, reply_markup=markup)
#         #
#         # elif USERS[message.from_user.id].email is None:
#         #     if message.text == "Пропустить":
#         #         USERS[message.from_user.id].email = "Пропущено"
#         #     elif u.is_email_valid(message.text):
#         #         USERS[message.from_user.id].email = message.text
#         #
#         #         # u.del_uid_from_dict(message.from_user.id, USERS)
#         #     else:
#         #         bot.send_message(message.from_user.id, "❗ Адрес электронной почты не распознан. "
#         #                                                "Введите, пожалуйста, в формате example@domain.ru")
#         #     if USERS[message.from_user.id].email is not None:
#         #         markup = u.get_keyboard(["/start"])
#         #         # markup = types.ReplyKeyboardRemove(selective=False)
#         #         bot.send_message(message.from_user.id, "Спасибо, за пройденный опрос", reply_markup=markup)
#         #         send_to_admins(USERS[message.from_user.id])
#         #         USERS[message.from_user.id] = u.User()
#         # else:
#         #     pass
#
#
# #
# # # Обработчик для документов и аудиофайлов
# # @bot.message_handler(content_types=['document', 'audio'])
# # def handle_document_audio(message):
# #     pass
#
# bot.polling(none_stop=True, interval=0)



# from telethon import TelegramClient, sync
# from telethon.tl.functions.channels import InviteToChannelRequest
#
# api_id = 384524
# api_hash = '6fd9e886360d69bc24a8076665cdd496'
#
# client = TelegramClient('MYSESSION228', api_id, api_hash).start()
# print(client.get_me().stringify())
#
# user = client.get_entity('+79179052684')
# channel = client.get_entity('autoinvitetest')
#
# # Add users.
# result = client(InviteToChannelRequest(
#     channel,
#     [user]
# ))
# # u = channels.InviteToChannelRequest("autoinvitetest", "tomatokiller")
# # print(u.users)
# # print(u.channel)
# # client.send_message('tomatokiller', 'Hello! Talking to you from Telethon')

