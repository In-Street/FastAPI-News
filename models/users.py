from datetime import datetime
from typing import Optional

from sqlalchemy import Index, Integer, String, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, DeclarativeBase
from sqlalchemy.testing.schema import mapped_column

from models.news import BaseColumns


# 用户表
class Users(BaseColumns):
	__tablename__ = "user"

	#索引项
	__table_args__ = (
		Index("username_UNIQUE", "username", unique=True),
		Index("phone_UNIQUE", "phone", unique=True),
	)

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
	password: Mapped[str] = mapped_column(String(50), nullable=False)
	gender: Mapped[str] = mapped_column(Enum('male', 'female', 'unknown'), nullable=False)

	nickname: Mapped[Optional[str]] = mapped_column(String(50))  # 当数据库字段允许为null，可设置为 Optional 可选项
	avatar: Mapped[Optional[str]] = mapped_column(String(50))

	phone: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)



# 用户令牌
class UserToken(BaseColumns):
	"""
		继承一个空的BaseNone，
	"""
	__tablename__ = "user_token"
	__table_args__ = (
		Index("token_UNIQUE", "token", unique=True),
	)
	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	token: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
	user_id: Mapped[int] = mapped_column(Integer, ForeignKey(Users.id), nullable=False)  # 设置外键对应的字段

	expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)