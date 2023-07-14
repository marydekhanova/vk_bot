import os
from dotenv import load_dotenv
import vk_api
from vk_api.longpoll import VkLongPoll


load_dotenv()
vk_bot_token = os.getenv('VK_BOT_TOKEN')

vk_session = vk_api.VkApi(token=vk_bot_token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
