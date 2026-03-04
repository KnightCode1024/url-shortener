from sqlalchemy import Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from url_shortener_api.models.base import Base


class Link(Base):
    original_link: Mapped[str] = mapped_column(String())
    short_code: Mapped[str] = mapped_column(
        String(),
        unique=True,
        nullable=False,
        index=True,
    )
    count_redirects: Mapped[int] = mapped_column(
        Integer(),
        nullable=False,
        default=0,
        server_default=text("0"),
    )
