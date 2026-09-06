"""
	通用成功响应格式
"""
from typing import Optional

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

def success_response(msg: Optional[str] = 'success', data=None):
	content = {
		"code": 200,
		"msg": msg,
		"data": data
	}

	# 把任何 fastapi、orm、pydantic 对象都响应成： code、msg、data 格式
	return  JSONResponse(content=jsonable_encoder(content))
