from dbuser import DBUser
from dbproject import DBProject
from dbtask import DBTask

# print(DBUser.add_user("Login232112313212112313132131", "password_hash131231323"))
# print(DBUser.get_user_by_login("Login232112313212112313132131"))

# print(DBProject.add_project({"name": "Project1221112", "created_at": "17.10.2026", "user_id": 1}))
# print(DBProject.get_projects_by_user_id(1))
# print(DBProject.delete_project_by_id(1))
# print(DBProject.update_project_by_id(4, {"name": "new new"}))
# print(DBProject.get_project_by_id(4))

print(DBTask.add_task({"name": "new new", "description": "...", "created_at": "17.10.2026", "project_id": 1}))
# print(DBTask.delete_task_by_id(3))
print(DBTask.update_task_by_id(4, {"new": "new new1"}))
print(DBTask.get_tasks_by_project_id(1))
# print(DBTask.get_task_by_id(1))