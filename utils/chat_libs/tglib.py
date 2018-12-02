import telebot
import telebot.types as types
import time
from telethon import TelegramClient, sync
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact
import  config as cfg

api_id = 384524
api_hash = '6fd9e886360d69bc24a8076665cdd496'

client = TelegramClient('MYSESSION228', api_id, api_hash).start()
tgbot = telebot.TeleBot("645100799:AAHr08yGqhY8PxAjeSJSdPiUZ-D2MgcB3i8", threaded=False)


def invite_to_chanell(number):
    contact = InputPhoneContact(client_id=0, phone=number, first_name="ABC", last_name="abc")

    result = client(ImportContactsRequest([contact]))
    print(result)
    user = client.get_entity(number)
    channel = client.get_entity('autoinvitetest')

    # Add users.
    result = client(InviteToChannelRequest(
        channel,
        [user]
    ))
    print(result)

invite_to_chanell('+72281211212')

def send_message(uid, text):
    res = tgbot.send_message(uid, text)
    print(res)


def send_keyboard_message(uid, text, answers):
    markup = get_keyboard(answers)
    res = tgbot.send_message(uid, text, reply_markup=markup)
    print(res)


def set_web_hook():
    tgbot.remove_webhook()
    time.sleep(0.1)
    # Set webhook
    res = tgbot.set_webhook(url='https://8922388106.com/{}/incomingtg'.format(cfg.bot_name))
    print(res)


def get_keyboard(list_btns):
    markup = types.ReplyKeyboardMarkup(row_width=len(list_btns))
    for i in list_btns:
        itembtn = types.KeyboardButton(i)
        markup.add(itembtn)
    if len(list_btns) < 1:
        return types.ReplyKeyboardRemove(selective=False)
    return markup
