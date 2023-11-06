# API for learning hebrew words

This is an example of an api application for learning Hebrew words.

Microservice architecture is used to further expand the capabilities of the project.

There are 2 main API services available to you:

Api-service on the FLASK framework

    Migrations to database;
    CRUD methods for managing words;
    User registration and authorisation methods;
    Method for populate database with words and their translation.

Api-service on the SANIC framework

    Method to obtaining a random word and 4 possible variants of its translation;
    Method to check the selected word translation option.

## Install

1. Create environment:

```
cp .env.example .env
```

2. Up docker containers (python and postgres):

```
docker-compose up -d
```

3. Run migrations and seed database with default user and words.

```
./flask/run.sh
```

## Result

Your application will be available on: http://localhost:5001/

Swagger: http://localhost:5001/swagger/

Flask API: http://localhost:5001/api/

Sanic API: http://localhost:5002/api/