from logic.login import registration, login
from logic.user import delete_user, update_password, update_login
from logic.project import get_projects, get_project, delete_project, add_project, update_project
import asyncio

# print(asyncio.run(registration("new user", "password123456789", "password123456789")))
# print(asyncio.run(delete_user("new user", "password123456789")))
# print(asyncio.run(update_password("new user", "password1234567890", "password1234567890")))
# print(asyncio.run(update_login("new user", "password1234567890", "new user 1")))
# print(asyncio.run(login("new user 1", "password1234567890")))
# print(asyncio.run(get_projects("new user 1")))
# print(asyncio.run(delete_project("new user 1", "project1")))
# print(asyncio.run(add_project("new user", "New project123", "2026-10-12 04:38")))
print(asyncio.run(update_project("new user", "New name project12345", None, None, "Description")))