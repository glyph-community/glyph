#!/bin/bash
set -e

# Dockerfile ENTRYPOINT script that will wait for database connections to be live

if [[ ${DATABASE_TYPE:=sqlite} == "mysql" ]]; then
    /opt/manage.py check_db
fi

/opt/manage.py collectstatic --no-input

# Allows for a wait period before spinning up
sleep ${PRE_RUN_SLEEP:=0}

exec "$@"