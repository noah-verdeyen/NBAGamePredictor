import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd


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


if __name__ == "__main__":
    away_team_stats = get_nba_stats(input("away? "), False)
    home_team_stats = get_nba_stats(input("home? "), True)
