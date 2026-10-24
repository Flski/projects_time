from dao.dbproject import DBProject
from dao.dbuser import DBUser
import datetime

def add_project(login, name, description=None, created_at=None):
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