#!/bin/bash

ids=$(docker ps -f "status=exited" -q)

# Iterate through all container id's
for id in $ids; do
    # Copy the database.db from the container into the current directory
    docker cp $id:/home/Cookietective/database.db $id.db

    # Copy the data from the database into the current database
    sqlite3 database.db """ATTACH DATABASE '$id.db' AS results;
    INSERT or IGNORE INTO CNAMEpackets SELECT * FROM results.CNAMEpackets;
    INSERT or IGNORE INTO ip SELECT * FROM results.ip;
    INSERT or IGNORE INTO cookie SELECT * FROM results.cookie;
    """

    rm $id.db
done
