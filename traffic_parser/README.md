# Traffic Parser
This portion of the code is designed to parse through networking traffic, grab the information wanted for Cookietective, then store those values into the database.db SQLite3 database. For the purposes of this project, the traffic being parsed is only DNS and HTTP/HTTPS packets to grab CNAME aliasing information and Set-Cookie header information found while web crawling. For the project, this code is run inside of the containers during the webcrawling, but can also be run directly on one's own machine. The specific reasons for using the information we gather is specified in the main README documentation.

## DNS Scanner (dnsscan.py)
Python script to be run in the background that parses through networking traffic for 15 seconds to search for DNS packets. If any DNS response packets are found with a CNAME-type resource record, it will store the following information into the SQLite3 database (per CNAME packet):

- domainName (Original domain that has a CNAME alias)
- sourceAddress (IP Address that the packet came from)
- CNAMEAlias (Domain name that the original domain is aliased as)
- hasAType (Boolean for if this packet contains any A-type resource records)
- originalURL (Web crawler's input URL)

## HTTPS scanner (mitmproxy_script.py)
Python script to be run with mitmproxy (man in the middle proxy). As the Man in the Middle proxy runs, it will use this script for whenever it intercepts any HTTP/HTTPS response packets. The response function specifies how we want the proxy to modify / parse through incoming HTTP/HTTPS packets. In this case, we're using it to see if the packet contains Set-Cookie headers (cookie settings) that we store into SQLite using this information gathered:

- domainName (Domain name of packet sender)
- sourceAddress (IP address that sent the packet)
- domain_setting (What are the domain settings specified if any)
- httponly (Does cookie settings contain HttpOnly attribute)
- secure (Does cookie settings contain Secure attribute)
- originalURL (Web crawler's input URL)

## Automated Scan / Crawl Bash Script (../cookie.sh)
Bash script that is run in all containers. It automates the setup stage for the MITMproxy (setting network settings to using the proxy, installing and trusting the mitmproxy certificate, then running the webcrawler and traffic parsing scripts).

## Automated Container Generation (../run_containers.sh)
Bash script that is used to generate the docker containers and run each with an even number of URLs when given a text file of URLs and an offset into those URLs. Currently is set to run 10 containers that run 3600 links each.
