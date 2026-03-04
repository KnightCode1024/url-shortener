from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from url_shortener_api.models.link import Link


class LinkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_short_code(self, short_code: str) -> Link | None:
        stmt = select(Link).where(Link.short_code == short_code)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, original_link: str, short_code: str) -> Link:
        link = Link(original_link=original_link, short_code=short_code)
        self.session.add(link)
        await self.session.flush()
        await self.session.refresh(link)
        return link

    async def increment_redirects(self, link: Link) -> None:
        link.count_redirects += 1
        await self.session.flush()
