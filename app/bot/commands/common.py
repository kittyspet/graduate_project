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

from app.bot.commands import common, admin, user

# class FSMStates(Enum):
#     SENDING_INFORMATION = auto()



# fsm = FSMCollector(FSMStates)

collector = HandlerCollector()


collectorAuth = HandlerCollector(middlewares=[db_session_middleware, ensure_admin_middleware])
collector = HandlerCollector()

class KeeperClass:
    milestones, phases = None, None
    readerLinq = ReaderLinq()

@collector.default_message_handler
async def default_handler(
    message: IncomingMessage,
    bot: Bot,
) -> None:
    """Run if command handler not found."""

    await bot.answer_message("Извините, команда неясна. Для получения отчета, пожалуйста, воспользуйтесь меню, кликнув на иконку с роботом справа, или отправьте сообщение с текстом «/start» в чат (без кавычек).")


@collectorAuth.chat_created
async def chat_created_handler(event: ChatCreatedEvent, bot: Bot) -> None:
    """Send a welcome message and the bot functionality in new created chat."""

    answer_body = strings.CHAT_CREATED_TEMPLATE.format(
        bot_project_name=strings.BOT_DISPLAY_NAME
    )

    keyboard = KeyboardMarkup()
    keyboard.add_button(command="/start", label="Начать")

    await bot.answer_message(answer_body, keyboard=keyboard)

@collectorAuth.command("/start", description="Начало")
async def start_command(message: IncomingMessage, bot: Bot) -> None:
    # print(message.body)
    print("/start")
    #await message.state.fsm.drop_state()

    if message.data["role"] == "admin":


        # await message.state.fsm.change_state(admin.FSMStates.WAITING_COMMAND)
        keyboard = KeyboardMarkup()
        keyboard.add_button(command='get_registration_requests', label="Получить запросы на регистрацию")
        await bot.answer_message(
        body="---Админ---\nВыберите действие",
            keyboard=keyboard
        )
        await message.state.fsm.change_state(admin.FSMStates.WAITING_COMMAND)
    elif message.data["role"] == "user":
        await bot.answer_message(
        body="---Админ---\nВыберите действие"
        )
        await message.state.fsm.change_state(user.FSMStates.CHOOSE_PROGRAMM)
        #await common.open_programm(message=message, bot=bot)
    else:
        await bot.answer_message(
        body="Доступ запрещён"
        )



# @fsm.on(FSMStates.SENDING_INFORMATION, middlewares=[db_session_middleware])
# async def sending_information(message: IncomingMessage, bot: Bot) -> None:
#     # if message.file:
#     #     await bot.answer_message(
#     #         body=strings.FILE_NOT_TITLE, keyboard=get_cancel_keyboard_button()
#     #     )
#     #     return
#     # либо тут делаем проверку
    
#     print("SENDING_INFORMATION_print")

# @collectorAuth.command("/start", description="Начало работы") # Тут сделать передачу в состояние get message, там где не проходит авторизация делать в состояние Auth
# async def open_programm(message: IncomingMessage, bot: Bot) -> None:
#     bubbles = BubbleMarkup()
#     bubbles.add_button(
#         command="/sendSJ", 
#         label="SJ-100", 
#         background_color="#868E96"
#     )
    
#     bubbles.add_button(
#         command="/sendMC", 
#         label="MC-21", 
#         background_color="#1864AB", 
#         new_row=False
#     )
#     await bot.answer_message("Вас приветствует чат-бот ПАО \"Яковлев\". \nДля получения актуальной информации о ходе работ по авиационным проектам, пожалуйста, выберите соответствующую программу из списка:",
#                              bubbles=bubbles)

# @collectorAuth.command("/open_programm", description="Начало работы")
# async def open_programm(message: IncomingMessage, bot: Bot) -> None:
#     bubbles = BubbleMarkup()
#     bubbles.add_button(
#         command="/sendSJ", 
#         label="SJ-100", 
#         background_color="#868E96"
#     )
    
