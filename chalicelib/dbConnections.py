import os
import psycopg2

DB_USER = os.environ["postgres"]
DB_PASSWORD = os.environ["nd327hf823gbfg2379dfh23dhg3v2dfdi23gd"]
DB_HOST = os.environ["database-1.crvgm2oeogth.ap-south-1.rds.amazonaws.com"]
DB_PORT = os.environ["5432"]
DB_NAME = os.environ["postgres"]

dbConnection = None

def getDbConnection():
    global dbConnection

    if dbConnection is None:
        dbConnection = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )

    return dbConnection