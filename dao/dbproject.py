from sqlalchemy import text
from dao.database import session_factory

class DBProject:
    @classmethod
    def get_projects_by_user_id(cls, user_id):
        with session_factory() as session:
            sql = text("SELECT * FROM projects WHERE user_id=:user_id")
            query = session.execute(sql, {"user_id": user_id})
            res = query.all()
            if len(res)!=0: return res
            else: return None

    @classmethod
    def get_project_by_id(cls, id):
        with session_factory() as session:
            sql = text("SELECT id, name, description, status, created_at FROM projects WHERE id=:id")
            query = session.execute(sql, {"id": id})
            result = query.first()
            if result: return result
            else: return None

    @classmethod
    def add_project(cls, dct):
        with session_factory() as session:
            try:
                if not session.execute(text("SELECT name FROM projects WHERE name=:name AND user_id=:user_id"),\
                {"name": dct["name"], "user_id": dct["user_id"]}).first():
                    if dct.get("description"):
                        sql = text(
                            """INSERT INTO projects(name, description, status, created_at, user_id)
                            VALUES (:name, :description, 'active', :created_at, :user_id)
                            """)
                        session.execute(sql, {"name": dct["name"], "description": dct["description"],
                        "created_at": dct["created_at"], "user_id": dct["user_id"]})
                    else:
                        sql = text(
                            """INSERT INTO projects(name, description, status, created_at, user_id)
                            VALUES (:name, NULL, 'active', :created_at, :user_id)
                            """)
                        session.execute(sql, {"name": dct["name"],
                        "created_at": dct["created_at"], "user_id": dct["user_id"]})
                    session.commit()
                    return True
                else: return False
            except: return False

    @classmethod
    def delete_project_by_id(cls, id):
        try:
            with session_factory() as session:
                sql = text("DELETE FROM projects WHERE id=:id")
                session.execute(sql, {"id": id})
                session.commit()
                return True
        except: return False

    @classmethod
    def update_project_by_id(cls, id, dct):
        try:
            if dct.get("name"):
                with session_factory() as session:
                    query = session.execute(text("SELECT user_id FROM projects WHERE id=:id"), {"id": id})
                    user_id = query.first()
                    if not session.execute(text("SELECT name FROM projects WHERE name=:name AND user_id=:user_id"), \
                        {"name": dct.get("name"), "user_id": user_id[0]}).first():
                        sql = text("UPDATE projects SET name=:name WHERE id=:id")
                        session.execute(sql, {"name": dct.get("name"), "id": id})
                        session.commit()
                        return True
            if dct.get("status"):
                with session_factory() as session:
                    sql = text("UPDATE projects SET status=:status WHERE id=:id")
                    session.execute(sql, {"status": dct.get("status"), "id": id})
                    session.commit()
                    return True
            if dct.get("description"):
                with session_factory() as session:
                    sql = text("UPDATE projects SET description=:description WHERE id=:id")
                    session.execute(sql, {"description": dct.get("description"), "id": id})
                    session.commit()
                    return True
            if dct.get("created_at"):
                with session_factory() as session:
                    sql = text("UPDATE projects SET created_at=:created_at WHERE id=:id")
                    session.execute(sql, {"created_at": dct.get("created_at"), "id": id})
                    session.commit()
                    return True
            return False
        except: return False

    @classmethod
    def join_projects_tasks(cls, user_id):
        with session_factory() as session:
            sql = text("""
                SELECT projects.id, projects.name, projects.description, projects.status, projects.created_at,
                projects.user_id, tasks.id, tasks.status
                FROM projects
                LEFT JOIN tasks ON projects.id=tasks.project_id
                WHERE projects.user_id=:user_id;          
             """)
            query = session.execute(sql, {"user_id": user_id})
            result = query.all()
            if len(result)!=0: return result
            else: return None
