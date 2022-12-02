from database import *
from datetime import date
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
    SELECT Player, Team, PPG__Points_Per_Game, FG___Field_Goal_Percentage 
    FROM `nbaproject-370202.nba_data_set.scoring`
    """
    query_result = client.query(query)
    print(query_result)

    home_data = []
    away_data = []

    for row in query_result:
        if row["Team"] == str(homeTeam.get()).upper():
            home_data.append(row)
        elif row["Team"] == str(awayTeam.get()).upper():
            away_data.append(row)


comp_button = customtkinter.CTkButton(master=frame, text="Compare", command=compare_team)
comp_button.pack(pady=12, padx=10)

update_button = customtkinter.CTkButton(master=frame, text="Update", command=update_db)
update_button.pack(pady=12, padx=10)

root.mainloop()
