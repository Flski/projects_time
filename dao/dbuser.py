from sqlalchemy import text
from dao.database import session_factory

class DBUser:
    @classmethod
    def get_user_by_login(cls, login):
        with session_factory() as session:
            sql = text("SELECT id, login, password_hash FROM clients WHERE login=:login")
            query = session.execute(sql, {"login": login})
            res = query.first()
            if res: return res
            else: return None


    @classmethod
    def add_user(cls, login, password_hash):
        with session_factory() as session:
            try:
                sql = text("INSERT INTO clients(login, password_hash) VALUES (:login, :password_hash)")
                session.execute(sql, {"login": login, "password_hash": password_hash})
                session.commit()
                return True
            except: return False

    @classmethod
    def delete_user_by_id(cls, id):
        with session_factory() as session:
            try:
                sql = text("DELETE FROM clients WHERE id=:id")
                session.execute(sql, {"id": id})
                session.commit()
                return True
            except: return False

    @classmethod
    def update_user_by_id(cls, id, password_hash):
        with session_factory() as session:
            try:
                sql = text("UPDATE clients SET password_hash=:password_hash WHERE id=:id")
                session.execute(sql, {"password_hash": password_hash, "id": id})
                session.commit()
                return True
            except: return False

