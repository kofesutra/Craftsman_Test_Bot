from typing import Callable, Awaitable, Any, Dict

import psycopg_pool
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from DB.db_requests import Request


class DbSession(BaseMiddleware):
    def __init__(self, connector: psycopg_pool.pool):
        super().__init__()
        self.connector = connector

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with self.connector.connection() as connect:
            data['request'] = Request(connect)
            return await handler(event, data)
