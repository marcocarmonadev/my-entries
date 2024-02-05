FROM python:3.12-alpine as builder

COPY /source/requirements/ /tmp/source/requirements/

RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir=/tmp/wheels --requirement=/tmp/source/requirements/dev.txt

FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    TZ=America/Mexico_City

WORKDIR /workspaces/my-api

COPY --from=builder /tmp/wheels /tmp/wheels

RUN apk update && \
    apk upgrade && \
    apk add git && \
    pip install --upgrade pip && \
    pip install --no-cache --no-cache-dir --upgrade /tmp/wheels/*

COPY . /workspaces/my-api/

CMD [ "uvicorn", "source.app.main:api", "--port", "8001", "--loop", "uvloop", "--use-colors", "--reload" ]