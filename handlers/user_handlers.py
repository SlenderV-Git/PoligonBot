from copy import deepcopy

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData
from database.users_data import user_dict_template, users_db


from keyboards.pagination_kb import (create_pagination_kb, 
                                    create_bookmarks_buttons, 
                                    create_del_buttons)
from lexicon.lexicon import LEXICON
from services.file_handlers import book

router = Router()


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)



# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


# Этот хэндлер будет срабатывать на команду "/beginning"
# и отправлять пользователю первую страницу книги с кнопками пагинации
@router.message(Command(commands='beginning'))
async def process_beginning_command(message: Message):
    users_db[message.from_user.id]['page'] = 1
    text = book[users_db[message.from_user.id]["page"]]
    await message.answer(
        text=text,
        reply_markup=create_pagination_kb(
            'backward',
            f'{users_db[message.from_user.id]["page"]}/{len(book)}',
            'forward'
        )
    )



# Этот хэндлер будет срабатывать на команду "/continue"
# и отправлять пользователю страницу книги, на которой пользователь
# остановился в процессе взаимодействия с ботом
@router.message(Command(commands='continue'))
async def process_continue_command(message: Message):
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination_kb(
            'backward',
            f'{users_db[message.from_user.id]["page"]}/{len(book)}',
            'forward'
        )
    )

@router.callback_query(F.data == 'forward')
async def process_forward_press(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] < len(book):
        users_db[callback.from_user.id]['page'] += 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_kb(
                'backward',
                f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                'forward'
            )
        )
    await callback.answer()


@router.callback_query(F.data == 'backward')
async def process_forward_press(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] > 1:
        users_db[callback.from_user.id]['page'] -= 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_kb(
                'backward',
                f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                'forward'
            )
        )
    await callback.answer()

@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def process_bookmark_menu(callback : CallbackQuery):
    users_db[callback.from_user.id]["bookmarks"].add(
        users_db[callback.from_user.id]["page"]
    )
    await callback.answer(LEXICON["add_bookmark"])

@router.message(Command(commands='bookmarks'))
async def process_continue_command(message: Message):
    if users_db[message.from_user.id]["bookmarks"]:
        await message.answer(
            text = LEXICON[message.text],
            reply_markup = create_bookmarks_buttons(
                *users_db[message.from_user.id]['bookmarks']
            )
        )
    else:
        await message.answer(text= LEXICON["no_bookmarks"])

@router.callback_query(IsDigitCallbackData())
async def change_cur_page(callback : CallbackQuery):
    text = book[int(callback.data)]
    users_db[callback.from_user.id]["page"] = int(callback.data)
    await callback.message.edit_text(
        text = text,
        reply_markup=create_pagination_kb(
                'backward',
                f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                'forward'
        )
    )
    await callback.answer()

@router.callback_query(IsDelBookmarkCallbackData())
async def del_bookmark(callback : CallbackQuery):
    users_db[callback.from_user.id]["bookmarks"].remove(int(callback.data[:-3]))
    if users_db[callback.from_user.id]["bookmarks"]:
        await callback.message.edit_text(
            text = LEXICON['edit_bookmarks'],
            reply_markup = create_bookmarks_buttons(
                *users_db[callback.from_user.id]['bookmarks']
            )
        )
    else:
        await callback.message.edit_text(
            text = LEXICON["no_bookmarks"]
        )
    await callback.answer()

@router.callback_query(F.data == 'edit_bookmarks')
async def show_del_menu(callback : CallbackQuery):
    await callback.message.edit_text(
        text= LEXICON[callback.data],
        reply_markup= create_del_buttons(
            *users_db[callback.from_user.id]['bookmarks']
        )
    )
    await callback.answer()

@router.callback_query(F.data == "cancel")
async def process_cancel_button(callback : CallbackQuery):
    await callback.message.edit_text(
        text = LEXICON["cancel_text"]
    )
    await callback.answer()