# go2_exam
Repository containing the source code for the go2 practical examination

# Running the application
This application is a bundle of services orchestrated through docker compose.

Building the docker compose images
> docker compose --file ./docker/docker-compose-0.yml build

Running the app
> docker compose --file ./docker/docker-compose-0.yml up

# Debugging
A dev docker-compose file is provided which exposes the services outside of the created docker network. This allows for connecting to each service externally for debugging and testing.

Running the app in dev mode
> docker compose --file ./docker/docker-compose-0.yml --file docker-compose-1-dev.yml up

# Running locally
To run locally, the packages should be installed using [Poetry](https://python-poetry.org/):

> poetry env use 3.10  # Use Python 3.10
> poetry install  # Installs every package (including dev packages)
> poetry shell  # Activate the created virtual environment

The external services should be created either through docker compose:
> docker compose --file ./docker/docker-compose-0.yml --file docker-compose-1-dev.yml up redis db smtp celery

Or by manually spinning up the containers

We can then run the db migrations:
> python orders_api/manage.py makemigrations orders_api
> python orders_api/manage.py migrate orders_api

And start the server
> python orders_api/manage.py runserver

# Notes
There are implementations that were deliberately skipped in the interest of time, namely:
- Automated tests such as unit/integration tests as well as explicit static code analysis
- Django permissions
- Running services as rootless containers
- Persisting Orders and Customers in the DB
- Input validation for Orders
- De-couple Celery from Django (or use another system)