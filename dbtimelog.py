from sqlalchemy import text
from database import session_factory

class DBTimelog:
    @classmethod
    def get_time_logs_by_task_id(cls, task_id):
        with session_factory() as session:
            sql = text("SELECT * FROM time_logs WHERE task_id=:task_id")
            query = session.execute(sql, {"task_id": task_id})
            result = query.all()
            if len(result)!=0: return result
            else: return None

    @classmethod
    def get_time_log_by_id(cls, id):
        with session_factory() as session:
            sql = text(
                """SELECT id, datetime_start, datetime_end, comment, duration, task_id
                FROM time_logs WHERE id=:id
            """)
            query = session.execute(sql, {"id": id})
            result = query.first()
            if result: return result
            else: return None

    @classmethod
    def delete_time_log_by_id(cls, id):
        try:
            with session_factory() as session:
                sql = text("DELETE FROM time_logs WHERE id=:id")
                session.execute(sql, {"id": id})
                session.commit()
                return True
        except: return False

    @classmethod
    def add_time_log(cls, dct):
        try:
            if dct.get("datetime_start") and dct.get("datetime_end"):
                with session_factory() as session:
                    sql = text("""INSERT INTO time_logs (datetime_start, datetime_end, comment, duration, task_id)
                    VALUES (:datetime_start, :datetime_end, 'stop', :duration, :task_id)                    
                    """)
                    session.execute(sql, {"datetime_start": dct.get("datetime_start"),
                    "datetime_end": dct.get("datetime_end"),
                    "duration": dct.get("duration"), "task_id": dct.get("task_id")})
                    session.commit()
                    return True
            if dct.get("datetime_start") and not dct.get("datetime_end"):
                with session_factory() as session:
                    sql = text("""INSERT INTO time_logs (datetime_start, comment, task_id)
                    VALUES (:datetime_start, 'start', :task_id)""")
                    session.execute(sql, {"datetime_start": dct.get("datetime_start"),
                    "task_id": dct.get("task_id")})
                    session.commit()
                    return True
        except: return False

    @classmethod
    def update_time_log_by_id(cls, id, dct):
        try:
            if dct.get("datetime_start"):
                with session_factory() as session:
                    sql = text("UPDATE time_logs SET datetime_start=:datetime_start WHERE id=:id")
                    session.execute(sql, {"datetime_start": dct.get("datetime_start"),
                    "id": id})
                    session.commit()
                    return True
            if dct.get("datetime_end"):
                with session_factory() as session:
                    sql = text("UPDATE time_logs SET datetime_end=:datetime_end WHERE id=:id")
                    session.execute(sql, {"datetime_end": dct.get("datetime_end"),
                    "id": id})
                    session.commit()
                    return True
            if dct.get("duration"):
                with session_factory() as session:
                    sql = text("UPDATE time_logs SET duration=:duration WHERE id=:id")
                    session.execute(sql, {"duration": dct.get("duration"),
                   "id": id})
                    session.commit()
                    return True
            if dct.get("comment"):
                with session_factory() as session:
                    sql = text("UPDATE time_logs SET comment=:comment WHERE id=:id")
                    session.execute(sql, {"comment": dct.get("comment"),
                   "id": id})
                    session.commit()
                    return True
        except: return False