import psycopg2

def connect_to_db():
    connection = psycopg2.connect(
        host="localhost",
        database="kvmp",
        user="kvmp",
        password="password"
    )
    return connection

CONNECTION = connect_to_db()

def get_users():
    cursor = CONNECTION.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()