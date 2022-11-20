import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_nba_stats():
    team = input("team? ")
    team = team.upper()
    bb_ref_url = "https://www.basketball-reference.com/teams/{}/2023.html".format(team)

    res = requests.get(bb_ref_url)
    with open("teams/{}.html".format(team), "w+") as f:
        f.write(res.text)

    soup = BeautifulSoup(res.text, 'html.parser')
    per36 = soup.find(id="per_minute")
    # per36tbl = pd.read_html(str(per36))
    # print(per36tbl)


if __name__ == "__main__":
    get_nba_stats()
    print("done:)")
