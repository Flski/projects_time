from dao.dbproject import DBProject
from dao.dbuser import DBUser
from dao.dbtask import DBTask
import datetime

async def get_projects(login):
    user = await DBUser.get_user_by_login(login)
    if not user: return {"error": "Пользователя не существует"}
    projects = await DBProject.get_projects_by_user_id(user[0])
    if not projects: return None
    else:
        res = []
        for i in projects:
            tasks = await DBTask.get_tasks_by_project_id(i[0])
            if len([i for i in tasks if i[3] in ('start', 'pause')]) > 0:
               res.append([i, "Активный"])
            if len([i for i in tasks if i[3] in ('passive', 'stop')]) == len(tasks):
                res.append([i, "Пассивный"])
        return res

async def get_project(login, project_name):
    user = await DBUser.get_user_by_login(login)
    if not user: return {"error": "Пользователя не существует"}
    project = await DBProject.get_project_by_name(project_name.strip(), user[0])
    if not project: return {"error": "Проекта не существует"}
    else:
        return project

async def delete_project(login, project_name):
    user = await DBUser.get_user_by_login(login)
    if not user: return {"error": "Пользователя не существует"}
    project = await DBProject.get_project_by_name(project_name.strip(), user[0])
    if not project: return {"error": "Проекта не существует"}
    else:
        if await DBProject.delete_project_by_id(project[0]):
            return True

async def add_project(login, name, created_at=None, description=None):
    user = await DBUser.get_user_by_login(login)
    if not user: return {"error": "Пользователя не существует"}
    dct = {}
    if 1 <= len(name.strip()) <= 100:
        dct["user_id"] = user[0]
        dct["name"] = name.strip()
        if created_at:
            try:
                datetime_now = str(datetime.datetime.now())[:16]
                #2026-11-13 12:26
                if int(created_at.strip()[:4]) <= int(datetime_now.strip()[:4]) \
                and 1 <= int(created_at.strip()[5:7]) <= 12 and 1 <= int(created_at.strip()[8:10]) <= 31 and\
                0 <= int(created_at.strip()[11:13]) <= 23 and 0<= int(created_at.strip()[14:]) <= 60:
                    if datetime.datetime.fromisoformat(created_at.strip()) <= datetime.datetime.now():
                        dct["created_at"] = created_at.strip()
                    else: return {"error": "Дата и время должны соответсвовать формату ГГГГ-ММ-ДД ЧЧ:ММ"}
                else: return {"error": "Дата и время должны соответсвовать формату ГГГГ-ММ-ДД ЧЧ:ММ"}
            except: return {"error": "Дата и время должны соответсвовать формату ГГГГ-ММ-ДД ЧЧ:ММ"}
        else: dct["created_at"] = str(datetime.datetime.now())[:16]
        if description:
            if len(description) <= 10000:
                dct["description"] = description
            else: return {"error": "Описание не должно превышать 10000 символов"}
        if await DBProject.add_project(dct):
            return True
        else: return False
    else: return {"error": "Название должно быть от 1 до 100 символов"}

async def update_project(login, first_name, name=None, created_at=None, description=None):
    user = await DBUser.get_user_by_login(login)
    if not user: return {"error": "Пользователя не существует"}
    project = await DBProject.get_project_by_name(first_name.strip(), user[0])
    if not project: return {"error": "Проекта не существует"}
    dct = {}
    dct["user_id"] = user[0]
    if name:
        if 1 <= len(name.strip()) <= 100:
            dct["name"] = name.strip()
        else: return {"error": ""}
    if created_at:
        try:
            datetime_now = str(datetime.datetime.now())[:16]
            #2026-11-13 12:26
            if int(created_at.strip()[:4]) <= int(datetime_now.strip()[:4]) \
            and 1 <= int(created_at.strip()[5:7]) <= 12 and 1 <= int(created_at.strip()[8:10]) <= 31 and\
            0 <= int(created_at.strip()[11:13]) <= 23 and 0<= int(created_at.strip()[14:]) <= 60:
                if datetime.datetime.fromisoformat(created_at.strip()) <= datetime.datetime.now():
                    dct["created_at"] = created_at.strip()
                else: return {"error": "Дата и время должны соответсвовать формату ГГГГ-ММ-ДД ЧЧ:ММ"}
            else: return {"error": "Дата и время должны соответсвовать формату ГГГГ-ММ-ДД ЧЧ:ММ"}
        except: return {"error": "Дата и время должны соответсвовать формату ГГГГ-ММ-ДД ЧЧ:ММ"}
    if description:
        if len(description) <= 10000:
            dct["description"] = description
        else: return {"error": "Описание не должно превышать 10000 символов"}
    if await DBProject.update_project_by_id(project[0], dct):
        return True
    else: return False