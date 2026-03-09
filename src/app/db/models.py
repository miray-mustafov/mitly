from datetime import datetime, timezone
from .database import Base  # relative import
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, func


class Url(Base):
    """
    short_url_id:
        String(length=8) bcs 62^8 = ~218 trillion combinations, which is enough
        index=True bcs we want fast lookups by short_url_id to redirect to original_url
    created_at:
        timezone=True to handle UTC offsets automatically at DB level
    """

    __tablename__ = "urls"

    url_id: Mapped[int] = mapped_column(primary_key=True)
    short_url_id: Mapped[str] = mapped_column(String(8), unique=True, index=True)
    original_url: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    @property
    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) > self.expires_at  # timezone aware

    def __repr__(self) -> str:
        return f"<Url(short='{self.short_url_id}', original='{self.original_url[:20]}...')>"
