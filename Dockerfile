FROM python:3.12-alpine as base
RUN --mount=type=cache,target=/var/cache/apk \
    apk update \
    && apk upgrade --available


FROM base as builder
ENV POETRY_HOME=/etc/poetry \
    POETRY_VIRTUALENVS_IN_PROJECT=1
RUN --mount=type=cache,target=/var/cache/apk \
    apk add curl
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && cd /usr/local/bin \
    && ln -s /etc/poetry/bin/poetry
WORKDIR /tmp/
RUN --mount=type=bind,source=poetry.lock,target=/tmp/poetry.lock \
    --mount=type=bind,source=pyproject.toml,target=/tmp/pyproject.toml \
    poetry install --only main


FROM base as runner
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT=production
RUN user_group_name="python" && \
    gid=1000 && \
    addgroup -S --gid "$gid" "$user_group_name" && \
    adduser -S -H -u "$gid" --ingroup "$user_group_name" "$user_group_name"
USER python
WORKDIR /code
COPY --chown=python:python --from=builder /tmp/.venv/ .venv/
COPY --chown=python:python source/ source/
COPY --chown=python:python alembic/ alembic/
COPY --chown=python:python alembic.ini alembic.ini
COPY --chown=python:python entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]