import sqlite3

# Insert functions
def insertCNAMEpacketsEntry(domainName, sourceAddress, CNAMEAlias, hasAType):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    # If fails to INSERT (if already exists as unique value, then do nothing)
    try:
        cur.execute("SELECT * FROM CNAMEpackets WHERE domainName = ? AND sourceAddress = ? AND CNAMEAlias = ?", (domainName, sourceAddress, CNAMEAlias))
        result = cur.fetchone()
        
        # Check if a result of the same values already exists. If new result is same except for Atype, just update old value
        if (result):
            if (result[3] == 0 and hasAType == 1):
                cur.execute("UPDATE CNAMEpackets set hasAType = 1 WHERE domainName = ? AND sourceAddress = ? AND CNAMEAlias = ?", (domainName, sourceAddress, CNAMEAlias))
                conn.commit()
            conn.close()
            return

        # Insert into the database
        cur.execute("INSERT INTO CNAMEpackets VALUES (?, ?, ?, ?, ?, ?)", (domainName, sourceAddress, CNAMEAlias, hasAType, None, None))
    except:
        conn.close()
    else:   
        conn.commit()
        conn.close()
        
    return

def insertIpEntry(domainName, ip):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    # If fails to INSERT (if already exists as unique value, then do nothing)
    try:
        cur.execute("INSERT INTO ip VALUES (?, ?)", (domainName, ip))
    except:
        conn.close()
    else:
        conn.commit()
        conn.close()
    return

def insertCookieEntry(domainName, src_ip, domain_setting):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    # If fails to INSERT (if already exists as unique value, then do nothing)
    try:
        cur.execute("INSERT INTO cookie VALUES (?, ?, ?, ?)", (domainName, src_ip, domain_setting, None))
    except:
        conn.close()
    else:
        conn.commit()
        conn.close()
    return

# Helper function to be run at the end of crawler to set all entries with no set originalURL to be that of URL that just got parsed
def insertOriginalURL(URL):
    # Connect to the database
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Update all originalURL values to be that of the current URL
    cur.execute("UPDATE CNAMEpackets SET originalURL=? WHERE originalURL IS NULL", (URL,))
    cur.execute("UPDATE cookie SET originalURL=? WHERE originalURL IS NULL", (URL,))

    # Commit changes
    conn.commit()
    conn.close()

    return

    # Update all values in cookie and CNAMEpackets
def insertWhoisAnalysis(rowNumber, whoisValue):
    # Connect to the database
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Update all whois to be that of the current URL
    cur.execute("UPDATE CNAMEpackets SET whoisAnalysis = ? WHERE rowid = ?", (whoisValue, rowNumber))

    # Commit changes
    conn.commit()
    conn.close()

    return


# Fetch functions

def fetchDomainFromAlias(CNAMEAlias):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT domainName FROM CNAMEpackets WHERE CNAMEAlias = ?", (CNAMEAlias,))
    result = cur.fetchall()

    conn.commit()
    conn.close()
    return result

def fetchIpFromDomain(domainName):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT ip FROM ip WHERE domainName = ?", (domainName,))
    result = cur.fetchall()
    return result

def fetchATypeRecordsFromDomain(domainName):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT hasAType FROM CNAMEpackets WHERE domainName = ?", (domainName,))
    result = cur.fetchall()

    return result

# Function for accuracy checking that will add in the comparator values
def setComparator(domainName, majmill, notrack):
    conn = sqlite3.connect('../sampledatabase.db')
    cur = conn.cursor()
    try:
        cur.execute("UPDATE findings SET majmill=?, notrack=? WHERE domainName=?", (majmill, notrack, domainName))
        conn.commit()
        conn.close()
    except:
        print("Error: Failed to update majmill and notrack values")
        conn.close()
    return
    
