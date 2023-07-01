from secret import TOKEN
import requests
import time

def get_user_token():
    return TOKEN #в потенциале можем допилить получение токена конкретного пользователя бота

class VkParser():
    url = 'https://api.vk.com/method/'

    def __init__(self, version = '5.131'):
        self.vk_params = {'access_token': get_user_token(), 'v': version}
        self.users = []

    def get_users(self, age_from, age_to, city, sex, offset):
        method_url = self.url + 'users.search'
        response = requests.get(url=method_url, params={**self.vk_params,
                                                        'age_from': age_from,
                                                        'age_to': age_to,
                                                        'hometown': city,
                                                        'sex': sex,
                                                        'fields': 'domain',
                                                        'offset': offset
                                                        })
        users = [{'id': item['id'], 'domain': r'https://vk.com/' + item['domain'], 'first_name': item['first_name'], 'last_name': item['last_name']} for item in response.json()['response']['items']]
        return users

    def get_user_photos(self, id):
        time.sleep(0.4)
        method_url = self.url + 'photos.get'
        responce = requests.get(url=method_url, params={**self.vk_params, 'owner_id': id, 'album_id': 'profile', 'extended': '1'})
        if 'response' in responce.json():
            photos = responce.json()['response']['items']
            photos = sorted(photos, key=lambda x: x['likes']['count'], reverse=True)
            if len(photos) > 3:
                photos = photos[0:3]
            return [photo['id'] for photo in photos]
        else:
            return []

    def get_user(self, user):
        user = {**user, 'photos': self.get_user_photos(user['id'])}
        return user

if __name__ == '__main__':
    vk = VkParser()
    users = vk.get_users(0,100,'Москва',1,1000000)
    for user in users:
        print(vk.get_user(user))

