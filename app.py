import pandas as pd 
import gspread
import gspread_dataframe as gdf
from oauth2client.service_account import ServiceAccountCredentials
import nflgame
from abbrevations import nfl_team_abbrev

games = nflgame.games(2019, week=17)
df = pd.DataFrame(data=None, columns = ['team', 'score', 'margin'])

for g in games:
    home_df = pd.DataFrame(
              [[g.home, g.score_home, g.score_home - g.score_away]], 
              columns = ['team', 'score', 'margin'])
    away_df = pd.DataFrame(
              [[g.away, g.score_away, g.score_away - g.score_home]], 
              columns = ['team', 'score', 'margin'])
    
    df = df.append(home_df, ignore_index=True)
    df = df.append(away_df, ignore_index=True)

df['team'] = df['team'].replace(nfl_team_abbrev, regex=True)

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open sheet by name
sheet = client.open("hello").worksheet("w17")

# Set sheet with scores dataframe
gdf.set_with_dataframe(sheet, df)

