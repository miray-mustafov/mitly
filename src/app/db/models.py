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
        """
        That additional check is necessary because testing database SQLite returns naive datetime,
        this way we avoid TypeError("can't compare offset-naive and offset-aware datetime")
        """
        if not self.expires_at:
            return False

        expires_at = self.expires_at

        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)  # force it to be UTC-aware so we can compare it.

        return datetime.now(timezone.utc) > expires_at

    def __repr__(self) -> str:
        return f"<Url(short='{self.short_url_id}', original='{self.original_url[:20]}...')>"
