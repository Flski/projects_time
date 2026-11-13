from dao.dbtask import DBTask
from dao.dbproject import DBProject
from dao.dbuser import DBUser
from dao.dbtimelog import DBTimelog
import datetime

async def get_tasks(login, project_name):
    user = await DBUser.get_user_by_login(login)
    if not user: return {"error": "Пользователя не существует"}
    project = await DBProject.get_project_by_name(project_name.strip(), user[0])
    if not project: return {"error": "Проекта не существует"}
    else:
        tasks = await DBTask.get_tasks_by_project_id(project[0])
        return tasks

async def get_task(login, project_name, task_name):
    user = await DBUser.get_user_by_login(login)
    if not user: return {"error": "Пользователя не существует"}
    project = await DBProject.get_project_by_name(project_name.strip(), user[0])
    if not project: return {"error": "Проекта не существует"}
    else:
        task = await DBTask.get_task_by_name(project_name, task_name)
        return task

async def delete_task(login, project_name, task_name):
    user = await DBUser.get_user_by_login(login)
    if not user: return {"error": "Пользователя не существует"}
    project = await DBProject.get_project_by_name(project_name.strip(), user[0])
    if not project:
        return {"error": "Проекта не существует"}
    else:
        task = await DBTask.get_task_by_name(project_name, task_name)
        if task:
            if await DBTask.delete_task_by_id(task[0]):
                return True
        else: return {"error": "Задачи не существует"}

async def add_task(login, project_name, name, created_at=None, description=None, datetime_start=None, datetime_end=None):
    user = await DBUser.get_user_by_login(login)
    if not user: return {"error": "Пользователя не существует"}
    project = await DBProject.get_project_by_name(project_name.strip(), user[0])
    if not project:
        return {"error": "Проекта не существует"}
    else:
        if 1 <= len(name.strip()) <= 100:
            dct = {}
            dct["name"] = name.strip()
            dct["project_id"] = project[0]

            if created_at:
                try:
                    datetime_now = str(datetime.datetime.now())[:16]
                    # 2026-11-13 12:26
                    if int(created_at.strip()[:4]) <= int(datetime_now.strip()[:4]) \
                            and 1 <= int(created_at.strip()[5:7]) <= 12 and 1 <= int(created_at.strip()[8:10]) <= 31 and \
                            0 <= int(created_at.strip()[11:13]) <= 23 and 0 <= int(created_at.strip()[14:]) <= 60:
                        if datetime.datetime.fromisoformat(created_at.strip()) <= datetime.datetime.now():
                            dct["created_at"] = created_at.strip()
                        else:
                            return {"error": "Дата и время должны соответсвовать формату ГГГГ-ММ-ДД ЧЧ:ММ"}
                    else:
                        return {"error": "Дата и время должны соответсвовать формату ГГГГ-ММ-ДД ЧЧ:ММ"}
                except:
                    return {"error": "Дата и время должны соответсвовать формату ГГГГ-ММ-ДД ЧЧ:ММ"}
            else:
                dct["created_at"] = str(datetime.datetime.now())[:16]

            if description:
                if len(description) <= 10000:
                    dct["description"] = description
                else:
                    return {"error": "Описание не должно превышать 10000 символов"}

            if await DBTask.add_task(dct):
                if not datetime_start and not datetime_end: return True
                else:
                    dct1 = {}
                    dct2 = {}
                    task = await DBTask.get_task_by_name(name.strip(), project[0])
                    dct1["task_id"] = task[0]
                    if datetime_end and not datetime_start: return {"error": "Дата и время завершения не может быть введена без"
                    "даты и времени начала"}

                    if datetime_start and not datetime_end: dct2["status"] = "start"
                    if datetime_start and datetime_end: dct2["status"] = "stop"

                    await DBTask.update_task_by_id(task[0], dct2)

                    if datetime_start:
                        try:
                            datetime_now = str(datetime.datetime.now())[:16]
                            # 2026-11-13 12:26
                            if int(datetime_start.strip()[:4]) <= int(datetime_now.strip()[:4]) \
                            and 1 <= int(datetime_start.strip()[5:7]) <= 12 and 1 <= int(datetime_start.strip()[8:10]) <= 31 and \
                            0 <= int(datetime_start.strip()[11:13]) <= 23 and 0 <= int(datetime_start.strip()[14:]) <= 60:
                                if datetime.datetime.fromisoformat(datetime_start.strip()) <= datetime.datetime.now():
                                    dct1["datetime_start"] = datetime_start.strip()
                                else:
                                    return {"error": "Дата и время должны соответсвовать формату ГГГГ-ММ-ДД ЧЧ:ММ"}
                            else:
                                return {"error": "Дата и время должны соответсвовать формату ГГГГ-ММ-ДД ЧЧ:ММ"}
                        except:
                            return {"error": "Дата и время должны соответсвовать формату ГГГГ-ММ-ДД ЧЧ:ММ"}

                    if datetime_end:
                        try:
                            datetime_now = str(datetime.datetime.now())[:16]
                            # 2026-11-13 12:26
                            if int(datetime_start.strip()[:4]) <= int(datetime_now.strip()[:4]) \
                            and 1 <= int(datetime_end.strip()[5:7]) <= 12 and 1 <= int(datetime_end.strip()[8:10]) <= 31 and \
                            0 <= int(datetime_end.strip()[11:13]) <= 23 and 0 <= int(datetime_end.strip()[14:]) <= 60:
                                if datetime.datetime.fromisoformat(datetime_start.strip()) <= datetime.datetime.fromisoformat(datetime_end.strip()) <= \
                                datetime.datetime.now():
                                    dct1["datetime_end"] = datetime_end.strip()
                                    dct1["duration"] = str(datetime.datetime.fromisoformat(datetime_end.strip()) - \
                                    datetime.datetime.fromisoformat(datetime_start.strip()))
                                else:
                                    return {"error": "Дата и время должны соответсвовать формату ГГГГ-ММ-ДД ЧЧ:ММ"}
                            else:
                                return {"error": "Дата и время должны соответсвовать формату ГГГГ-ММ-ДД ЧЧ:ММ"}
                        except:
                            return {"error": "Дата и время должны соответсвовать формату ГГГГ-ММ-ДД ЧЧ:ММ"}

                    if await DBTimelog.add_time_log(dct1):
                        return True

            else: return {"error": "Задача с таким названием уже есть для проекта"}
