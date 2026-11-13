from sqlalchemy import text
from dao.database import session_factory

class DBTask:
    @classmethod
    async def get_tasks_by_project_id(cls, project_id):
        async with session_factory() as session:
            sql = text("SELECT * FROM tasks WHERE project_id=:project_id")
            query = await session.execute(sql, {"project_id": project_id})
            result = query.all()
            if len(result)!=0: return result
            else: return None

    @classmethod
    async def get_task_by_id(cls, id):
        async with session_factory() as session:
            sql = text("""
                SELECT id, name, description, status, created_at, project_id
                FROM tasks WHERE id=:id
            """)
            query = await session.execute(sql, {"id": id})
            result = query.first()
            if result: return result
            else: return None

    @classmethod
    async def delete_task_by_id(cls, id):
        try:
            async with session_factory() as session:
                sql = text("DELETE FROM tasks WHERE id=:id")
                await session.execute(sql, {"id": id})
                await session.commit()
                return True
        except: return False

    @classmethod
    async def add_task(cls, dct):
        async with session_factory() as session:
            try:
                if not await session.execute(text("SELECT name FROM tasks WHERE name=:name AND project_id=:project_id"),\
                    {"name": dct["name"], "project_id": dct["project_id"]}).first():
                    if dct.get("description"):
                        sql = text(
                            """INSERT INTO tasks(name, description, status, created_at, project_id)
                            VALUES (:name, :description, 'passive', :created_at, :project_id)
                            """)
                        await session.execute(sql, {"name": dct["name"], "description": dct["description"],
                        "created_at": dct["created_at"], "project_id": dct["project_id"]})
                    else:
                        sql = text(
                            """INSERT INTO tasks(name, description, status, created_at, project_id)
                            VALUES (:name, NULL, 'passive', :created_at, :project_id)
                            """)
                        await session.execute(sql, {"name": dct["name"],
                        "created_at": dct["created_at"], "project_id": dct["project_id"]})
                    await session.commit()
                    return True
                else:
                    return False
            except:
                return False

    @classmethod
    async def update_task_by_id(cls, id, dct):
        try:
            if dct.get("name"):
                async with session_factory() as session:
                    query = await session.execute(text("SELECT project_id FROM tasks WHERE id=:id"), {"id": id})
                    project_id = query.first()
                    if not await session.execute(text("SELECT name FROM tasks WHERE name=:name AND project_id=:project_id"),\
                        {"name": dct.get("name"), "project_id": project_id[0]}).first():
                        sql = text("UPDATE tasks SET name=:name WHERE id=:id")
                        await session.execute(sql, {"name": dct.get("name"), "id": id})
                        await session.commit()
                        return True
            if dct.get("status"):
                async with session_factory() as session:
                    sql = text("UPDATE tasks SET status=:status WHERE id=:id")
                    await session.execute(sql, {"status": dct.get("status"), "id": id})
                    await session.commit()
                    return True
            if dct.get("description"):
                async with session_factory() as session:
                    sql = text("UPDATE tasks SET description=:description WHERE id=:id")
                    await session.execute(sql, {"description": dct.get("description"), "id": id})
                    await session.commit()
                    return True
            if dct.get("created_at"):
                async with session_factory() as session:
                    sql = text("UPDATE tasks SET created_at=:created_at WHERE id=:id")
                    await session.execute(sql, {"created_at": dct.get("created_at"), "id": id})
                    await session.commit()
                    return True
            return False
        except:
            return False

    @classmethod
    def join_tasks_time_log(cls, project_id):
        with session_factory() as session:
            sql = text("""
               SELECT tasks.id, tasks.name, tasks.description, tasks.status, tasks.created_at, tasks.project_id, 
               time_logs.id, time_logs.datetime_start, time_logs.datetime_end, time_logs.comment, 
               time_logs.duration, time_logs.task_id 
               FROM tasks
               LEFT JOIN time_logs ON tasks.id=time_logs.task_id
               WHERE tasks.project_id=:project_id;
               """)
            query = session.execute(sql, {"project_id": project_id})
            result = query.all()
            if len(result) != 0:
                return result
            else:
                return None
