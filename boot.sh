#!/bin/bash
source venv/bin/activate
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    else
        flask db stamp head
        flask db migrate -m 'pstg'
        flask db upgrade
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done
exec gunicorn -w 3 -b 0.0.0.0:5005 --access-logfile - --error-logfile - testnet:app
