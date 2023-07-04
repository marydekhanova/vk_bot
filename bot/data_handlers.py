from db.db_main import add_bot_user, search_city_change, search_gender_change, search_age_change, \
    get_bot_user_data, add_vk_users, add_last_VK_user_to_favourite, add_last_VK_user_to_blacklist
from vk_data.config import vk_parser
from bot.keyboard import keyboard_next
from bot.send_functions import send_keyboard, send_msg
from bot.lexicon import lexicon


def save_city_to_db(id, text):
    city = text.split()[1].lower().capitalize()
    search_city_change(id, city)


def save_gender_to_db(id, text):
    if text == 'C парнем':
        gender = 1
    else:
        gender = 2
    search_gender_change(id, gender)


def save_age_range_to_db(id, text):
   age_range = text.split()
   age_from = age_range[1]
   age_to = age_range[3]
   search_age_change(id, age_from, age_to)


def save_candidates(id):
    vk_users = vk_parser.get_users(**get_bot_user_data(id))
    add_vk_users(id, vk_users)


def save_favorite_candidate(id):
    add_last_VK_user_to_blacklist(id)
    send_msg(id, lexicon['favorite'])
    send_keyboard(id, keyboard_next, 'Если вы готовы продолжить, нажмите на кнопку:')


def save_to_blacklist(id):
    add_last_VK_user_to_favourite(id)
    send_msg(id, lexicon['blacklist'])
    send_keyboard(id, keyboard_next, 'Если вы готовы продолжить, нажмите на кнопку:')

