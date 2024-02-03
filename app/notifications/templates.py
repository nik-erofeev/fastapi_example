def send_password_template(login, password):
    return {
        "header": "Регистарция в систему",
        "body": f"Вас добавили в систему \n" f" данные для входа:\n" f"Логин: {login}\n" f"Пароль: {password}",
    }
