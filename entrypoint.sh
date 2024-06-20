#!/bin/sh
.venv/bin/python .venv/bin/alembic upgrade head
.venv/bin/python source/main.py