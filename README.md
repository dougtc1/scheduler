# Copyright (c) 2020 Douglas Enrique Torres Cuevas 

# Appointments (python 3.7 - Django 3.1.2)
Small appointment management app

## How to run the project?
To run a project you need to have the following prerequisites:
    - Docker engine (CE) version 19.03 or later installed for your OS.
    - docker-compose version 1.26  or later installed 
    - Source code
    - Docker configured to be used without sudo (Optional, in case your user does not belong to Docker group, you will need to add `sudo` in front of every `docker` command)
    - Postman version v7.34.0 (Optional, only needed to import collection and environment)

After cloning the project repository (or unzipping the source code), you should see a folder called `scheduler` and this README.md.

Enter django's project root folder:
```
$ cd scheduler
```

Run `docker-compose` to build the images and execute the containers:
```
$ docker-compose up -d --build
```

This will execute 2 containers, that can be seen executing the following command:
```
$ docker ps
```

It should output something similar to:
```
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
9dfd1ea35906        scheduler_web       "bash -c 'python man…"   About an hour ago   Up 5 seconds        0.0.0.0:8000->8000/tcp   scheduler_web_1
73b2f2e818c1        postgres            "docker-entrypoint.s…"   About an hour ago   Up 5 seconds        5432/tcp                 scheduler_db_1
```

## Working endpoints
Here is the list of working endpoints in this solution:
* GET -> http://127.0.0.1:8000/swagger/ (OpenAPI documentation)
* GET -> http://127.0.0.1:8000/appointment/ (List all available appointments)
* POST -> http://127.0.0.1:8000/appointment/ (Create new appointment)
* GET -> http://127.0.0.1:8000/appointment/{id}/ (Get a specific appointment)
* PUT -> http://127.0.0.1:8000/appointment/{id}/ (Update a specific appointment)
* DELETE -> http://127.0.0.1:8000/appointment/{id}/ (Delete a specific appointment)

## Django commands
There are two Django commands to do specific useful tasks:
* initializedb -> Command to initialize starting data for the project
* listappointments -> Command to list all appointments

You can run a Django command by executing this in the root folder of the Django project:
```
$ python manage.py <command>
```

To create a new appointment, here it is an example body request to do it:
```
{
    "subject": "test appointment",
    "start_time": "2020-11-05 01:00:00",
    "end_time": "2020-11-05 03:00:00",
    "location": {
        "name": "Leahton"
    },
    "participants": [
        {
            "username":"rickbrown"
        },
        {
            "username": "kiddcourtney"
        }
    ]
}
```

## Notes

* If you have a PostgreSQL database server or another webserver running in your computer, there can be a conflict with the ports in the host machine (5432 or 8000).
    To solve this, make sure you stop the running services first before executing `docker-compose`

* The `docker-compose.yml` automatically runs a Django command to initialize the database with some data. If you try to run `docker-compose up` command more than one time, it will raise an exception due to the fact that this data already exists on the database. You would need to delete the volume named `scheduler_dbdata` with:
```
$ docker volume rm scheduler_dbdata
```

* Together in the repository, you can find two files that can pe opened with Postman:
    1. appointments.postman_collection.json (Postman collection with requests)
    2. appointment_local.postman_environment.json (Postman environment with variables used in collection)

    Please note that the `id` value in `appointment_local.postman_environment.json` must be updated by running the request named `list_appointments`. This is done through the `Tests` tab in Postman.

* Project monitoring is done with `Sentry`
* Structured logging is accomplished with `django-structlog`
