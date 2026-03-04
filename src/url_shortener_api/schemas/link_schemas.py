from pydantic import BaseModel


class CreateShorten(BaseModel):
    original_link: str


class ShortenResponse(BaseModel):
    short_id: str


class LinkStats(BaseModel):
    count_redirects: int
