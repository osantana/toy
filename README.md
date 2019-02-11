# HelloFresh Recipes API

Recipes API allows you to manage a collection of recipes and rate it.

## Requirements

To run HelloFresh Recipes API you need to install:

 * [docker-compose](https://docs.docker.com/compose/)
 * [git](https://git-scm.com)


## Running

Clone the project repository:

```shell
git clone git@github.com:hellofreshdevtests/osantana-api-test.git
```

Then select the `dev` branch on repository:

```shell
cd osantana-api-test
git checkout dev
```

Build the images and start the containers:

```shell
docker-compose build
docker-compose up
```


## Creating Database and Credentials

To use some endpoints of the API, you must create a user with its credentials on
the database.

To do this, you must run `initdb` and `adduser` management command at API
container using `docker.env` configuration file (copy it to `.env` file).

```shell
docker-compose exec api bash
[ -f .env ] || cp -f docker.env .env
python -m recipes initdb
python -m recipes adduser --email test@hellofresh.com --password=SEKRET
exit
```


## Accessing

Recipes API server is listening at `http://localhost:8080`.
You can see full documentation of the API at
[Postman Workspace](https://documenter.getpostman.com/view/716192/RztprTuH).
