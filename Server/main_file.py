import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import json
import sys
import config

vk_session = vk_api.VkApi(token=config.TOKEN)
longpoll = VkBotLongPoll(vk_session, config.ID)
k = 0


def main():
    global k
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and k == 0:
            greeting(event)
            k = 1
            print(event)


def greeting(event):
    vk = vk_session.get_api()
    name = vk.users.get(user_id=event.obj.message['from_id'])[0]['first_name']
    vk.messages.send(user_id=event.obj.message['from_id'],
                     message=config.GREETING.format(name),
                     random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()