#     bubbles.add_button(
#         command="/sendMC", 
#         label="MC-21", 
#         background_color="#1864AB", 
#         new_row=False
#     )
#     await bot.answer_message("Вас приветствует чат-бот ПАО \"Яковлев\". \nДля получения актуальной информации о ходе работ по авиационным проектам, пожалуйста, выберите соответствующую программу из списка:",
#                              bubbles=bubbles)
    
@collectorAuth.command("/add_programm", description="Добавить программу", visible=True)
async def add_programm(message: IncomingMessage, bot: Bot) -> None:

    auth: Auth = get_auth()
    auth.addProgramm(message.state.db_session, "MC-21")

    await bot.answer_message("Программа добавлена")
    

#    await bot.answer_message("Привет! \nЭто бот-демонстратор интеграции с Advanta.")
#sfdf
    #await bot.enable_stealth(
    #    bot_id = message.bot.id,
    #    chat_id = message.chat.id,
    #    total_ttl = 600,
    #    ttl_after_read = 600
    #    )

@collectorAuth.command("/feedback", description="Оставить отзыв", visible=True)
async def send_feedback(message: IncomingMessage, bot: Bot) -> None:
    await bot.answer_message("Если у Вас есть предложения или замечания по работе чат-бота, то Вы можете написать письмо на адрес chatbot@yakovlev.ru с темой \"Чат-бот - обратная связь\".")
#    await bot.answer_message("Привет! \nЭто бот-демонстратор интеграции с Advanta.")
    #await bot.enable_stealth(
    #    bot_id = message.bot.id,
    #    chat_id = message.chat.id,
    #    total_ttl = 600,
    #    ttl_after_read = 600
    #    )


@collectorAuth.command("/help", description="Как работает чат-бот",visible=True)
async def help_handler(message: IncomingMessage, bot: Bot) -> None:
    """Show commands list."""


#    status_recipient = StatusRecipient.from_incoming_message(message)

#    status = await bot.get_status(status_recipient)
#    command_map = dict(sorted(status.items()))

#    answer_body = "\n".join(
#        f"`{command}` -- {description}" for command, description in command_map.items()
#    )

    await bot.answer_message("Порядок действий по использованию чат-бота:\n1) Выбрать программу; \n2) Получить мастер-план по выбранной программе; \n3) Запросить список доступных направлений/этапов; \n4) Выбрать направление/этап; \n5) Получить список вех в выбранном этапе; \n6) Выбрать необходимую веху; \n7) Получить отчет по запрашиваемой вехе. \n**Информация в чат-боте обновляется каждую среду после 15:00. \nЕсли информация не была вовремя обновлена, то Вы можете написать письмо на** \nchatbot@yakovlev.ru.")


@collectorAuth.command("/_debug:git-commit-sha", visible=False)
async def git_commit_sha(message: IncomingMessage, bot: Bot) -> None:
    """Show git commit SHA."""

    await bot.answer_message(environ.get("GIT_COMMIT_SHA", "<undefined>"))


@collectorAuth.command("/_debug:version", visible=False)
async def build_version(message: IncomingMessage, bot: Bot) -> None:
    """Show app version."""
    cmd = "poetry version --short"
    output = run(cmd.split(), stdout=PIPE, stderr=STDOUT, text=True).stdout
    await bot.answer_message(output.strip("\n"))


# #SJ-100 Основной мастер план 
# @collectorAuth.command("/sendSJ", description="Сформировать мастер-план по проекту SJ-100", visible=False)
# async def open_milestone(message: IncomingMessage, bot: Bot) -> None:
#     image_path = "/media/SJ.png"
#     await bot.answer_message("Запрошен отчёт \"Мастер-план по проекту SJ-100\". \nПожалуйста, подождите...")
#     #await bot_stealth(message, bot, 5)
#     async with aiofiles.open(image_path, "rb") as image_file:
#         file = await OutgoingAttachment.from_async_buffer(image_file, "SJ_report.png")
#     await bot.answer_message(body="Отчёт сформирован успешно:",file=file)
    
