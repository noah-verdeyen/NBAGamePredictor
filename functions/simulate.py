import numpy
import random

def run_sim(home_roster, away_roster):

	home_score = 0
	away_score = 0
	for player in home_roster:
		raptor_offense = float(player[3])
		raptor_defense = float(player[4])

		home_score += raptor_offense + raptor_defense

	for player in away_roster:
		raptor_offense = float(player[3])
		raptor_defense = float(player[4])

		away_score += raptor_offense + raptor_defense

	print(round(int(home_score), 1))
	print(round(int(away_score), 1))
	if round(home_score) > round(away_score):
		print("Home Team Wins!")
	elif round(home_score) < round(away_score):
		print("Away Team Wins!")
	else:
		print("Tie")
