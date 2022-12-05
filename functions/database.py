import requests
from bs4 import BeautifulSoup
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
	'C:/Users/noahv/OneDrive/Desktop/NBA_Game_Predictor/nbaproject-370202-d8f9d59c5682.json')
def update_db():
	lookup = ["scoring", "rebounds", "assists-turnovers", "steals", "blocks", "fouls-minutes"]
	data = []
	client = bigquery.Client(credentials=credentials)

	for metric in lookup:
		p = 1
		while p <= 6:
			cbs_url = "https://www.cbssports.com/nba/stats/player/{}/nba/regular/all-pos/qualifiers/?page={}".format(metric, p)

			req = requests.get(cbs_url)
			soup = BeautifulSoup(req.text, 'html.parser')

			table = soup.findAll("table")
			curr_frame = pd.concat(pd.read_html(str(table)))
			data.append(curr_frame)
			csv_path = "C:/Users/noahv/OneDrive/Desktop/NBA_Game_Predictor/data/{}.csv".format(metric)
			p = p + 1
			if p == 6:
				with open(csv_path, "w", encoding="utf8") as f:
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
					print(final_data_frame.to_csv())
					data.clear()
					f.write(final_data_frame.to_csv())

					table_id = "nbaproject-370202.nba_data_set.{}".format(metric)

					job_config = bigquery.LoadJobConfig(
						source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1, autodetect=True,
						write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE)

					with open(csv_path, "rb") as source_file:
						job = client.load_table_from_file(file_obj=source_file, destination=table_id, job_config=job_config)

					print(job.result())

	print("getting injuries...")
	get_injury_report()

	get_team_stats()

	get_advanced_stats()
	print("done")


def get_injury_report():
	client = bigquery.Client(credentials=credentials)
	cbs_url = "https://www.cbssports.com/nba/injuries/"
	req = requests.get(cbs_url)
	soup = BeautifulSoup(req.text, 'html.parser')

	table = soup.findAll("table")
	curr_frame = pd.concat(pd.read_html(str(table)))

	curr_frame.reset_index(inplace=True)

	table_id = "nbaproject-370202.nba_data_set.injuries"

	job_config = bigquery.LoadJobConfig(
		source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1, autodetect=True,
		write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE)

	data = open("injuries.csv", "w")
	data.write(curr_frame.to_csv())
	data.close()

	data = open("injuries.csv", "rb")
	job = client.load_table_from_file(file_obj=data, destination=table_id, job_config=job_config)
	print(job.result())


def get_team_stats():
	print("GETTING TEAM STATS")
	client = bigquery.Client(credentials=credentials)
	bb_ref_url = "https://www.basketball-reference.com/leagues/NBA_2023.html"
	req = requests.get(bb_ref_url)
	soup = BeautifulSoup(req.text, 'html.parser')
	for n in (8, 10, 11):
		table = soup.findAll("table")[n]
		curr_frame = pd.concat(pd.read_html(str(table)))
		print(curr_frame)
		job_config = bigquery.LoadJobConfig(
			source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1, autodetect=True,
			write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE)

		if n == 8:
			table_name = "team-per-100-stats"
		elif n == 10:
			table_name = "team-advanced-stats"
		else:
			table_name = "team-shooting-stats"

		table_id = "nbaproject-370202.nba_data_set.{}".format(table_name)
		data = open("{}.csv".format(table_name), "w")
		data.write(curr_frame.to_csv())
		data.close()

		data = open("{}.csv".format(table_name), "rb")
		job = client.load_table_from_file(file_obj=data, destination=table_id, job_config=job_config)
		print(job.result())


def get_advanced_stats():
	print("GETTING advanced STATS")
	client = bigquery.Client(credentials=credentials)
	five_thirty_eight = "https://projects.fivethirtyeight.com/nba-model/2023/latest_RAPTOR_by_team.csv"
	req = requests.get(five_thirty_eight)
	table = req.text
	print(table)

	data = open("player_advanced_stats.csv", "w")
	data.write(table)
	data.close()
	table_id = "nbaproject-370202.nba_data_set.player_advanced_stats"
	job_config = bigquery.LoadJobConfig(
		source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1, autodetect=True,
		write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE)
	data = open("player_advanced_stats.csv", "rb")
	job = client.load_table_from_file(file_obj=data, destination=table_id, job_config=job_config)
	print(job.result())
