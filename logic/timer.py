from dao.dbtask import DBTask
from dao.dbproject import DBProject
from dao.dbuser import DBUser
from dao.dbtimelog import DBTimelog
import datetime

async def start(login, project_name, task_name):
    user = await DBUser.get_user_by_login(login)
    if not user: return {"error": "Пользователя не существует"}
    project = await DBProject.get_project_by_name(project_name.strip(), user[0])
    if not project:
        return {"error": "Проекта не существует"}
    else:
        task = await DBTask.get_task_by_name(task_name, project[0])
        if task:
            dct = {}
            dct1 = {}
            if task[3] in ("passive", "pause"):
                dct["task_id"] = task[0]
                dct["datetime_start"] = str(datetime.datetime.now())[:16]
                if await DBTimelog.add_time_log(dct):
                    dct1["status"] = "start"
                    if await DBTask.update_task_by_id(task[0], dct1):
                        return True
            else: return {"error": "Задача уже была запущена или завершена"}
        else: return {"error": "Задачи не существует"}

async def pause(login, project_name, task_name):
    user = await DBUser.get_user_by_login(login)
    if not user: return {"error": "Пользователя не существует"}
    project = await DBProject.get_project_by_name(project_name.strip(), user[0])
    if not project:
        return {"error": "Проекта не существует"}
    else:
        task = await DBTask.get_task_by_name(task_name, project[0])
        if task:
            dct = {}
            dct1 = {}
            if task[3] == "start":
                dct["datetime_end"] = str(datetime.datetime.now())[:16]
                timelogs = await DBTimelog.get_time_logs_by_task_id(task[0])
                if timelogs:
                    last_timelog = timelogs[-1]
                    dct["duration"] = str(datetime.datetime.fromisoformat(dct.get("datetime_end")) - datetime.datetime.fromisoformat(last_timelog[1]))
                    if await DBTimelog.update_time_log_by_id(last_timelog[0], dct):
                        dct1["status"] = "pause"
                        if await DBTask.update_task_by_id(task[0], dct1):
                            return True
            return {"error": "Задача не запущена"}
        else: return {"error": "Задачи не существует"}

async def stop(login, project_name, task_name):
    user = await DBUser.get_user_by_login(login)
    if not user: return {"error": "Пользователя не существует"}
    project = await DBProject.get_project_by_name(project_name.strip(), user[0])
    if not project:
        return {"error": "Проекта не существует"}
    else:
        task = await DBTask.get_task_by_name(task_name, project[0])
        if task:
            dct = {}
            dct1 = {}
            if task[3] != "stop":
                timelogs = await DBTimelog.get_time_logs_by_task_id(task[0])
                if timelogs:
                    last_timelog = timelogs[-1]
                    if last_timelog[2]:
                        dct["datetime_end"] = str(datetime.datetime.now())[:16]
                        dct["duration"] = str(datetime.datetime.fromisoformat(dct.get("datetime_end")) - datetime.datetime.fromisoformat(last_timelog[1]))
                        await DBTimelog.update_time_log_by_id(last_timelog[0], dct)
                    dct1["status"] = "stop"
                    if await DBTask.update_task_by_id(task[0], dct1):
                        return True
            return {"error": "Задача уже остановлена"}
        else: return {"error": "Задачи не существует"}
