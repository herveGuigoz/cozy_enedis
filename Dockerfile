#syntax=docker/dockerfile:1.4

# Versions
FROM python:3.11-slim-buster as python_upstream
FROM bitnami/keycloak:22-debian-11 AS keycloak_upstream

# ---------------------------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------------------------
FROM python_upstream as builder

WORKDIR /tmp
 
RUN pip install poetry
 
COPY ./pyproject.toml ./poetry.lock* /tmp/
 
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# ---------------------------------------------------------------------------------------------
# Dev
# ---------------------------------------------------------------------------------------------
FROM python_upstream as dev
 
WORKDIR /code

RUN pip install psycopg2-binary

COPY --from=builder /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]

# ---------------------------------------------------------------------------------------------
# Caddy
# ---------------------------------------------------------------------------------------------
FROM caddy:builder AS app_caddy_builder

RUN xcaddy build

FROM caddy:latest AS app_caddy

WORKDIR /srv/app

COPY --from=app_caddy_builder --link /usr/bin/caddy /usr/bin/caddy
COPY --link docker/caddy/Caddyfile /etc/caddy/Caddyfile
