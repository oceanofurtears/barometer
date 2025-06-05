from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.mixins import TimestampModelMixin
from src.database.db_helpers import Base


class BarModel(Base):
    __tablename__ = "bars"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(nullable=True)
    address: Mapped[str] = mapped_column(String(200))
    phone: Mapped[str] = mapped_column(String(20))
    rating: Mapped[float] = mapped_column(nullable=True, default=0.0)

    favorited_by = relationship(
        "UserModel",
        secondary="user_favorite_bar_association",
        back_populates="favorite_bars",
    )
    gallery = relationship("BarGalleryModel", back_populates="bar")
    cocktails = relationship("CocktailModel", back_populates="bar")
    reviews = relationship("ReviewBarModel", back_populates="bar")
    tags = relationship(
        "TagModel",
        secondary="bar_and_tag_association",
        back_populates="bars",
    )


class BarGalleryModel(Base):
    __tablename__ = "bars_gallery"

    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(String(200))
    bar_id: Mapped[int] = mapped_column(ForeignKey("bars.id"))

    bar = relationship("BarModel", back_populates="gallery")


class ReviewBarModel(Base, TimestampModelMixin):
    __tablename__ = "review_bar"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=True)
    rating: Mapped[int] = mapped_column(nullable=False)
    bar_id: Mapped[int] = mapped_column(ForeignKey("bars.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    bar = relationship("BarModel", back_populates="reviews")
    user = relationship("UserModel", back_populates="reviews_bar")
