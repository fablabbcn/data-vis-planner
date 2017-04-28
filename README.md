# datavizplatform-infrastructure
A docker compose for the Data Viz platform

-	**Based on the tutorial:** [Dockerize a Flask, Celery, and Redis Application with Docker Compose â€” Nick Janetakis](https://nickjanetakis.com/blog/dockerize-a-flask-celery-and-redis-application-with-docker-compose)
-	**With the next repository to consult:** https://github.com/nickjj/build-a-saas-app-with-flask
-	Flask uses, gunicorn as a server in deploy

Instructions
------------

Clone this repo with its submodules:

-	`git clone --recursive`


-	`docker-compose up`


-	Enter to **localhost:8000** --> flask-celery

-	Enter to **localhost:3000** --> Meteor-mongo