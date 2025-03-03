# web/db/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 获取数据库连接 URL，可通过环境变量设置，例如：
# SQLite:     sqlite:///./data/sql_app.db
# PostgreSQL: postgresql+asyncpg://user:password@localhost/dbname
# MySQL:      mysql+pymysql://user:password@localhost/dbname
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/sql_app.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    获取数据库会话
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
