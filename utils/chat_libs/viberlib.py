from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import (
    TextMessage,
    KeyboardMessage
)
import copy

bot_configuration = BotConfiguration(
    name='Халва Бета',
    avatar='http://viber.com/avatar.jpg',
    auth_token='489dfb600267d384-f945b37ddf43e01c-450da3b3f85de11a'
)
viber = Api(bot_configuration)


# res = viber.set_webhook('https://8922388106.com/test/incoming')
# print(res)


def parse_request(request):
    try:
        viber_request = viber.parse_request(request.get_data())
        return viber_request
    except BaseException:
        return None


def send_message(uid, text):
    text_message = TextMessage(text=text)
    viber.send_messages(uid, [text_message])


def get_keyboard_from_list(list_btn):
    keyboard = copy.deepcopy(_keyboard)
    column = 1
    row = 1
    for b in list_btn:
        new_btn = copy.deepcopy(_btn)
        new_btn['ActionBody'] = b
        new_btn['Text'] = b
        new_btn["Columns"] = column
        new_btn['Rows'] = row
        keyboard['Buttons'].append(new_btn)
        if row == 6 and column == 2:
            return keyboard
        if row < 6:
            row += 1
        else:
            row = 1
            column = 2
    return keyboard


def send_message_request_number(uid, text):
    msg = KeyboardMessage(keyboard=_keyboard_request_number)
    text_mse = TextMessage(text=text)
    viber.send_messages(to=uid, messages=[text_mse, msg])


def send_message_keyboard(uid, text, keyboard):
    k = get_keyboard_from_list(keyboard.split('; '))
    msg = KeyboardMessage(keyboard=k)
    text_mse = TextMessage(text=text)
    viber.send_messages(to=uid, messages=[text_mse, msg])


_keyboard = {
    "Type": "keyboard",
    "DefaultHeight": True,
    "Buttons": []
}

_btn = {
    "ActionType": "reply",
    "ActionBody": "",
    "Text": "",
    "TextSize": "regular",
    "Columns": 1,
    "Rows": 1
    # /var/www/html;
}

_keyboard_request_number = {
    "Type": "keyboard",
    "DefaultHeight": True,
    "Buttons":
        [
            {
                "ActionType": "share-phone",
                "ActionBody": "reply",
                "Text": "Отправить номер телефона",
                "TextSize": "regular",
                "Columns": 1,
                "Rows": 1
            }
        ]

}
