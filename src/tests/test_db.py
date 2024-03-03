""" Test database related elements of the project 
@Author: Jai Wargacki"""

import psycopg2

def test_database_connection():
    try:
        conn = psycopg2.connect("dbname='dashcam' user='postgres' host='localhost' password='postgres'")
        assert True
    except Exception as e:
        print(e)
        assert False

def test_database_number_of_tables():
    conn = psycopg2.connect("dbname='dashcam' user='postgres' host='localhost' password='postgres'")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
    count = cur.fetchone()[0]
    assert count == 11
    cur.close()
    conn.close()