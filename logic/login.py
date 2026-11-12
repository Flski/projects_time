from dao.dbuser import DBUser
from werkzeug.security import generate_password_hash, check_password_hash

async def registration(login_, password, password1):
    if 4 <= len(login_.strip()) <= 100  and 16 <= len(password.strip()) <= 10000 and password.strip() == password1.strip():
        s = [i for i in password.strip() if i in "йёцукенгшщзхъфывапролджэячсмитьбюabcdefghijklmnopqrstuvwxyzABCD"
        "EFGHIJKLMNOPQRSTUVWXYZЙЁЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ"]
        d = [i for i in password.strip() if i in "0123456789"]
        if len(s) >= 1 and len(d) >= 1:
            if not await DBUser.get_user_by_login(login_.strip()):
                password_hash = generate_password_hash(password.strip())
                if await DBUser.add_user(login_.strip(), password_hash):
                    return True
            else:
                return {"error": "Логин занят"}
        else:
            return {"error": "Пароль должен содержать хотя бы одну букву и цифру одновременно"}
    else:
        return {"error": "Длина логина должна быть не менее 4 символов, длина пароля должна быть не менее 16 символов, пароли должны совпадать"}

async def login(login_, password):
    if 16 <= len(password.strip()) <= 10000 and  4 <= len(login_.strip()) <= 100:
        s = [i for i in password.strip() if i in "йёцукенгшщзхъфывапролджэячсмитьбюabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZЙЁЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ"]
        d = [i for i in password.strip() if i in "0123456789"]
        if len(s) >= 1 and len(d) >= 1:
            user = await DBUser.get_user_by_login(login_.strip())
            if user:
                if check_password_hash(user.password_hash, password.strip()):
                    return True
                else:
                    return {"error": "Неверный логин или пароль"}
            else:
                return {"error": "Неверный логин или пароль"}
        else:
            return {"error": "Пароль должен содержать хотя бы одну букву и цифру одновременно"}
    else:
        return {"error": "Длина логина должна быть не менее 4 символов, длина пароля должна быть не менее 16 символов"}
