import asyncio
import contextlib
import logging
from datetime import datetime

from Handlers.handlers import reg_handlers
from Middlewares.db_middleware import DbSession
from Utils.bot_commands import set_commands
from Utils.get_logging import get_logging
from Utils.psycopg_pool import create_pool
from Utils.loader import dp, bot


async def start():
    get_logging()
    await set_commands(bot)
    pooling = await create_pool()
    dp.update.middleware.register(DbSession(pooling))
    reg_handlers()

    try:
        logging.error(f'[Successful start]: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', exc_info=True)
        await dp.start_polling(bot)
    except Exception as ex:
        logging.error(f"[ERROR] - {ex}", exc_info=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(start())
