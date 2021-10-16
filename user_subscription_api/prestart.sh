#! /usr/bin/env bash

export PYTHONPATH=$(readlink -f ./)
alembic upgrade head