#     bubbles = BubbleMarkup()
#     bubbles.add_button(
#         command="/open_phase",
#         label="Запросить список",
#         background_color="#008080",
#         new_row=True,
#         data = {"programm_name": "SJ-100"}
#     )
#     await bot.answer_message("Выберите направление/этап для SJ-100",bubbles=bubbles)

# #Тест на отложенный режим конфиденциальности
# async def bot_stealth(message: IncomingMessage, bot: Bot, delay: int) -> None:
#     delay = 0 # TODO: убрать
#     await asyncio.sleep(delay)
#     await bot.enable_stealth(
#     bot_id = message.bot.id,
#     chat_id = message.chat.id,
#     total_ttl = 600,
#     ttl_after_read = 600
#     )

# #Тест на отправку сообщения
# async def answer_MC(message: IncomingMessage, bot: Bot, delay: int) -> None:
#     await asyncio.sleep(delay)
#     image_path = "/media/MC.png"
#     async with aiofiles.open(image_path, "rb") as image_file:
#         file = await OutgoingAttachment.from_async_buffer(image_file, "MC_report.png")
#         await bot.answer_message(body="Отчёт сформирован успешно:",file=file)



# #MC-21 основной мастер план
# @collectorAuth.command("/sendMC", description="Сформировать мастер-план по проекту МС-21", visible=False)
# async def sendMC(message: IncomingMessage, bot: Bot) -> None:
#     image_path = "/media/MC.png"
#     await bot.answer_message("Запрошен отчёт \"Мастер-план по проекту MC-21\". \nПожалуйста, подождите...")
    
#     #await bot_stealth(message, bot, 5)
    
#     async with aiofiles.open(image_path, "rb") as image_file:
#        file = await OutgoingAttachment.from_async_buffer(image_file, "MC_report.png")
#        await bot.answer_message(body="Отчёт сформирован успешно:",file=file)

#     bubbles = BubbleMarkup()
#     bubbles.add_button(
#         command="/open_phase",
#         label="Запросить список",
#         background_color="#008080",
#         new_row=True,
#         data = {"programm_name": "MC-21"}
#     )
#     await bot.answer_message("Выберите направление/этап для МС-21",bubbles=bubbles)

# #Вывод сообщения при запросе списка вех для SJ
# @collectorAuth.command("/open_phase", description="Вывод списка вех", visible=False)
# async def open_phase(message: IncomingMessage, bot: Bot) -> None:
#     bubbles = BubbleMarkup()

#     program_name = message.data["programm_name"]
#     await sendProgram("Выберите направление/этап.", programm_name=program_name, bot=bot)


# async def sendProgram(text_message, programm_name, bot: Bot):
#     bubbles = BubbleMarkup()

#     if programm_name == 'MC-21':
#         color = "#1864AB"
#         file_name = "dataMC.json"
#     elif programm_name == 'SJ-100':
#         color = "#868E96"
#         file_name = "dataSJ.json"

#     data = ReaderLinq.getResponseJsonFromFile(file_name)
#     milestones, phases = ProgrammParser.parseProgramm(data)

#     KeeperClass.phases = phases
#     # await asyncio.gather(
#     #     bot_stealth(message, bot, 5),
#     #     answer_MC(message, bot, 1),)
    
#     for phase in reversed(phases.keys()):
#         bubbles.add_button(
#             command="/open_milestone",
#             label=phase,
#             background_color=color,
#             new_row=True,
#             data = {"phase_name": phase, "programm_name": programm_name}
#         )

#     if programm_name == 'MC-21':
#         bubbles.add_button(
#             command="/sendCOS1",
#             label="Готовность ВС МС.0012",
#             background_color="#FCC419",
#             new_row=True
#         )

#         bubbles.add_button(
#             command="/sendCOS2",
#             label="Готовность ВС МС.0013",
#             background_color="#FCC419",
#             new_row=True
#         )

