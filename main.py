import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd


def get_nba_stats():
    team = input("team? ")
    team = team.upper()
    bb_ref_url = "https://www.basketball-reference.com/teams/{}/2023.html".format(team)

    res = requests.get(bb_ref_url)

    soup = BeautifulSoup(res.text, 'html.parser')

    div = soup.find("table")
    per36tbl = pd.read_html(str(div))

    print(per36tbl)

    # tbl = div.find(id="div_per_minute")
    # soup = soup.find(id="div_per_minute")
    # print(tbl)
    # per36tbl = pd.read_html(str(per36))
    # print(per36tbl)


if __name__ == "__main__":
    get_nba_stats()
    print("done:)")
