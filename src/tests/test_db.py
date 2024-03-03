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