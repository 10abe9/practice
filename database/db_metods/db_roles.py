from database.database import db


def db_add_role(login: str, role: str):
    """добавить роль по логину"""
    db(f"update roles set {role} = True where login = '{login}'")


def db_check_role(login: str):
    """возвращает роль по логину"""
    if db(f"select admin from roles where login ='{login}'"):
        return 'admin'
    if db(f"select moder from roles where login ='{login}'"):
        return 'moder'
    if db(f"select writer from roles where login ='{login}'"):
        return 'writer'
    else:
        return 'reader'
