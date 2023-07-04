from vk_api.keyboard import VkKeyboard, VkKeyboardColor


keyboard_candidates = VkKeyboard(one_time=True)
keyboard_candidates.add_button('Добавить в избранные', color=VkKeyboardColor.POSITIVE)
keyboard_candidates.add_button('Больше не показывать', color=VkKeyboardColor.NEGATIVE)
keyboard_candidates.add_line()
keyboard_candidates.add_button('Посмотреть другой вариант', color=VkKeyboardColor.SECONDARY)
keyboard_candidates.add_line()
keyboard_candidates.add_button('Вывести список избранных', color=VkKeyboardColor.SECONDARY)


keyboard_gender = VkKeyboard(one_time=True)
keyboard_gender.add_button('С парнем')
keyboard_gender.add_button('С девушкой')


keyboard_next = VkKeyboard(one_time=True)
keyboard_next.add_button('Следующий кандидат')