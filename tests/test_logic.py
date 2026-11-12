from logic.login import registration, login
from logic.user import delete_user, update_password, update_login
import asyncio

# print(asyncio.run(registration("new user", "password123456789", "password123456789")))
# print(asyncio.run(delete_user("new user", "password123456789")))
# print(asyncio.run(update_password("new user", "password1234567890", "password1234567890")))
# print(asyncio.run(update_login("new user", "password1234567890", "new user 1")))
print(asyncio.run(login("new user 1", "password1234567890")))