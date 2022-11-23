import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_nba_stats(team, is_home_team, table_id):
    # implement a way to select different tables
    bb_ref_url = "https://www.basketball-reference.com/teams/{}/2023.html".format(team.upper())
    req = requests.get(bb_ref_url)
    soup = BeautifulSoup(req.text, 'html.parser')

    table = soup.findAll("table")
    list_of_frames = pd.read_html(str(table[table_id]))
    res = pd.concat(list_of_frames)

    if is_home_team:
        with open("head_to_head/home.csv", "+w") as f:
            f.write(str(res.to_csv("head_to_head/home.csv")))
    else:
        with open("head_to_head/away.csv", "+w") as f:
            f.write(str(res.to_csv("head_to_head/away.csv")))


def compare_scoring():
    data = []
    with open("head_to_head/away.csv", 'r', encoding="utf8") as f:
        for line in f:
            data.append(line.strip().split(','))

    line = data[len(data) - 1]
    total_away_points = line[len(line) - 1]

    data = []
    with open("head_to_head/home.csv", 'r', encoding="utf8") as f:
        for line in f:
            data.append(line.strip().split(','))

    line = data[len(data) - 1]
    total_home_points = line[len(line) - 1]

    return total_home_points, total_away_points


def compare_rebounding():
    data = []
    with open("head_to_head/away.csv", 'r', encoding="utf8") as f:
        for line in f:
            data.append(line.strip().split(','))

    line = data[len(data) - 1]
    total_away_rebounds = line[22]

    data = []
    with open("head_to_head/home.csv", 'r', encoding="utf8") as f:
        for line in f:
            data.append(line.strip().split(','))

    line = data[len(data) - 1]
    total_home_rebounds = line[22]

    return total_home_rebounds, total_away_rebounds


def compare_assists():
    data = []
    with open("head_to_head/away.csv", 'r', encoding="utf8") as f:
        for line in f:
            data.append(line.strip().split(','))

    line = data[len(data) - 1]
    total_away_assists = line[23]

    data = []
    with open("head_to_head/home.csv", 'r', encoding="utf8") as f:
        for line in f:
            data.append(line.strip().split(','))

    line = data[len(data) - 1]
    total_home_assists = line[23]

    return total_home_assists, total_away_assists


def get_games_played():
    data = []
    with open("head_to_head/away.csv", 'r', encoding="utf8") as f:
        for line in f:
            data.append(line.strip().split(','))

    line = data[len(data) - 1]
    total_away_games = float(line[4])

    data = []
    with open("head_to_head/home.csv", 'r', encoding="utf8") as f:
        for line in f:
            data.append(line.strip().split(','))

    line = data[len(data) - 1]
    total_home_games = float(line[4])

    return total_home_games, total_away_games


def convert_to_per_game(data):
    gp_home = int(data[0][0])
    gp_away = int(data[0][1])

    res = []

    for pair in data:
        home_data = float(pair[0]) / gp_away
        away_data = float(pair[1]) / gp_home
        res.append((home_data, away_data))

    return res


def collect_player_data():
    data = []
    with open("head_to_head/away.csv", 'r', encoding="utf8") as f:
        for line in f:
            data.append(line.strip().split(','))
            if line != data[len(data) - 1]:
                continue

    return


def average_true_shooting():
    data = []
    with open("head_to_head/away.csv", 'r', encoding="utf8") as f:
        for line in f:
            data.append(line.strip().split(','))
    ts = []
    for line in data:
        if line == data[0]:
            continue

        if int(line[1]) <= 5:
            ts.append(float(line[7]))
        elif 12 > int(line[1]) > 5:
            ts.append(float(line[7]) * 0.67)

    away_ts_percent = sum(ts) / len(ts)

    data = []
    with open("head_to_head/home.csv", 'r', encoding="utf8") as f:
        for line in f:
            data.append(line.strip().split(','))
    ts = []
    for line in data:
        if line == data[0]:
            continue

        if int(line[1]) <= 5:
            ts.append(float(line[7]))
        elif 12 > int(line[1]) > 5:
            ts.append(float(line[7]) * 0.67)

    home_ts_percent = sum(ts) / len(ts)

    return home_ts_percent, away_ts_percent


def average_vorp():
    data = []
    with open("head_to_head/away.csv", 'r', encoding="utf8") as f:
        for line in f:
            data.append(line.strip().split(','))
    ts = []
    for line in data:
        if line == data[0]:
            continue

        ts.append(float(line[len(line) - 1]))

    away_vorp = sum(ts) / len(ts)

    data = []
    with open("head_to_head/home.csv", 'r', encoding="utf8") as f:
        for line in f:
            data.append(line.strip().split(','))
    ts = []
    for line in data:
        if line == data[0]:
            continue

        ts.append(float(line[len(line) - 1]))

    home_vorp = sum(ts) / len(ts)

    return home_vorp, away_vorp


def average_box_plus_minus():
    data = []
    with open("head_to_head/away.csv", 'r', encoding="utf8") as f:
        for line in f:
            data.append(line.strip().split(','))
    ts = []
    for line in data:
        if line == data[0]:
            continue

        if int(line[1]) <= 5:
            ts.append(float(line[len(line) - 2]))
        elif 12 > int(line[1]) > 5:
            ts.append(float(line[len(line) - 2]) * 0.67)

    away_bpm = sum(ts) / len(ts)

    data = []
    with open("head_to_head/home.csv", 'r', encoding="utf8") as f:
        for line in f:
            data.append(line.strip().split(','))
    ts = []
    for line in data:
        if line == data[0]:
            continue

        if int(line[1]) <= 5:
            ts.append(float(line[len(line) - 2]))
        elif 12 > int(line[1]) > 5:
            ts.append(float(line[len(line) - 2]) * 0.67)

    home_bpm = sum(ts) / len(ts)

    return home_bpm, away_bpm


def average_win_shares_per48(column):
    data = []
    with open("head_to_head/away.csv", 'r', encoding="utf8") as f:
        for line in f:
            data.append(line.strip().split(','))
    ws = []
    for line in data:
        if line == data[0]:
            continue

        if int(line[1]) <= 5:
            ws.append(float(line[len(line) - column]))
        elif 12 > int(line[1]) > 5:
            ws.append(float(line[len(line) - column]) * 0.67)

    away_ws = sum(ws) / len(ws)

    data = []
    with open("head_to_head/home.csv", 'r', encoding="utf8") as f:
        for line in f:
            data.append(line.strip().split(','))
    ws = []
    for line in data:
        if line == data[0]:
            continue

        if int(line[1]) <= 5:
            ws.append(float(line[len(line) - column]))
        elif 12 > int(line[1]) > 5:
            ws.append(float(line[len(line) - column]) * 0.67)

    home_ws = sum(ws) / len(ws)

    return home_ws, away_ws
