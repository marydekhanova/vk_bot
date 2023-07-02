import random
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from db_models import create_tables, BotUser, Blacklist, FavouriteUserLink, Favourite, Photo, BufferUser
from db_config import LOGIN, PASSWORD, DB_PORT, DB_NAME
import vk_parser


DSN = f'postgresql://{LOGIN}:{PASSWORD}@localhost:{DB_PORT}/{DB_NAME}'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)

#Создание нового пользователя бота
def add_bot_user(bot_user_id):
    with Session() as session:
        session.add(BotUser(bot_user_id=bot_user_id, offset=1, VK_offset=0))
        session.commit()

#Изменение города для поиска
def search_city_change(bot_user_id, city):
    with Session() as session:
        session.get(BotUser, bot_user_id).city = city
        session.commit()

#Изменения возраста поиска
def search_age_change(bot_user_id, from_age, to_age):
    with Session() as session:
        user = session.get(BotUser, bot_user_id)
        user.from_age = from_age
        user.to_age = to_age
        session.commit()

#Изменение пола поиска
def search_gender_change(bot_user_id, gender):
    with Session() as session:
        session.get(BotUser, bot_user_id).gender = gender
        session.commit()

#Добавление буффера пользователей vk, которые будут выдаваться пользователю бота
#На вход получает id пользователя бота и массив словарей пользователей vk
#Структура словаря такая же, как возвращается в vk_parser
def add_vk_users(bot_user_id, vk_users):
    with Session() as session:
        buffer = []
        for user in vk_users:
            buffer.append(BufferUser(VK_id=user['id'], name=user['first_name'],
                                               surname=user['last_name'], link_to_profile=user['domain'],
                                               bot_user_id=bot_user_id))
        session.add_all(buffer)
        bot_user = session.get(BotUser, bot_user_id)
        bot_user.offset = session.query(BufferUser).filter(BufferUser.bot_user_id == bot_user_id)[0].user_id
        bot_user.VK_offset += 20 if bot_user.VK_offset <= 979 else 0
        session.commit()

#Выдача пользователю бота следующего человека для рассмотрения
#На вход - id пользователя бота и айди его 3 лучших фоток
#Возвращает словарь пользователя в вк для рассмотрения
def get_next_vk_user(bot_user_id, photo_ids):
    with Session() as session:
        bot_user = session.get(BotUser, bot_user_id)
        vk_user = session.get(BufferUser, bot_user.offset)
        bot_user.offset += 1
        vk_user.photo_ids = photo_ids
        session.commit()
        return {'id': vk_user.VK_id, 'name': vk_user.name, 'surname': vk_user.surname, 'link': vk_user.link_to_profile, 'photos': vk_user.photo_ids}

#Удаляет буферезированных пользователей в вк
def delete_vk_users(bot_user_id):
    with Session() as session:
        session.query(BufferUser).filter(bot_user_id==bot_user_id).delete()
        session.commit()

#Получение vk id пользователя из буфера, который будет рассматриваться следующим
#Возвращает ошибку (которую нужно обработать), если в буфере не пользователей vk для данного пользователя бота.
def get_current_vk_user_id(bot_user_id):
    with Session() as session:
        id = session.get(BotUser, bot_user_id).offset
        vk_user = session.get(BufferUser, id)
        if vk_user == None:
            raise Exception('Too big offset')
        return vk_user.VK_id

#Добавление последнего рассмотренного пользователя vk в избранное
#На вход - id пользователя бота
def add_last_VK_user_to_favourite(bot_user_id):
    with Session() as session:
        bot_user = session.get(BotUser, bot_user_id)
        user = session.get(BufferUser, bot_user.offset - 1)
        if session.get(Favourite, user.VK_id) is None:
            session.add(Favourite(favourite_VK_id=user.VK_id, name=user.name,
                                                   surname=user.surname, link_to_profile=user.link_to_profile))
            for photo in user.photo_ids:
                session.add(Photo(user_VK_id=user.VK_id, photo_id=photo))
        session.add(FavouriteUserLink(bot_user_id=bot_user_id, favourite_id=user.VK_id))
        session.commit()

#Добалвение последнего рассмотренного пользователя в черный список
#На вход - id пользователя бота
def add_last_VK_user_to_blacklist(bot_user_id):
    with Session() as session:
        bot_user = session.get(BotUser, bot_user_id)
        user = session.get(BufferUser, bot_user.offset - 1)
        session.add(Blacklist(blacklist_VK_id=user.VK_id, bot_user_id=bot_user_id))
        session.commit()

#Получение черного списка (в виде массива id) для данного пользователя бота
def get_user_blacklist(bot_user_id):
    with Session() as session:
        query = session.query(Blacklist).filter(Blacklist.bot_user_id == bot_user_id)
        return [blacklist.blacklist_VK_id for blacklist in query]

#Получение списка избранных (в виде списке словарей) для данного пользователя бота.
def get_favourites(bot_user_id):
    with Session() as session:
        query = session.query(FavouriteUserLink, Favourite). \
                 filter(FavouriteUserLink.bot_user_id == bot_user_id).\
            join(Favourite, Favourite.favourite_VK_id == FavouriteUserLink.favourite_id).all()
        favourites = [{'id': favourite.favourite_VK_id, 'name': favourite.name, 'surname': favourite.surname, 'link': favourite.link_to_profile, 'photos': []} for _, favourite in query]
        for fav in favourites:
            fav['photos'] = [photo.photo_id for photo in session.query(Photo).filter(Photo.user_VK_id == fav['id']).all()]
        return favourites

#Получение параметров поиска для данного пользователя бота
def get_bot_user_data(bot_user_id):
    with Session() as session:
        bot_user = session.get(BotUser, bot_user_id)
        return {   'age_from': bot_user.from_age,
                    'age_to': bot_user.to_age,
                    'city': bot_user.city,
                    'sex': bot_user.gender,
                    'offset': bot_user.VK_offset
                   }

if __name__ == '__main__':
    create_tables(engine)
    vk = vk_parser.VkParser()
    add_bot_user(1)
    add_bot_user(2)
    for i in range(22):
        try:
            print(get_next_vk_user(1, vk.get_user_photos(get_current_vk_user_id(1))))
        except:
            users = vk.get_users(**get_bot_user_data(1))
            delete_vk_users(1)
            add_vk_users(1, users)
            print(get_next_vk_user(1, vk.get_user_photos(get_current_vk_user_id(1))))
        if random.randint(1, 10) > 5:
            add_last_VK_user_to_favourite(1)
        else:
            add_last_VK_user_to_blacklist(1)
    print('\n')
    for i in range(22):
        try:
            print(get_next_vk_user(2, vk.get_user_photos(get_current_vk_user_id(2))))
        except:
            users = vk.get_users(**get_bot_user_data(2))
            delete_vk_users(2)
            add_vk_users(2, users)
            print(get_next_vk_user(2, vk.get_user_photos(get_current_vk_user_id(2))))
        if random.randint(1, 10) > 5:
            add_last_VK_user_to_favourite(2)
        else:
            add_last_VK_user_to_blacklist(2)
    print('\n')
    print(get_favourites(1))
    print('\n')
    print(get_favourites(2))
    print('\n')
    print(get_user_blacklist(1))
    print('\n')
    print(get_user_blacklist(2))

