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
# viber = Api(bot_configuration)
# res = viber.set_webhook('https://8922388106.com/test/incoming')
# print(res)


def parse_request(request):
    try:
        viber_request = viber.parse_request(request.get_data())
        return viber_request
    except BaseException:
        return None


def send_message(uid, text):
    text_message = TextMessage(text)
    viber.send_messages(uid, [text_message])


def get_keyboard_from_list(list_btn):
    keyboard = copy.deepcopy(_keyboard)
    for b in list_btn:
        new_btn = copy.deepcopy(_btn)
        new_btn['ActionBody'] = b
        new_btn['Text'] = b
        keyboard['keyboard']['Buttons'].append(new_btn)
    return keyboard


def send_message_keyboard(uid, text, keyboard):
    send_message(uid, text)
    k = get_keyboard_from_list(keyboard)
    msg = KeyboardMessage(keyboard=k)
    viber.send_messages(to=uid, messages=[msg])


_keyboard = {
    "keyboard": {
        "DefaultHeight": True,
        "BgColor": "#FFFFFF",
        "Buttons": []
    }
}

_btn = {
        "Columns": 6,
        "Rows": 1,
        "BgColor": "#2db9b9",
        "BgMediaType": "gif",
        "BgMedia": "http://www.url.by/test.gif",
        "BgLoop": True,
        "ActionType": "reply",
        "OpenURLType": "internal",
        "InternalBrowser": {
            "Mode": "fullscreen",
            "CustomTitle": ""
        },
        "ActionBody": "",
        "Image": "",
        "Text": "",
        "TextVAlign": "middle",
        "TextHAlign": "center",
        "TextOpacity": 60,
        "TextSize": "regular"
        }
# /var/www/html;
