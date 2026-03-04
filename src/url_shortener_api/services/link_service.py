from contextlib import asynccontextmanager
import secrets
import string
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from url_shortener_api.exceptions.link_exceptionals import (
    InvalidOriginalLinkError,
    ShortCodeGenerationError,
    ShortLinkNotFoundError,
)
from url_shortener_api.repositories.link_repository import LinkRepository


class LinkService:
    def __init__(
        self,
        repository: LinkRepository,
        session: AsyncSession,
    ) -> None:
        self.repository = repository
        self.session = session

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[None]:
        try:
            yield
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

    async def create_short_link(self, original_link: str) -> str:
        if not (
            original_link.startswith("http://")
            or original_link.startswith(
                "https://",
            )
        ):
            raise InvalidOriginalLinkError(
                "original_link must start with http:// or https://"
            )

        alphabet = string.ascii_letters + string.digits

        async with self.transaction():
            for _ in range(10):
                short_code = "".join(secrets.choice(alphabet) for _ in range(6))
                existing = await self.repository.get_by_short_code(short_code)
                if existing is None:
                    await self.repository.create(
                        original_link=original_link,
                        short_code=short_code,
                    )
                    return short_code

        raise ShortCodeGenerationError("Failed to generate unique short code")

    async def resolve_short_link(self, short_id: str) -> str:
        async with self.transaction():
            link = await self.repository.get_by_short_code(short_id)
            if link is None:
                raise ShortLinkNotFoundError(short_id)

            await self.repository.increment_redirects(link)
            return link.original_link

    async def get_redirects_count(self, short_id: str) -> int:
        link = await self.repository.get_by_short_code(short_id)
        if link is None:
            raise ShortLinkNotFoundError(short_id)
        return link.count_redirects
