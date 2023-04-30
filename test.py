import sqlite3

con = sqlite3.connect('compiledDatabase.db')
cur = con.cursor()

cur.execute("""CREATE TABLE findings (
    originalURL text NOT NULL,
    domainName text NOT NULL,
    party int,
    vuln int,
    majmill int,
    notrack int,
    UNIQUE(originalURL, domainName)
    )""")

con.commit()
con.close()