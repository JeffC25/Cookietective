from mitmproxy import http
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import sql.sql_func as sql

# Response function that is used whenever mitmproxy encounters an https response message
def response(flow: http.HTTPFlow) -> None:
    # Check if the response has Set-Cookie headers
    if ("set-cookie" in flow.response.headers):
        
        # Get the Set-Cookie headers and extract the cookie values
        set_cookie_headers = flow.response.headers.get_all("set-cookie")

        # Get the source domain and IP address
        src_domain = flow.request.pretty_host
        src_ip = flow.server_conn.ip_address[0]
        # Parse through each Set-Cookie header found in the HTTPS packet
        for set_cookie_header in set_cookie_headers:
            cookies = set_cookie_header.split(";")
            # Secure = False
            # httpOnly = False
            domain = ""

            # Parse through each value in the Set-Cookie header and write values to file
            for cookie in cookies:
                # Check if any of the current header values are secure, httponly, or domain attributes
                if (cookie):
                    # if (cookie == " Secure"):
                    #     Secure = True
                    # if (cookie == " HttpOnly"):
                    #     httpOnly = True
                    if ("domain=" in cookie):
                        domain = cookie[8:]
                
                sql.insertCookieEntry(src_domain, src_ip, domain)