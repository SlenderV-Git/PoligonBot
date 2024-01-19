from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

button_1 = KeyboardButton(text= "Кто ты?")
button_2 = KeyboardButton(text= "Кто твой мастер?")

keyboard = ReplyKeyboardMarkup(
    keyboard= [[button_1, button_2]],
    resize_keyboard= True,
    one_time_keyboard= True
)

