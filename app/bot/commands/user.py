"""Handlers for default bot commands and system events."""

from os import environ
from subprocess import PIPE, STDOUT, run
import aiofiles
import asyncio
import datetime
from app.bot.middlewares.ensure_admin import ensure_admin_middleware
from app.bot.middlewares.smart_logger import smart_logger_middleware
from app.bot.middlewares.depends import *
from app.bot.middlewares.db_session import *
from app.bot.commands.admin_utils import add_user_huid
from app.bot.commands.admin_utils import delete_user

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
    CHOOSE_PROGRAMM = auto()
    SENDSJ = auto()
    SENDMC = auto()
    OPENPHASE = auto()
    OPENMILESTONE = auto()
    BACKPROGRAMM = auto()
    PROCESSMILESTONE = auto()
    BACKPHASE = auto()
    BACKMILESTONE = auto()
    TESTSTATE = auto()


fsm = FSMCollector(FSMStates)



class KeeperClass:
    milestones, phases = None, None
    readerLinq = ReaderLinq()
    
# TODO:
# async def changeState(state, message, bot):
#     map[state]() or decorators
#     message.state.fsm.chage_state(state)

@fsm.on(FSMStates.CHOOSE_PROGRAMM, middlewares=[db_session_middleware])
async def open_program(message: IncomingMessage, bot: Bot) -> None:

#    keyboard = KeyboardMarkup()
#    keyboard.add_button(command='sendSJ', label="SJ-100")
#    keyboard.add_button(command='sendMC', label="MC-21")

    #await message.state.fsm.drop_state() #сброс состояния

    # bubbles = BubbleMarkup()
    # bubbles.add_button(
    #     command="/sendSJ", 
    #     label="SJ-100", 
    #     background_color="#868E96"
    # )
    
    # bubbles.add_button(
    #     command="/sendMC", 
    #     label="MC-21", 
    #     background_color="#1864AB", 
#     #     new_row=False
#     # )
    
# #    if message.body == "sendSJ":
# #       await common.open_milestone(message=message, bot=bot)

#     await bot.answer_message(
#                             "Вас приветствует чат-бот ПАО \"Яковлев\". \nДля получения актуальной информации о ходе работ по авиационным проектам, пожалуйста, выберите соответствующую программу из списка:"
#                             )
    

    print("fffff 1")
    if message.body == "sendSJ":
        await message.state.fsm.change_state(FSMStates.SENDSJ)
        return 
    elif message.body == "sendMC":
        print("fffff 2")
        await bot.answer_message("Смена состояний")
        await message.state.fsm.change_state(FSMStates.SENDMC)
        return
    elif message.body == "testState":
        await bot.answer_message("Смена на тестовое состояние")
        await testState(message, bot)
        await message.state.fsm.change_state(FSMStates.TESTSTATE)
        return

    keyboard = KeyboardMarkup()  
    print("fffff 3")
    keyboard.add_button(
        command="sendSJ", 
        label="SJ-100", 
        background_color="#868E96"
    )
        
    keyboard.add_button(
        command="sendMC", 
        label="MC-21", 
        background_color="#1864AB", 
    )

    print("added buttons")
        
        
    await bot.answer_message("Вас приветствует чат-бот ПАО \"Яковлев\". \nДля получения актуальной информации о ходе работ по авиационным проектам, пожалуйста, выберите соответствующую программу из списка:",
                                keyboard=keyboard)
        

@fsm.on(FSMStates.TESTSTATE, middlewares=[db_session_middleware])
async def testState(message: IncomingMessage, bot: Bot) -> None:
    await bot.answer_message(body="Тестовое состояние:")
    print("test")
    if message.body == "drop":
        await message.state.fsm.drop_state()
    #SJ-100 Основной мастер план 
@fsm.on(FSMStates.SENDSJ, middlewares=[db_session_middleware])
async def sendSJ(message: IncomingMessage, bot: Bot) -> None:
    image_path = "/media/SJ.png"
    await bot.answer_message("Запрошен отчёт \"Мастер-план по проекту SJ-100\". \nПожалуйста, подождите...")
    #await bot_stealth(message, bot, 5)
    async with aiofiles.open(image_path, "rb") as image_file:
        file = await OutgoingAttachment.from_async_buffer(image_file, "SJ_report.png")
    await bot.answer_message(body="Отчёт сформирован успешно:",file=file)
    

    if message.body == "/open_phase":
        await message.state.fsm.change_state(FSMStates.OPENPHASE)
        await open_phase(message, bot)
        return
    
        
    bubbles = BubbleMarkup()
    bubbles.add_button(
        command="/open_phase",
        label="Запросить список",
        background_color="#008080",
        new_row=True,
        data = {"programm_name": "SJ-100"}
    )
    await bot.answer_message("Выберите направление/этап для SJ-100",bubbles=bubbles)

