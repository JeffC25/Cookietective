import re
from urllib.parse import urlparse
from whois_check import compareWhois
import sqlite3

"""
Test URLS

http://www.drugemporium.com/cec/cstage?eccookie=@eccookie@&ecaction=de_ecwalkin&template=de_walkin.en.htm
http://preview.ynot.com/cgibin/nd_CGI_50.cgi/YnotPhoenix/CFsMain.
pa.clients6.google.com
https://https:⁄⁄www.netmeister.org@https://www.netmeister.org/https:⁄⁄www.netmeister.org⁄?https://www.netmeister.org=https://www.netmeister.org;https://www.netmeister.org#https://www.netmeister.org


"""
def mostMatching(url1, url2): # returns number of matching domains, array of what they are

    # split the arrays based on the . character
    url1Array = url1.split(".")
    url2Array = url2.split(".")

    # reverse the arrays so highest level domains are first
    url1Array.reverse()
    url2Array.reverse()
    
    # compare the arrays in a loop until they are not the same or the array is done.
    matches = []
    if len(url1Array) > len(url2Array):
        num_checks = len(url2Array)
        main_comp = url2Array
        sec_comp = url1Array
        iter_checks = len(url1Array)
    else:
        num_checks = len(url1Array)
        main_comp = url1Array
        sec_comp = url2Array
        iter_checks = len(url2Array)

    
    matchCount = 0
    #print(main_comp)
    #print(sec_comp)
    for i in range(num_checks):
        match_found = False
        for j in range(iter_checks):
            if main_comp[i] == sec_comp[j] and sec_comp[j] != '':
                matches.append(sec_comp[j])
                matchCount += 1
                match_found = True
                break
        if match_found == False:
            matches.append("")

    return matchCount, matches

def parse_url(url):
    
    first_run = urlparse(url)
    pattern = r"^((?P<scheme>[^:/?#]+):(?=//))?(//)?(((?P<login>[^:]+)(?::(?P<password>[^@]+)?)?@)?(?P<host>[^@/?#:]*)(?::(?P<port>\d+)?)?)?(?P<path>[^?#]*)(\?(?P<query>[^#]*))?(#(?P<fragment>.*))?"
    matches = []
    if first_run[1] == "":
        a = re.search(pattern,first_run[2])
        matches.append(a.group('host'))
    else:
        a = re.search(pattern,first_run[1])
        b = re.search(pattern,first_run[2])
        matches.append(a.group('host'))
        if b.group('host') != "":
            matches.append(b.group('host'))
    return matches

def match_found(match_count,check_url):
    #print(match_count)
    #print(check_url)
    match_num = 0
    if match_count > 1:
        for m in check_url:
            if m != "":
                match_num += 1
                if match_num == match_count:
                    return True
            else:
                match_num = 0
    else:
        return False
    

