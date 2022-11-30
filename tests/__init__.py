import asyncio
from aredis_om import Migrator

asyncio.run(Migrator().run())