#MC-21 основной мастер план
@fsm.on(FSMStates.SENDMC, middlewares=[db_session_middleware])
async def sendMC(message: IncomingMessage, bot: Bot) -> None:

    print("state SENDMC")

    image_path = "/media/MC.png"
    await bot.answer_message("Запрошен отчёт \"Мастер-план по проекту MC-21\". \nПожалуйста, подождите...")
    
    #await bot_stealth(message, bot, 5)
    
    async with aiofiles.open(image_path, "rb") as image_file:
       file = await OutgoingAttachment.from_async_buffer(image_file, "MC_report.png")
       await bot.answer_message(body="Отчёт сформирован успешно:",file=file)
       
    if message.body == "/open_phase":
        await message.state.fsm.change_state(FSMStates.OPENPHASE)
        await open_phase(message, bot)
        return
        
    bubbles = BubbleMarkup()
    bubbles.add_button(
        command="/open_phase",
        label="Запросить список",
        background_color="#008080",
        new_row=True,
        data = {"programm_name": "MC-21"}
    )
    await bot.answer_message("Выберите направление/этап для МС-21",bubbles=bubbles)

#Вывод сообщения при запросе списка вех для SJ
@fsm.on(FSMStates.OPENPHASE, middlewares=[db_session_middleware])
async def open_phase(message: IncomingMessage, bot: Bot) -> None:
    bubbles = BubbleMarkup()

    if message.body == "/open_milestone":
        await message.state.fsm.change_state(FSMStates.OPENMILESTONE)
        await open_milestone(message, bot)
        return
    elif message.body == "/back_to_programm":
        await message.state.fsm.change_state(FSMStates.BACKPROGRAMM)
        await back_to_programm(message, bot)
        return
        
    program_name = message.data["programm_name"]
    await sendProgram("Выберите направление/этап.", programm_name=program_name, bot=bot)

        
async def sendProgram(text_message, programm_name, bot: Bot):
    bubbles = BubbleMarkup()

    if programm_name == 'MC-21':
        color = "#1864AB"
        file_name = "dataMC.json"
    elif programm_name == 'SJ-100':
        color = "#868E96"
        file_name = "dataSJ.json"

    data = ReaderLinq.getResponseJsonFromFile(file_name)
    milestones, phases = ProgrammParser.parseProgramm(data)

    KeeperClass.phases = phases
    # await asyncio.gather(
    #     bot_stealth(message, bot, 5),
    #     answer_MC(message, bot, 1),)

            
    for phase in reversed(phases.keys()):
        bubbles.add_button(
            command="/open_milestone",
            label=phase,
            background_color=color,
            new_row=True,
            data = {"phase_name": phase, "programm_name": programm_name}
        )

    if programm_name == 'MC-21':
        bubbles.add_button(
            command="/sendCOS1",
            label="Готовность ВС МС.0012",
            background_color="#FCC419",
            new_row=True
        )

        bubbles.add_button(
            command="/sendCOS2",
            label="Готовность ВС МС.0013",
            background_color="#FCC419",
            new_row=True
        )

    bubbles.add_button(
        command="/back_to_programm",
        label="Вернуться к выбору программ",
        background_color="#008080",
        new_row=True
    )

    await bot.answer_message(text_message,bubbles=bubbles)

@fsm.on(FSMStates.OPENMILESTONE, middlewares=[db_session_middleware])
async def open_milestone(message: IncomingMessage, bot: Bot) -> None:

    bubbles = BubbleMarkup()
    phase_nameVar = message.data["phase_name"]
    programm_name = message.data["programm_name"]; 
    milestones = KeeperClass.phases[phase_nameVar][2]
    if programm_name == 'MC-21':
        color = "#1864AB"
    elif programm_name == 'SJ-100':
        color = "#868E96"

    #await bot_stealth(message, bot, 5)

    if message.body == "/process_milestone":
        await message.state.fsm.change_state(FSMStates.PROCESSMILESTONE)
        await process_milestone(message, bot)
        return
    elif message.body == "/back_to_phase":
        await message.state.fsm.change_state(FSMStates.BACKPHASE)
        await back_to_phase(message, bot)
        return

    for milestone in milestones:
        bubbles.add_button(
        command="/process_milestone",
        label=milestone["nameProject"],
        background_color=color,
        new_row=True,
        data = {"id_milestone": milestone["id"], "name_milestone": milestone["nameProject"], "phase_name": phase_nameVar, "programm_name": programm_name}
    )
    
    bubbles.add_button(
        command="/back_to_phase",
        label="Вернуться к выбору направлений",
        background_color="#008080",
        new_row=True,
        data = {"phase_name": phase_nameVar, "programm_name": programm_name}
    )


    await bot.answer_message("Выберите веху для " + phase_nameVar ,bubbles=bubbles)
    
    
