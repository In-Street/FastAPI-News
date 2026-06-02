from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserRequest(BaseModel):
	username: str = Field(min_length=2, max_length=5, description="用户名长度在2～5之间")
	password: str
	nickname:Optional[str] = None


class UserInfoBase(BaseModel):
	"""
		用户基础信息，可选属性
	"""
	nickname: Optional[str] = Field(..., max_length=50, description="昵称")
	avatar: Optional[str] = Field(max_length=255)
	gender: Optional[str] = Field(max_length=1)


class UserInfoResponse(UserInfoBase):
	"""
		用户信息，必填属性
	"""
	id: int
	username: str

	model_config = ConfigDict(
		from_attributes=True,
	)


class UserResponse(BaseModel):
	token: str
	user_info: UserInfoResponse = Field(..., alias="userInfo")  # ... ：声明字段为必填项、 alias：设置前端接受的字段名

	model_config = ConfigDict(
		populate_by_name=True,  # alias/字段名的兼容
		from_attributes=True, # 允许从 orm对象中取值。当从数据库中获取到模型类后需要转成pydantic类，通过 UserResponse.model_validate(模型类) 来转换
	)
