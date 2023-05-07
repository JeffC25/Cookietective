Copyright Timothy Borunov 2023 timobohr@bu.edu

The whois_api folder contains the code necessary for the analysis of packets obtained using the webcrawler. By specifying the
database in the url_parser.py, you can run the parser using:

python3 url_parser.py

Running the parser will initiate the analysis of the database, matching originalURL, CNAMEAlias, and DomainName from packets
using whois API first, and url parser second, before parsing through the cookies if the domains do not match. Output gives
the number of cookies scanned, how many were third party, and how many are potentially vulnerable due to CNAME cloaking
of third party domains.
