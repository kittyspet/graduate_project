
from dataclasses import dataclass
from app.db.record.models import Users, Programm
from sqlalchemy.orm import Session

@dataclass
class InfoUser:
    is_admin: bool
    huid: str
    user_name: str
    login: str
    

# TODO: добавить singelton и redis
class Auth:
    def __init__(self):
        self.roles = {
            "admin": [],
            "user": []
        }



        self.users = {}

    # Это по-другому делать
    def addUser(self, db_session: Session, is_admin, huid, user_name, login):
        self.users[huid] = InfoUser(
        is_admin=is_admin,
        huid=huid,
        user_name=user_name,
        login=login
        )
        # new_u
        # db_session

    def addProgramm(self, db_session: Session, name):
        programm = Programm(designation=name)
        db_session.add(programm)
        db_session.commit()
        db_session.refresh(programm)
        return programm

    def getUsers(self):
        return self.users
    
    def register():
        pass

    # Просто отправка сообщения
    def sendMessage():
        pass
        #await bot.send_message(
        #     bot_id=message.bot.id,
        #     chat_id="4e75f043-6eba-50d2-8822-474e164c8a9b",
        #     body="text",
        # )

