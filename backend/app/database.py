from sqlmodel import create_engine, Session
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3

# 使用SQLModel兼容的配置
SQLALCHEMY_DATABASE_URL = "sqlite:///./chainorg.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=True
)

# 使SQLite支持ForeignKey约束  
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

SessionLocal = Session