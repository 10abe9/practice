import uvicorn
from fastapi import FastAPI

app = FastAPI()
bd = []


@app.get('/')
def root():
    return {'hell': 'o'}


@app.post('/new_user/{login}&{password}')
def new_user(login, password):
    if login != '123123' and len(login) > 5:
        '''ВЕРНУТЬ НУЖНУЮ СТРАНИЦУ '''
        return {login: password}
        bd.append({login: password})#ВЫПОЛНЯЕМ ЗАГРУЗКУ ЛОГИНА И ПАРОЛЯ В БД.
    elif len(login) < 5:
        return 'login is short'
    else:
        return 'login is not free'


uvicorn.run(app)
