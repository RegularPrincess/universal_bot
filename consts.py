#!/usr/bin/env python3
## -*- coding: utf-8 -*-

# Кнопки
import model as m
BTN_CANCEL = "⛔ Отмена"
BTN_BROADCAST = "Рассылка"
BTN_ADD_ADMIN = "Добавить администратора"
BTN_ADMINS = "Администраторы"
BTN_SUBS = "Подписчики"
BTN_MENU = "Меню пользователя"
BTN_ADD_BROADCAST_BY_TIME = 'Создать рассылку по расписанию'
BTN_BROADCAST_BY_TIME = 'Запланированные рассылки'
BTN_LEAVE_REASON = 'Причины отписки'
BTN_QUESTIONS = 'Вопросы пользователю'
BTN_END = 'Закончить'
BTN_SKIP = 'Пропустить'
BTN_FIRST_MSG_EDIT = "Ред-ть приветственное сообщение"
BTN_MAIL_MSG_EDIT = "Ред-ть запрос email"
BTN_NUMBER_MSG_EDIT = "Ред-ть запрос номера"
BTN_FIRST_BTN_EDIT = "Ред-ть текст кнопки"
BTN_COLOR_BTN_EDIT = 'Ред-ть цвет кнопки'
__COLOR_BTN = "positive"
__BTN_ENROLL = "Записаиться на занятие"


BTN_COLORS_MAP = {"Синий": "primary",
                  "Белый": "default",
                  "Красный": "negative ",
                  "Зеленый": "positive"}

START_WORDS = ['start', 'начать', 'старт',
               'привет', 'привет!', 'привет.',
               'здравствуйте', 'здравствуйте.', 'здравствуйте!']
USER_ACCEPT_WORDS = ['да', 'конечно', 'хочу']

# Сообщения для пользователя
MSG_WELCOME_FOLLOWER = 'Здравствуйте! {}, подберём вам лучший тур за один день 🙂'
MSG_ACCEPT_NAME = 'Напишите, пожалуйста, как к Вам обращаться?'
MSG_ACCEPT_EMAIL = 'Введите, пожалуйста, адрес Вашей електронной почты (email) 📧'
MSG_ACCEPT_NUMBER = 'Введите, пожалуйста, Ваш номер телефона ☎'
MSG_ENROLL_COMPLETED = 'Спасибо, {}! ' \
                       'Мы очень ценим, что Вы выбрали нас! В ближайшее время наш сотрудник свяжется с Вами!'
MSG_CANCELED_MESSAGE = 'Действие успешно отменено.'
MSG_DEFAULT_ANSWER = 'Ничего не понятно('
MSG_PLEASE_STAND_BY = 'Это может занять некоторое время...'
MSG_MEMBERS_COUNT = 'Пользователей в группе - {0}'
MSG_ADDED_COUNT = 'Команда parsegroup завершена. Пользователи добавлены в базу.'
MSG_UNCORECT_NUMBER = '❗ Данный формат номера телефона не распознан! \n' \
                      'Пожалуйста введите в формате +7 321 123456789, либо 8 (код города) 111 11 11'
MSG_UNCORECT_EMAIL = '❗ Адрес электронной почты не распознан. Введите, пожалуйста, в формате example@domain.ru'
MSG_LEAVING = '😢 Сообщите, пожалуйса, причину по которой вы покидайте нашу группу' \
              ' или выберите вариант из предложенного списка.'
MSG_THANK_YOU = 'Спасибо!'
MSG_SUBS = '🔥 ПОДПИСЧИКИ БОТА 🔥'
DEFAULT_QUESTS = [m.QuestMsg(quest=MSG_ACCEPT_EMAIL), m.QuestMsg(quest=MSG_ACCEPT_NUMBER)]

# Статусы подписчиков
USER_LEAVE_STATUS = 'leave'
USER_SUB_STATUS = 'member'
USER_RETURN_STATUS = 'return'
USER_NOT_SUB_STATUS = 'notmember'

# Сообщения для администраторов
NOTIFY_ADMIN = 'Пользователь с id{} записался на подбор тура. \n\n' \
               'Его данные: \n🖐 обращение - {},\n📧 email - {},\n☎ номер телефона - {}.\n{}'
ADMIN_KEY_WORDS = ['admin', 'админ']
MSG_YOU_NOT_ADMIN = 'Вы не являйтесь администратором.'
MSG_ADMIN_EXIT = 'Выйти из меню администратора'
MSG_ACCEPT_BROADCAST = '🖊 Введите сообщение для рассылки:'
MSG_BROADCAST_COMPLETED = 'Сообщение разослано {} пользователям.'
MSG_ADMIN_REMOVING = '🐩 Для удаления администратора введите его номер ID'
MSG_VALUE_ERROR = 'Не корректно! Введите только цифры id.'
MSG_ADMIN_REMOVED = 'Администратор успешно удален!'
CMD_PARSE_GROUP = 'parsegroup'
MSG_ADMIN_ADDING = '🔥 ДОБАВИТЬ АДМИНИСТРАТОРА: 🔥\n\n' \
                   '🔑 ВВЕДИТЕ id НОВОГО АДМИНИСТРАТОРА БОТА. \n' \
                   'id – ЭТО ЧИСЛОВОЕ ЗНАЧЕНИЕ ПОСЛЕ https://vk.com/id.\n\n' \
                   '👉 НАПРИМЕР: В СЛУЧАЕ ПОЛНОГО id: https://vk.com/id12345678 ' \
                   'НЕОБХОДИМО ВВЕСТИ: 12345678'
