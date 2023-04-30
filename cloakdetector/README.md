# Info
The purpose of the CloakDetector is to detect if a domain could be sharing first party cookies with
third parties by CNAME cloaking. It incorporates the checks specified in Approach 2:

• A domain name set in a Domain attribute does not have any A records.

• A domain name set in a Domain attribute has CNAME record(s).

• The domain name set in the above CNAME record is not a first-party domain name.

• The IP address of the domain name set in the above CNAME record is not an IP address of the input URL.


## Functions
#### sameOwner(url1, url2)
This function is used in the firstPartyCheck() function. It makes a guess as to whether or not two URLs
belong to the same owner by examining their strings and conducting a WHOIS lookup if a match isn't
detected in their strings.

#### hasAType(domainName, dbFile='../database.db')
This function queries the CNAMEpackets table in our database to check if the specified domain has
any A records.

#### hasCNAMErecord(domainName, dbFile='../database.db')
This function queries the CNAMEpackets table in our database to check if the specified domain has
CNAME records.

#### firstPartyCheck(domainName, dbFile='../database.db')
This function queries the CNAMEpackets table in our database to retrieve the CNAMEalias value of the
specified domain. It then checks to see if the two belong to the same owner using the previously
defined sameOwner() function.

#### IPcheck(domainName, dbFile='../database.db')
This function queries the CNAMEpackets table in our database to retrieve the CNAMEalias and originalURL
values of the specified domain. It retrieves the IP addresses of the two and checks if the IP address of 
the domain name set in the CNAME record is an IP address of the input URL.

### cloakDetector(domainName, dbFile='../database.db')
This is the primary CloakDetector function. It runs the input domain through hasAType(), hasCNAMErecord(),
firstPartyCheck(), and IPcheck() and, using the conditions specified in the Info section, determines if 
(1) first party cookies are likely being shared with third parties by CNAME cloaking, or
(0) first party cookies are likely NOT being shared with third parties by CNAME cloaking.

## Additional Functionality
CloakDetector can be imported as a package into other Python programs. Additionally, the cloakDetector() 
function can be run in the command line when executing cloakdetector.py in the following format:
```
python3 cloakdetector.py domainName [dbFile]
```
The result of cloakDetector() is output.
