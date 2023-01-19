import pytest
import os
os.environ['DATABASE_URL'] = 'postgresql://kvmp:password@127.0.0.1:5432/kvmp?sslmode=disable'
import kvmp.db as db
from kvmp.db import cur, con
import psycopg2
db.con = psycopg2.connect('postgresql://kvmp:password@127.0.0.1:5432/kvmp_test?sslmode=disable')
db.cur = db.con.cursor()

def test_user_login():
    db.cur.execute("DELETE FROM users")
    db.add_user('admin', 'admin@example.com', 'password')
    db.cur.execute("select * from users")
    db.cur.fetchall()
    assert db.user_login('admin', 'password') != [], 'It should not be empty'
    assert db.user_login('admin', 'e34fddsfafd') == [], 'It should not find a user'

def test_get_user():
    db.cur.execute("DELETE FROM users")
    db.add_user('admin', 'admin@example.com', 'password')
    user = db.get_user_by_email('admin@example.com')
    db.get_user(user[0])
    

# def test_get_by_id_table():
#     assert db.get_by_id_table(1, 'servers')[0]['id'] == 1

# def test_find_server_by_host():
#     db.insert_server("hostname.com", "root", "/path/to/keyfile")
# #     db.find_server_by_host("hostname.com")

def test_crud_server():
    db.cur.execute("DELETE FROM servers")
    db.add_server("hostname.com", "root", "/path/to/keyfile")
    server = db.get_server_by_host("hostname.com")[0]
    db.update_server(server[0], "host1.cloud", "root", "/path/to/keyfile")
    server = db.get_server_by_host("host1.cloud")[0]
    assert server[1] == "host1.cloud"
    db.delete_server(server[0])

def test_get_servers():
    db.cur.execute("DELETE FROM servers")
    db.add_server("hostname.com", "root", "/path/to/keyfile")
    ss = db.get_servers()
    assert type(ss) == list, 'It should be a list'
    assert type(ss[0]) == dict, 'It should be a list of dictionaries'
    assert ss[0]['host'] == "hostname.com"