#     bubbles.add_button(
#         command="/back_to_programm",
#         label="Вернуться к выбору программ",
#         background_color="#008080",
#         new_row=True
#     )

#     await bot.answer_message(text_message,bubbles=bubbles)


# @collectorAuth.command("/open_milestone", description="Сформировать мастер-план по проекту МС-21", visible=False)
# async def open_milestone(message: IncomingMessage, bot: Bot) -> None:
#     bubbles = BubbleMarkup()
#     phase_name = message.data["phase_name"]
#     programm_name = message.data["programm_name"]; 
#     milestones = KeeperClass.phases[phase_name][2]
#     if programm_name == 'MC-21':
#         color = "#1864AB"
#     elif programm_name == 'SJ-100':
#         color = "#868E96"

#     #await bot_stealth(message, bot, 5)

#     for milestone in milestones:
#         bubbles.add_button(
#         command="/process_milestone",
#         label=milestone["nameProject"],
#         background_color=color,
#         new_row=True,
#         data = {"id_milestone": milestone["id"], "name_milestone": milestone["nameProject"], "phase_name": phase_name, "programm_name": programm_name}
#     )
    
#     bubbles.add_button(
#         command="/back_to_phase",
#         label="Вернуться к выбору направлений",
#         background_color="#008080",
#         new_row=True,
#         data = {"phase_name": phase_name, "programm_name": programm_name}
#     )


#     await bot.answer_message("Выберите веху для " + phase_name ,bubbles=bubbles)


# @collectorAuth.command("/process_milestone", description="Сформировать мастер-план по проекту", visible=False)
# async def process_milestone(message: IncomingMessage, bot: Bot) -> None:
#     id_milestone = message.data["id_milestone"]; 
#     text_report = await generate_report_by_milestone(id_milestone)

#     phase_name = message.data["phase_name"]
#     programm_name = message.data["programm_name"]; 

#     bubbles = BubbleMarkup()
#     bubbles.add_button(
#         command="/back_to_phase",
#         label="Вернуться к выбору направлений",
#         background_color="#008080",
#         new_row=True,
#         data = {"phase_name": phase_name, "programm_name": programm_name}
#     )

#     bubbles.add_button(
        
#         command="/back_to_milestone",
#         label="Вернуться к выбору вех",
#         background_color="#008080",
#         new_row=True,
#         data = {"phase_name": phase_name, "programm_name": programm_name}
#     )
#     await bot.answer_message("***Отчёт о статусе вехи: " + message.data["name_milestone"] + "***\n" + text_report, bubbles=bubbles)
    
    
# async def generate_report_by_milestone(id_milestone):
#     print("process veh")

#     # TODO: LINQ
#     data = ReaderLinq.getResponseJsonFromFile(id_milestone + '.json')

#     if not data or not len(data):
#         return "Некорректный отчёт о статусе вех"

#     message = "\n".join([
#         "\n**Дата предоставления отчета:**",
#         datetime.datetime.strptime(data[-1]["Дата_предоставления_отчета"][0:10], '%Y-%m-%d').strftime('%d.%m.%Y') if data[-1]["Дата_предоставления_отчета"] else "Отсутствует дата предоставления отчёта",
#         "\n**Автор записи:**",
#         data[-1]["Автор_записи"] if data[-1]["Автор_записи"] else "Отсутствует автор",
#         "\n**Текущий статус:**",
#         data[-1]["Текущий_статус"] if data[-1]["Текущий_статус"] else "Статус отсутствует",
#         "\n**Риски:**",
#         data[-1]["Риски"] if data[-1]["Риски"] else "Некорректно заполненные риски",
#         "\n**Прогнозная дата завершения:**",
#         datetime.datetime.strptime(data[-1]["Прогнозная_дата_завершения"][0:10], '%Y-%m-%d').strftime('%d.%m.%Y') if data[-1]["Прогнозная_дата_завершения"] else "Отсутствует дата завершения отчёта",
#     ])

