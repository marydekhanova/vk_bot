from db.db_main import search_city_change, search_gender_change, \
    search_age_change, add_last_VK_user_to_favourite, \
    add_last_VK_user_to_blacklist, check_db_user_bot
from bot.keyboard import keyboard_next
from bot.send_functions import send_keyboard, send_msg
from bot.lexicon import lexicon


def save_city_to_db(id, city):
    city = (' '.join(city[1:])).lower().capitalize()
    search_city_change(id, city)


def save_gender_to_db(id, text):
    if text == 'С парнем':
        gender = 2
    elif text == 'С девушкой':
        gender = 1
    search_gender_change(id, gender)


def save_age_range_to_db(id, age_from, age_to):
    search_age_change(id, age_from, age_to)


def save_favorite_candidate(id):
    add_last_VK_user_to_blacklist(id)
    send_msg(id, lexicon['favorite'])
    send_keyboard(id, keyboard_next,
                  'Если вы готовы продолжить, нажмите на кнопку:')


def save_to_blacklist(id):
    add_last_VK_user_to_favourite(id)
    send_msg(id, lexicon['blacklist'])
    send_keyboard(id, keyboard_next,
                  'Если вы готовы продолжить, нажмите на кнопку:')


def check_user_bot(id):
    return check_db_user_bot(id)
