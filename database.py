import psycopg2
from psycopg2 import sql

DB_CONFIG = {
    "dbname": "student",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def get_city():
    conn = None
    city = []
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT id_gorod, href FROM gorod;")
        city = cursor.fetchall()
    except Exception as e:
        print(f"Ошибка: {str(e)}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()
    return city

def insert_city(data):
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.executemany(
            "INSERT INTO gorod (href, city) VALUES (%s, %s)",
            data
        )
        conn.commit()
        print(f"Успешно добавлено {cursor.rowcount} gorod")
    except Exception as e:
        print(f"Ошибка: {str(e)}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()


def insert_institutes(data):
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        # Подготавливаем данные для вставки
        cursor.executemany(
            "INSERT INTO institutes (id_gorod, full_name, name_small, href) VALUES (%s, %s, %s, %s)",
            data
        )
        conn.commit()
        print(f"Успешно добавлено {cursor.rowcount} institutes")
    except Exception as e:
        print(f"Ошибка: {str(e)}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()

# insert_institutes()
def get_institutes():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                id_institutes, 
                id_gorod, 
                full_name, 
                name_small, 
                href 
            FROM institutes
        """)
        institutes = cursor.fetchall()

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()
    return institutes



def insert_directions(data):
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Пакетная вставка
        cursor.executemany(
            "INSERT INTO directions (id_institutes, fac, direction, level_program, code_program, profile_program, form_study) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            data
        )
        conn.commit()
        print(f"Успешно добавлено {cursor.rowcount} directions")

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()

def get_id_direction(id_instit, params):
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """SELECT id_directions 
            FROM directions 
            WHERE 
                id_institutes = %s AND
                fac = %s AND
                direction = %s AND
                level_program = %s AND
                code_program = %s AND
                profile_program = %s AND
                form_study = %s
        """
        cursor.execute(query, tuple(params))
        id_directions = cursor.fetchall()
        conn.commit()

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()
    return id_directions


def insert_ball(data):
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Пакетная вставка
        cursor.executemany(
            "INSERT INTO ball (ball, year, id_directions) VALUES (%s, %s, %s)",
            data
        )
        conn.commit()
        print(f"Успешно добавлено {cursor.rowcount} ball")

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()

def insert_exam(data):
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.executemany(
            "INSERT INTO exam (id_directions, exam, view) VALUES (%s, %s, %s)",
            data
        )
        conn.commit()
        print(f"Успешно добавлено {cursor.rowcount} exam")

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()