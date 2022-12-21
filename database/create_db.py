from database import db


# создаем таблицы и юзера admin с паролем 123
db('''CREATE TABLE users (
     id SERIAL PRIMARY KEY,
     login VARCHAR(50) NOT NULL,
     password VARCHAR(50) NOT NULL,
     states VARCHAR(80),
     access BOOLEAN NOT NULL);''')

db('''CREATE TABLE states (
     id SERIAL PRIMARY KEY,
     author_id VARCHAR(50) NOT NULL,
     name VARCHAR(50) NOT NULL,
     text VARCHAR(500) NOT NULL,
     status VARCHAR(50) NOT NULL)''')

db('''CREATE TABLE comments (
     id SERIAL PRIMARY KEY,
     login VARCHAR(50) NOT NULL,
     text VARCHAR(70) NOT NULL,
     state_id int not null)''')

db('''CREATE TABLE roles (
     id SERIAL PRIMARY KEY,
     login VARCHAR(50) NOT NULL,
     admin boolean NOT NULL,
     moder boolean NOT NULL,
     writer boolean NOT NULL, 
     reader boolean NOT NULL)''')


db("""insert into users (login, password, access) values('admin', '123', True),
      insert into roles(login, admin, moder, writer, reader) values ('admin',True, True, True, True)""")