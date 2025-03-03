import os
import sys
from contextlib import asynccontextmanager  # 新增导入

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from web.api.admin import admin
from web.api.auth import auth as auth_router
from web.api.auth.dependencies import get_current_active_user

# 新增 lifespan 处理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时逻辑
    from web.api.db import models, database
    models.Base.metadata.create_all(bind=database.engine)
    print("数据库表检查完成，如果不存在则已创建！")
    yield  # 这里之后是关闭时逻辑（如果需要可以添加）

app = FastAPI(
    lifespan=lifespan,  # 添加 lifespan 参数
    title="App",
    description="",
    summary="你好小智",
    version="0.0.1",
    contact={
        "name": "xiaozhi-esp32-server",
        "url": "https://github.com/xinnan-tech/xiaozhi-esp32-server",
    },
    license_info={
        "name": "MIT",
        "url": "https://github.com/xinnan-tech/xiaozhi-esp32-server/blob/main/LICENSE",
    },
)

# 允许所有域名跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名
    allow_credentials=True,  # 允许携带 Cookies
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)

# 注册认证路由
app.include_router(auth_router.router, prefix="/web/v1/user", tags=["user"])
app.include_router(admin.router, prefix="/web/v1/admin", tags=["admin"])

# 示例：受保护接口，需要 Bearer Token 验证
@app.get("/users/me")
async def read_users_me(current_user = Depends(get_current_active_user)):
    return current_user

# 挂载 React 静态文件
# app.mount("/", StaticFiles(directory="dist", html=True), name="dist")

