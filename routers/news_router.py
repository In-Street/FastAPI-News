from fastapi import APIRouter
from fastapi.params import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_session
from config.page import page_info
from services import news_service

new_router = APIRouter(prefix="/api/news", tags=["news"])


@new_router.get("/categories")
async def get_categories(page: dict = Depends(page_info), session: AsyncSession = Depends(get_session)):
	# return news_service.get_categories(session, page)   需 await
	result = await news_service.get_categories(session, page)
	return {
		"code": "200",
		"msg": "success",
		"data": result
	}


@new_router.get("/list")
async def get_news_list(page: dict = Depends(page_info),
                        session: AsyncSession = Depends(get_session),
                        category_id: int = Query(description="分类id", alias="categoryId", gt=0)):

	news_list = await news_service.get_news(session, page, category_id)
	total = await news_service.get_news_total(session, category_id)
	return {
		"code": "200",
		"msg": "success",
		"data": news_list,
		"total": total
	}
