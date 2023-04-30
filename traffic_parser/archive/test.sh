#!/bin/bash

# Check that the HTTPS and UDP ports are given as inputs
if [[ $# < 2 ]]; then
    echo "URL bounds not specified: 'bash test.sh [begin index] [end index]'"
    exit
fi

URL_LIST_START=$1
URL_LIST_END=$2

HTTP_PORT=8080
UDP_PORT=53
ADDRESS=http://localhost:$HTTP_PORT/

# Set up the network settings based on the operating system
# Install the mitmproxy certificate

# Install certificate and set up proxies for Mac
if [[ "$OSTYPE" == "darwin"* ]]; then

    # Add in the mitmproxy certificate
    if [[ ! -f "mitmproxy-ca-cert.crt" ]]; then
        openssl x509 -in ~/.mitmproxy/mitmproxy-ca-cert.pem -out mitmproxy-ca-cert.crt
        sudo security add-trusted-cert -d -p ssl -p basic -k /Library/Keychains/System.keychain mitmproxy-ca-cert.crt
    fi

    networksetup -setwebproxy "Wi-Fi" localhost $HTTP_PORT
    networksetup -setsecurewebproxy "Wi-Fi" localhost $HTTP_PORT

# Install certificate and set up proxies for Linux
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then

    # Add in mitmproxy certificate for local user
    if [[ ! -f "mitmproxy-ca-cert.crt" ]]; then
        sudo cp ~/./mitmproxy-ca-cert.pem /usr/local/share/ca-certificates
        sudo update-ca-certificates
    fi

    export http_proxy=$ADDRESS
    export https_proxy=$ADDRESS

else
    echo "ERROR: Not a supported Operating System"
fi

# Code that runs the traffic scanners in the background
mitmdump -q --listen-port $HTTP_PORT -s traffic_parser/mitmproxy_script.py &
sleep 3
sudo python3 traffic_parser/dnsscan.py $UDP_PORT &
# python3 httpsscan.py &

# Run the crawler
python3 crawler/crawler.py sample_urls.txt $URL_LIST_START $URL_LIST_END

#End code cleanup: Remove the proxies and certificates
if [[ "$OSTYPE" == "darwin"* ]]; then
    # security delete-certificate -c "mitmproxy" /Library/Keychains/System.keychain
    networksetup -setwebproxystate "Wi-Fi" off
    networksetup -setsecurewebproxystate "Wi-Fi" off
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # trust anchor --remove mitmproxy-ca-cert.pem
    unset http_proxy
    unset https_proxy
fi
