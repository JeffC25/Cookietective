from mitmproxy import http
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import sql.sql_func as sql

from mitmproxy.options import Options
from mitmproxy.tools.dump import DumpMaster
import asyncio

# Addon class to be used for mitmproxy (parses traffic for Set-Cookie and stores settings in database.db)
class Addon(object):
    # Response function that is used whenever mitmproxy encounters an https response message
    def response(self, flow):
        # Check if the response has Set-Cookie headers
        if ("set-cookie" in flow.response.headers):
            
            # Get the Set-Cookie headers and extract the cookie values
            set_cookie_headers = flow.response.headers.get_all("set-cookie")

            # Get the source domain and IP address
            src_domain = flow.request.pretty_host
            src_ip = flow.server_conn.peername[0]
            # Parse through each Set-Cookie header found in the HTTPS packet
            for set_cookie_header in set_cookie_headers:
                cookies = set_cookie_header.split(";")
                Secure = False
                httpOnly = False
                domain = ""

                # Parse through each value in the Set-Cookie header and write values to file
                for cookie in cookies:
                    # Check if any of the current header values are secure, httponly, or domain attributes
                    if (cookie):
                        if (cookie == " Secure"):
                            Secure = True
                        if (cookie == " HttpOnly"):
                            httpOnly = True
                        if ("domain=" in cookie):
                            domain = cookie[8:]
                    
                    sql.insertCookieEntry(src_domain, src_ip, domain, httpOnly, Secure)

# Main function for mitmproxy that specifies options and runs mitmproxy
async def run_proxy(port):
    
    settings = Options(
        listen_host='localhost',
        listen_port=port
    )
    m = DumpMaster(settings, with_termlog=False, with_dumper=False)
    m.addons.add(Addon())

    # Run the proxy until it times out, then shutdown the proxy
    try:
        await asyncio.wait_for(m.run(), timeout=20)
    except asyncio.TimeoutError:
        m.shutdown()

# Function that runs the proxy with the command line-specified port
def run():

    # Error checking if a port was given
    if (len(sys.argv) < 2):
        print("Error: No port specified")
        exit(0)

    port = int(sys.argv[1])

    # Run the function asynchronously
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_proxy(port))
    finally:
        loop.close()

run()