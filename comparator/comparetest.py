import sqlite3
import os
from comparator import comparator
import pandas as pd

dbFile = '../compiledDatabase.db'
dbFile = os.path.abspath(os.path.join(os.path.dirname(__file__), dbFile))
conn = sqlite3.connect(dbFile)
cur = conn.cursor()

cur.execute("SELECT domainName FROM CNAMEpackets")
results = cur.fetchall()


stringsin = [result[0].decode('utf-8').strip('.') for result in results]

df = comparator(stringsin)

df.to_csv('output.csv', index=False)

conn.close()

