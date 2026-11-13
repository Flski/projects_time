from logic.login import registration, login
from logic.user import delete_user, update_password, update_login
from logic.project import get_projects, get_project, delete_project, add_project, update_project
from logic.task import get_tasks, get_task, add_task, update_task
from logic.timer import start, pause, stop
import asyncio

print(asyncio.run(registration("new user", "password123456789", "password123456789")))
print(asyncio.run(add_project("new user", "New project123", "2026-10-12 04:38")))
print(asyncio.run(add_task("new user", "New project123", "Task82887", "2026-10-01 12:41", "...", )))
print(asyncio.run(stop("new user", "New project123", "Task82887")))