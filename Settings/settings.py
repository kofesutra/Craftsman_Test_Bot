from dataclasses import dataclass
from environs import Env


@dataclass
class Bot:
    admin_id: int
    bot_token: str


@dataclass
class Data:
    group_to_check: int
    group_url: str
    channel_to_check: int
    channel_url: str
    logname: str
    csvname: str
    xlsxname: str


@dataclass
class Db:
    user: str
    host: str
    password: str
    db: str
    users: str
    categories: str
    subcategories: str
    goods: str
    orders: str
    incoming_users: str


@dataclass
class Pay:
    pay_token: str


@dataclass
class Settings:
    bot: Bot
    data: Data
    db: Db
    pay: Pay


def get_settings(path: str):
    env = Env()
    env.read_env()
    return Settings(
        bot=Bot(
            admin_id=env.int('ADMIN_ID'),
            bot_token=env.str('BOT_TOKEN')
        ),
        data=Data(
            group_to_check=env.int('GROUP_TO_CHECK'),
            group_url=env.str('GROUP_URL'),
            channel_to_check=env.int('CHANNEL_TO_CHECK'),
            channel_url=env.str('CHANNEL_URL'),
            logname=env.str('LOGNAME'),
            csvname=env.str('CSVNAME'),
            xlsxname=env.str('XLSXNAME')

        ),
        db=Db(
            user=env.str('DB_USER'),
            host=env.str('DB_HOST'),
            password=env.str('DB_PASSWORD'),
            db=env.str('DB_DATABASE'),
            users=env.str('TABLE_USERS'),
            categories=env.str('TABLE_CATEGORIES'),
            subcategories=env.str('TABLE_SUBCATEGORIES'),
            goods=env.str('TABLE_GOODS'),
            orders=env.str('TABLE_ORDERS'),
            incoming_users=env.str('TABLE_INCOMING')
        ),
        pay=Pay(
            pay_token=env.str('PAY_TOKEN')
        )
    )


settings = get_settings(".env")
