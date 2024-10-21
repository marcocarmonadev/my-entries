FROM python:3.12-slim
ENV UV_NO_CACHE=1 \
    UV_COMPILE_BYTECODE=1
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt update \
    && apt upgrade -y
RUN user_group_name="nonroot" && \
    gid=1000 && \
    addgroup --system --gid "$gid" "$user_group_name" && \
    adduser --system --no-create-home --uid "$gid" --ingroup "$user_group_name" "$user_group_name"
USER nonroot
WORKDIR /app/
RUN --mount=type=bind,from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    --mount=type=bind,source=uv.lock,target=/app/uv.lock \
    --mount=type=bind,source=pyproject.toml,target=/app/pyproject.toml \
    uv sync --frozen --no-dev --no-install-project
COPY --chown=nonroot:nonroot source/ source/
ENTRYPOINT [ ".venv/bin/python", "-m" ]
CMD [ "source" ]