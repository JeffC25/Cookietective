import threading
import sys
import socket
from datetime import datetime as dt

import time
import sqlite3

def get_whois_data(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("whois.arin.net", 43))
    s.send(('n ' + ip + '\r\n').encode())

    response = b""

    # setting time limit in secondsmd
    startTime = time.mktime(dt.now().timetuple())
    timeLimit = 3
    while True:
        elapsedTime = time.mktime(dt.now().timetuple()) - startTime
        data = s.recv(4096)
        response += data
        if (not data) or (elapsedTime >= timeLimit):
            break
    s.close()

    return response.decode()

def findOrgName(whoisString):
    orgNameIndex = whoisString.find("OrgName")
    orgNameEnd = whoisString.find("OrgId")
    orgName = whoisString[orgNameIndex+16:orgNameEnd-1]
    return orgName

def compareWhois(rowNum, database): # given the row number of the table, compare the domain that belongs to the
    conn = sqlite3.connect(database)
    cur = conn.cursor()

    # Execute the SELECT statement to retrieve the domainName and originalURL values for a specific row
    cur.execute("SELECT domainName, originalURL FROM CNAMEpackets WHERE rowid = ?", (rowNum,))

    # Fetch the result set and retrieve the values
    row = cur.fetchone()
    domainName = row[0].decode()
    originalURL = row[1]

    #print("Domain Name: " + domainName)
    #print("Original URL: " + originalURL)

    domainNameIP = socket.gethostbyname(domainName);
    domainNameWhois = get_whois_data(domainNameIP)
    domainNameOrg = findOrgName(domainNameWhois)
    #print(domainNameOrg)

    originalURLIP = socket.gethostbyname(originalURL);
    originalURLWhois = get_whois_data(originalURLIP)
    originalURLOrg = findOrgName(originalURLWhois)
    #print(originalURLOrg)

    returnVal = 0
    if domainNameOrg is None or originalURLOrg is None:
        # print("Unknown owner status.")
        returnVal = 2

    # If the organizations are the same, write one to database and return 1
    elif domainNameOrg == originalURLOrg:
        # print("Same owner.")
        returnVal = 1

    # If they are not the same, return 0
    elif domainNameOrg != originalURLOrg:
        # print("Different owner.")
        returnVal = 0

    conn.commit()
    conn.close()
    return returnVal

'''Test Code
DB_file = '../sampledatabase.db'
rowid = 3
whois_res = compareWhois(rowid+1,DB_file)
'''
