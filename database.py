import requests
from bs4 import BeautifulSoup
import pandas as pd
from header import *


def update_db():
	print("updating...")
	p = 1
	open('data/players.csv', 'w').close()
	while p <= 6:
		cbs_url = "https://www.cbssports.com/nba/stats/player/scoring/nba/regular/all-pos/qualifiers/?page={}".format(p)
		req = requests.get(cbs_url)
		soup = BeautifulSoup(req.text, 'html.parser')

		table = soup.findAll("table")
		data = pd.concat(pd.read_html(str(table)))

		with open("data/players.csv", "a", encoding="utf8") as f:
			data_as_csv = str(data.to_csv().replace(cbs_table_top_line, ""))

			f.write(data_as_csv)

		p = p + 1

	return "exit"


def scrub_csv():
	data = []
	with open("data/players.csv", 'r', encoding="utf8") as f:
		for line in f:
			data.append(line.strip().split(','))

	print(data)
