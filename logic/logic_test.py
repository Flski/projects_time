from logic.login import login, registration
from logic.project import add_project

print(registration("user2", "password1", "password1"))
print(login("user2", "password1"))

print(add_project("user2", "Project111231231223213", None, "24:10:2026 21:30"))