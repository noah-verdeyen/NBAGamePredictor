import requests

print("running...")
print()

five_thirty_eight = "https://projects.fivethirtyeight.com/nba-model/2023/latest_RAPTOR_by_team.csv"
req = requests.get(five_thirty_eight)
table = req.text

data = open("player_stats.csv", "w")
data.write(table)
data.close()
