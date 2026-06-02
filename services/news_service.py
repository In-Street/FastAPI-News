from sqlalchemy import Select, func, Update
from sqlalchemy.ext.asyncio import AsyncSession

from models.news import NewsCategory, News


async def get_categories(session: AsyncSession, page: dict):
	select_ = Select(NewsCategory).offset((page['page'] - 1) * page['size']).limit(page['size'])
	result = await session.execute(select_)
	return result.scalars().all()


async def get_news(session: AsyncSession, page: dict, news_category_id: int):
	select_ = Select(News).where(News.category_id == news_category_id).offset((page['page'] - 1) * page['size']).limit(
		page['size'])

	# return result.scalars().all()  # 全量字段的数据

	# 只查询部分字段，并设置返回的名称。
	# result.scalars().all() ： 直接返回第一个字段的值，没有字段名称，也没有第二个字段的值
	# result.mappings().all()：返回字典形式，{"newsId":54,"newsAuthor":"环保在线"}。 或者返回全量字段，然后列表推导式进行手动拼接要返回的字段
	select_2 = (Select(News.id.label("newsId"),
	                   News.author.label("newsAuthor"))
	.where(News.category_id == news_category_id)
	.order_by(News.id.desc())
	.offset((page['page'] - 1) * page['size']).limit(page['size']))

	result = await session.execute(select_2)
	return result.mappings().all()

# return [  # 返回指定字段
# 	{
# 		"title": new_detail.title,
# 		"description": new_detail.description,
# 		"author": new_detail.author,
# 		"category_id": news_category_id,
# 		"id": new_detail.id
# 	}
# 	 for new_detail in result.scalars().all()
# ]

async def get_news_total(session: AsyncSession, news_category_id: int):
	select_ = Select(func.count(News.id)).where(News.category_id == news_category_id)
	result = await session.execute(select_)

	update_ = Update(News).where(News.id == 52).values(views=News.views + 1)
	update_result = await session.execute(update_)
	print(update_result.rowcount)  # 受影响行数

	return result.scalar_one()  # 只能有一个结果
