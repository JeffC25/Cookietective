# Cookietective: An Automated Scanner for CNAME Cloaking-based Cookie Leaking

Cookietective consists of three major components. The first is a data-gathering module consisting of a web crawler and two network traffic scanners, which takes in URLs to gather cookie and CNAME information from. The output is then sent to the second portion of this project, the analysis portion. Here, we look specifically at packets which contain a CNAME record to determine whether or not the packet is being sent from first-party to first-party or to a cloaked third party domain. The final portion of our project is an accuracy checker, which we use to attempt to see how many of the websites flagged by our analysis engine were known third party T/A services.

## Running Data-Gathering
1. Run `git clone https://github.com/Cybersecurity-Project-Group/Cookietective.git` 
2. Run `cd Cookietective`
3. Install Python dependencies with `install -r requirements.txt` 
4. Install SQLite3 with `apt-get install sqlite3`
5. Install [Docker](https://docs.docker.com/engine/install/)
6. Put desired domains into `sample_urls.txt` (currently has the 20,000 top values from Majestic Million).
7. Specify the number of containers, domains needed to scan, and offset into the URL list in `run_containers.sh` (Default: 8 containers, 3600 URLs, and offset of 0)
8. Run `bash run_containers.sh` to build and spin Containers and start scanning
9. After containers have exited, run `bash gather_data.sh` to extract the local databases from exited containers and merge into database.db - NOTE: this currently extracts information from ALL exited containers

## Running Analysis
1. Run `cd whois_api`
2. Run `python3 url_parser.py` to record findings into database.db

## CNAME Cloaking
The second method is called CNAME Cloaking, where third party servers are labeled as a subdomain of the first party server through the usage of a CNAME aliasing in the DNS server. CNAMEs unite resources used on a website under a single domain name by providing an alias that actually points to another domain. An identifying CNAME record is created to be part of a subdomain of a first party server, but instead of redirecting to an IP address in the domain, it redirects to a third party. So within the domain, a third party server is seen as if it is a first party subdomain. This can lead to leaking first-party cookies if it is paired with lax cookie settings where the Domain attribute automatically shares cookies with all domains of the ancestor-domain of the origin. Since cookies would be directly shared with all first-party subdomains, third party servers are able to receive whatever cookies the first party vendor specifies. This can create security vulnerabilities, as attackers can use these third party services to inject malicious code or steal user data.
Both of these methods are done with the direct intention of avoiding the built-in security features, and as such create incredibly vulnerable paths of attack since decorated links can be accessed relatively easily, and sharing through CNAME has no security measures tied to sharing with third parties, so the attacks which the built-in security measures attempt to prevent are no longer blocked in any way.

## Implementation

# Information Gathering
	
For the data-gathering phase of our project, we implemented a web crawler using the Selenium framework in Python. The crawler spawns a browser instance (Firefox 112.0.2) using the Mozilla Geckodriver. A list of URLs (obtained from the Majestic Million List) is inputted into the crawler, which iterates through each URL to use as a source node. For each source node, the Selenium driver sends a request and traverses any additional links located on the site (Selenium 2023). The traversal runs in a Breadth-First-Search algorithm and continues for 20 seconds per source node. 
	
While the webcrawler generates network traffic, we utilize an HTTPS traffic scanner implemented through mitmproxy (Cortesi 2023) and a DNS traffic scanner implemented through the Scapy (Creativecommons 2023) python library. The DNS traffic scanner uses a python script that we wrote to search for DNS packets with CNAME resource records. If the scanner runs into any such packets while receiving traffic generated by the webcrawler, it will store the CNAME aliasing information to be used during the analysis section (such as the domain, CNAME alias, and original URL being crawled through). Similarly, the HTTPS scanner searches for HTTPS response packets with Set-Cookie headers and, if it intercepts any, it stores the Set-Cookie information like the Domain attribute.

To scale up the information gathering process, we decided to utilize multiple containers at a time by building a Docker image consisting of the Selenium crawler, network scanners, and SQLite3 database in a Linux environment (Ubuntu 20.04), as seen in Figure 1. Next, we spun up 32 containers across 4 machines, each with distinct ports to separate their traffic from one another and distinct ranges to index into and divide up a list of 17,100 URLs. After every container has completed its crawling process, a Bash script is executed to export the local database inside each excited container and merge them into a central database.

# Analysis	
For the analysis portion of our project we had the greatest challenge determining the method by which we would label first and third party domains. Lists exist of known tracking and advertising services which we could use to match with potential third party domains we parse from the gathered packets. However, it is also possible for a first party different from the current domain to be cloaked and thus act as a third party even though it is not a tracking service. As such, there needed to be a way to check that each packet we gathered had an original URL which was part of the domain we were scanning.
	
There are many suggestions on the web of how to do this, whether it was through reverse DNS lookup of IPs or checking databases of known domain names. The issue is that none of these methods are completely reliable. We ended up settling with utilizing a combination of methods to increase the end accuracy of our analysis.

The first part of our method involved using Whois lookup in order to check if we could determine the organization that owned the original URL that we were scanning and the domain name that it was receiving cookies from. A Whois database record contains all of the contact information associated with the person, group, or company that registers a particular domain name. The American Registry for Internet numbers provides a REST(ful) API for Whois queries that we implemented in order to get this information. A query can be sent to their server with the URL of a website and it will respond with the entire Whois entry as text. This data is in a standardized format, so we created a function to parse out specifically the OrgName entry, which contains the name of the company that registered the domain name. This function is used to find the owner of each domain and then compare them. If they are the same, they are marked as first-party. If they are different or if the information is blank, the URL parser is used.

The second part of our analysis method utilized a url parser which simply picked apart the urls of the domain and original URL of the site we received a packet from in order to determine if the website belongs to that domain. This was done with a complicated regular expression, but due to the fixed nature of the algorithm this method is prone to more errors than the Whois checker and is therefore used as a secondary means when the Whois is unable to.

# Domain List Comparator

To evaluate our vulnerability analysis, we created the Comparator module. The Comparator module takes in the table outputted by the analysis portion as input, checks for the existence of each domain name in the Majestic Million and NoTracking lists, and outputs into the same table whether or not each aliased domain is in each of the domain lists. The Comparator was utilized in our evaluation program comparetest.py by querying the ‘findings’ table in our final SQLite database for the domain names which were obtained from the captured CNAME packets. These domain names were then passed through the Comparator to identify domain names present in either the Majestic Million or NoTracking lists. These results were then committed to the ‘findings’ table in the database.

It is important to note that subdomains present with each domain name entry were included as part of the check for inclusion in either the Majestic Million or NoTracking lists. For our purposes, this is important because, to give an example, ads.youtube.com is not the same as youtube.com. In other words, ads.youtube.com is one of the tracking/advertisement services included in the NoTracking list while youtube.com is one of the top sites listed in the Majestic Million. Therefore, it is important that the subdomains are included because, otherwise, ads.youtube.com would be indicated as being present in the Majestic Million when that is not actually the case. Similarly, ahfd79zx.amazon.com should not be indicated as being part of the Majestic Million because it is specifically amazon.com that is on the list, and that is crucial to our evaluation.

Look at individual folder README's for how to run each section.

