from sqlalchemy import text
from dao.database import session_factory

class DBUser:
    @classmethod
    async def get_user_by_login(cls, login):
        async with session_factory() as session:
            sql = text("SELECT id, login, password_hash FROM clients WHERE login=:login")
            query = await session.execute(sql, {"login": login})
            res = query.first()
            if res: return res
            else: return None


    @classmethod
    async def add_user(cls, login, password_hash):
        async with session_factory() as session:
            try:
                sql = text("INSERT INTO clients(login, password_hash) VALUES (:login, :password_hash)")
                await session.execute(sql, {"login": login, "password_hash": password_hash})
                await session.commit()
                return True
            except: return False

    @classmethod
    async def delete_user_by_id(cls, id):
        async with session_factory() as session:
            try:
                sql = text("DELETE FROM clients WHERE id=:id")
                await session.execute(sql, {"id": id})
                await session.commit()
                return True
            except: return False

    @classmethod
    async def update_user_by_id(cls, id, password_hash):
        async with session_factory() as session:
            try:
                sql = text("UPDATE clients SET password_hash=:password_hash WHERE id=:id")
                await session.execute(sql, {"password_hash": password_hash, "id": id})
                await session.commit()
                return True
            except: return False

    @classmethod
    async def update_user_by_id1(cls, id, login):
        async with session_factory() as session:
            try:
                sql = text("UPDATE clients SET login=:login WHERE id=:id")
                await session.execute(sql, {"login": login, "id": id})
                await session.commit()
                return True
            except: return False
