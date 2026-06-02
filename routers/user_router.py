from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import model_validator
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_session
from dtos.user import UserRequest, UserResponse, UserInfoResponse
from services import user_service
from utils import response_util

user_router = APIRouter(prefix="/api/users", tags=["users"])


@user_router.post("/register")
async def create_user(user_request: UserRequest, db_session: AsyncSession = Depends(get_session)):
	user = await user_service.create_user(db_session, user_request.username, user_request.password,user_request.nickname)
	print(f'获取user_id:{user.id}')
	token = await user_service.create_user_token(db_session,user.id)

	data = UserResponse(token=token,  user_info=UserInfoResponse.model_validate(user))
	return response_util.success_response("注册成功", data=data)