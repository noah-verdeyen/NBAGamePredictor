from data_collection import *
from compare_functions import *


if __name__ == "__main__":
    # scrape BBallRef for counting data
    home_team_input = input("Home: ")
    away_team_input = input("Away: ")
    get_nba_stats(home_team_input, True, 2)
    get_nba_stats(away_team_input, False, 2)

    # data collection
    games_played = get_games_played()
    scoring = compare_scoring()
    rebounding = compare_rebounding()
    assists = compare_assists()

    # get data on a per game level
    per_game_data = convert_to_per_game((games_played, scoring, rebounding, assists))
    scoring_per_game = per_game_data[1]
    rebounding_per_game = per_game_data[2]
    assists_per_game = per_game_data[3]

    # start comparisons (-) means away team is ahead (+) means home team is ahead
    offense_ppg_diff = per_game_diff(scoring_per_game)
    reb_per_game_diff = per_game_diff(rebounding_per_game)
    ass_per_game_diff = per_game_diff(assists_per_game)

    per_game_winner = compare_per_game_stats((offense_ppg_diff, reb_per_game_diff, ass_per_game_diff))

    if per_game_winner > 0:
        print(home_team_input.upper(), " WINS!")
        print("RANK: ", per_game_winner)
    elif per_game_winner < 0:
        print(away_team_input.upper(), " WINS!")
        print("RANK: ", per_game_winner)
    else:
        print("NO CURRENT WINNER, ADD MORE DATA")
