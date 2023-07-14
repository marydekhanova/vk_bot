from bot.send_functions import send_msg, send_keyboard
from bot.lexicon import lexicon
from bot.keyboard import keyboard_gender, keyboard_candidates, keyboard_next
from db.db_main import get_current_vk_user_id, get_next_vk_user,\
    get_favourites, add_bot_user, get_bot_user_data, delete_vk_users, \
    add_vk_users
from vk_data.config import vk_parser
from bot.data_handlers import save_city_to_db, save_age_range_to_db
from vk_api.exceptions import ApiError


def send_greeting(id):
    send_msg(id, lexicon['начать'])
    add_bot_user(id)


def ask_about_city(id):
    send_msg(id, lexicon['city'])


def ask_about_gender(id, text):
    city = text.split()
    if len(city) > 1:
        save_city_to_db(id, city)
        send_keyboard(id, keyboard_gender, 'С кем вы хотите познакомиться?')
    else:
        send_msg(id, lexicon['incorrect_city'])


def ask_about_age(id):
    send_msg(id, lexicon['age_range'])


def send_candidate(id):
    try:
        id_candidate = get_current_vk_user_id(id)
    except Exception:
        users = vk_parser.get_users(**get_bot_user_data(id))
        delete_vk_users(id)
        add_vk_users(id, users)
        id_candidate = get_current_vk_user_id(id)
    photos_candidate = vk_parser.get_user_photos(id_candidate)
    candidate = get_next_vk_user(id, photos_candidate)
    text = f'- {candidate["name"]} {candidate["surname"]}\n' \
           f'- {candidate["link"]}'
    attachments = []
    for photo in candidate['photos']:
        attachment = 'photo' + str(id_candidate) + '_' + str(photo)
        attachments.append(attachment)
    attachments = ','.join(attachments)
    send_msg(id, text, attachments)
    send_keyboard(id, keyboard_candidates, 'Нажмите подходящую кнопку:')


def send_first_candidate(id, text):
    age_range = text.split()
    if len(age_range) == 4:
        age_from = int(age_range[1])
        age_to = int(age_range[3])
        if age_from != 0 and age_to != 0 and age_to > age_from:
            save_age_range_to_db(id, age_from, age_to)
            send_candidate(id)
        else:
            send_msg(id, lexicon['incorrect_age'])
    else:
        send_msg(id, lexicon['incorrect_age'])


def send_favorites(id):
    try:
        favorites = get_favourites(id)
        lines = ''
        for favorite in favorites:
            line = f'{favorite["name"]} {favorite["surname"]} ' \
                   f'{favorite["link"]}\n'
            lines += line
        send_msg(id, lines)
        send_keyboard(id, keyboard_next,
                      'Если вы готовы продолжить, нажмите на кнопку:')
    except ApiError:
        send_msg(id, lexicon['empty_favorites'])
    send_keyboard(id, keyboard_next,
                  'Если вы готовы продолжить, нажмите на кнопку:')
