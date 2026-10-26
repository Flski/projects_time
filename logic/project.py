from dao.dbproject import DBProject
from dao.dbuser import DBUser
import datetime

def add_project(login, name, description, created_at):
    if len(name.strip()) >= 1:
        if description:
           if len(description) > 10000:
                return {"error": "Описание не должно превышать 10000 символов"}
        if created_at:
            try:
                if len(created_at):
                    # ДД:ММ:ГГГГ ЧЧ:ММ
                    date_list = [i for i in (created_at.replace(" ", ":")).split(":")]
                    date_nums = [int(i) for i in (created_at.replace(" ", ":")).split(":")]
                    if 0 < date_nums[0] <= 31 and 0 < date_nums[1] <= 12 and 1000 < date_nums[2] <= 7000 and \
                        0 <= date_nums[3] <= 23 and 0 <= date_nums[3] <= 60:
                        date = (date_list[2]+"-"+date_list[1]+"-"+date_list[0]+" "+
                        date_list[-2]+":"+date_list[-1]
                        )
                        if datetime.datetime.fromisoformat(date) >= datetime.datetime.now():
                            return {"error": "Дата должна удовлетворять формату: ДД:ММ:ГГГГ ЧЧ:ММ"}
                        created_at_ = datetime.datetime.fromisoformat(date)
                    else:
                        return {"error": "Дата должна удовлетворять формату : ДД:ММ:ГГГГ ЧЧ:ММ"}
            except: return {"error": "Дата должна удовлетворять формату: ДД:ММ:ГГГГ ЧЧ:ММ"}
        else: created_at_ = datetime.datetime.now()
        user_id = (DBUser.get_user_by_login(login))[0]
        if DBProject.add_project({"name": name, "description": description, "created_at": str(created_at_),
            "user_id": user_id}):
            return {"new_project": True}
        else:
            return {"error": "Название проекта используется в других проектах пользователя"}
    else:
        return {"error": "Название не может быть пустым"}

def update_project(login, id, name, description, created_at):
    user = (DBUser.get_user_by_login(login))
    project = DBProject.get_project_by_id(id)
    try:
        if user[0] != project[-1]:
            return {"error": "Проект не принадлежит пользователю"}
    except: return {"error": "Пользователь или проект не существуют"}
    if len(name.strip()) >= 1:
        if description:
           if len(description) > 10000:
                return {"error": "Описание не должно превышать 10000 символов"}
        if created_at:
            try:
                if len(created_at):
                    # ДД:ММ:ГГГГ ЧЧ:ММ
                    date_list = [i for i in (created_at.replace(" ", ":")).split(":")]
                    date_nums = [int(i) for i in (created_at.replace(" ", ":")).split(":")]
                    if 0 < date_nums[0] <= 31 and 0 < date_nums[1] <= 12 and 1000 < date_nums[2] <= 7000 and \
                        0 <= date_nums[3] <= 23 and 0 <= date_nums[3] <= 60:
                        date = (date_list[2]+"-"+date_list[1]+"-"+date_list[0]+" "+
                        date_list[-2]+":"+date_list[-1]
                        )
                        if datetime.datetime.fromisoformat(date) >= datetime.datetime.now():
                            return {"error": "Дата должна удовлетворять формату: ДД:ММ:ГГГГ ЧЧ:ММ"}
                        created_at_ = datetime.datetime.fromisoformat(date)
                    else:
                        return {"error": "Дата должна удовлетворять формату : ДД:ММ:ГГГГ ЧЧ:ММ"}
            except: return {"error": "Дата должна удовлетворять формату: ДД:ММ:ГГГГ ЧЧ:ММ"}
        else: created_at_ = datetime.datetime.now()
        if DBProject.update_project_by_id(id, {"name": name, "description": description, "created_at": str(created_at_),
            "user_id": user[0]}):
            return {"update_project": True}
        else:
            return {"error": "Название проекта используется в других проектах пользователя"}
    else:
        return {"error": "Название не может быть пустым"}

def delete_project(login, id):
    user = DBUser.get_user_by_login(login)
    project = DBProject.get_project_by_id(id)
    if project and user:
        if project[-1] == user[0]:
            if DBProject.delete_project_by_id(project[0]):
                return {"delete": True}
    return {"delete": False}

def get_projects(login):
    user = DBUser.get_user_by_login(login)
    if user:
        projects = DBProject.get_projects_by_user_id(user[0])
        return projects
    return None

def get_project(login, id):
    user = DBUser.get_user_by_login(login)
    project = DBProject.get_project_by_id(id)
    if user and project:
        if user[0] == project[-1]:
            return project
    return None