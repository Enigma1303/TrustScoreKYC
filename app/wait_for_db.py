import time
import os
import MySQLdb

DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "complaint_db")
DB_USER = os.environ.get("DB_USER", "complaint_user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "complaint_pass")
DB_PORT = int(os.environ.get("DB_PORT", 3306))

while True:
    try:
        MySQLdb.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            db=DB_NAME,
            port=DB_PORT,
        )
        break
    except MySQLdb.OperationalError:
        print("Database not ready, waiting...")
        time.sleep(1)

print("Database is ready!")
