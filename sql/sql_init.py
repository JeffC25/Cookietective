import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

# Initialize the CNAME table
cur.execute("""CREATE TABLE CNAMEpackets (
    domainName text,
    sourceAddress text,
    CNAMEAlias text,
    hasAType int,
    originalURL text DEFAULT NULL,
    whoisAnalysis int,
    UNIQUE(domainName, sourceAddress, CNAMEAlias, hasAType)
    )""")

# Initialize the IP table that stores IP packets associated with A-type packets
cur.execute("""CREATE TABLE ip (
    domainName text NOT NULL,
    ip text NOT NULL,
    UNIQUE(domainName, ip)
    )""")

# Initialize the cookie table that stores Set-Cookie information from MITMproxy
cur.execute("""CREATE TABLE cookie (
    domainName text NOT NULL,
    sourceAddress text NOT NULL,
    domain_setting text NOT NULL,
    originalURL text DEFAULT NULL,
    UNIQUE(domainName, sourceAddress, domain_setting)
    )""")

# Initialize the findings table that stores output of the compiledDatabase analysis
cur.execute("""CREATE TABLE findings (
    originalURL text NOT NULL,
    domainName text NOT NULL,
    domain_setting text DEFAULT NULL,
    party int,
    vuln int,
    majmill int,
    notrack int,
    UNIQUE(originalURL, domainName)
    )""")

# cur.execute("""CREATE TABLE cookie (
#     domainName text NOT NULL,
#     sourceAddress text NOT NULL,
#     domain_setting text NOT NULL,
#     httponly int,
#     secure int,
#     originalURL text DEFAULT NULL,
#     UNIQUE(domainName, sourceAddress, domain_setting, httponly, secure, originalURL)
#     )""")

conn.commit()
conn.close()