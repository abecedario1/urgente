from config import config
import mysql.connector

db_config = config['database']()

def dbConnection():
    try:
        mydb = mysql.connector.connect(
            host="212.1.211.1",
            user="u138453277_expo",
            password="Expo2025@*",
            database="u138453277_expo_tec"
        )
        return mydb, None
    except Exception as ex:
        return None, ex
