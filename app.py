import pandas as pd 
import gspread
import gspread_dataframe as gdf
from oauth2client.service_account import ServiceAccountCredentials

url = 'https://www.pro-football-reference.com/boxscores/'

# get boxscores
list_of_dfs = pd.read_html(url, skiprows=1)
# We just want scores, remove rushing/receiving stats
res = list_of_dfs[::2]

#rename columns
for i in res:
    i.rename(columns = {0 :'team', 1 : 'score', 2: 'margin'}, inplace = True)

# calculate margin of victory for each df
for i in res:
   i.loc[0, 'margin'] = i['score'][0] - i['score'][1]
   i.loc[1, 'margin'] = i['score'][1] - i['score'][0] 

# flatten the list of data frames into a a single data frame
df = pd.concat(res)

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("hello").worksheet("w15")

# Set sheet1 with scores dataframe
gdf.set_with_dataframe(sheet, df)

