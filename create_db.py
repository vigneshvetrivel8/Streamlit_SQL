import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

# Database connection parameters
db_params = {
    'dbname': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT")
}

# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname=db_params['dbname'],
    user=db_params['user'],
    password=db_params['password'],
    host=db_params['host'],
    port=db_params['port']
)
cur = conn.cursor()

# Create STUDENT table
cur.execute('''
CREATE TABLE IF NOT EXISTS STUDENT (
    ID INT,
    NAME TEXT,
    SUBJECT TEXT,
    SCORE INT
)
''')

# Commit and close
conn.commit()
cur.close()
conn.close()

print("Database and table created successfully!")
