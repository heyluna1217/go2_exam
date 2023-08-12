#!/bin/bash

set -e


run-app makemigrations orders_api
run-app migrate orders_api

run-app runserver "0.0.0.0:8000"