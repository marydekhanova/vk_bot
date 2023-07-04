from vk_data.vk_parser import VkParser
from vk_data.config import vk_parser


def get_user():

    users = vk.get_users(0, 100, 'Москва', 1, 100)

vk = VkParser(TOKEN)
users = vk.get_users(0, 100, 'Москва', 1, 100)
print(users)
for user in users:
    print(vk.get_user(user))
    print('hi')
