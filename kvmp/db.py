import psycopg2
import os
from typing import List, Tuple

con = psycopg2.connect(os.environ['DATABASE_URL'])
cur = con.cursor()

def as_dict(ss, c):
    return [{c[i]:v for i, v in enumerate(list(s))} for s in ss]

# USERS ---------------------

def user_login(username, password) -> int:
    cur.execute("SELECT id FROM users WHERE username=%s AND password=md5(%s)", (username, password,))
    return cur.fetchall()

def get_user(id):
    cur.execute("SELECT id FROM users WHERE id=%s", (id,))
    return cur.fetchone()

def get_user_by_email(email):
    cur.execute("SELECT id FROM users WHERE email=%s", (email,))
    return list(cur.fetchone())

def add_user(username: str, email: str, password: str) -> None:
    cur.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, md5(%s))", 
            (username, email, password)
    )
    con.commit()

# END USERS ------------------

def get_by_id_table(id, table):
    cur.execute(
        f"SELECT * FROM {table} WHERE id=:id", id=id
    )
    return cur.fetchall()

# SERVERS ---------------------------------
def add_server(host, username, key_file):
    cur.execute(
        "INSERT INTO servers (host, username, key_file) VALUES (%s, %s, %s)", 
            (host, username, key_file)
    )
    con.commit()

def get_servers():
    columns = ['id', 'host', 'username', 'key_file', 'created_at']
    cur.execute(f"SELECT {', '.join(columns)} FROM servers ORDER BY id")
    return as_dict(cur.fetchall(), columns)

def get_server(id):
    cur.execute("SELECT id, host, username, key_file FROM servers WHERE id = %s", (id,))
    return cur.fetchone()

def get_server_by_host(host: str) -> List[Tuple]:
    cur.execute("SELECT id, host, username, key_file FROM servers WHERE host = %s", (host,))
    return cur.fetchall()

def update_server(id: int, host: str, username: str, key_file: str):
    cur.execute(
            "UPDATE servers SET host = %s, username = %s, key_file = %s WHERE id = %s", 
            (host, username, key_file, id))
    con.commit()
    return "Server updated successfully"

def delete_server(id: int):
    cur.execute("DELETE FROM servers WHERE id = %s", (id,))
    con.commit()
    return "Server delete successfully"       

# END SERVERS -----------------------------
