import scapy.all as scapy
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import sql.sql_func as sql

listCNAMES = []

# TO DO: 
# - 

class CNAME_packet():
    def __init__(self, packet, A, ip):
        self.packet = packet
        self.has_A = A
        self.domain = packet.rrname
        self.cname = packet.rdata
        if len(ip) < 1:
            self.ip = None
        else:
            self.ip = ip
        

# Function to be run everytime sniffer encounters a DNS packet
def parseDNS(packet):
    # Check if packet contains Transport layer UDP and Application layer DNS
    if (packet and packet.haslayer('DNS') and packet.haslayer('UDP')):
        udp = packet['UDP']
        dns = packet['DNS']

        has_CNAME = False
        has_Atype = False
        src_ip = packet['IP'].src
        
        CNAME_index = 0
        ip = []

        # Check if packet is DNS response (source binded to DNS port)
        if (int(udp.sport) == 53):
            # Iterate through all DNS resource records
            for i in range(dns.ancount):
                dnsrr = dns.an[i]
                type_field = dnsrr.get_field('type')

                # If DNS entry is of type CNAME, store it in listCNAMES (There can only be 1 CNAME entry per packet)
                if (type_field.i2repr(dnsrr, dnsrr.type) == 'CNAME'):
                    CNAME_index = i
                    has_CNAME = True
                
                if (type_field.i2repr(dnsrr, dnsrr.type) == 'A'):
                    has_Atype = True
                    ip.append(dnsrr.rdata)
        
        # Insert CNAME packet information into SQLite database
        if (has_CNAME):
            domain = dns.an[CNAME_index].rrname
            alias = dns.an[CNAME_index].rdata

            # Insert into SQLite database
            sql.insertCNAMEpacketsEntry(domain, src_ip, alias, has_Atype)

            # Iterate through all of the stored ip addresses from A-type records and insert into SQLite if there are any
            for addr in ip:
                if addr is not None:
                    sql.insertIpEntry(domain, addr)
            
# Main function that executes the DNSscanner
def main(dns_port):
    # Listens to traffic for DNS traffic (udp port 53) for 15 seconds then prints summary
    scapy.sniff(filter="udp port " + dns_port, prn=parseDNS)

# Check which port to use to search for DNS traffic (53 by default unless specified otherwise)
if (len(sys.argv) > 1):
    dns_port = sys.argv[1]
else:
    dns_port = 53

# Run the scapy library to parse through DNS traffic on port dns_port
main(dns_port)