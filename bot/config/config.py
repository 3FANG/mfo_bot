from dataclasses import dataclass
from environs import Env

@dataclass
class YooMoney:
    token: str
    account_number: int
    redirect_uri: str

@dataclass
class DBConfig:
    host: str
    password: str
    user: str
    database: str
    port: str

@dataclass
class TgBot:
    token: str

@dataclass
class Config:
    tg_bot: TgBot
    db: DBConfig
    ym: YooMoney

def load_environment():
    env = Env()
    env.read_env()
    return env

def load_config():
    env = load_environment()
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN')
        ),
        db=DBConfig(
            host=env('HOST'),
            password=env('PASSWORD'),
            user=env('USER'),
            database=env('DATABASE'),
            port=env('PORT')
        ),
        ym=YooMoney(
            token=env('YOOMONEY_TOKEN'),
            account_number=env('YOOMONEY_ACCOUNT_NUMBER'),
            redirect_uri=env('REDIRECT_URI')
        )
    )
