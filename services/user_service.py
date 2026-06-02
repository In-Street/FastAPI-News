import datetime
import uuid
from datetime import timedelta
from typing import Optional

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import Users, UserToken
from utils import security_util

"""
	session.flush:  session ->Database（推）
		1. 目的：将内存中的变更同步到数据库。如 insert/update/delete，是事务的一部分，可以回滚
		2. 通常用于：
				获取自增ID、触发数据库的约束检查、批量操作时释放内存
	
	session.refresh(instance):  Database -> Instance（拉）
		1. 目的： 从数据库重新加载实例的最新状态，用数据库中的当前值覆盖内存中的值。 是只读操作，不影响事务
		2. 通常用于：
				避免脏读，确保数据一致性、处理并发更新场景
"""
async def get_user_by_username(session: AsyncSession, username: str):
	select_ = Select(Users).where(Users.username == username)
	result = await session.execute(select_)
	user = result.scalar_one_or_none()
	return user


async def create_user(session: AsyncSession, username: str, password: str, nickname: Optional[str]) -> Users:
	u = Users()
	u.username = username
	u.password = security_util.crypt(password)
	u.nickname =nickname
	session.add(u)

	await session.flush()
	# await session.commit()
	# await session.refresh(u)  # refresh 必须在commit/flush之后使用，把数据库中最新数据覆盖回本地u对象
	return u


async def create_user_token(session: AsyncSession, user_id):
	token = str(uuid.uuid4())
	expire = datetime.datetime.now() + timedelta(hours=5)
	user_token = UserToken(user_id=user_id, token=token, expires_at=expire)
	session.add(user_token)
	return token
