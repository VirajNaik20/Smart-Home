import os

import postgres as postgres
import psycopg2

DB_USER = os.environ["postgres"]
DB_PASSWORD = os.environ["viraj"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["5432"]
DB_NAME = os.environ["postgres"]

dbConnection = None

def getDbConnection():

    global dbConnection
    
    if dbConnection is None:
        dbConnection = psycopg2.connect(user=postgres,password=viraj,host=localhost,port=5432,database=postgres)

    return dbConnection