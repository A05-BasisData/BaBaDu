from django.db import DatabaseError, IntegrityError, transaction
from collections import namedtuple
import psycopg2
from psycopg2 import Error

try:

    connection = psycopg2.connect(user="postgres",
                        password="KelompokA05Basdut",
                        host="db.hyowwnuxbttgwulfqabf.supabase.co",
                        port="5432",)

    # Create a cursor to perform database operations
    cursor = connection.cursor()
        
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)


# def namedtuplefetchall(cursor):
#     "Return all rows from a cursor as a namedtuple"
#     desc = cursor.description
#     if desc:
#         nt_result = namedtuple('Result', [col[0] for col in desc])
#         return [nt_result(*row) for row in cursor.fetchall()]


# def query(str):
#     '''Execute SQL query and return its result as a list'''
#     cursor = connection.cursor()
#     result = []
#     try:
#         cursor.execute(str)
#         result = namedtuplefetchall(cursor)
#     except Exception as e:
#         print(e)
#         result = e
#     finally:
#         cursor.close()
#         return result

def map_cursor(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def query(query_str: str):
    hasil = []
    # tmp = connection.cursor()
    with connection.cursor() as cursor:
        try:
            cursor.execute("SET SEARCH_PATH TO BABADU")
        except Exception as e:
            hasil = e
            connection.rollback()
            # cursor = tmp


        try:
            cursor.execute(query_str)

            if query_str.strip().lower().startswith("select"):
                # Kalau ga error, return hasil SELECT
                hasil = map_cursor(cursor)
            else:
                # Kalau ga error, return jumlah row yang termodifikasi oleh INSERT, UPDATE, DELETE
                hasil = cursor.rowcount
                # Buat commit di database
                connection.commit()
        except Exception as e:
            # Ga tau error apa
            hasil = e
            connection.rollback()

    return hasil