@fsm.on(FSMStates.PROCESSMILESTONE, middlewares=[db_session_middleware])
async def process_milestone(message: IncomingMessage, bot: Bot) -> None:
     
    #############################
    id_milestoneVar = message.data["id_milestone"]; 
    text_report = await generate_report_by_milestone(id_milestoneVar)

    phase_nameVar = message.data["phase_name"]
    programm_name = message.data["programm_name"]; 

    if message.body == "/back_to_milestone":
        await message.state.fsm.change_state(FSMStates.BACKMILESTONE)
        await back_to_milestone(message, bot)
        return
    elif message.body == "/back_to_phase":
        await message.state.fsm.change_state(FSMStates.BACKPHASE)
        await back_to_phase(message, bot)
        return
        
    bubbles = BubbleMarkup()
    bubbles.add_button(
        command="/back_to_phase",
        label="Вернуться к выбору направлений",
        background_color="#008080",
        new_row=True,
        data = {"phase_name": phase_nameVar, "programm_name": programm_name}
    )

    bubbles.add_button(
        
        command="/back_to_milestone",
        label="Вернуться к выбору вех",
        background_color="#008080",
        new_row=True,
        data = {"phase_name": phase_nameVar, "programm_name": programm_name}
    )
    await bot.answer_message("***Отчёт о статусе вехи: " + message.data["name_milestone"] + "***\n" + text_report, bubbles=bubbles)
    
    
async def generate_report_by_milestone(id_milestoneVar):
    print("process veh")

    # TODO: LINQ
    data = ReaderLinq.getResponseJsonFromFile(id_milestoneVar + '.json')

    if not data or not len(data):
        return "Некорректный отчёт о статусе вех"

    message = "\n".join([
        "\n**Дата предоставления отчета:**",
        datetime.datetime.strptime(data[-1]["Дата_предоставления_отчета"][0:10], '%Y-%m-%d').strftime('%d.%m.%Y') if data[-1]["Дата_предоставления_отчета"] else "Отсутствует дата предоставления отчёта",
        "\n**Автор записи:**",
        data[-1]["Автор_записи"] if data[-1]["Автор_записи"] else "Отсутствует автор",
        "\n**Текущий статус:**",
        data[-1]["Текущий_статус"] if data[-1]["Текущий_статус"] else "Статус отсутствует",
        "\n**Риски:**",
        data[-1]["Риски"] if data[-1]["Риски"] else "Некорректно заполненные риски",
        "\n**Прогнозная дата завершения:**",
        datetime.datetime.strptime(data[-1]["Прогнозная_дата_завершения"][0:10], '%Y-%m-%d').strftime('%d.%m.%Y') if data[-1]["Прогнозная_дата_завершения"] else "Отсутствует дата завершения отчёта",
    ])

    return message

#вернуться на уровень выше к выбору программ
@fsm.on(FSMStates.BACKPROGRAMM, middlewares=[db_session_middleware])
async def back_to_programm(message: IncomingMessage, bot: Bot) -> None:
    bubbles = BubbleMarkup()
    
    if message.body == "/sendSJ":
        await message.state.fsm.change_state(FSMStates.SENDSJ)
        await sendSJ(message, bot)
        return
    elif message.body == "/sendMC":
        await message.state.fsm.change_state(FSMStates.SENDMC)
        await sendMC(message, bot)
        return
        
    bubbles.add_button(
        command="/sendSJ",
        label="SJ-100",
        background_color="#ADB5BD"
    )

    bubbles.add_button(
        command="/sendMC",
        label="MC-21",
        background_color="#1864AB",
        new_row=False
    )
    await bot.answer_message("Вас приветствует чат-бот ПАО \"Яковлев\". \nДля получения актуальной информации о ходе работ по авиационным проектам, пожалуйста, выберите соответствующую программу из списка:",
                             bubbles=bubbles)

@fsm.on(FSMStates.BACKPHASE, middlewares=[db_session_middleware])
async def back_to_phase(message: IncomingMessage, bot: Bot) -> None:
    # TODO: выбрать фазы какой программы.
    bubbles = BubbleMarkup()

    programm_name = message.data["programm_name"]

    await message.state.fsm.change_state(FSMStates.OPENPHASE)
    
#вернуться на уровень выше к выбору фаз
@fsm.on(FSMStates.BACKMILESTONE, middlewares=[db_session_middleware])
async def back_to_milestone(message: IncomingMessage, bot: Bot) -> None:
    # TODO: выбрать фазы какой программы.
    bubbles = BubbleMarkup()
    await message.state.fsm.change_state(FSMStates.OPENMILESTONE)
    await open_milestone(message, bot)
    return    