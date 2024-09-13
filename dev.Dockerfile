FROM python:3.12

# Install required system dependencies
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential libpq-dev libsasl2-dev libldap2-dev libssl-dev

COPY pyproject.toml /api/

WORKDIR /api
RUN pip install poetry
RUN poetry install --no-root --no-interaction --no-ansi
