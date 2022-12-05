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
            SELECT ppg.Player,
            ppg.Team,
            ppg.MPG__Minutes_Per_Game,
            ppg.PPG__Points_Per_Game,
            ppg.FG___Field_Goal_Percentage,
            passing.A_TO__Assists_Per_Turnover
            
            FROM `nbaproject-370202.nba_data_set.scoring` ppg
            INNER JOIN `nbaproject-370202.nba_data_set.assists-turnovers` passing
            ON ppg.Player = passing.Player
            """
    query_result = client.query(query)
    # print(query_result)

    home_roster = []
    away_roster = []
    for row in query_result:
        player = (row['Player'], row['Team'], row['PPG__Points_Per_Game'], row['FG___Field_Goal_Percentage'],
                  row['MPG__Minutes_Per_Game'], row['A_TO__Assists_Per_Turnover'])

        # if row["Team"] == str(homeTeam.get()).upper():
        if row["Team"] == 'SAC':
            home_roster.append(player)
        # if row["Team"] == str(awayTeam.get()).upper():
        elif row["Team"] == 'CHI':
            away_roster.append(player)

    # print(home_roster)
    # print(away_roster)

    print('calculating...')
    run_sim(home_roster, away_roster, 10)


comp_button = customtkinter.CTkButton(master=frame, text="Compare", command=compare_team)
comp_button.pack(pady=12, padx=10)

update_button = customtkinter.CTkButton(master=frame, text="Update", command=update_db)
update_button.pack(pady=12, padx=10)

root.mainloop()
