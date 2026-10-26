from dao.dbuser import DBUser
from werkzeug.security import check_password_hash, generate_password_hash
from string import ascii_lowercase

def update_password(login, password, new_password):
    user = DBUser.get_user_by_login(login.strip())
    if user:
        if len(new_password.strip()) >= 16 and len(new_password.strip()) <= 10000\
        and len(password.strip()) >= 16 and len(password.strip()) <= 10000:
            s1 = [i for i in password.strip() if i in ascii_lowercase+"йёцукенгшщзхъфывапролджэячсмитьбю"]
            d1 = [i for i in password.strip() if i in "0123456789"]
            s2 = [i for i in new_password.strip() if i in ascii_lowercase + "йёцукенгшщзхъфывапролджэячсмитьбю"]
            d2 = [i for i in new_password.strip() if i in "0123456789"]
            if len(s1) >= 1 and len(d1) >= 1 and len(s2) >= 1 and len(d2) >= 1:
                if password.strip() != new_password.strip():
                    if check_password_hash(user[-1], password.strip()) and not check_password_hash(user[-1], new_password.strip()):
                        hash = generate_password_hash(new_password.strip())
                        if DBUser.update_user_by_id(user[0], hash):
                            return {"update_password": True}
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

def delete_user(login, password):
    user = DBUser.get_user_by_login(login.strip())
    if user:
        if len(password.strip()) >= 16 and len(password.strip()) <= 10000:
            if check_password_hash(user[-1], password.strip()):
                if DBUser.delete_user_by_id(user[0]):
                    return {"delete_user": True}
            else:
                return {"error": "Неверный пароль"}
        else: 
            {"error": "Длина пароля должна быть не менее 16 символов"}
    else:
        return {"error": "Пользователя не существует"}
