from dao.dbuser import DBUser
from werkzeug.security import check_password_hash, generate_password_hash

async def update_password(login, password, new_password):
    user = await DBUser.get_user_by_login(login.strip())
    if user:
        if 16 <= len(new_password.strip()) <= 10000 and 16 <= len(password.strip()) <= 10000:
            s1 = [i for i in password.strip() if i in "йёцукенгшщзхъфывапролджэячсмитьбюabcdefghijklmnopqrstuvwxyzA"
            "BCDEFGHIJKLMNOPQRSTUVWXYZЙЁЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ"]
            d1 = [i for i in password.strip() if i in "0123456789"]
            s2 = [i for i in new_password.strip() if i in "йёцукенгшщзхъфывапролджэячсмитьбюabcdefghijklmnopqrstuvwxy"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZЙЁЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ"]
            d2 = [i for i in new_password.strip() if i in "0123456789"]
            if len(s1) >= 1 and len(d1) >= 1 and len(s2) >= 1 and len(d2) >= 1:
                if password.strip() != new_password.strip():
                    if check_password_hash(user[-1], password.strip()) and not check_password_hash(user[-1], new_password.strip()):
                        hash = generate_password_hash(new_password.strip())
                        if await DBUser.update_user_by_id(user[0], hash):
                            return True
                        else:
                            return {"error": "Ошибка изменения пароля"}
                    else:
                        return {"error": "Неверный текущий пароль"}
                else:
                    return {"error": "Пароли совадают"}
            else:
                return {"error": "Пароль должен содержать хотя бы одну букву и цифру одновременно"}
        else:
            return {"error": "Длина пароля должна быть не менее 16 символов, пароли не должны совпадать"}
    else:
        return {"error": "Пользователя не существует"}

async def update_login(login, password, new_login):
    user = await DBUser.get_user_by_login(login)
    if user:
        if 16 <= len(password.strip()) <= 10000 and 4 <= len(new_login.strip()) <= 100:
            if check_password_hash(user[2], password.strip()):
                if not await DBUser.get_user_by_login(new_login.strip()):
                    if await DBUser.update_user_by_id1(user[0], new_login):
                        return True
                    else: return {"error": "Ошибка изменения логина"}
                else: return {"error": "Логин занят"}
            else: return {"error": "Неверный пароль"}
        else: {"error": "Длина пароля должна быть не менее 16 символов"}

async def delete_user(login, password):
    user = await DBUser.get_user_by_login(login.strip())
    if user:
        if 16 <= len(password.strip()) <= 10000:
            if check_password_hash(user[-1], password.strip()):
                if await DBUser.delete_user_by_id(user[0]):
                    return True
                else:
                    return {"error": "Ошибка удаления учётной записи"}
            else:
                return {"error": "Неверный пароль"}
        else: 
            {"error": "Длина пароля должна быть не менее 16 символов"}
    else:
        return {"error": "Пользователя не существует"}
