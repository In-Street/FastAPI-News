from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, func, String, Integer, Text, Index, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column, Column


class BaseColumns(DeclarativeBase):
	created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
	updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=func.now(), onupdate=func.now())



class NewsCategory(BaseColumns):
	__tablename__ = "news_category"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	name: Mapped[str] = mapped_column(String(50))
	sort_order: Mapped[int] = mapped_column(Integer, default=0)


class News(BaseColumns):
	__tablename__ = "news"

	__table_args__ = (
		Index("fk_news_category_idx","category_id"),
		Index("idx_publish_time","publish_time")
	)

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	title: Mapped[str] = mapped_column(String(50))
	description: Mapped[str] = mapped_column(String(500), nullable=False, comment="新闻简介")
	content: Mapped[str] = mapped_column(Text, nullable=False)
	image: Mapped[str] = mapped_column(String(255), nullable=False)
	author: Mapped[str] = mapped_column(String(50), nullable=False)
	views: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="浏览量")
	category_id: Mapped[int] = mapped_column(Integer, ForeignKey("news_category.id"))
	publish_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="发布时间")
