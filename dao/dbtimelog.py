from sqlalchemy import text
from dao.database import session_factory

class DBTimelog:
    @classmethod
    async def get_time_logs_by_task_id(cls, task_id):
        async with session_factory() as session:
            sql = text("SELECT * FROM time_logs WHERE task_id=:task_id")
            query = await session.execute(sql, {"task_id": task_id})
            result = query.all()
            if len(result)!=0: return result
            else: return None

    @classmethod
    async def get_time_log_by_id(cls, id):
        async with session_factory() as session:
            sql = text(
                """SELECT id, datetime_start, datetime_end, comment, duration, task_id
                FROM time_logs WHERE id=:id
            """)
            query = await session.execute(sql, {"id": id})
            result = query.first()
            if result: return result
            else: return None

    @classmethod
    async def delete_time_log_by_id(cls, id):
        try:
            async with session_factory() as session:
                sql = text("DELETE FROM time_logs WHERE id=:id")
                await session.execute(sql, {"id": id})
                await session.commit()
                return True
        except: return False

    @classmethod
    async def delete_time_logs_by_task_id(cls, task_id):
        try:
            async with session_factory() as session:
                sql = text("DELETE FROM time_logs WHERE task_id=:task_id")
                await session.execute(sql, {"task_id": task_id})
                await session.commit()
                return True
        except: return False

    @classmethod
    async def add_time_log(cls, dct):
        try:
            if dct.get("datetime_start") and dct.get("datetime_end"):
                async with session_factory() as session:
                    sql = text("""INSERT INTO time_logs (datetime_start, datetime_end, duration, task_id)
                    VALUES (:datetime_start, :datetime_end, :duration, :task_id)                    
                    """)
                    await session.execute(sql, {"datetime_start": dct.get("datetime_start"),
                    "datetime_end": dct.get("datetime_end"),
                    "duration": dct.get("duration"), "task_id": dct.get("task_id")})
                    await session.commit()
                    return True
            if dct.get("datetime_start") and not dct.get("datetime_end"):
                async with session_factory() as session:
                    sql = text("""INSERT INTO time_logs (datetime_start, task_id)
                    VALUES (:datetime_start, :task_id)""")
                    await session.execute(sql, {"datetime_start": dct.get("datetime_start"),
                    "task_id": dct.get("task_id")})
                    await session.commit()
                    return True
        except: return False

    @classmethod
    async def update_time_log_by_id(cls, id, dct):
        try:
            if dct.get("datetime_start"):
                async with session_factory() as session:
                    sql = text("UPDATE time_logs SET datetime_start=:datetime_start WHERE id=:id")
                    await session.execute(sql, {"datetime_start": dct.get("datetime_start"),
                    "id": id})
                    await session.commit()
                    return True
            if dct.get("datetime_end"):
                async with session_factory() as session:
                    sql = text("UPDATE time_logs SET datetime_end=:datetime_end WHERE id=:id")
                    await session.execute(sql, {"datetime_end": dct.get("datetime_end"),
                    "id": id})
                    await session.commit()
                    return True
            if dct.get("duration"):
                async with session_factory() as session:
                    sql = text("UPDATE time_logs SET duration=:duration WHERE id=:id")
                    await session.execute(sql, {"duration": dct.get("duration"),
                   "id": id})
                    await session.commit()
                    return True
        except: return False
