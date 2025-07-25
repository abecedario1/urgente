from dotenv import load_dotenv
import os

load_dotenv()

class DevelopmentConfig:
    DEBUG = True
    PORT = int(os.getenv('PORT', 5000))

class DatabaseConfig:
    host = os.getenv('MYSQL_HOST')
    user = os.getenv('MYSQL_USER')
    password = os.getenv('MYSQL_PASSWORD')
    database = os.getenv('MYSQL_DB')

config = {
    'development': DevelopmentConfig,
    'database': DatabaseConfig
}