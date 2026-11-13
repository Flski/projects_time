from sqlalchemy import text
from dao.database import session_factory

class DBProject:
    @classmethod
    async def get_projects_by_user_id(cls, user_id):
        async with session_factory() as session:
            sql = text("SELECT * FROM projects WHERE user_id=:user_id")
            query = await session.execute(sql, {"user_id": user_id})
            res = query.all()
            if len(res)!=0: return res
            else: return None

    @classmethod
    async def get_project_by_name(cls, name, user_id):
        async with session_factory() as session:
            sql = text("SELECT id, name, description, created_at, user_id FROM projects WHERE user_id=:user_id AND name=:name")
            query = await session.execute(sql, {"user_id": user_id, "name": name})
            result = query.first()
            if result: return result
            else: return None

    @classmethod
    async def add_project(cls, dct):
        async with session_factory() as session:
            try:
                found_project = await session.execute(text("SELECT name FROM projects WHERE name=:name AND user_id=:user_id"),\
                {"name": dct["name"], "user_id": dct["user_id"]})
                if not found_project.all():
                    if dct.get("description"):
                        sql = text(
                            """INSERT INTO projects(name, description, created_at, user_id)
                            VALUES (:name, :description, :created_at, :user_id)
                            """)
                        await session.execute(sql, {"name": dct["name"], "description": dct["description"],
                        "created_at": dct["created_at"], "user_id": dct["user_id"]})
                    else:
                        sql = text(
                            """INSERT INTO projects(name, description, created_at, user_id)
                            VALUES (:name, NULL, :created_at, :user_id)
                            """)
                        await session.execute(sql, {"name": dct["name"],
                        "created_at": dct["created_at"], "user_id": dct["user_id"]})
                    await session.commit()
                    return True
                else: return False
            except: return False

    @classmethod
    async def delete_project_by_id(cls, id):
        try:
            async with session_factory() as session:
                sql = text("DELETE FROM projects WHERE id=:id")
                await session.execute(sql, {"id": id})
                await session.commit()
                return True
        except: return False

    @classmethod
    async def update_project_by_id(cls, id, dct):
        try:
            if dct.get("name"):
                async with session_factory() as session:
                    found_project = await session.execute(text("SELECT name FROM projects WHERE name=:name AND user_id=:user_id"), \
                    {"name": dct["name"], "user_id": dct["user_id"]})
                    if not found_project.all():
                        sql = text("UPDATE projects SET name=:name WHERE id=:id")
                        await session.execute(sql, {"name": dct.get("name"), "id": id})
                        await session.commit()
                    else: return False
            if dct.get("description"):
                async with session_factory() as session:
                    sql = text("UPDATE projects SET description=:description WHERE id=:id")
                    await session.execute(sql, {"description": dct.get("description"), "id": id})
                    await session.commit()
            if dct.get("created_at"):
                async with session_factory() as session:
                    sql = text("UPDATE projects SET created_at=:created_at WHERE id=:id")
                    await session.execute(sql, {"created_at": dct.get("created_at"), "id": id})
                    await session.commit()
            return True
        except: return False