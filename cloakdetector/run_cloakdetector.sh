#!/bin/bash
while read url; do
    python3 cloakdetector.py $url ../compiledDatabase.db
done < sample_urls.txt

