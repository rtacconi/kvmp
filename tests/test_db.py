import pytest
import kvmp.db as db
from records import Database
from kvmp.config import CONFIG

db.DB = Database(CONFIG['TEST_DATABASE_URL'])

def test_user_login():
    assert db.user_login('admin', 'password') == [{'id': 1}], 'It should return user ID 1'
    assert db.user_login('admin', 'e34fddsfafd') == [], 'It should not find a user'

# def test_get_by_id_table():
#     assert db.get_by_id_table(1, 'servers')[0]['id'] == 1

def test_find_server_by_host():
    db.insert_server("hostname.com", "root", "/path/to/keyfile")
#     db.find_server_by_host("hostname.com")