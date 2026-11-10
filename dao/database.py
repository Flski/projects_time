from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os

if "projects.db" not in os.listdir("."):
    from sqlalchemy import create_engine
    engine = create_engine(
      "sqlite:///"+os.path.join(os.path.abspath(os.path.dirname(__file__)), "projects.db"),
      connect_args={"check_same_thread": False}
    )
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "init.sql"), "r", encoding="UTF-8") as file:
      script = file.read()
    with engine.begin() as conn:
      conn.connection.executescript(script)
