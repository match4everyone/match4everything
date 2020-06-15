#!/usr/bin/env bash
while ! [ $(docker-compose -f docker-compose.yml -f docker-compose.prod.yml ps | grep backend | wc -l) -gt 0 ]; do
    sleep 1
done
