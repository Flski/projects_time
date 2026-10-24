from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

engine = create_engine(
    "sqlite:///"+os.path.join(os.path.abspath(os.path.dirname(__file__)), "projects.db"),
    connect_args={"check_same_thread": False}
)
session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "init.sql"), "r", encoding="UTF-8") as file:
    script = file.read()

if "projects.db" not in os.listdir("."):
    with engine.begin() as conn:
        conn.connection.executescript(script)
