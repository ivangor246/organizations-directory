#!/bin/sh

until nc -z $DB_HOST $DB_PORT; do
    sleep 1
done

export PYTHONPATH=/project/src
poetry run alembic upgrade head

if [ -z "$FOR" ]; then
    pytest tests/
else
    pytest tests/$FOR/
fi
