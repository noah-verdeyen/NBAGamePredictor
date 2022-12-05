from database import *
from simulate import *
import customtkinter
from google.cloud import bigquery
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    'C:/Users/noahv/OneDrive/Desktop/NBA_Game_Predictor/nbaproject-370202-d8f9d59c5682.json')
client = bigquery.Client(credentials=credentials)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.geometry("640x360")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

homeTeam = customtkinter.CTkEntry(master=frame, placeholder_text="Home Team")
awayTeam = customtkinter.CTkEntry(master=frame, placeholder_text="Away Team")

homeTeam.pack(pady=12, padx=10)
awayTeam.pack(pady=12, padx=10)


def compare_team():
    query = """
    SELECT player_name, team, mp, raptor_offense, raptor_defense, predator_offense, predator_defense, war_total
    FROM `nbaproject-370202.nba_data_set.player_advanced_stats` 
    LIMIT 750
    """

    query_result = client.query(query)
    print(query_result)

    home_roster = []
    away_roster = []
    for row in query_result:
        player = (row['player_name'], row['team'], row['mp'], row['raptor_offense'], row['raptor_defense'],
                  row['predator_offense'], row['predator_defense'], row['war_total'])

        if row["team"] == str(homeTeam.get()).upper() and int(row['mp']) > 80:
            home_roster.append(player)
        elif row["team"] == str(awayTeam.get()).upper() and int(row['mp']) > 80:
            away_roster.append(player)

    print(home_roster, away_roster)
    run_sim(home_roster, away_roster)


comp_button = customtkinter.CTkButton(master=frame, text="Compare", command=compare_team)
comp_button.pack(pady=12, padx=10)

update_button = customtkinter.CTkButton(master=frame, text="Update", command=update_db)
update_button.pack(pady=12, padx=10)

root.mainloop()
