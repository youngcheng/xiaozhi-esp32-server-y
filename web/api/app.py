# api/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.admin import admin
from api.auth import auth as auth_router
from api.auth.dependencies import get_current_active_user

description = """
`VScode`启动! 🚀
"""

app = FastAPI(
    title="App",
    description=description,
    summary="我们生来，就是为了，在宇宙中，留下印记。",
    version="0.0.1",
    terms_of_service="https://blog.kalicyh.love/",
    contact={
        "name": "kalicyh",
        "url": "https://blog.kalicyh.love/",
        "email": "kalicyh@qq.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://mit-license.org/",
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
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

# 示例：受保护接口，需要 Bearer Token 验证
@app.get("/users/me")
async def read_users_me(current_user = Depends(get_current_active_user)):
    return current_user

# 挂载 React 静态文件
app.mount("/", StaticFiles(directory="dist", html=True), name="dist")

# 应用启动时检查并创建数据库表
@app.on_event("startup")
def on_startup():
    from api.db import database, models
    models.Base.metadata.create_all(bind=database.engine)
    print("数据库表检查完成，如果不存在则已创建！")
