from google.cloud import bigquery
from database import update_db
from google.oauth2 import service_account

if __name__ == "__main__":
    credentials = service_account.Credentials.from_service_account_file(
        'C:/Users/noahv/OneDrive/Desktop/NBA_Game_Predictor/nbaproject-370202-d8f9d59c5682.json')
    # update_db()
    print("connecting")
    client = bigquery.Client(credentials=credentials)
    user = input("home team: ")
    query = """
    SELECT Player, Team, PPG__Points_Per_Game, FG___Field_Goal_Percentage 
    FROM `nbaproject-370202.nba_data_set.scoring`
    """
    query_result = client.query(query)
    print(query_result)
    for row in query_result:
        player = row["Player"]
        ppg = row["PPG__Points_Per_Game"]
        fg = row["FG___Field_Goal_Percentage"]
        print(f"{player} | {ppg} _ {fg}")
