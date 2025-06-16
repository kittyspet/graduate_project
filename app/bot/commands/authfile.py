from os import environ
from subprocess import PIPE, STDOUT, run
import aiofiles
import asyncio
import datetime
from app.bot.middlewares.ensure_admin import ensure_admin_middleware
from app.bot.middlewares.smart_logger import smart_logger_middleware
from app.bot.middlewares.depends import *
from app.bot.middlewares.db_session import *

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




# class FSMStates(Enum):
#     START_STATE = auto()
#     WAITING_FULLNAME = auto()
#     WAITING_APPROVAL = auto() # только подумать как разделить пользователя и админа
#     WAITING_CODE = auto()



# fsm = FSMCollector(FSMStates)

# collector = HandlerCollector()


# @collector.command("/start", description="Начало")
# async def create_task_handler(message: IncomingMessage, bot: Bot) -> None:
#     await message.state.fsm.change_state(
#         FSMStates.START_STATE
#     )
#     keyboard = KeyboardMarkup()
#     keyboard.add_button(command="cancel", label="Отменить")

     
    

#     await bot.answer_message(
#         body="Начало по старту", keyboard=keyboard
#     )

# @fsm.on(FSMStates.WAITING_FULLNAME, middlewares=[db_session_middleware])
# async def waiting_full_name(message: IncomingMessage, bot: Bot) -> None:
#     # if message.file:
#     #     await bot.answer_message(
#     #         body=strings.FILE_NOT_TITLE, keyboard=get_cancel_keyboard_button()
#     #     )
#     #     return
#     # либо тут делаем проверку

#     full_name = message.body
#     await bot.answer_message(
#         body=f"Ваше имя {full_name}. Введите код авторизации полученный от администратора:"
#     )

#     contact = MentionBuilder.contact(message.sender.huid)
#     # contact2 = MentionBuilder.contact("9f75fbfa-5261-54da-b655-2f04c905b484")
#     # await bot.answer_message(f"Author is {contact}")

#     await bot.send_message(
#             bot_id=message.bot.id,
#             chat_id="8f9f0d9a-948c-05a5-0b9e-4ac5adacd04d7",
#             body=f"ЗАпрос на предоставление пользователю {contact} прав"
#         )

#     # await message.state.fsm.change_state(FSMStates.WAITING_CODE)
#     print("START_STATE_print")

# @fsm.on(FSMStates.WAITING_CODE, middlewares=[db_session_middleware])
# async def waiting_code(message: IncomingMessage, bot: Bot) -> None:
#     # if message.file:
#     #     await bot.answer_message(
#     #         body=strings.FILE_NOT_TITLE, keyboard=get_cancel_keyboard_button()
#     #     )
#     #     return
#     # либо тут делаем проверку
#     code = message.body
#     # TODO: запустить проверку кода

#     await message.state.fsm.change_state(FSMStates.WAITING_FULLNAME)
#     # await message.state.fsm.change_state(FSMStates.)SENDING_INFORMATION
#     print("WAITING_CODE_code")

# @fsm.on(FSMStates.WAITING_APPROVAL, middlewares=[db_session_middleware])
# async def waiting_approval(message: IncomingMessage, bot: Bot) -> None:
#     # if message.file:
#     #     await bot.answer_message(
#     #         body=strings.FILE_NOT_TITLE, keyboard=get_cancel_keyboard_button()
#     #     )
#     #     return
#     # либо тут делаем проверку
    
#     print("WAITING_APPROVAL_print")

# @fsm.on(FSMStates.START_STATE, middlewares=[db_session_middleware])
# async def waiting_task_title_handler(message: IncomingMessage, bot: Bot) -> None:
#     # if message.file:
#     #     await bot.answer_message(
#     #         body=strings.FILE_NOT_TITLE, keyboard=get_cancel_keyboard_button()
#     #     )
#     #     return
    
    
#     # на авторизацию в midlleware тут делаем проверку

#     # await message.state.fsm.change_state(FSMStates.WAITING_FULLNAME)


#     contact = MentionBuilder.contact(message.sender.huid)

#     keyboard = KeyboardMarkup()
#     keyboard.add_button(command="approve", label="Предоставить")
#     keyboard.add_button(command="deny", label="Не предоставить")
    

#     await bot.send_message(
#             bot_id=message.bot.id,
#             chat_id="8f9f0d9a-948c-05a5-0b9e-4ac5adacd04d",
#             body=f"Запрос на предоставление пользователю {contact} прав",
#             keyboard=keyboard
#         )
#     # or  await message.state.fsm.change_state(FSMStates.SENDING_INFORMATION)
    
#     print("START_STATE_print")
