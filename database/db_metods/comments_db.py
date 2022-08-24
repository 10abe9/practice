from database.database import db, db_all


def db_write_comment(login, text, state_id):
    """пишем комментарий в бд"""
    db(f"insert into comments (login, text, state_id) values ('{login}', '{text}', {state_id}) ")


def read_comments(login, state_id):
    """возвращаем комментарии к статье"""
    return db_all(f"select * from comments where state_id = {state_id} ")


def delete_comment(id):
    """удаляем комментарий"""
    db(f"delete from comments where id = {id}")
