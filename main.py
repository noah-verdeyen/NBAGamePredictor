import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import csv


def get_nba_stats(team, is_home_team):
    # implement a way to select different tables
    bb_ref_url = "https://www.basketball-reference.com/teams/{}/2023.html".format(team.upper())
    req = requests.get(bb_ref_url)
    soup = BeautifulSoup(req.text, 'html.parser')

    table = soup.findAll("table")
    list_of_frames = pd.read_html(str(table[3]))
    res = pd.concat(list_of_frames)

    if is_home_team:
        with open("head_to_head/home.csv", "+w") as f:
            f.write(str(res.to_csv("head_to_head/home.csv")))
    else:
        with open("head_to_head/away.csv", "+w") as f:
            f.write(str(res.to_csv("head_to_head/away.csv")))

    return res


def compare_scoring():
    with open("head_to_head/home.csv") as home_csv_file:
        home_data = csv.reader(home_csv_file)

    with open("head_to_head/away.csv") as away_csv_file:
        away_data = csv.reader(away_csv_file)

    print(home_data)
    print(away_data)

    total_away_scoring = 0
    for rows in away_data:
        # if total_away_scoring == 0:

        print(rows)

    return 0


if __name__ == "__main__":
    # scrape data
    away_team_stats = get_nba_stats(input("away? "), False)
    home_team_stats = get_nba_stats(input("home? "), True)

    # first metric, scoring, home team is a positive value, away is a negative
    scoring = compare_scoring()
