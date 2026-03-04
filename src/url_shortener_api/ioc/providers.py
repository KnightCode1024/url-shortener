from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from url_shortener_api.config import Config, config
from url_shortener_api.repositories.link_repository import LinkRepository
from url_shortener_api.services.link_service import LinkService


class AppProvider(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> Config:
        return config

    @provide(scope=Scope.APP)
    async def get_engine(
        self,
        app_config: Config,
    ) -> AsyncIterable[AsyncEngine]:
        engine = create_async_engine(
            app_config.database.get_db_url,
            echo=False,
        )
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    def get_session_maker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    link_repository = provide(LinkRepository, scope=Scope.REQUEST)
    link_service = provide(LinkService, scope=Scope.REQUEST)
