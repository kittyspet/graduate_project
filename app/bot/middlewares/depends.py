from fastapi import Depends
from app.bot.middlewares.Auth import *



auth = Auth()
def get_auth() -> Auth:
    return auth