
from os import environ
from subprocess import PIPE, STDOUT, run
import aiofiles
import asyncio
import datetime
from app.bot.middlewares.ensure_admin import ensure_admin_middleware
from app.bot.middlewares.smart_logger import smart_logger_middleware
from app.bot.middlewares.depends import *
from app.bot.middlewares.db_session import *
from app.db.record.models import Users

from app.bot.linq_reader.ReaderLinq import ReaderLinq
from app.bot.linq_reader.ProgrammParser import ProgrammParser

from pybotx import (
    Bot,
    BubbleMarkup,
    ChatCreatedEvent,
    HandlerCollector,
    IncomingMessage,
    KeyboardMarkup,
    StatusRecipient,
    OutgoingAttachment,
    MentionBuilder,
)

from enum import Enum, auto
from pybotx import Bot, HandlerCollector, IncomingMessage
from pybotx_fsm import FSMCollector

from app.resources import strings

from sqlalchemy import select


collector = HandlerCollector()

async def add_user_huid(message: IncomingMessage, bot: Bot) -> None:
    db_session = message.state.db_session      
    new_entry = Users(full_name=message.data["full_name"], email="test@mail.ru" ,huid=message.data["huid"])
    db_session.add(new_entry)
    await db_session.commit() #Закрываем сессию
    

async def delete_user(message: IncomingMessage, bot: Bot) -> None:
    db_session = message.state.db_session
    
    # Удаление необходимой записи по full_name
    user_to_delete = await db_session.execute(
        select(Users).where(Users.full_name == message.data["full_name"])
    )
    user_to_delete = user_to_delete.scalars().first()
    
    if user_to_delete:
        await db_session.delete(user_to_delete)
        await db_session.commit()  # Сохраняем изменения в базе данных
    else:
        await bot.send_message(message.chat.id, f"Пользователь с именем {full_name} не найден.")

    # Закрываем сессию
    await db_session.close()