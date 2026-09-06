"""
	全局异常处理器。
	注意：
		定义的函数的参数，必须包含：request: Request ，且放在第一位置
"""
import traceback

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Request
from starlette import status


DEBUG_MODE = True


async def http_exception_handler(request: Request, exc: HTTPException):
	"""
		处理 HTTPException 异常
	"""
	return JSONResponse(
		status_code=exc.status_code,
		content={
			"code": exc.status_code,
			"message": exc.detail + "-----",
			"traceback": traceback.format_exc(),
			"data": None
		}
	)

async def sqlalchemy_error_handler(request: Request,exc: SQLAlchemyError):
	"""
		处理 sqlalchemy 数据库错误
	"""
	error_data = None
	if DEBUG_MODE:
		error_data = {
			"error_detail": str(exc),
			"error_type": type(exc).__name__,
			"traceback": traceback.format_exc(),
			"path": request.url.path
		}

	return JSONResponse(
		status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
		content={
			"code": 500,
			"message": "--数据库操作失败，请稍后重试--",
			"data": error_data
		}
	)


async def general_exception_handler(request: Request,exc: Exception):
	"""
		处理所有未捕获的异常
	"""
	error_data = None
	if DEBUG_MODE:
		error_data = {
			"error_detail": str(exc),
			"error_type": type(exc).__name__,
			"traceback": traceback.format_exc(),
			"path": request.url.path
		}

	return JSONResponse(
		status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
		content={
			"code": 500,
			"message": "服务器内部错误",
			"data": error_data
		}
	)
