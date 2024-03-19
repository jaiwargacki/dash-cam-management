""" Test database related elements of the project 
@Author: Jai Wargacki"""

import database

def test_database_connection():
    try:
        db = database.Database()
        assert True
    except Exception as e:
        print(e)
        assert False

def test_database_number_of_tables():
    db = database.Database()
    result = db.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
    count = result[0][0]
    assert count == 11