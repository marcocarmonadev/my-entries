FROM mcr.microsoft.com/devcontainers/python:3.12
USER vscode
ENV ENVIRONMENT=development \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN curl -sSL https://install.python-poetry.org | python3 -