#!/bin/bash
python -m alembic upgrade head
python -m utils.fixtures.image_fixtures # Loads sample image data to db
./gunicorn_start