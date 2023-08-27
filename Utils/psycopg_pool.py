import psycopg_pool

from Settings.settings import settings


async def create_pool():
    return psycopg_pool.AsyncConnectionPool(
        f'host={settings.db.host} port=5432 dbname={settings.db.db} user={settings.db.user} '
        f'password={settings.db.password} connect_timeout=10'
    )
