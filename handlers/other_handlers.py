from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU

router = Router()

@router.message()
async def reply_message(message : Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except:
        await message.reply(text= LEXICON_RU['no_echo'])