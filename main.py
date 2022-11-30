from fastapi import FastAPI

from StoreAPI import StoreAPI_router
from aredis_om import Migrator

app = FastAPI()
app.include_router(StoreAPI_router)


@app.on_event('startup')
async def connect_db():
    await Migrator().run()
