import requests
from bs4 import BeautifulSoup
import pandas as pd


def update_db():
	print("updating...")
	data = []
	p = 1
	open('../data/players.csv', 'w').close()
	while p <= 6:
		cbs_url = "https://www.cbssports.com/nba/stats/player/scoring/nba/regular/all-pos/qualifiers/?page={}".format(p)
		req = requests.get(cbs_url)
		soup = BeautifulSoup(req.text, 'html.parser')

		table = soup.findAll("table")
		curr_frame = pd.concat(pd.read_html(str(table)))
		data.append(curr_frame)

		p = p + 1

	final_data_frame = pd.concat(data)
	final_data_frame.reset_index(inplace=True)
	final_data_frame.drop(["index"], axis=1, inplace=True)

	list_of_names_dirty = final_data_frame["Player  Player on team"].to_list()
	list_of_names_clean = []
	for name in list_of_names_dirty:
		first = name.index("  ")
		second = name.index("  ", first+1)
		third = name.index("  ", second+1)
		new_str = name[third:].strip()
		new_str = new_str.replace("  ", ",")
		list_of_names_clean.append(new_str)

	final_data_frame.drop(["Player  Player on team"], axis=1, inplace=True)

	final_data_frame["Player"] = [x.split(",")[0] for x in list_of_names_clean]
	final_data_frame["Position"] = [x.split(",")[1] for x in list_of_names_clean]
	final_data_frame["Team"] = [x.split(",")[2] for x in list_of_names_clean]

	with open("../data/players.csv", "a", encoding="utf8") as f:
		f.write(final_data_frame.to_csv(header=False))

	return "exit"
