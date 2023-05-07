import sqlite3
import os
from comparator import comparator
import pandas as pd
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import sql.sql_func as sql

dbFile = '../sampledatabase.db'
dbFile = os.path.abspath(os.path.join(os.path.dirname(__file__), dbFile))
conn = sqlite3.connect(dbFile)
cur = conn.cursor()

cur.execute("SELECT DISTINCT domainName FROM findings")
results = cur.fetchall()


stringsin = [result[0].strip('.') for result in results]

#comparator(stringsin)

df = comparator(*stringsin)

#df.to_csv('output.csv', index=False)

conn.close()

# iterate through every row of the DataFrame df
for index, row in df.iterrows():

    # get the domain name, MajesticMillion flag, and NoTracking flag from the row
    domainName = row['Address']+"."
    majmill = row['MajesticMillion']
    notrack = row['NoTracking']
    # print(domainName)
    # call the setComparator function with the domainName, majmill, and notrack values
    sql.setComparator(domainName, majmill, notrack)

