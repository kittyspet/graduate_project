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
    StatusRecipient,
    OutgoingAttachment,
    MentionBuilder,
)

from enum import Enum, auto
from pybotx import Bot, HandlerCollector, IncomingMessage
from pybotx_fsm import FSMCollector

from app.resources import strings

collector = HandlerCollector()


collectorAuth = HandlerCollector(middlewares=[ensure_admin_middleware])
collector = HandlerCollector()
