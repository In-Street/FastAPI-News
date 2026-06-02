from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers.news_router import new_router
from routers.user_router import user_router

app = FastAPI(title="新闻", version="1.0.0")

# 注册路由
app.include_router(new_router)
app.include_router(user_router)

# 跨域
origins = [
	"http://localhost:3000",
]
app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,  # 允许携带Cookie
	allow_methods=["*"],  # 允许的请求方法
	allow_headers=["*"],  # 允许的请求头
)
