
def get_diff(data):
	diff = float(data[0]) - float(data[1])
	return diff


def compare_per_game_stats(data):

	if data[0] >= -2:
		ppg = 1
	else:
		ppg = -1

	if data[1] >= 0:
		rpg = 1
	else:
		rpg = -1

	if data[2] >= 0:
		apg = 1
	else:
		apg = -1

	return (ppg + rpg + apg) * 0.8