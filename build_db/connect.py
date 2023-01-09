import mariadb
import sys

try:
    conn = mariadb.connect(
        user="admin",
        password="NBAiscool456",
        host="192.0.2.1",
        port=3306,
        database="nba_test"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()
print("SUCCESS")
sys.exit(0)
