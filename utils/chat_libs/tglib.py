from telethon import TelegramClient, sync
from telethon.tl.functions.channels import InviteToChannelRequest

api_id = 384524
api_hash = '6fd9e886360d69bc24a8076665cdd496'

client = TelegramClient('MYSESSION228', api_id, api_hash).start()
print(client.get_me().stringify())

user = client.get_entity('+79179052684')
channel = client.get_entity('autoinvitetest')

# Add users.
result = client(InviteToChannelRequest(
    channel,
    [user]
))