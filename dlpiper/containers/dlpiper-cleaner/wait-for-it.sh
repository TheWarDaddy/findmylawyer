#!/bin/bash
# wait-for-postgres.sh

set -e

host="$1"

shift
cmd="$@"

until PGPASSWORD="tvzygcdiu" psql -h "$host" -U "postgres" -c 'SELECT name, COUNT(name) FROM names GROUP BY name HAVING COUNT (name) > 1;'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command" && PGPASSWORD="tvzygcdiu" psql -h "$host" -U "postgres" -f names_cleaner.sql && python3 ./cleaner.py
exec $cmd
