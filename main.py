from vk_api.longpoll import VkEventType

from bot.config import longpoll
from bot.senders import send_greeting, ask_about_city, ask_about_gender, ask_about_age, send_candidate, \
    send_favorites
from bot.data_handlers import save_city_to_db, save_gender_to_db, save_age_range_to_db, \
    save_favorite_candidate, save_to_blacklist, check_user_bot
from bot.send_functions import send_msg
from bot.lexicon import lexicon
from bot.bot_exception import IncorrectData
from db.db_main import engine
from db.db_models import create_tables


create_tables(engine)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            id = event.user_id
            text = event.text
            if not check_user_bot(id) or text.lower() == 'начать':
                send_greeting(id)
                ask_about_city(id)
            else:
                if 'город' in text.lower():
                    ask_about_gender(id, text)

                if text == 'С парнем' or text == 'С девушкой':
                    save_gender_to_db(id, text)
                    ask_about_age(id)

                if 'от' in text.lower() and 'до' in text.lower():
                    try:
                        save_age_range_to_db(id, text)
                        send_candidate(id)
                    except (IndexError, ValueError, IncorrectData) as Error:
                        send_msg(id, lexicon['incorrect_age'])

                if text == 'Добавить в избранные':
                    save_favorite_candidate(id)

                if text == 'Следующий кандидат':
                    send_candidate(id)

                if text == 'Больше не показывать':
                    save_to_blacklist(id)

                if text == 'Посмотреть другой вариант':
                    send_candidate(id)

                if text == 'Вывести список избранных':
                    send_favorites(id)






