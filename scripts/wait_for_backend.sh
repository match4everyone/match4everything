#!/usr/bin/env bash

echo -n "Waiting for backend to be running"
while [ -z "$(docker-compose -f docker-compose.yml -f docker-compose.prod.yml ps --services --filter "status=running"|grep backend)" ]; do
    echo -n .
    sleep .2
done
echo " OK"

WAIT_FOR="\[INFO\] Listening at"
counter=0
echo -n "Wait for '$WAIT_FOR' in backend log"
while [ -z "$(docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs backend|grep "${WAIT_FOR}")" ]; do
    echo -n .
    counter=$((counter + 1))

    if [[ $counter -ge 60 ]]; then
	    echo "Error on check availability, dumping logs..."
	    docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs
	    exit 1
    fi

    sleep 1
done
echo " Found"
exit 0
