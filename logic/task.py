from dao.dbtask import DBTask
from dao.dbproject import DBProject
from dao.dbtimelog import DBTimelog
from dao.dbuser import DBUser
import datetime

def get_tasks(login, project_id):
  user = DBUser.get_user_by_login(login)
  if user:
    project = DBProject.get_project_by_id(project_id)
    if project:
      if user[0] == project[-1]:
        tasks = DBNote.get_tasks_by_project_id(project_id)
        return tasks
      else: return {"error": "Проект не принадлежит пользователю"}
    else: return {"error": "Проекта не существует"}
  else: return {"error": "Пользователя не существует"}

def get_task(login, project_id, task_id):
  user = DBUser.get_user_by_login(login)
  if user:
    project = DBProject.get_project_by_id(project_id)
    if project:
      if user[0] == project[-1]:
        task = DBNote.get_task_by_id(task_id)
        if task:
          if task[-1] == project[0]:
            return task
          else:
            return {"error": "Задача не принадлежит проекту"}
        else: return {"error": "Задачи не существует"}
      else: return {"error": "Проект не принадлежит пользователю"}
    else: return {"error": "Проекта не существует"}
  else: return {"error": "Пользователя не существует"}

def delete_task(login, project_id, task_id):
  user = DBUser.get_user_by_login(login)
  if user:
    project = DBProject.get_project_by_id(project_id)
    if project:
      if user[0] == project[-1]:
        task = DBNote.get_task_by_id(task_id)
        if task:
          if task[-1] == project[0]:
            if DBTask.delete_task_by_id(task_id):
              return True
            else: return {"error": "Ошибка удаления"}
          else:
            return {"error": "Задача не принадлежит проекту"}
        else: return {"error": "Задачи не существует"}
      else: return {"error": "Проект не принадлежит пользователю"}
    else: return {"error": "Проекта не существует"}
  else: return {"error": "Пользователя не существует"}

def add_task(login, project_id, name, description, created_at, datetime_start, datetime_end):
  user = DBUser.get_user_by_login(login)
  if user:
    project = DBProject.get_project_by_id(project_id)
    if project:
      if user[0] == project[-1]:
        if name:
          #Основные параметры (название, описание, дата создания):
          dct = {}
          dct["project_id"] = project[0]
          if len(name.strip) >= 1 and len(name.strip()) <= 100:
            dct["name"] = name.strip()
          else: return {"error": "Название задачи должно включать хотя 1 символ и не более 100"}
          if description:
            if len(description) >= 1 and len(description) <= 10000:
              dct["description"] = description
            else: return {"error": "Описание задачи должно включать хотя бы 1 символ и не более 10000 символов"}
          if created_at:
            try:
                if len(created_at) == 16:
                    # ДД:ММ:ГГГГ ЧЧ:ММ
                    date_list = [i for i in (created_at.replace(" ", ":")).split(":")]
                    date_nums = [int(i) for i in (created_at.replace(" ", ":")).split(":")]
                    if 0 < date_nums[0] <= 31 and 0 < date_nums[1] <= 12 and int(str(datetime.datetime.now())[:4]) == date_nums[2] and \
                        0 <= date_nums[3] <= 23 and 0 <= date_nums[3] <= 60:
                        date = (date_list[2]+"-"+date_list[1]+"-"+date_list[0]+" "+
                        date_list[-2]+":"+date_list[-1]
                        )
                        if datetime.datetime.fromisoformat(date) >= datetime.datetime.now():
                            return {"error": "Дата должна удовлетворять формату: ДД:ММ:ГГГГ ЧЧ:ММ"}
                        dct["created_at"] = str(datetime.datetime.fromisoformat(date))
                    else:
                        return {"error": "Дата должна удовлетворять формату : ДД:ММ:ГГГГ ЧЧ:ММ"}
            except: return {"error": "Дата должна удовлетворять формату: ДД:ММ:ГГГГ ЧЧ:ММ"}
          else: dct["created_at"] = str(datetime.datetime.now())[:16]
          #Дополнительные параметры (даты и время старта, завершения)
          if datetime_start:
            try:
                if len(datetime_start) == 16:
                    # ДД:ММ:ГГГГ ЧЧ:ММ
                    date1_list = [i for i in (datetime_start.replace(" ", ":")).split(":")]
                    date1_nums = [int(i) for i in (datetime_start.replace(" ", ":")).split(":")]
                    if 0 < date_nums1[0] <= 31 and 0 < date_nums1[1] <= 12 and int(str(datetime.datetime.now())[:4]) == date_nums[2] and \
                        0 <= date_nums1[3] <= 23 and 0 <= date_nums1[3] <= 60:
                        date1 = (date_list1[2]+"-"+date_list1[1]+"-"+date_list1[0]+" "+
                        date1_list[-2]+":"+date_list[-1]
                        )
                        if datetime.datetime.fromisoformat(date1) >= datetime.datetime.now():
                            return {"error": "Дата должна удовлетворять формату: ДД:ММ:ГГГГ ЧЧ:ММ"}
                        dct["datetime_start"] = str(datetime.datetime.fromisoformat(date1))
                    else:
                        return {"error": "Дата должна удовлетворять формату : ДД:ММ:ГГГГ ЧЧ:ММ"}
                    if datetime_stop:
                      if len(datetime_stop) == 16:
                        # ДД:ММ:ГГГГ ЧЧ:ММ
                        date_list2 = [i for i in (datetime_stop.replace(" ", ":")).split(":")]
                        date_nums2 = [int(i) for i in (datetime_stop.replace(" ", ":")).split(":")]
                        if 0 < date_nums2[0] <= 31 and 0 < date_nums2[1] <= 12 and int(str(datetime.datetime.now())[:4]) == date_nums[2] and \
                          0 <= date_nums2[3] <= 23 and 0 <= date_nums2[3] <= 60:
                          date2 = (date_list2[2]+"-"+date_list2[1]+"-"+date_list2[0]+" "+
                          date2_lis2t[-2]+":"+date_list2[-1]
                          )
                          if datetime.datetime.fromisoformat(date2) <= datetime.datetime.fromisoformat(date1):
                            return {"error": "Дата завершения должна быть больше или равной дате старта"}
                          dct["datetime_stop"] = str(datetime.datetime.fromisoformat(date2))
                        else:
                          return {"error": "Дата должна удовлетворять формату : ДД:ММ:ГГГГ ЧЧ:ММ"}
            except: return {"error": "Даты должны удовлетворять формату: ДД:ММ:ГГГГ ЧЧ:ММ"}
          else: datetime_start = str(datetime.datetime.now())[:16]
          if DBTask.add_task(dct):
            return True
          else: return {"error": "Ошибка создания задачи"}
        else: return {"error": "Название не должно быть пустым"}
      else: return {"error": "Проект не принадлежит пользователю"}
    else: return {"error": "Проекта не существует"}
  else: return {"error": "Пользователя не существует"}
