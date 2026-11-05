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
          dct = {}
          if len(name.strip) >= 1 and len(name.strip()) <= 100:
            dct["name"] = name.strip()
          else: return {"error": "Название задачи должно включать хотя 1 символ и не более 100"}
          if description:
            if len(description) >= 1 and len(description) <= 10000:
              dct["description"] = description
            else: return {"error": "Описание задачи должно включать хотя бы 1 символ и не более 10000 символов"}
              
        else: return {"error": "Название не должно быть пустым"}
      else: return {"error": "Проект не принадлежит пользователю"}
    else: return {"error": "Проекта не существует"}
  else: return {"error": "Пользователя не существует"}
