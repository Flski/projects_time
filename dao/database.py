from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
import os
import asyncio

dir_path = os.path.dirname(__file__)

if "projects.db" not in os.listdir(dir_path):
    from sqlalchemy import create_engine
    engine = create_engine(
      "sqlite:///"+os.path.join(dir_path, "projects.db"),
      connect_args={"check_same_thread": False}
    )
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "init.sql"), "r", encoding="UTF-8") as file:
      script = file.read()
    with engine.begin() as conn:
      conn.connection.executescript(script)

async_engine = create_async_engine("sqlite+aiosqlite:///"+os.path.join(dir_path, "projects.db"))

sesion_factory = async_sessionmaker(bind=async_engine, autoflush=False, autocommit=False)

async def foreign_keys():
    async with session_factory() as session:
        await session.execute(text("PRAGMA foreign_keys=ON;"))
        await session.commit()

asyncio.run(foreign_keys())
