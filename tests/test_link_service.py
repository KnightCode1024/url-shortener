from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from url_shortener_api.exceptions.link_exceptionals import (
    InvalidOriginalLinkError,
    ShortCodeGenerationError,
    ShortLinkNotFoundError,
)
from url_shortener_api.services.link_service import LinkService


@pytest.fixture
def repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def session() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def service(repository: AsyncMock, session: AsyncMock) -> LinkService:
    return LinkService(repository=repository, session=session)


@pytest.mark.asyncio
async def test_create_short_link_invalid_url_raises_error(
    service: LinkService,
    repository: AsyncMock,
    session: AsyncMock,
) -> None:
    with pytest.raises(InvalidOriginalLinkError):
        await service.create_short_link("example.com")

    repository.get_by_short_code.assert_not_called()
    repository.create.assert_not_called()
    session.commit.assert_not_called()
    session.rollback.assert_not_called()


@pytest.mark.asyncio
async def test_create_short_link_success_commits_transaction(
    service: LinkService,
    repository: AsyncMock,
    session: AsyncMock,
) -> None:
    repository.get_by_short_code.return_value = None

    with patch(
        "url_shortener_api.services.link_service.secrets.choice",
        return_value="a",
    ):
        short_id = await service.create_short_link("https://example.com")

    assert short_id == "aaaaaa"
    repository.create.assert_awaited_once_with(
        original_link="https://example.com",
        short_code="aaaaaa",
    )
    session.commit.assert_awaited_once()
    session.rollback.assert_not_called()


@pytest.mark.asyncio
async def test_create_short_link_after_collision(
    service: LinkService,
    repository: AsyncMock,
    session: AsyncMock,
) -> None:
    repository.get_by_short_code.side_effect = [object(), None]

    with patch(
        "url_shortener_api.services.link_service.secrets.choice",
        return_value="b",
    ):
        short_id = await service.create_short_link("https://example.com")

    assert short_id == "bbbbbb"
    assert repository.get_by_short_code.await_count == 2
    repository.create.assert_awaited_once_with(
        original_link="https://example.com",
        short_code="bbbbbb",
    )
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_short_link_raises_when_code_not_generated(
    service: LinkService,
    repository: AsyncMock,
    session: AsyncMock,
) -> None:
    repository.get_by_short_code.return_value = object()

    with patch(
        "url_shortener_api.services.link_service.secrets.choice",
        return_value="c",
    ):
        with pytest.raises(ShortCodeGenerationError):
            await service.create_short_link("https://example.com")

    assert repository.get_by_short_code.await_count == 10
    repository.create.assert_not_called()
    session.commit.assert_awaited_once()
    session.rollback.assert_not_called()


@pytest.mark.asyncio
async def test_resolve_short_link_increments_and_commits(
    service: LinkService,
    repository: AsyncMock,
    session: AsyncMock,
) -> None:
    link = SimpleNamespace(
        original_link="https://example.com",
        count_redirects=0,
    )
    repository.get_by_short_code.return_value = link

    result = await service.resolve_short_link("abc123")

    assert result == "https://example.com"
    repository.increment_redirects.assert_awaited_once_with(link)
    session.commit.assert_awaited_once()
    session.rollback.assert_not_called()


@pytest.mark.asyncio
async def test_resolve_short_link_not_found_rolls_back(
    service: LinkService,
    repository: AsyncMock,
    session: AsyncMock,
) -> None:
    repository.get_by_short_code.return_value = None

    with pytest.raises(ShortLinkNotFoundError):
        await service.resolve_short_link("missing")

    repository.increment_redirects.assert_not_called()
    session.commit.assert_not_called()
    session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_redirects_count_success(
    service: LinkService,
    repository: AsyncMock,
) -> None:
    link = SimpleNamespace(
        original_link="https://example.com",
        count_redirects=7,
    )
    repository.get_by_short_code.return_value = link

    result = await service.get_redirects_count("abc123")

    assert result == 7
    repository.get_by_short_code.assert_awaited_once_with("abc123")


@pytest.mark.asyncio
async def test_get_redirects_count_not_found(
    service: LinkService,
    repository: AsyncMock,
) -> None:
    repository.get_by_short_code.return_value = None

    with pytest.raises(ShortLinkNotFoundError):
        await service.get_redirects_count("missing")
