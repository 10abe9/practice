from database.database import db, db_all
from database.db_metods.db_roles import db_check_role


def db_reg(login, password):
    """проверяет есть ли юзер с таким логином, добавляет данные в бд"""
    if db(f"SELECT id from users where login = '{login}'") is not None:
        return 'this login is not free'
    else:
        db(f"""insert into users (login, password, access) values ('{login}', '{password}', 'True' ) ;
               insert into roles (login, admin, moder, writer, reader) values ('{login}','False','False','False','True')""")
        return 'Hello, new user'


def db_getlog(login):
    """возвращает логин или false"""
    """AUTHO RETURN TRUE IF LOG, PASS AND ACCESS ARE TRUE"""
    if db(f"SELECT id from users where login = '{login}'") is None:
        return False
    else:
        return login


def db_getpass(login):
    """возвращает пароль  из бд"""
    return db(f"SELECT password from users where login = '{login}'")


def db_block(login):
    """меняет доступ(access) с true на false"""
    """block user using login"""
    return db(f"update users set access = False where login = '{login}'")


def add_author(login, state_id):
    """добавляет автора статьи"""
    states = db(f"select states from users where login = '{login}'")
    if states is None:
        db(f"update users set states = '{state_id}' where login = '{login}'")
    else:
        states = str(states) + "," + str(state_id)
        db(f"update users set states = '{states}' where login = '{login}'")


def is_free(login):
    """проверяет свободен ли логин"""
    if db(f"SELECT id from users where login = '{login}'") is not None:
        return False
    else:
        return True


def db_author_of(login):
    """возвращает список статей автора"""
    if db(f"select states from users where login = '{login}'") is not None:
        return (db(f"select states from users where login = '{login}'")).split(',')
    else:
        return None


def db_get_users():
    """возвращает всех юзеров"""
    return db_all("select* from users")


def db_is_author(login, state_id):
    """проверяет является ли юзер автором статьи"""
    if db_check_role(login) == 'admin':
        return True
    if db_author_of(login) is not None:
        if str(state_id) in db_author_of(login):
            return True
    else:
        return False

