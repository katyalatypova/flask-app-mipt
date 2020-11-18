from datetime import datetime
import psycopg2
import time

def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    for i in range(20):
        try:
            connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            )
            print("Connection to PostgreSQL db successful")

            return connection
        except Exception as e:
            # так как база данных в контейнере стартует не сразу,
            # попроуем подключиться макс. 20 раз, с паузой в 3 сек
            time.sleep(1)
            print(f"The error '{e}' occurred {i + 1} times")


def create_table(connection, file_path='init.sql'):
    
    sql_file = open(file_path,'r')

    cursor = connection.cursor()
    cursor.execute(sql_file.read())
    connection.commit()

def insert_line(line):
    connection = create_connection("postgres", "postgres", "postgres", "127.0.0.1", "5432")
    cursor = connection.cursor()
    
    cursor.execute("INSERT INTO data VALUES (%s, %s, %s, %s)", (line.split(";")))
    
    connection.commit()
    connection.close()
    
def read_table_htmlfriendly():

    result = [{"date": 'Введите дату', 'amount': 'Введите сумму', 'category': "Введите категорию", 'comment': 'Введите комментарий'}]
    connection = create_connection("postgres", "postgres", "postgres", "127.0.0.1", "5432")

    try:
        cursor = connection.cursor()
        cursor.execute("select * from data")
        connection.commit()
        result = cursor.fetchall()
        result = list(sorted(result, key = lambda x: datetime.strptime(x[0], "%d.%M.%Y"), reverse=True))
        result = [{"date": elem[0], 'amount': elem[1], 'category': elem[2], 'comment': elem[3]} for elem in result]
        
    except psycopg2.errors.UndefinedTable:
        connection.close()
        connection = create_connection("postgres", "postgres", "postgres", "127.0.0.1", "5432")
        create_table(connection, file_path='../data/init.sql')
        
    finally:
        connection.close()
    
    return result

def read_table_framefriendly():

    result = {"date": [], 'amount': [], 'category': [], 'comment': []}
    connection = create_connection("postgres", "postgres", "postgres", "127.0.0.1", "5432")

    try:
        cursor = connection.cursor()
        cursor.execute("select * from data")
        connection.commit()
        sql_res = cursor.fetchall()
        sql_res = list(sorted(sql_res, key = lambda x: datetime.strptime(x[0], "%d.%M.%Y"), reverse=True))

        for elem in sql_res:
            result['date'].append(elem[0])
            result['amount'].append(elem[1])
            result['category'].append(elem[2])
            result['comment'].append(elem[3])

    except psycopg2.errors.UndefinedTable:
        connection.close()
        connection = create_connection("postgres", "postgres", "postgres", "127.0.0.1", "5432")
        create_table(connection, file_path='../data/init.sql')
        
    finally:
        connection.close()
    
    return result