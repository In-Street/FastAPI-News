from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from utils.exception_util import http_exception_handler, sqlalchemy_error_handler, general_exception_handler


def global_exception_registry(app:FastAPI):
	"""
		注册全局异常处理： 子类在前，父类在后； 具体在前，抽象在后
	"""
	app.add_exception_handler(HTTPException, http_exception_handler)
	app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
	app.add_exception_handler(Exception, general_exception_handler) # 兜底异常处理