#     return message

# #вернуться на уровень выше к выбору программ
# @collectorAuth.command("/back_to_programm", description="Назад", visible=False)
# async def back_to_programm(message: IncomingMessage, bot: Bot) -> None:
#     bubbles = BubbleMarkup()
#     bubbles.add_button(
#         command="/sendSJ",
#         label="SJ-100",
#         background_color="#ADB5BD"
#     )

#     bubbles.add_button(
#         command="/sendMC",
#         label="MC-21",
#         background_color="#1864AB",
#         new_row=False
#     )
#     await bot.answer_message("Вас приветствует чат-бот ПАО \"Яковлев\". \nДля получения актуальной информации о ходе работ по авиационным проектам, пожалуйста, выберите соответствующую программу из списка:",
#                              bubbles=bubbles)

# #вернуться на уровень выше к выбору фаз
# @collectorAuth.command("/back_to_phase", description="Назад", visible=False)
# async def back_to_phase(message: IncomingMessage, bot: Bot) -> None:
#     # TODO: выбрать фазы какой программы.
#     bubbles = BubbleMarkup()

#     programm_name = message.data["programm_name"]

#     await sendProgram("Выберите направление/этап", programm_name, bot)
    
# #вернуться на уровень выше к выбору фаз
# @collectorAuth.command("/back_to_milestone", description="Назад", visible=False)
# async def back_to_milestone(message: IncomingMessage, bot: Bot) -> None:
#     # TODO: выбрать фазы какой программы.
#     bubbles = BubbleMarkup()
#     await open_milestone(message=message, bot=bot)


#     # await bot.answer_message("Выберите направление/этап",
#     #                          bubbles=bubbles)


#             #Готовность ВС МС.0012
# @collectorAuth.command("/sendCOS1", description="Готовность ВС МС.0012", visible=False)
# async def sendCOS1(message: IncomingMessage, bot: Bot) -> None:
#     image_path = "/media/COS1.pdf"
#     await bot.answer_message("Запрошен отчёт \"Готовность ВС МС.0012\". \nПожалуйста, подождите...")
#     await asyncio.sleep(5)
#     async with aiofiles.open(image_path, "rb") as image_file:
#         file = await OutgoingAttachment.from_async_buffer(image_file, "COS1_report.pdf")
#         await bot.enable_stealth(
#         bot_id = message.bot.id,
#         chat_id = message.chat.id,
#         total_ttl = 600,
#         ttl_after_read = 600
#         )
#         await bot.answer_message(body="Отчёт сформирован успешно:",file=file)

#     bubbles = BubbleMarkup()
#     bubbles.add_button(
#         command="/backMC",
#         label="Вернуться к выбору направления/этапа",
#         background_color="#008080",
#         new_row=True
#     )
    
#     await bot.answer_message("Выберите уровень к которому хотите вернуться:",bubbles=bubbles)


#             #Готовность ВС МС.0013
# @collectorAuth.command("/sendCOS2", description="Готовность ВС МС.0013", visible=False)
# async def sendCOS2(message: IncomingMessage, bot: Bot) -> None:
#     image_path = "/media/COS2.png"
#     await bot.answer_message("Запрошен отчёт \"Готовность ВС МС.0013\". \nПожалуйста, подождите...")
#     await asyncio.sleep(5)
#     async with aiofiles.open(image_path, "rb") as image_file:
#         file = await OutgoingAttachment.from_async_buffer(image_file, "COS2_report.png")
#         await bot.enable_stealth(
#         bot_id = message.bot.id,
#         chat_id = message.chat.id,
#         total_ttl = 600,
#         ttl_after_read = 600
#         )
#         await bot.answer_message(body="Отчёт сформирован успешно:",file=file)

#     bubbles = BubbleMarkup()
#     bubbles.add_button(
#         command="/backMC",
#         label="Вернуться к выбору направления/этапа",
#         background_color="#008080",
#         new_row=True
#     )

