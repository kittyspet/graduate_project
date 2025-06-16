from uuid import UUID
from pybotx import *
from app.bot.middlewares.depends import get_auth
from app.bot.middlewares.Auth import *
from fastapi import Depends
from app.bot.middlewares.db_session import db_session_middleware


ADMIN_HUIDS = (#UUID("test_id1"), 
               UUID("test_id2"), 
            #    UUID("test_id3"), 
               UUID("test_id4"), 
                )

USER_HUIDS = (
               UUID("test_id5"),
               UUID("test_id6"),
               UUID("test_id7"), 
               )

async def ensure_admin_middleware(
    message: IncomingMessage, 
    bot: Bot,
    call_next: IncomingMessageHandlerFunc,
) -> None:
    
    # TODO: тут должна быть проверка через базу данных
    if message.sender.huid  in ADMIN_HUIDS:
        message.data = {"role": 'admin'}
    elif message.sender.huid  in USER_HUIDS:
        message.data = {"role": 'user'}
    else:
        message.data = {"role": 'denied'}
    
    #if message.sender.huid in 


        # print("my message bot id dlfkkjsdfiubjhdfigubhdfogibuhdfgoub", message.bot.id)
        # await bot.send_message(
        #     bot_id=message.bot.id,
        #     chat_id="9ec5ce49-ce31-08c0-3d64-ae568a575c7b",
        #     body="asdasd",
        # )


        # if (message.sender.huid == "4e75f043-6eba-50d2-8822-474e164c8a9b"):
        #      await bot.answer_message("АНДВАНТА ГОВНО")
        # await bot.answer_message("У вас нет доступа к этой команде бота. Доступ на функционал чат-бота должен быть согласован с проектным офисом.")
        # return

    # print ("test get message", message.sender.huid)
    # if str(message.sender.huid) == "54ba9316-cfa4-561f-b1f5-77bf59d4a7d7":
    #     print("in condition")
        # auth: Auth = get_auth()
        # print("type auth -- ", type(auth))
        # print("user print ffffffffffff", auth.getUsers())
        # auth.addUser(huid="sdfdsfgsdfg", is_admin=True, user_name="Kirill", login="sdfsfer")



    # await message.state.fsm.change_state(common.FSMStates.SENDING_INFORMATION, email=email(тут передавать нужную роль))
    # print ("common.FSMStates.SENDING_INFORMATION")
    # await bot.answer_message("Введите имя")
    # await db_session_middleware(message=message, bot=bot, call_next=call_next)
    await call_next(message, bot)
