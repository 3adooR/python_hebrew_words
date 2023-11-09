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

Telegram Bot

    Simple telegram bot which show you word and variants of translation.
    You can choose translation and see correct it or not.

## Install

1. Add your own Telegram bot with @BotFather, and get your token for it:

```
https://t.me/BotFather
```

2. Put token into .env file:

```
TGBOT_TOKEN=******
```

3. Up docker containers:

```
docker-compose up -d
```

4. Run migrations and seed database with default user and words.

```
./flask/run.sh
```

## Result

Your application will be available on: http://localhost:5001/

Swagger: http://localhost:5001/swagger/

Flask API: http://localhost:5001/api/

Sanic API: http://localhost:5002/api/