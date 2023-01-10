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
sql = """USE nba_test"""
cur.execute(sql)
sql = """CREATE TABLE player_stats (
         player_name varchar(30), player_id varchar(10),
         season int, season_type varchar(5), team varchar(3),
         poss int, mp int, raptor_box_offense float,
         raptor_box_defense float, raptor_box_total float,
         raptor_onoff_offense float, raptor_onoff_defense float,
         raptor_onoff_total float, raptor_offense float,
         raptor_defense float, raptor_total float, war_total float,
         war_reg_season float, war_playoffs float,
         predator_offense float, predator_defense float,
         predator_total float, pace_impact float)"""
cur.execute(sql)
# entire NBA player stats
sql = """LOAD DATA LOCAL INFILE '/home/noah/NBAGamePredictor/player_stats.csv' INTO TABLE player_stats
         FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'"""
cur.execute(sql)
sql = """ALTER IGNORE TABLE player_stats ADD UNIQUE INDEX u(player_id)"""
cur.execute(sql)
# make tables for each team
teams = ['ATL', 'BOS', 'BRK', 'CHA', 'CHI',
         'CLE', 'DAL', 'DEN', 'DET', 'GSW',
         'HOU', 'IND', 'LAC', 'LAL', 'MEM',
         'MIA', 'MIL', 'MIN', 'NOP', 'NYK',
         'OKC', 'ORL', 'PHI', 'PHO', 'POR',
         'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

for team in teams:
    sql = """DROP TABLE {}""".format(team.lower())
    cur.execute(sql)
    sql = """CREATE TABLE IF NOT EXISTS {} (SELECT * FROM player_stats WHERE team = '{}') """.format(team.lower(), team)
    print(sql)
    cur.execute(sql)
    sql = """ALTER IGNORE TABLE {} ADD UNIQUE INDEX u(player_id)""".format(team.lower())
    print(sql)
    cur.execute(sql)
