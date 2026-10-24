from dao.dbuser import DBUser
from dao.dbproject import DBProject
from dao.dbtask import DBTask
from dao.dbtimelog import DBTimelog

print(DBUser.add_user("Login232112313212112313132131", "password_hash131231323"))
print(DBUser.get_user_by_login("Login232112313212112313132131"))

print(DBProject.add_project({"name": "Project1221123132112", "created_at": "17.10.2026", "user_id": 1}))
print(DBProject.get_projects_by_user_id(1))
print(DBProject.delete_project_by_id(1))
print(DBProject.update_project_by_id(4, {"name": "new new"}))
print(DBProject.get_project_by_id(4))

print(DBTask.add_task({"name": "new new task task", "description": "...", "created_at": "17.10.2026", "project_id": 1}))
print(DBTask.delete_task_by_id(3))
print(DBTask.update_task_by_id(4, {"new": "new new1"}))
print(DBTask.get_tasks_by_project_id(1))
print(DBTask.get_task_by_id(1))

print(DBTimelog.get_time_log_by_id(1))
print(DBTimelog.get_time_logs_by_task_id(4))
print(DBTimelog.delete_time_log_by_id(4))
print(DBTimelog.add_time_log({"datetime_start": "28.10.2026", "task_id": 2}))
print(DBTimelog.update_time_log_by_id(3, {"duration": "8 mouth"}))

print(DBProject.join_projects_tasks(2))
print(DBTask.join_tasks_projects(1))
print(DBTask.join_tasks_time_log(2))
