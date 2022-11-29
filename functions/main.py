from data_collection import *
from compare_functions import *
from database import *
import mysql.connector


def compare_two_teams():
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
    offense_ppg_diff = get_diff(scoring_per_game)
    reb_per_game_diff = get_diff(rebounding_per_game)
    ass_per_game_diff = get_diff(assists_per_game)

    # scrape for advanced stats
    get_nba_stats(home_team_input, True, 3)
    get_nba_stats(away_team_input, False, 3)

    true_shooting = average_true_shooting()
    avg_vorp = average_vorp()
    avg_bpm = average_box_plus_minus()
    avg_win_shares = average_win_shares_per48(6)
    avg_def_win_shares = average_win_shares_per48(7)
    avg_off_win_shares = average_win_shares_per48(8)

    ts_diff = get_diff(true_shooting)
    vorp_diff = get_diff(avg_vorp)
    bpm_diff = get_diff(average_box_plus_minus())
    ws_diff = get_diff(avg_win_shares)
    ws_def_diff = get_diff(avg_def_win_shares)
    ws_off_diff = get_diff(avg_off_win_shares)

    per_game_winner = compare_per_game_stats((offense_ppg_diff, reb_per_game_diff, ass_per_game_diff))
    adv_winner = sum((ts_diff, vorp_diff, bpm_diff, ws_diff, ws_def_diff, ws_off_diff))

    total_winner = per_game_winner + adv_winner

    # todo counting stats are probably too strong for first run through
    if total_winner > 0:
        print(home_team_input.upper(), " WINS!")
        print()
        print("COUNTING RANK: ", per_game_winner)
        print("ADVANCED RANK: ", adv_winner)
        print("TOTAL RANK: ", total_winner)

        return "comp"
    elif total_winner < 0:
        print(away_team_input.upper(), " WINS!")
        print()
        print("COUNTING RANK: ", per_game_winner)
        print("ADVANCED RANK: ", adv_winner)
        print("TOTAL RANK: ", total_winner)

        return "comp"
    else:
        print("NO CURRENT WINNER, ADD MORE DATA")

        return "comp"

    return "comp"


if __name__ == "__main__":
    # user = input("update? y/n: ")
    # if user.lower() == "y":
    # update_db()

    print("connecting")
    cnx = mysql.connector.connect(user='noahver', password='noahnoah',
                                  host='127.0.0.1',
                                  database='nba_stats')
    print("status: ", cnx)
    cursor = cnx.cursor()

    while not cnx.is_closed():
        user = input("home team: ")
        query = "select player_name, games_played, minutes_per_game, points_per_game, " \
                "field_goal_percent, 3pt_field_goal_percent from current_players " \
                "where team_id = '{}'".format(user.upper())

        cursor.execute(str(query))
        # | Player Name | Games Played | MPG | PPG | FG% | 3PT% |
        for (player_name, games_played, mpg, ppg, fg, three) in cursor:
            print(player_name, games_played, mpg, ppg, fg, three)
        cnx.close()
