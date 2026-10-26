from logic.login import login, registration
from logic.project import add_project, delete_project, update_project, get_projects, get_project
from logic.user import update_password, delete_user

# print(registration("user", "password1", "password1"))
# print(login("user", "password1"))

# print(add_project("user", "Project12", None, None))
# print(update_project("user", 5, "New new new new name", "New description","10:10:2026 18:00"))
# print(delete_project("user", 6))
print(get_projects("user"))
# print(get_project("user", 5))

# print(update_password("user", "new_password2", "new_password3"))
# print(delete_user("user", "password1"))