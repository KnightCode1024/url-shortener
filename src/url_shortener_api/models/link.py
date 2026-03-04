from sqlalchemy import String
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
