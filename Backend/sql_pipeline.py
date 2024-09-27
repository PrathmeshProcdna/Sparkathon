import sqlite3

conn = sqlite3.connect('hacka.db')

import pandas as pd

df = pd.read_excel(r"C:\Users\PrathmeshLandge\Downloads\Sparkathon_data_dynamos_HCP_level_data.xlsx")
# print(df.tail(5))
df.to_sql('hacka',conn,if_exists='replace',index=False)

query = "select count(*) from hacka limit 5"
df = pd.read_sql_query(query,conn)
print(df)
