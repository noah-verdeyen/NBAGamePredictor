import mariadb
import sys

try:
    conn = mariadb.connect(
        user="admin",
        password="NBAiscool456",
        host="127.0.0.1",
        port=3306,
        database="nba_test"
    )
    print(conn)
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

teams = ['ATL', 'BOS', 'BRK', 'CHA', 'CHI',
         'CLE', 'DAL', 'DEN', 'DET', 'GSW',
         'HOU', 'IND', 'LAC', 'LAL', 'MEM',
         'MIA', 'MIL', 'MIN', 'NOP', 'NYK',
         'OKC', 'ORL', 'PHI', 'PHO', 'POR',
         'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

for team in teams:
    sql = """CREATE TABLE {} (SELECT * FROM player_stats.team = '{}') """.format(team, team)
    print(sql)
    cur.execute(sql)
    sql = """ALTER IGNORE TABLE {} ADD UNIQUE INDEX u(player_id)""".format(team)
    print(sql)
    cur.execute(sql)
