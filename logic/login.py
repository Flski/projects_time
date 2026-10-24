from dao.dbuser import DBUser
from string import ascii_lowercase
from werkzeug.security import generate_password_hash, check_password_hash

def registration(login, password, password1):
    if len(login.strip()) >= 4 and len(login) <= 100 and len(password.strip()) >= 8 and len(password) <= 10000 \
        and password == password1:
        s = [i for i in password if i in ascii_lowercase+"йёцукенгшщзхъфывапролджэячсмитьбю"]
        d = [i for i in password if i in "0123456789"]
        if len(s) >= 1 and len(d) >= 1:
            if not DBUser.get_user_by_login(login.strip()):
                password_hash = generate_password_hash(password)
                if DBUser.add_user(login, password_hash):
                    return {"registartion": True}
            else:
                return {"error": "Логин занят"}
        else:
            return {"error": "Пароль должен содержать хотя бы одну букву и цифру одновременно"}
    else: return {"error": "Длина логина должна быть не менее 4 символов, длина пароля должна быть не менее"
    "8 символов, пароли должны совпадать"}

def login(login, password):
    if len(login.strip()) >= 4 and len(password.strip()) >= 8:
        user = DBUser.get_user_by_login(login)
        if user:
            if check_password_hash(user.password_hash, password):
                return {"login": True}
            else:
                return {"error": "Неверный логин или пароль"}
        else:
            return {"error": "Неверный логин или пароль"}
    else:
        return {"error": "Длина логина должна быть не менее 4 символов, длина пароля должна быть не менее 8 символов"}