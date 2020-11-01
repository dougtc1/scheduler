# Copyright (c) 2020 Douglas Enrique Torres Cuevas 
# IN DEVELOPMENT

# appointments
Small appointment management app

To run a project you need to have the following prerequisites:
    - Docker engine (CE) version 19.03 or later installed for your OS.
    - docker-compose version 1.26  or later installed 
    - Source code

After cloning the project repository (or unzipping the source code), enter django's project root folder:
```
$ cd scheduler
```

Run `docker-compose` to build the images and execute the containers:
```
$ docker-compose up -d
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

Currently, the only working routes are the Swagger UI, list appointments and create appointment.

## Note

If you have a PostgreSQL database server or another webserver running in your computer, there can be a conflict with the ports in the host machine (5432 or 8000).

To solve this, make sure you stop the running services first before executing `docker-compose`

## To Do
* Create volume for postgresql DB
* Create commands to initialize DB and execute list endpoint
* Create tests (pytest, bamboo, etc)