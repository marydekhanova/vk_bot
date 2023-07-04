from vk_api.longpoll import VkEventType

from db.db_main import create_tables, engine
from bot.config import longpoll
from bot.senders import send_greeting, ask_about_city, ask_about_gender, ask_about_age, send_candidate, \
    send_favorites
from bot.data_handlers import save_city_to_db, save_gender_to_db, save_age_range_to_db, save_candidates, \
    save_favorite_candidate, save_to_blacklist

create_tables(engine)
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            id = event.user_id
            text = event.text

            if text.lower() == 'начать':
                # Когда пользователь напишет "Начать", отправляем приветственное сообщение
                send_greeting(id)

            if text.lower() == 'да':
                ask_about_city(id)

            if 'город' in text.lower():
                save_city_to_db(id, text)
                ask_about_gender(id)

            if text == 'С парнем' or text == 'С девушкой':
                save_gender_to_db(id, text)
                ask_about_age(id)

            if 'от' in text.lower() and 'до' in text.lower():
                save_age_range_to_db(id, text)
                save_candidates(id)
                send_candidate(id)

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



