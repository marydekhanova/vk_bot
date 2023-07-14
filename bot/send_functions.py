from random import randrange
from vk_api.keyboard import VkKeyboard


from bot.config import vk_session


def send_msg(id, text=None, attachment=None):
    vk_session.method("messages.send", {"user_id": id, "message": text,
                                        'attachment': attachment,
                                        'random_id': randrange(10 ** 7)})


def send_keyboard(id, keyboard: VkKeyboard, text):
    vk_session.method("messages.send", {"user_id": id, "message": text,
                                        "random_id": randrange(10 ** 7),
                                        "keyboard": keyboard.get_keyboard()})
