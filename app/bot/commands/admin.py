"""Handlers for default bot commands and system events."""

from os import environ
from subprocess import PIPE, STDOUT, run
from types import SimpleNamespace
import aiofiles
import asyncio
import datetime
from app.bot.middlewares.ensure_admin import ensure_admin_middleware
from app.bot.middlewares.smart_logger import smart_logger_middleware
from app.bot.middlewares.depends import *
from app.bot.middlewares.db_session import *
from app.bot.commands.admin_utils import add_user_huid
from app.bot.commands.admin_utils import delete_user

from pybotx_fsm.templates import KEY_TEMPLATE

from typing import Any, Optional


from app.bot.commands import common

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

collector = HandlerCollector()

class FSMStates(Enum):
    WAITING_MENTION = auto()
    WAITING_COMMAND = auto()

fsm = FSMCollector(FSMStates)


@fsm.on(FSMStates.WAITING_COMMAND, middlewares=[db_session_middleware])
async def waiting_full_name(message: IncomingMessage, bot: Bot) -> None:
    # if message.file:
    #     await bot.answer_message(
    #         body=strings.FILE_NOT_TITLE, keyboard=get_cancel_keyboard_button()
    #     )
    #     return
    # либо тут делаем проверк

    keyboard = KeyboardMarkup()
    keyboard.add_button(command='to_commands', label="В меню")


    if message.body == "get_registration_requests":
        await message.state.fsm.change_state(FSMStates.WAITING_MENTION)
        contact = MentionBuilder.contact("54ba9316-cfa4-561f-b1f5-77bf59d4a7d7")

        await bot.send_message(
                bot_id=message.bot.id,
                chat_id=message.chat.id,
                body=f"Запросы:  {contact}\n Выберите пользователя",
                keyboard=keyboard
            )
    
# @dataclass
# class FSMStateData:
#     state: Enum
#     storage: SimpleNamespace
# async def get_state(message) -> Optional[Enum]:
#     fsm_state_data: Optional[FSMStateData] = await self._state_repo.get(
#         KEY_TEMPLATE.format(
#             host=self._message.bot.host,
#             bot_id=self._message.bot.id,
#             chat_id=self._message.chat.id,
#             user_huid=self._message.sender.huid,
#         ),
#     )

#     if not fsm_state_data:
#         return None

#     return fsm_state_data.state


@dataclass
class FSMStateData:
    state: Enum
    storage: SimpleNamespace

@fsm.on(FSMStates.WAITING_MENTION, middlewares=[db_session_middleware])
async def waiting_mention(message: IncomingMessage, bot: Bot) -> None:
    # if message.file:
    #     await bot.answer_message(
    #         body=strings.FILE_NOT_TITLE, keyboard=get_cancel_keyboard_button()
    #     )
    #     return
    # либо тут делаем проверку

    keyboard = KeyboardMarkup()
    keyboard.add_button(command="to_commands", label="В меню")

    if message.body == "approve" and message.data["huid"] is not None:
        huid = message.data["huid"]
        await add_user_huid(message, Bot)
        await bot.answer_message(
            body=f"Доступ для {huid} - одобрен",
            keyboard=keyboard
        )
        print("test drop state")
        await message.state.fsm.drop_state()
        return
    elif message.body == "deny" and message.data["huid"] is not None:
        huid = message.data["huid"]
        await bot.answer_message(
            body=f"Доступ для {huid} - запрещён",
            keyboard=keyboard
        )
        return
    elif message.body == "delete" and message.data["huid"] is not None:
        huid = message.data["huid"]
        # await delete_user(message, Bot)
        
        print("delete state ")
        print("host: ", message.bot.host)
        print("id: ", message.bot.id)
        print("chatid: ", message.chat.id)
        print("senderhuid: ", message.sender.huid)
        print("huid: ", huid)
        await message.state.fsm._state_repo.delete(
            KEY_TEMPLATE.format(
                host=message.bot.host,
                bot_id=message.bot.id,
                chat_id="29d13a59-4d9d-0b85-2da0-520e4d26ab31",
                user_huid=huid
            )
        )

        await bot.answer_message(
            body=f"Удаление пользователя - {huid}",
            keyboard=keyboard
        )

        # new_message = IncomingMessage()
        # new_message.state.fsm.dr
        return
    if message.body == "to_commands":
        keyboard2 = KeyboardMarkup()
        keyboard2.add_button(command='get_registration_requests', label="Получить запросы на регистрацию")
        await bot.answer_message(
                body= "Выберите действие",
                keyboard=keyboard2)
        await message.state.fsm.change_state(FSMStates.WAITING_COMMAND)
    print(message)
    print(type(message))

    mentions = message.mentions

    print(mentions)

    for mention in mentions:
        print(mention)
        # mention.entity_id
        bubbles = BubbleMarkup()
        bubbles.add_button(command="approve", label="Предоставить", data={"huid": str(mention.entity_id), "full_name": mention.name})
        bubbles.add_button(command="deny", label="Не предоставить", data={"huid": str(mention.entity_id)})
        bubbles.add_button(command="delete", label="Удалить пользователя", data={"huid": str(mention.entity_id), "full_name": mention.name})
        full_name = mention.name
        await bot.answer_message(
            body=f"Одобрить доступ {full_name}?",
            bubbles=bubbles,
            keyboard=keyboard
        )
        
# @collector.command("/approve", description="Одобрить", visible=False)
# async def approve(message: IncomingMessage, bot: Bot) -> None:
#     huid = message.data["huid"]
#     await bot.answer_message(
#         body=f"Доступ для {huid} - одобрен",
#     )


# @collector.command("/deny", description="Запретить", visible=False)
# async def deny(message: IncomingMessage, bot: Bot) -> None:
#     huid = message.data["huid"]
#     await bot.answer_message(
#         body=f"Доступ для {huid} - запрещён",
#     )
