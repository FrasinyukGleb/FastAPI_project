import multiprocessing

from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings

from fastapi.security import OAuth2PasswordBearer


# специальный класс для настройки авторизации в Swagger
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/user/token')

class AppSettings(BaseSettings):
    app_port: int = 8000
    app_host: str = 'localhost'
    reload: bool = True
    cpu_count: int | None = None
    jwt_secret: str = "your_super_secret"
    algorithm: str = "HS256"

    postgres_dsn: PostgresDsn = MultiHostUrl(
    'postgresql+asyncpg://admin:admin@localhost/fastapi')
    class Config:
        _env_file = ".env"
        _extra = 'allow'


app_settings = AppSettings()

# набор опций для запуска сервера
uvicorn_options = {
    "host": app_settings.app_host,
    "port": app_settings.app_port,
    "workers": app_settings.cpu_count or multiprocessing.cpu_count(),
    "reload": app_settings.reload,
}