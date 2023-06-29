import os
from dotenv import load_dotenv
from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


load_dotenv()
vk_bot_token = os.getenv('VK_BOT_TOKEN')

vk_session = vk_api.VkApi(token=vk_bot_token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def send_msg(id, text):
    vk_session.method("messages.send", {"user_id": id, "message": text, "random_id": randrange(10 ** 7)})


keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Посмотреть другой вариант', color=VkKeyboardColor.NEGATIVE)
keyboard.add_button('Добавить в избранные', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('Вывести список избранных', color=VkKeyboardColor.SECONDARY)


def get_keyboard(id, text):
    vk_session.method("messages.send", {"user_id": id, "message": text, "random_id": randrange(10 ** 7), "keyboard": keyboard.get_keyboard()})


# В данную функцию мы передаём id написавшего человека
def get_new_candidate(id):
    # Функция get_candidates возвращает список подходящих людей в соответствии с информацией
    # на странице написавшего пользователя (город, возраст, пол)
    # Каждая кандидатура является тоже списком из трех элементов:
    # - имя и фамилия,
    # - ссылка на профиль,
    # - три фотографии в виде attachment(https://dev.vk.com/method/messages.send)
    candidates = get_candidates(id)
    for candidate in candidates:
        # Если кандидата нет в таблицах "избранные" и "отсеянные" в бд,
        # Данная функция возвращает подходящего кандидата
        if candidate not in favorites and candidate not in disliked:
            return candidate


# Здесь мы сохраняем для каждого написавшего человека кандидата,
# который просматривается на данный момент для сохранения его в дальнейшем в бд
save_candidate = {}

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            id = event.user_id

            if event.text == 'Начать':
                # когда пользователь напишет "Начать", отправляем приветственное сообщение
                send_msg(id, "Привет! Здесь ты можешь найти свою вторую половинку! Вот первая кандидатура!")
                candidate = get_new_candidate(id)
                save_candidate[id] = candidate
                # отправляем первую кандидатуру
                send_msg(id, candidate)
                # в диалоге высвечивается клавиатура
                get_keyboard(id, 'Нажми на кнопку, если ты хочешь')

            if event.text == 'Добавить в избранные':
                # Здесь мы удаляем из словаря кандидатуру и сразу сохраняем ее в переменную
                # для сохранения в бд
                candidate = save_candidate.pop(id, None)
                # Передаем id написавшего и избранную кандидатуру
                save_favorite_candidate_to_db(id, candidate)
                get_keyboard(id, 'Нажми на кнопку, если ты хочешь')

            if event.text == 'Посмотреть другой вариант':
                # Перед просмотром другого варианта проверяем, добавил ли пользователь
                # предыдущую кандидатуру в избранные
                # Если в словаре save_candidate нет подходящего ключа,
                # возвращается указанное значение после запятой в методе pop
                candidate = save_candidate.pop(id, None)
                if candidate != None:
                    # если в словаре был кандидат (значит его ранее не добавили в избранные),
                    # то добавляем его в отсеянные в бд
                    save_dislike_candidate_to_db(id, candidate)
                # Ищем нового кандидата
                candidate = get_new_candidate(id)
                send_msg(id, candidate)
                get_keyboard(id, 'Нажми на кнопку, если ты хочешь')

            if event.text == 'Вывести список избранных':
                # Из бд получаем список по id
                favorites_candidates = get_favorites_candidates_from_db(id)
                send_msg(id, favorites_candidates)
                get_keyboard(id, 'Нажми на кнопку, если ты хочешь')




