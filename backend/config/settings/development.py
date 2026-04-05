from .base import *
from decouple import config
import dj_database_url

DEBUG = True

DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}