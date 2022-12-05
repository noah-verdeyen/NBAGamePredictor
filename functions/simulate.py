import numpy
import random

def run_sim(home_roster, away_roster, n):
	# roster(Player, Team, PPG__Points_Per_Game, FG___Field_Goal_Percentage, MPG__Minutes_Per_Game, A_TO__Assists_Per_Turnover)
	if n is None:
		n = 10
	home_score = 0
	away_score = 0
	for player in home_roster:
		ppg_floor   = float(player[2]) * 0.75
		ppg_ceiling = float(player[2]) * 1.25

		ast_turnover_floor = float(player[4]) * 0.75
		ast_turnover_ceiling = float(player[4]) * 1.25
		home_score += numpy.average((ppg_ceiling, ppg_floor))

	for player in away_roster:
		ppg_floor   = float(player[2]) * 0.75
		ppg_ceiling = float(player[2]) * 1.25
		away_score += numpy.average((ppg_ceiling, ppg_floor))

	print(home_roster[0][1] + ": {}".format(int(home_score)))
	print(away_roster[0][1] + ": {}".format(int(away_score)))
	if round(home_score) > round(away_score):
		print("Home Wins!")
	elif round(home_score) < round(away_score):
		print("Away Wins!")
	else:
		print("Overtime")
