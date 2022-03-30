#!/usr/bin/env sh

# https://stackoverflow.com/a/64799824
# get the container IP
IP=$(ifconfig eth0 | grep 'inet ' | awk '{print $2}' | cut -d":" -f2)

# extract the replica number from the same PTR entry
INDEX=$(nslookup $IP | awk '/name = / {print $4}' | sed 's/.*_\([0-9]*\)\..*/\1/')

echo $INDEX

export CLI_ID=$INDEX

/client
