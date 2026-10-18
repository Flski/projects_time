from sqlalchemy import text
from database import session_factory

class DBTask:
    @classmethod
    def get_tasks_by_project_id(cls, project_id):
        with session_factory() as session:
            sql = text("SELECT * FROM tasks WHERE project_id=:project_id")
            query = session.execute(sql, {"project_id": project_id})
            result = query.all()
            if len(result)!=0: return result
            else: return None

    @classmethod
    def get_task_by_id(cls, id):
        with session_factory() as session:
            sql = text("""
                SELECT id, name, description, status, created_at, project_id
                FROM tasks WHERE id=:id
            """)
            query = session.execute(sql, {"id": id})
            result = query.first()
            if result: return result
            else: return None

    @classmethod
    def delete_task_by_id(cls, id):
        try:
            with session_factory() as session:
                sql = text("DELETE FROM tasks WHERE id=:id")
                session.execute(sql, {"id": id})
                session.commit()
                return True
        except: return False

    @classmethod
    def add_task(cls, dct):
        with session_factory() as session:
            try:
                if not session.execute(text("SELECT name FROM tasks WHERE name=:name AND project_id=:project_id"),\
                    {"name": dct["name"], "project_id": dct["project_id"]}).first():
                    if dct.get("description"):
                        sql = text(
                            """INSERT INTO tasks(name, description, status, created_at, project_id)
                            VALUES (:name, :description, 'passive', :created_at, :project_id)
                            """)
                        session.execute(sql, {"name": dct["name"], "description": dct["description"],
                        "created_at": dct["created_at"], "project_id": dct["project_id"]})
                    else:
                        sql = text(
                            """INSERT INTO tasks(name, description, status, created_at, project_id)
                            VALUES (:name, NULL, 'passive', :created_at, :project_id)
                            """)
                        session.execute(sql, {"name": dct["name"],
                        "created_at": dct["created_at"], "project_id": dct["project_id"]})
                    session.commit()
                    return True
                else:
                    return False
            except:
                return False

    @classmethod
    def update_task_by_id(cls, id, dct):
        try:
            if dct.get("name"):
                with session_factory() as session:
                    query = session.execute(text("SELECT project_id FROM tasks WHERE id=:id"), {"id": id})
                    project_id = query.first()
                    if not session.execute(text("SELECT name FROM tasks WHERE name=:name AND project_id=:project_id"),\
                        {"name": dct.get("name"), "project_id": project_id[0]}).first():
                        sql = text("UPDATE tasks SET name=:name WHERE id=:id")
                        session.execute(sql, {"name": dct.get("name"), "id": id})
                        session.commit()
                        return True
            if dct.get("status"):
                with session_factory() as session:
                    sql = text("UPDATE tasks SET status=:status WHERE id=:id")
                    session.execute(sql, {"status": dct.get("status"), "id": id})
                    session.commit()
                    return True
            if dct.get("description"):
                with session_factory() as session:
                    sql = text("UPDATE tasks SET description=:description WHERE id=:id")
                    session.execute(sql, {"description": dct.get("description"), "id": id})
                    session.commit()
                    return True
            if dct.get("created_at"):
                with session_factory() as session:
                    sql = text("UPDATE tasks SET created_at=:created_at WHERE id=:id")
                    session.execute(sql, {"created_at": dct.get("created_at"), "id": id})
                    session.commit()
                    return True
            return False
        except:
            return False

    @classmethod
    def join_tasks_projects(cls, project_id):
        with session_factory() as session:
            sql = text("""
            SELECT tasks.id, tasks.name, tasks.description, tasks.status, tasks.created_at, tasks.project_id, projects.id, projects.name
            FROM tasks
            FULL JOIN projects ON tasks.project_id=:project_id
            """)
            query = session.execute(sql, {"project_id": project_id})
            result = query.all()
            if len(result)!=0: return result
            else: return None