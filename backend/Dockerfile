FROM python:3.12-slim

EXPOSE $PORT

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip3 install poetry==1.8.4


WORKDIR /app
COPY . /app

ENV PYTHONPATH=/app/src/

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
RUN chmod +x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

EXPOSE $PORT

CMD poetry run uvicorn src.fileshare.main:app --host 0.0.0.0 --port $PORT