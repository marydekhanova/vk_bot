from bot.send_functions import send_msg, send_keyboard
from bot.lexicon import lexicon
from db.db_main import add_bot_user
from bot.keyboard import keyboard_gender, keyboard_candidates, keyboard_next
from db.db_main import get_current_vk_user_id, get_next_vk_user, get_favourites
from vk_data.config import vk_parser


def send_greeting(id):
    send_msg(id, lexicon['начать'])


def ask_about_city(id):
    add_bot_user(id)
    send_msg(id, lexicon['да'])


def ask_about_gender(id):
    send_keyboard(id, keyboard_gender, 'С кем вы хотите познакомиться?')


def ask_about_age(id):
    send_msg(id, lexicon['age_range'])


def send_candidate(id):
    id_candidate = get_current_vk_user_id(id)
    photos_candidate = vk_parser.get_user_photos(id_candidate)
    candidate = get_next_vk_user(id, photos_candidate)
    text = f'-{candidate["name"]} {candidate["surname"]}\n-{candidate["link"]}'
    attachments = []
    for photo in candidate['photos']:
        attachment = 'photo' + str(id_candidate) + '_' + str(photo)
        attachments.append(attachment)
    attachments = ','.join(attachments)
    send_msg(id, text, attachments)
    send_keyboard(id, keyboard_candidates, 'Нажмите подходящую кнопку:')


def send_favorites(id):
    favorites = get_favourites(id)
    lines = ''
    for favorite in favorites:
        line = f'{favorite["name"]} {favorite["surname"]} {favorite["link"]}\n'
        lines += line
    send_msg(id, lines)
    send_keyboard(id, keyboard_next, 'Если вы готовы продолжить, нажмите на кнопку:')





