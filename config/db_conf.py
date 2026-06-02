from fastapi import HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

db_url = "mysql+aiomysql://root:taylor18@localhost:3306/fastapi_news_app"

# 创建异步引擎
engine = create_async_engine(db_url,
                             echo=True,
                             pool_pre_ping=True,
                             pool_recycle=3600,
                             max_overflow=10,  # 池中允许创建的额外连接数
                             pool_size=5,  # 池中保持的持久连接数
                             )

# 创建会话工厂
sessionmaker = async_sessionmaker(
	bind=engine,
	expire_on_commit=False,
)

# 创建依赖项，用于路由函数获取数据库会话
async def get_session():
	async with sessionmaker() as session:
		try:
			yield session
			await session.commit()
		except Exception as e:
			await session.rollback()
			raise HTTPException(status_code=500, detail=str(e))