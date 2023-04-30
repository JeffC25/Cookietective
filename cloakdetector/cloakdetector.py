import sqlite3
import socket
import ipaddress
import tldextract
import whois
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import sql.sql_func
import url_checker.url_func

def sameOwner(url1, url2):
    ext1 = tldextract.extract(url1)
    ext2 = tldextract.extract(url2)

    # check if the extracted top-level domains match
    if ext1.suffix == ext2.suffix:
        return True

    # if the top-level domains don't match, use the mostMatching function to check if they belong to the same owner
    matchCount, matches = mostMatching(url1, url2)

    # if there is only one matching domain and it is the top-level domain, assume they belong to the same owner
    if matchCount == 1 and matches[0] == ext1.suffix:
        return True

    # perform a WHOIS lookup for both domains and compare the registrant organization fields
    try:
        w1 = whois.whois(url1)
        w2 = whois.whois(url2)
        if w1.status == w2.status == None and w1.registrant_org == w2.registrant_org:
            return True
    except:
        pass

    return False



def get_ip_address(domain):
    ip_address = socket.gethostbyname(domain)
    return ip_address



def hasAType(domainName, dbFile='../database.db'):
    dbFile = os.path.abspath(os.path.join(os.path.dirname(__file__), dbFile))
    conn = sqlite3.connect(dbFile)
    c = conn.cursor()
    c.execute("SELECT hasAType FROM CNAMEpackets WHERE domainName=?", (domainName,))
    result = c.fetchone()
    conn.close()
    if result is not None:
        return result[0]
    else:
        return None
        

def hasCNAMErecord(domainName, dbFile='../database.db'):
    dbFile = os.path.abspath(os.path.join(os.path.dirname(__file__), dbFile))
    conn = sqlite3.connect(dbFile)
    c = conn.cursor()
    c.execute("SELECT EXISTS(SELECT 1 FROM CNAMEpackets WHERE domainName = ? LIMIT 1)", (domainName,))
    result = c.fetchone()[0]
    conn.close()
    return result
    
    

def firstPartyCheck(domainName, dbFile='../database.db'):
    dbFile = os.path.abspath(os.path.join(os.path.dirname(__file__), dbFile))
    conn = sqlite3.connect(dbFile)
    c = conn.cursor()
    c.execute(f"SELECT CNAMEAlias FROM CNAMEpackets WHERE domainName='{domainName}'")
    result = c.fetchone()
    conn.close()

    if result is None:
        return 0

    cnameAlias = result[0]
    if sameOwner(domainName, cnameAlias):
        return 1
    else:
        return 0



def IPcheck(domainName, dbFile='../database.db'):
    dbFile = os.path.abspath(os.path.join(os.path.dirname(__file__), dbFile))
    conn = sqlite3.connect(dbFile)
    c = conn.cursor()

    # get the associated CNAMEAlias and originalURL values
    c.execute("SELECT CNAMEAlias, originalURL FROM CNAMEpackets WHERE domainName=?", (domainName,))
    row = c.fetchone()

    # check if a row was returned
    if row is None:
        return None

    cnameDomain, inputURL = row[0], row[1]

    # get the IP addresses of the domain and input URL
    cnameIP = socket.gethostbyname(cnameDomain)
    inputIP = socket.gethostbyname(inputURL)

    # check if cnameIP is a subnetwork of inputIP
    if ipaddress.IPv4Address(cnameIP) in ipaddress.IPv4Network(inputIP):
        return 1
    else:
        return 0
        
        
        
def cloakDetector(domainName, dbFile='../database.db'):
    dbFile = os.path.abspath(os.path.join(os.path.dirname(__file__), dbFile))
    Arecord_test = hasAType(domainName, dbFile)
    CNAMErecord_test = hasCNAMErecord(domainName, dbFile)
    firstParty_test = firstPartyCheck(domainName, dbFile)
    IP_test = IPcheck(domainName, dbFile)

    if Arecord_test == 0 and CNAMErecord_test == 1 and firstParty_test == 0 and IP_test == 0:
        return 1
    else:
        return 0


if len(sys.argv) < 2:
    print("Usage: python3 cloakdetector.py domainName [dbFile]")
    sys.exit(1)

domainName = sys.argv[1]
dbFile = '../database.db' if len(sys.argv) < 3 else sys.argv[2]
result = cloakDetector(domainName, dbFile)

if result == 1:
    print(domainName, ": -!!- According to Approach 2, first party cookies are likely being shared with third parties by CNAME cloaking")
else:
    print(domainName, ": -XX- According to Approach 2, first party cookies are likely NOT being shared with third parties by CNAME cloaking")
