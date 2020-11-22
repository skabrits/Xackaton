import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import json
import sys
import config
import keyboards
import Analysys.lenin_trainer
import os


vk_session = vk_api.VkApi(token=config.TOKEN)
longpoll = VkBotLongPoll(vk_session, config.ID)
k = 0
m = 0
keyboard = json.dumps(keyboards.KEYBOARD).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))


def main():
    global k
    global m
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and k == 0:
            greeting(event)
            k = 1
            print(event)
        if event.type == VkBotEventType.MESSAGE_NEW and m == 1:
            cc(event)
            m = 0
        if event.type == VkBotEventType.MESSAGE_NEW and event.obj.message['text'] == 'Предположительное качество дороги':
            road(event)
        # if event.type == VkBotEventType.MESSAGE_NEW and event.obj.message['text'] == 'Период ремонта конкретной дороги':
        #     rep(event)


def greeting(event):
    vk = vk_session.get_api()
    name = vk.users.get(user_id=event.obj.message['from_id'])[0]['first_name']
    vk.messages.send(user_id=event.obj.message['from_id'],
                     message=config.GREETING.format(name),
                     random_id=random.randint(0, 2 ** 64), keyboard=keyboard)


def road(event):
    global m
    vk = vk_session.get_api()
    vk.messages.send(user_id=event.obj.message['from_id'],
                         message='Введите параметры, разделяя пробелами',
                         random_id=random.randint(0, 2 ** 64), keyboard=keyboard)
    m = 1


def cc(event):
    vk = vk_session.get_api()
    try:
        ia = list(map(lambda x:float(x), str(event.obj.message['text']).split(" ")))
        cat = Analysys.lenin_trainer.calcit(ia[0],ia[1],ia[2],ia[3],ia[4])
        vk.messages.send(user_id=event.obj.message['from_id'],
                         message=cat,
                         random_id=random.randint(0, 2 ** 64), keyboard=keyboard)
    except ValueError as e:
        vk.messages.send(user_id=event.obj.message['from_id'],
                         message='Неправильно введены параметры. Введите параметры, разделяя пробелами',
                         random_id=random.randint(0, 2 ** 64), keyboard=keyboard)


# def rep(event):
#     vk = vk_session.get_api()
#     vk.messages.send(user_id=event.obj.message['from_id'],
#                      message="Введите название улицы",
#                      random_id=random.randint(0, 2 ** 64), keyboard=keyboard)
#     os.remove(os.path.abspath('repairs.py').replace('repairs.py', 'data-108554-2020-11-20.xlsx'))


if __name__ == '__main__':
    main()