from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse

from url_shortener_api.exceptions.link_exceptionals import (
    InvalidOriginalLinkError,
    ShortLinkNotFoundError,
)
from url_shortener_api.schemas.link_schemas import (
    CreateShorten,
    LinkStats,
    ShortenResponse,
)
from url_shortener_api.services.link_service import LinkService

router = APIRouter(
    prefix="",
    tags=["Shortener"],
    route_class=DishkaRoute,
)


@router.post(
    "/shorten",
    response_model=ShortenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_shorten_url(
    shorten: CreateShorten,
    service: FromDishka[LinkService],
) -> ShortenResponse:
    try:
        short_id = await service.create_short_link(shorten.original_link)
    except InvalidOriginalLinkError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error),
        )

    return ShortenResponse(short_id=short_id)


@router.get("/{short_id}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def get_short_url(
    short_id: str,
    service: FromDishka[LinkService],
) -> RedirectResponse:
    try:
        original_url = await service.resolve_short_link(short_id)
    except ShortLinkNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short link not found",
        )

    return RedirectResponse(
        url=original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )


@router.get("/stats/{short_id}", response_model=LinkStats)
async def get_short_url_stats(
    short_id: str,
    service: FromDishka[LinkService],
) -> LinkStats:
    try:
        count_redirects = await service.get_redirects_count(short_id)
    except ShortLinkNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short link not found",
        )

    return LinkStats(count_redirects=count_redirects)
