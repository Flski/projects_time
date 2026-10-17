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