#     await bot.answer_message("Выберите уровень к которому хотите вернуться:",bubbles=bubbles)  





'''
#Упоминание пользователя чата в сообщении
@collector.command("/send-contact", description="Send author's contact")
async def send_contact_handler(message: IncomingMessage, bot: Bot) -> None:
    contact = MentionBuilder.contact(message.sender.huid)
    name  = MentionBuilder.user(message.sender.username)
    await bot.answer_message(f"Author is {contact}")
    await bot.answer_message(f"Author name is {name}")
    
    #Заготовка для презентации Servicedesk
@collectorAuth.command("/start", description="Начало работы")
async def start_temp(message: IncomingMessage, bot: Bot) -> None:
    bubbles = BubbleMarkup()
    bubbles.add_button(
        command="/sendIS", 
        label="Исполнитель", 
        background_color="#868E96"
    )
    
    bubbles.add_button(
        command="/sendZA", 
        label="Инициатор", 
        background_color="#1864AB", 
        new_row=False
    )
    await bot.answer_message("Вас приветствует чат-бот \"Яковлев HelpDesk\".\n Пожалуйста, выберите группу группу пользователей:\n Исполнитель / Инициатор",
                             bubbles=bubbles)
    
@collectorAuth.command("/sendIS", description="", visible=False)
async def tempIS(message: IncomingMessage, bot: Bot) -> None:
    bubbles = BubbleMarkup()
    bubbles.add_button(
        command="/nazn",
        label="Назначено на РГ",
        background_color="#799C42",
        new_row=True,
    )
    bubbles.add_button(
        command="/vrab",
        label="В работе",
        background_color="#CE6317",
        new_row=True,
    )
    bubbles.add_button(
        command="/otl",
        label="Отложено",
        background_color="#3486D2",
        new_row=True,
    )
    bubbles.add_button(
        command="/pros",
        label="Просрочено",
        background_color="#A10800",
        new_row=True,
    )
    await bot.answer_message("Выбрана роль \"Исполнитель\".\n Выберите статус обращения",bubbles=bubbles)
    
@collectorAuth.command("/vrab", description="", visible=False)
async def tempSD(message: IncomingMessage, bot: Bot) -> None:
    bubbles = BubbleMarkup()
    bubbles.add_button(
        command="/sotr",
        label="Подключение нового сотрудника",
        background_color="#008080",
        new_row=True,
    )
    bubbles.add_button(
        command="/pom",
        label="Помощь в настройке",
        background_color="#008080",
        new_row=True,
    )
    bubbles.add_button(
        command="/obs",
        label="Организация ВКС",
        background_color="#008080",
        new_row=True,
    )
    bubbles.add_button(
        command="/inc",
        label="Инцидент",
        background_color="#FF2400",
        new_row=True,
    )
    await bot.answer_message("Типы обращений в статусе \"В работе\":",bubbles=bubbles)

@collectorAuth.command("/inc", description="", visible=False)
async def tempSD(message: IncomingMessage, bot: Bot) -> None:
    bubbles = BubbleMarkup()
    bubbles.add_button(
        command="/zad1",
        label="352663 от Иванова И.И",
        background_color="#008080",
        new_row=True,
    )
    bubbles.add_button(
        command="/zad2",
        label="352658 от Петрова П.П.",
        background_color="#008080",
        new_row=True,
    )
    bubbles.add_button(
        command="/zad3",
        label="352303 от Воробьева В.В.",
        background_color="#008080",
        new_row=True,
    )
    await bot.answer_message("Текущие задачи типа \"Инцидент\" в статусе \"В работе\":",bubbles=bubbles)
    
@collectorAuth.command("/zad3", description="", visible=False)
async def tempSD(message: IncomingMessage, bot: Bot) -> None:
    bubbles = BubbleMarkup()
    bubbles.add_button(
        command="/naz",
        label="Назад",
        background_color="#008080",
        new_row=True,
    )

    await bot.answer_message("Ответ по конкретной задаче",bubbles=bubbles)
    
    #Заготовка под заказчика
@collectorAuth.command("/sendZA", description="", visible=False)
async def tempIS(message: IncomingMessage, bot: Bot) -> None:
    bubbles = BubbleMarkup()
    bubbles.add_button(
        command="/inc1",
        label="352619 \"Инцидент\" от 20.02.25",
        background_color="#008080",
        new_row=True,
    )
    bubbles.add_button(
        command="/nas1",
        label="352105 \"Настройка оборудования\" от 14.02.25",
        background_color="#008080",
        new_row=True,
    )
    bubbles.add_button(
        command="/org1",
        label="351849 \"Организация ВКС\" от 29.01.25",
        background_color="#008080",
        new_row=True,
    )
    await bot.answer_message("Выбрана роль \"Инициатор\".\n Пожалуйста, выберите номер обращения:",bubbles=bubbles)
    
@collectorAuth.command("/nas1", description="", visible=False)
async def tempSD(message: IncomingMessage, bot: Bot) -> None:
    bubbles = BubbleMarkup()
    bubbles.add_button(
        command="/naz",
        label="Назад",
        background_color="#008080",
        new_row=True,
    )

    await bot.answer_message("**Выбрано обращение \"352105\"**\n\n**Тема:**\nПодключение оборудования\n\n**Описание:**\nДобрый день! Прошу подключить новый телефон в кабинете 320.\n\n**Дата регистрации запроса:**\n14.02.25\n\n**Регламентное время решения:**\n21.02.25\n\n**Статус:**\nРешено\n\n**Время входа в статус:**\n14.02.25",bubbles=bubbles)
    
    #Заготовка для презентации Redmine
@collectorAuth.command("/startred", description="Начало работы")
async def start_temp(message: IncomingMessage, bot: Bot) -> None:
    bubbles = BubbleMarkup()
    bubbles.add_button(
        command="/mzad", 
        label="Назначенные мне", 
        background_color="#868E96"
    )
    
    bubbles.add_button(
        command="/szad", 
        label="Созданные мною", 
        background_color="#1864AB", 
        new_row=False
    )
    await bot.answer_message("Вас приветствует чат-бот \"Помощник по Отделу\"\nВыберите группу задач:",
                             bubbles=bubbles)
    
@collectorAuth.command("/mzad", description="", visible=False)
async def tempIS(message: IncomingMessage, bot: Bot) -> None:
    bubbles = BubbleMarkup()
    bubbles.add_button(
        command="/zadr1",
        label="1418 - Редактор модуля данных",
        background_color="#008080",
        new_row=True,
    )
    bubbles.add_button(
        command="/zadr2",
        label="1426 - Интеграция с RAMan",
        background_color="#008080",
        new_row=True,
    )
    bubbles.add_button(
        command="/zadr3",
        label="1396 - БДЗЧ",
        background_color="#008080",
        new_row=True,
    )
    await bot.answer_message("Список назначенных мне задач:",bubbles=bubbles)
    
@collectorAuth.command("/zadr1", description="", visible=False)
async def tempSD(message: IncomingMessage, bot: Bot) -> None:
    bubbles = BubbleMarkup()
    bubbles.add_button(
        command="/file",
        label="Показать прикрепленные файлы",
        background_color="#008080",
        new_row=True,
    )
    bubbles.add_button(
        command="/svaz",
        label="Связанные задачи",
        background_color="#008080",
        new_row=True,
    )
    bubbles.add_button(
        command="/izm",
        label="Список изменений",
        background_color="#008080",
        new_row=True,
    )
    await bot.answer_message("**Выбрана задача 1418 - Редактор модуля данных**\n\n**Статус:**\nВ работе\n\n**Описание:**\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n\n**Оценка временных затрат:**\n40 ч.\n\n**Рейтинг задачи:**\n133",bubbles=bubbles)

@collectorAuth.command("/file", description="", visible=False)
async def tempSD(message: IncomingMessage, bot: Bot) -> None:
    bubbles = BubbleMarkup()
    bubbles.add_button(
        command="/file1",
        label="Блок-схема",
        background_color="#008080",
        new_row=True,
    )
    bubbles.add_button(
        command="/file2",
        label="Получение логов",
        background_color="#008080",
        new_row=True,
    )
    bubbles.add_button(
        command="/file3",
        label="Модель данных",
        background_color="#008080",
        new_row=True,
    )
    bubbles.add_button(
        command="/file4",
        label="Набор",
        background_color="#008080",
        new_row=True,
    )
    await bot.answer_message("**Прикреплённые файлы к задаче 1418 - Редактор модуля данных**",bubbles=bubbles)

@collectorAuth.command("/izm", description="", visible=False)
async def tempSD(message: IncomingMessage, bot: Bot) -> None:
    bubbles = BubbleMarkup()
    bubbles.add_button(
        command="/naz",
        label="Назад",
        background_color="#008080",
        new_row=True,
    )
    await bot.answer_message("Список изменений по задаче **1418 - Редактор модуля данных**\n\n#2\n*Параметр Оценка временных затрат изменился на 40.00 ч\nПараметр Трудозатраты изменился на Низкие\nПараметр Рейтинг задачи изменился на 133.00*\n\n**Комментарий:** Меняем приоритет задачи на \"Низкий\"\n\n#1\n*Параметр Влияние изменился на Среднее\nПараметр Воздействие изменился на Среднее\nПараметр Достаточность информации изменился на Минимальная\nПараметр Срочность изменился на Низкая*",bubbles=bubbles)
    
        #Заготовка для презентации Админки
@collectorAuth.command("/startadm", description="Начало работы")
async def start_temp(message: IncomingMessage, bot: Bot) -> None:
    bubbles = BubbleMarkup()
    bubbles.add_button(
        command="/pol", 
        label="Получить запросы на регистрацию", 
        background_color="#868E96"
    )
    
    bubbles.add_button(
        command="/udal", 
        label="Удалить пользователя", 
        background_color="#1864AB", 
        new_row=True
    )
    await bot.answer_message("---Админ---\nВыберите действие:",
                             bubbles=bubbles)
    
@collectorAuth.command("/pol", description="", visible=False)
async def tempIS(message: IncomingMessage, bot: Bot) -> None:
    bubbles = BubbleMarkup()
    bubbles.add_button(
        command="/ivan",
        label="Иванов П.П",
        background_color="#008080",
        new_row=True,
    )
    bubbles.add_button(
        command="/pet",
        label="Петров И.И",
        background_color="#008080",
        new_row=True,
    )
    bubbles.add_button(
        command="/vas",
        label="Васильев В.В",
        background_color="#008080",
        new_row=True,
    )
    await bot.answer_message("Запросы:\n\nИванов П.П\nПетров И.И\nВасильев В.В\n\nВыберите пользователя:",bubbles=bubbles)
    
@collectorAuth.command("/ivan", description="", visible=False)
async def tempSD(message: IncomingMessage, bot: Bot) -> None:
    bubbles = BubbleMarkup()
    bubbles.add_button(
        command="/ssj",
        label="Участник SSJ",
        background_color="#008080",
        new_row=True,
    )
    bubbles.add_button(
        command="/adssj",
        label="Руководитель SSJ",
        background_color="#008080",
        new_row=True,
    )
    bubbles.add_button(
        command="/mc",
        label="Участник MC21",
        background_color="#008080",
        new_row=True,
    )
    bubbles.add_button(
        command="/admc",
        label="Руководитель MC21",
        background_color="#008080",
        new_row=True,
    )
    bubbles.add_button(
        command="/adm",
        label="Админ",
        background_color="#008080",
        new_row=True,
    )
    bubbles.add_button(
        command="/vib",
        label="Точечная настройка доступа",
        background_color="#008080",
        new_row=True,
    )
    await bot.answer_message("Выберите предоставляемый шаблон прав:",bubbles=bubbles)
    '''