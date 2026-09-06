from fastapi import APIRouter, Header
from fastapi.params import Depends
from pydantic import model_validator
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_session
from dtos.user import UserRequest, UserResponse, UserInfoResponse, UpdateUserInfoRequest
from services import user_service
from services.user_service import get_user_by_token_2
from utils import response_util

user_router = APIRouter(prefix="/api/users", tags=["users"])


@user_router.post("/register")
async def create_user(user_request: UserRequest, db_session: AsyncSession = Depends(get_session)):
	user = await user_service.create_user(db_session, user_request.username, user_request.password,
	                                      user_request.nickname)
	print(f'获取user_id:{user.id}')
	token = await user_service.create_user_token(db_session, user.id)

	data = UserResponse(token=token, user_info=UserInfoResponse.model_validate(user))
	return response_util.success_response("注册成功", data=data)


@user_router.get("/get_user_by_token")
async def get_user_by_token(
		session: AsyncSession = Depends(get_session),
		authorization: str = Header(..., alias="Authorization"),
):
	current_user = await user_service.get_user_by_token(authorization, session)
	return response_util.success_response("获取当前用户成功", data=current_user)

@user_router.get("/get_user_by_token_2")
async def get_user_by_token_(
	current_user = Depends(get_user_by_token_2)
):
	"""
		将获取用户信息的方法，直接注入来获取当前用户
	"""
	return response_util.success_response("获取当前用户成功", data=current_user)

@user_router.post("/update_user_info")
async def update_user_info(
	update_user_request: UpdateUserInfoRequest,
	current_user:UserInfoResponse = Depends(get_user_by_token_2),
	se: AsyncSession = Depends(get_session)
):
	count = await user_service.update_user(update_user_request, current_user,se)
	return response_util.success_response("获取当前用户成功", data=count)