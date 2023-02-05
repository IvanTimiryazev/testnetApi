#!/bin/bash
sleep 10
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done
exec gunicorn -w 3 -b 0.0.0.0:5005 --timeout 600 --access-logfile - --error-logfile - testnet:app
