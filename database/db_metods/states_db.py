from database.database import db, db_all
from database.db_metods.users_db import add_author, db_author_of
from database.db_metods.db_roles import db_check_role


def db_write_state(login, name: str, text: str, status: str='draft'):
    """пишем статью, добавляем роль "писатель", добавляем автора статьи"""
    author_id = db(f"select id from users where login = '{login}'")
    db(f"insert into states(author_id, name, text, status) values({author_id},'{name}', '{text}', '{status}')")
    add_author(login, db("select max (id) from states "))


def db_edit_text(state_id, text):
    """меняет текст статьи"""
    db(f"update states set text = '{text}' where id = {state_id}  ")


def db_get_status(state_id):
    """получает статус статьи"""
    return db(f"select status from states where id = {state_id}")


def db_edit_status(state_id, status):
    """меняет статус статьи"""
    db(f"update states set status = '{status}'  where id = {state_id} ")


def db_get_states(login):
    """возвращает статьи в завис от роли"""
    if db_check_role(login) == 'admin' or db_check_role(login) == 'moder':
        return db_all("select * from states")
    if db_author_of(login) is not None:
        id = db(f"select id from users where login = '{login}'")
        return db_all(f"select * from states where status = 'accepted'"), db(f"select states where author_id = {id}")
    else:
        return db_all(f"select * from states where status = 'publicated'")


def db_add_author(state_id, login):
    """добавляет автора статьи"""
    author_id = db(f"select id from users where login = '{login}'")
    auth = db(f"select author_id from states where id = {state_id}")
    auth = str(auth) + ',' + str(author_id)
    db(f"update states set author_id = '{auth}' where id = {state_id}")