def compare_url(row_id, database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT domainName,CNAMEAlias,originalURL FROM CNAMEpackets WHERE rowid = "+str(row_id))
    c = cur.fetchall()
    curr = c[0]
    domainName = curr[0].decode()
    CNAMEAlias = curr[1].decode()
    originalURL = str(curr[2])
    
    matchingDvO = False
    matchingCvO = False
    parsed_domainName = parse_url(domainName)
    parsed_CNAMEAlias = parse_url(CNAMEAlias)
    parsed_originalURL = parse_url(originalURL)

    #PART 1
    #Check domainName vs original URL
    for a in parsed_originalURL:
        if matchingDvO == False:
            for b in parsed_domainName:
                count, matching = mostMatching(a,b)
                if match_found(count,matching) == True:
                    matchingDvO = True
        if matchingCvO == False:
            for d in parsed_CNAMEAlias:
                count, matching = mostMatching(a,d)
                if match_found(count,matching) == True:
                    matchingCvO = True

    if matchingDvO == True and matchingCvO == True:
        return True
    else:
        return False

def cookie_check(rowid, database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT CNAMEAlias,originalURL FROM CNAMEpackets WHERE rowid="+str(rowid))
    c = cur.fetchall()
    curr = c[0]
    CNAMEAlias = curr[0]
    original_URL = curr[1]
    parsed_CNAMEAlias = parse_url(CNAMEAlias.decode())
    cur.execute("SELECT domain_setting FROM cookie WHERE originalURL = ?",(original_URL,))#original_URL)
    c = cur.fetchall()
    bad_matching = False
    domainSet = None
    for d in c:
        if bad_matching == True:
            break
        domain_setting = parse_url(d[0])
        if domain_setting != None or domain_setting != "":
            for a in domain_setting:
                for e in parsed_CNAMEAlias:
                    count, matching = mostMatching(a,e)
                    if match_found(count,matching) == True:
                        bad_matching = True
                        domainSet = d[0]
                        break
        #print("If next two match:")
        #print(CNAMEAlias.decode())
        #print(d[0])

    return bad_matching, domainSet
    


    """
    domainName text,
    sourceAddress text,
    CNAMEAlias text,
    hasAType int,
    originalURL text DEFAULT NULL,
    """
def main():
    """
    test_urls = ["http://www.drugemporium.com/cec/cstage?eccookie=@eccookie@&ecaction=de_ecwalkin&template=de_walkin.en.htm",
                 "http://preview.ynot.com/cgibin/nd_CGI_50.cgi/YnotPhoenix/CFsMain.",
                 "pa.clients6.google.com",
                 "https://https:⁄⁄www.netmeister.org@https://www.netmeister.org/https:⁄⁄www.netmeister.org⁄?https://www.netmeister.org=https://www.netmeister.org;https://www.netmeister.org#https://www.netmeister.org", "http://username:password@example.com/"]

    a_match = "pa.clients6.google.com"
    b_match = "https://mail.google.com/mail/u/1/#inbox/FMcgzGsNTcfRRvxvJxDrFkNcqjvf"
    DB_file = '../sampledatabase.db'

    for site in test_urls:
        m=parse_url(site)
        print(m)
    print("\n\n")
    a = parse_url(a_match)
    b = parse_url(b_match)
    print(a)
    print(b)
    
    count, matching = mostMatching(a[0],b[0])
    print(count,matching)
    print(match_found(count,matching))

    conn = sqlite3.connect(DB_file)
    cur = conn.cursor()

    cur.execute("SELECT rowid FROM CNAMEpackets")
    c = cur.fetchall()
    print(c)
    """
    # !!!!

    """
    party: 0 = 1st party, 1 = 3rd party, 2 = unknown
    vuln: 0 = no, 1 = yes, 2 = unknown
    """
    
    """
    CREATE TABLE findings (
    originalURL text NOT NULL,
    domainName text NOT NULL,
    domain_setting default NULL
    party int, 
    vuln int,
    majmill int,
    notrack int,
    UNIQUE(originalURL, domainName)
    );
    """

    DB_file = '../database.db'

    conn = sqlite3.connect(DB_file)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS findings (
    originalURL text NOT NULL,
    domainName text NOT NULL,
    domain_setting text DEFAULT NULL,
    party int,
    vuln int,
    majmill int,
    notrack int,
    UNIQUE(originalURL, domainName)
    )""")
    conn.commit()

    cur.execute("SELECT rowid FROM CNAMEpackets")
    c = cur.fetchall()
    
    thirdparty = 0
    vuln = 0
    scanned = 0
    for m in c:
        rowid = m[0]
        cur.execute("SELECT domainName,originalURL FROM CNAMEpackets WHERE rowid="+str(rowid))
        b = cur.fetchall()
        curr = b[0]
        domainName = curr[0].decode()
        originalURL = str(curr[1])
        cur.execute("SELECT originalURL,domainName FROM findings WHERE originalURL=? AND domainName=?",(originalURL,domainName))
        k = cur.fetchall()
        if len(k) == 0:
            continue
        else:
            whoisval = compareWhois(rowid, DB_file)
            if whoisval == 2:
                if compare_url(rowid,DB_file) == False:
                    bad_matching, domainset = cookie_check(rowid,DB_file)
                    if bad_matching == True:
                        cur.execute("INSERT OR IGNORE INTO findings VALUES (?,?,?,?,?,?,?)",(originalURL,domainName,domainset,1,1,0,0))
                        conn.commit()
                        thirdparty += 1
                        vuln += 1
                    else:
                        conn.execute("INSERT OR IGNORE INTO findings VALUES (?,?,?,?,?,?,?)",(originalURL,domainName,None,1,0,0,0))
                        conn.commit()
                        thirdparty += 1
                else:
                    cur.execute("INSERT OR IGNORE INTO findings VALUES (?,?,?,?,?,?,?)",(originalURL,domainName,None,0,0,0,0))
                    conn.commit()
            elif whoisval == 0:
                bad_matching, domainset = cookie_check(rowid,DB_file)
                if bad_matching == True:
                    cur.execute("INSERT OR IGNORE INTO findings VALUES (?,?,?,?,?,?,?)",(originalURL,domainName,domainset,1,1,0,0))
                    conn.commit()
                    thirdparty += 1
                    vuln += 1
                else:
                    conn.execute("INSERT OR IGNORE INTO findings VALUES (?,?,?,?,?,?,?)",(originalURL,domainName,None,1,0,0,0))
                    conn.commit()
                    thirdparty += 1
            else:
                cur.execute("INSERT OR IGNORE INTO findings VALUES (?,?,?,?,?,?,?)",(originalURL,domainName,None,0,0,0,0))
                conn.commit()
            scanned += 1

    cur.execute("SELECT domainName,originalURL,domain_setting FROM findings WHERE party=1 AND vuln=1")
    c = cur.fetchall()
    for curr in c:
        domainName = curr[0]
        originalURL = str(curr[1])
        domainset = curr[2]
        print("These are vulnerable results: ")
        print(domainName)
        print(originalURL)
        print(domainset)
        print("\nThese are the general results of the scan: ")
        print("Scanned:               "+str(scanned))
        print("Third Party Found:     "+str(thirdparty))
        print("Vulnerabilities Found: "+str(vuln))
    """
        elif whois_res == 1:
            print("NO CLOAKING FOUND\n")
        else:
            if cookie_check(rowid,DB_file) == True:
                print("FOUND CLOAKING\n")
            else:
                print("NO CLOAKING FOUND\n")
    """
    conn.close()
    """
    for m in c:
        rowid = m[0]
        whois_res = compareWhois(rowid,DB_file)
        if whois_res == 2:
            if compare_url(rowid,DB_file) == False:
                if cookie_check(rowid,DB_file) == True:
                    print("FOUND CLOAKING\n")
                else:
                    print("NO CLOAKING FOUND\n")
            else:
                print("NO CLOAKING FOUND\n")
        elif whois_res == 1:
            print("NO CLOAKING FOUND\n")
        else:
            if cookie_check(rowid,DB_file) == True:
                print("FOUND CLOAKING\n")
            else:
                print("NO CLOAKING FOUND\n")
       """     
        #print(rowid)
   
    # !!!!


    
    
    
if __name__ == "__main__":
    main()
    
