import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from database.db_metods.users_db import db_getlog, db_getpass, db_author_of, db_reg, db_get_users, db_block, db_is_author
from database.db_metods.states_db import db_get_states, db_write_state, db_edit_text, db_edit_status, db_get_status
from database.db_metods.db_roles import db_check_role, db_add_role
from database.db_metods.comments_db import read_comments, db_write_comment


app = FastAPI()#создаем объект класса для запуска


def hash_password(password: str):
    """функция для 'хеширования' - пока она ничего не меняет, но при желании сюда что-то можно добавить """
    return password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") #обозначаем url для получения токена


class User(BaseModel):
    """создаем класс юзер"""
    username: str
    access: bool = True


class UserInDB(User):
    """и класс юзер в бд"""
    password: str


def get_user(username: str):
    """получаем юзера по логину"""
    if db_getlog(username):
        return UserInDB(username=username, password=hash_password(db_getpass(username)))


def fake_decode_token(token):
    """при желании можно кодировать и декодировать токен"""
    user = get_user(token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """получаем текущего юзера по токену"""
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """получаем не заблокированного юзера"""
    if not current_user.access:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post('/registation', tags=['registration'])
def registration(login, password):
    """принимаем логин и пароль, проверяем есть ли логин в бд"""
    if not db_getlog(login):
        db_reg(login, password)
        return f'Hello, {login}, you was registered. Authorize now, please '
    else:
        return f'User with login ({login}) exist. Choose another login.'


@app.post("/token", tags=['Token'])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """получение токена(фейк)"""
    username = db_getlog(form_data.username)
    if not username:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(username=username, password=db_getpass(form_data.username))
    hashed_password = hash_password(form_data.password)
    if not hashed_password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if user.access is not True:
        raise HTTPException(status_code=400, detail="This user was banned")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me", tags=['user'])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """информация о текущем пользователе"""
    return current_user


@app.get("/states/read", tags=['states'])
async def read_states(current_user: User = Depends(get_current_active_user)):
    """читаем статьи в зависимости от роли"""
    if not db_get_states(current_user.username):
        """возвращает статьи в зависимости от роли"""
        return 'There is not avaiable states for you'
    else:
        return db_get_states(current_user.username)


@app.post("/states/write", tags=['states'])
async def write_states(name: str, text: str, status='draft', current_user: User = Depends(get_current_active_user)):
    """пишем статью, добавляем автора, присваиваем роль писатель"""
    if status:
        status = 'sent'
        db_write_state(login=current_user.username, name=name, text=text, status=status)
    else:
        db_write_state(login=current_user.username, name=name, text=text, status=status)
    return 'your state was sent ', name, text, status


@app.put("/states/edit", tags=['states'])
async def edit_state(state_id, new_text=None, new_status=None, current_user: User = Depends(get_current_active_user)):
    """меняем статью если у пользователя есть права"""
    login = current_user.username
    status = db_get_status(state_id)
    if db_is_author(login, state_id):
        if status == 'publicated' and new_text is not None:
            return 'you can not change this state. Try to change status'
        if new_status:
            db_edit_status(state_id, new_status)
        if new_text:
            db_edit_text(state_id, new_text)
        return 'your state was changed'
    else:
        return "you can not change this state"


@app.get('/users', tags=['admin'])
def get_users(current_user: User = Depends(get_current_active_user)):
    """список пользователей для админа"""
    if db_check_role(current_user.username) == 'admin':
        return db_get_users()


@app.put('/users/edit', tags=['admin'])
def edit_user(login, role=None, block=None, current_user: User = Depends(get_current_active_user)):
    """меняем юзера(если block, то блокируем"""
    if db_check_role(current_user.username) == 'admin':
        if role:
            db_add_role(login, role)
        if block:
            db_block(login)
    return 'Edited'


@app.get('/states/read/{state_id}/comment', tags=['comments'])
def read_comment(state_id, current_user: User = Depends(get_current_active_user)):
    """читаем комменты к статье"""
    return read_comments(current_user.username, state_id)


@app.post('/states/read/{state_id}/comment/write', tags=['comments'])
def write_comment(state_id, text, current_user: User = Depends(get_current_active_user)):
    """пишем коммент к статье"""
    db_write_comment(current_user.username, text, state_id)
    return f'your comment: {text}'


if __name__ == '__main__':#запускаем приложение
    uvicorn.run(app)