MSG_ADMIN_SUCCCES_ADDED = "Администратор успешно добавлен"
MSG_SERVER_RESTARTED = 'Сервер перезапущен'
MSG_ADMINS = '🔥 СПИСОК АДМИНИСТРАТОРОВ: 🔥 \n\n'
MSG_USER_SHORT_INFO = '👉 Количество участников в группе: {} \n' \
                      '👍 Рассылка возможна {} участникам'
MSG_ADD_BRDCST_BY_TIME = "👉 Введите дату с которой следует начать рассылку, " \
                         "затем время рассылки(мск), " \
                         "затем количество дней через котрое рассылка будет повторена.\n\n" \
                         "👉 Пример: 22.08.2018 15:22 3"
MSG_PLANNED_BCST = 'Дата начала - {}, время - {}, периодичность повторений (дней) - {}, id - {}\n' \
                   '🖊 Сообщение - {} \n\n'
MSG_USER_LEAVED = 'Пользоваетль {} id{} покинул группу, указав причину: \"{}\"'
MSG_ACCEPT_QUEST_MSG = '👉 Для удаления вопроса отправьте цифры ID. \n\
                        👉 Для добавления нового отправьте текст вопроса.\n' \
                       '👉 Для изменения - ID и текст нового вопроса через пробел.\n' \
                       '(Вопросы о телефне и email всегда присутствуют и выводятся в конце опроса. ' \
                       'Используйте {} для обращения к пользователю)'
MSG_ADDING_ANSWS_VAR = '🖊 Вы можете добавить варианты ответов к вопросу, отправив их через точку с запятой.\n' \
                       '👉 ПРИМЕР: Турция; Алжир; Куба' \
                       '\n👉 Или закончить создания вопроса, нажав на кнопку.'
MSG_GROUP_JOIN = '''
Приветствуем, {!s}! 
'''
GROUP_LEAVE_MESSAGE = '''
Ждем тебя снова!
'''
MSG_LEAVE_REASON = "👉 Текущие возможные причины: \n\n {} " \
                   "\n\n🖊 Вы можете заменить эти причины, " \
                   "отправив новые, разделенные точкой с запятой (до 7 вариантов)\n\n" \
                   "👉 ПРИМЕР: Просто так; Надоела рассылка; Тема больше не интересна"
MSG_LEAVE_REASON_SAVED = "Причины отписки успешно сохранены (старые удалены). Количество - {}."
# MSG_LEAVE_REASON_NOT_SAVED = "Причины не указаны"


# Клавиатуры
EMPTY_KEYBOARD = ''

one_button_pattern = [{
    "action": {
        "type": "text",
        "payload": "{\"button\": \"3\"}",
        "label": ""
    },
    "color": "default"
}]
enroll_btn = [{
    "action": {
        "type": "text",
        "payload": "{\"button\": \"1\"}",
        "label": __BTN_ENROLL
    },
    "color": __COLOR_BTN
}]

cancel_btn = [{
    "action": {
        "type": "text",
        "payload": "{\"button\": \"1\"}",
        "label": BTN_CANCEL
    },
    "color": "default"
}]

keyboard_pattern = \
    {
        "one_time": False,
        "buttons": []
    }

KEYBOARD_USER = {
    "one_time": False,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": __BTN_ENROLL
            },
            "color": __COLOR_BTN
        }],
    ]
}

KEYBOARD_CANCEL = {
    "one_time": False,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": BTN_CANCEL
            },
            "color": "default"
        }]
    ]
}

KEYBOARD_CANCEL_AND_MSG_EDIT = {
    "one_time": False,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": BTN_CANCEL
            },
            "color": "default"
        }],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": BTN_FIRST_MSG_EDIT
            },
            "color": "default"
        }],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": BTN_MAIL_MSG_EDIT
            },
            "color": "default"
        },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"1\"}",
                    "label": BTN_NUMBER_MSG_EDIT
                },
                "color": "default"
            }
        ],
[{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": BTN_FIRST_BTN_EDIT
            },
            "color": "default"
        },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"1\"}",
                    "label": BTN_COLOR_BTN_EDIT
                },
                "color": "default"
            }
        ]
    ]
}

MSG_ADMIN_PANEL = '''🔥 ПАНЕЛЬ АДМИНИСТРАТОРА 🔥'''

KEYBOARD_END_AND_CANCELE = {
    "one_time": False,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": BTN_END
            },
            "color": "default"
        }],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": BTN_CANCEL
            },
            "color": "default"
        }]
    ]
}

KEYBOARD_END_AND_SKIP = {
    "one_time": False,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": BTN_SKIP
            },
            "color": "default"
        }],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": BTN_CANCEL
            },
            "color": "default"
        }]
    ]
}

KEYBOARD_ADMIN = {
    "one_time": False,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": BTN_BROADCAST
            },
            "color": "default"
        },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": BTN_SUBS
                },
                "color": "default"
            }],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"3\"}",
                "label": BTN_ADMINS
            },
            "color": "default"
        },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"4\"}",
                    "label": BTN_ADD_ADMIN
                },
                "color": "default"
            }],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"6\"}",
                "label": BTN_ADD_BROADCAST_BY_TIME
            },
            "color": "default"
        },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"7\"}",
                    "label": BTN_BROADCAST_BY_TIME
                },
                "color": "default"
            }],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"4\"}",
                "label": BTN_LEAVE_REASON
            },
            "color": "default"
        },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"5\"}",
                    "label": MSG_ADMIN_EXIT
                },
                "color": "default"
            }],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"4\"}",
                "label": BTN_QUESTIONS
            },
            "color": "default"
        }]]
    # {
    #     "action": {
    #         "type": "text",
    #         "payload": "{\"button\": \"5\"}",
    #         "label": MSG_ADMIN_EXIT
    #     },
    #     "color": "default"
    # }]
    # ]
}
