from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from url_shortener_api.ioc.registry import container
from url_shortener_api.routers.link_router import router as link_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


app = FastAPI(lifespan=lifespan)
setup_dishka(container=container, app=app)


@app.get("/ping")
async def ping():
    return {"msg": "pong"}


app.include_router(link_router)
