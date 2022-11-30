from decouple import config

REDIS_DB_URL = config('REDIS_DB_URL', default='redis://localhost:6379')
