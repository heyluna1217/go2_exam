#!/bin/bash

set -e

python -m celery -A orders_api worker -l info