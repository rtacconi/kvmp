from records import Database
from kvmp.config import CONFIG

DB = Database(CONFIG['DATABASE_URL'])

def user_login(username, password) -> int:
    rows = DB.query(f"SELECT id FROM users WHERE username='{username}' AND password=md5('{password}')")
    return rows.as_dict()

def get_md5(password):
    rows = DB.query(f"select md5('{password}')")

def get_user(id):
    rows = DB.query(f"SELECT id FROM users WHERE id='{id}'")
    return rows.as_dict()


def insert_server(host, username, key_file):
    DB.query('''
        INSERT INTO servers 
        (host, username, key_file) 
        VALUES (:host, :username, :key_file
    )''',
    host=host, username=username, key_file=key_file)

# def find_server_by_host(host):
#     rows = DB.query(f"SELECT * FROM server WHERE host=:host", host)
#     return rows.as_dict()

def get_by_id_table(id, table):
    rows = DB.query(
        f"SELECT * FROM {table} WHERE id=:id", id=id
    )
    return rows.as_dict()