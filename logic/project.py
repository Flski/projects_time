from dao.dbproject import DBProject
from dao.dbuser import DBUser

async def get_projects(login):
    user = await DBUser.get_user_by_login(login)
    if not user: return {"error": "Пользователя не существует"}
    projects = await DBProject.get_projects_by_user_id(user[0])
    if not projects: return None
    else:
        join_projects_tasks = await DBProject.join_projects_tasks(user[0])
        return join_projects_tasks

async def get_project(login, name):
    user = await DBUser.get_user_by_login(login)
    if not user: return {"error": "Пользователя не существует"}
    project = await DBProject.get_project_by_name(name.strip(), user[0])
    if not project: return {"error": "Проекта не существует"}
    else:
        return project