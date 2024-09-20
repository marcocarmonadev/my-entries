FROM python:3.12-alpine AS base
RUN --mount=type=cache,target=/var/cache/apk \
    apk update \
    && apk upgrade --available \
    && apk add curl


FROM base AS builder
ENV POETRY_HOME=/etc/poetry \
    POETRY_VIRTUALENVS_IN_PROJECT=1
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && cd /usr/local/bin \
    && ln -s /etc/poetry/bin/poetry
WORKDIR /tmp/
RUN --mount=type=bind,source=poetry.lock,target=/tmp/poetry.lock \
    --mount=type=bind,source=pyproject.toml,target=/tmp/pyproject.toml \
    poetry install --only main


FROM base AS runner
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT=production
RUN user_group_name="gamma" && \
    gid=1000 && \
    addgroup --system --gid "$gid" "$user_group_name" && \
    adduser --system --no-create-home --uid "$gid" --ingroup "$user_group_name" "$user_group_name"
USER gamma
WORKDIR /workdir
COPY --chown=gamma:gamma --from=builder /tmp/.venv/ .venv/
COPY --chown=gamma:gamma source/ source/
COPY --chown=gamma:gamma alembic.ini alembic.ini
ENTRYPOINT [ ".venv/bin/python", "-m" ]
CMD [ "source" ]
