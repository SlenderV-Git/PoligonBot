from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from services.file_handlers import book


# Функция, генерирующая клавиатуру для страницы книги
def create_pagination_kb(*buttons: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Добавляем в билдер ряд с кнопками
    kb_builder.row(*[InlineKeyboardButton(
        text=LEXICON[button] if button in LEXICON else button,
        callback_data=button) for button in buttons])
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

def create_bookmarks_buttons(*buttons: str) -> InlineKeyboardBuilder:
    bk_builder = InlineKeyboardBuilder()
    for button in buttons:
        bk_builder.row(InlineKeyboardButton(
            text= f"{button} - {book[button][:100]}",
            callback_data=str(button)
            )
        )
    bk_builder.row(
        InlineKeyboardButton(
            text = LEXICON["edit_bookmarks_button"],
            callback_data='edit_bookmarks'
        ),
        InlineKeyboardButton(
            text="cancel",
            callback_data= "cancel"
        )
    )
    return bk_builder.as_markup()

def create_del_buttons(*buttons: str):
    dl_builder = InlineKeyboardBuilder()
    for button in buttons:
        dl_builder.row(InlineKeyboardButton(
            text= f"{LEXICON['del']}{button} - {book[button][:100]}",
            callback_data=f"{button}del"
            )
        )
    dl_builder.row(
        InlineKeyboardButton(
            text = LEXICON["edit_bookmarks_button"],
            callback_data='edit_bookmarks'
        ),
        InlineKeyboardButton(
            text="cancel",
            callback_data= "cancel"
        )
    )
    return dl_builder.as_markup()