import sqlite3
from sqlite3 import Error
import time


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB is successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")


def fetch_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        data = cursor.fetchall()
        return data
    except Error as e:
        print(f"The error '{e}' occurred")


def insert_price(price):
    query = f"""
    INSERT INTO eth_token
        (time, price)
        VALUES
        ({int(time.time())}, {price})
    """
    return query
