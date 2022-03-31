#!/bin/env bash

opt_container="server"
opt_host="server"
opt_port=12345

VALID_ARGS=$(getopt -o c:h:p: --long container:,host:,port:,help -- "$@")
if [[ $? -ne 0 ]]; then
	exit 1
fi

eval set -- "$VALID_ARGS"
while [ : ]; do
	case "$1" in
	-c | --container)
		opt_container=$2
		shift 2
		;;
	-h | --host)
		opt_host=$2
		shift 2
		;;
	-p | --port)
		opt_port=$2
		shift 2
		;;
	--help)
		echo "Usage: ./test_server.sh [--container=$opt_container] [--host=$opt_host] [--port=$opt_port]"
		exit 0
		;;
	--)
		shift
		break
		;;
	*)
		echo "Unrecognized parameter: $1"
		exit 1
		;;
	esac
done

TESTSTR="Hello, server, this is a test string!"

RESULT=$(docker run --rm -i --network container:$opt_container busybox:latest sh -c "echo $TESTSTR | nc $opt_host $opt_port | awk -v RS= -F': ' '{print \$NF}'")
if [ "$RESULT" = "$TESTSTR" ]; then
	echo "Server is up and returning expected value!"
else
	echo "Output was not the expected"
fi
