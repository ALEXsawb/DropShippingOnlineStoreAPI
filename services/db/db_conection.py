from aredis_om import get_redis_connection

from services.db.url import REDIS_DB_URL

db = get_redis_connection(url=REDIS_DB_URL, decode_responses=True)
