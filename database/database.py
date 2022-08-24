import psycopg2
from psycopg2 import Error


def db(sql_command):
    '''подключается к бд, принимает на вход строку- команду sql, возвращает результат (первый элемент) или false'''
    try:
        connection = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="123",
            host="127.0.0.1")
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(sql_command)
            try:
                fetch = cursor.fetchall()[0][0]
                return fetch
            except:
                fetch = None

    except(Exception, Error) as error:
        print('!!!DATABASE HAS NO CONNECTION!!!', error)
    finally:
        if connection:
            connection.close()
            print('connection with db was closed')


def db_all(sql_command):
    '''то же самое, что дб, только возвращает чистый результат (несколько значений если есть)'''
    try:
        connection = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="123",
            host="127.0.0.1")
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(sql_command)
            try:
                fetch = cursor.fetchall()
                return fetch
            except:
                fetch = None

    except(Exception, Error) as error:
        print('!!!DATABASE HAS NO CONNECTION!!!', error)
    finally:
        if connection:
            connection.close()
            print('connection with db was closed')

