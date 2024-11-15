#!/bin/sh
set -e

# Run custom management command
echo "Running custom management command..."
echo $PWD
poetry lock --no-update
poetry install
mkdir /app/src/fileshare/database/alembic/versions
poetry run alembic revision --autogenerate -m "Model init"
poetry run alembic upgrade head
# Run the WSGI server
echo "Starting ASGI server..."
exec "$@"