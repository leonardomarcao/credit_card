# Card Vault

## Docker Quickstart

This app can be run completely using **Docker** and **`docker-compose`**. Using Docker is recommended, as it guarantees the application is run using compatible versions of Python.

To run the app using Docker (detached mode), run the following command:

```bash
docker-compose up card-vault-app -d
```



Go to http://localhost:8080 to view the app.

Go to http://localhost:8080/docs to view the API documentation.

## Running locally

Run the following commands to bootstrap your environment if you wish to run the application locally:

```bash
pip install -r requirements
flask db upgrade
flask run
```

Go to http://localhost:8080 to view the app.

Go to http://localhost:8080/docs to view the API documentation.

## Running Tests

To ensure the integrity of the application, you can run a suite of tests that have been written using pytest. Whether you are running the application locally or using Docker, you can use the following commands to run the tests:

### Running tests locally

To run the tests locally, navigate to the root directory of your application and run:

```bash
pytest
```

This will discover and run all the test cases that exist in your tests directory.

### Running tests using Docker

If you are running the application in Docker, you can run the tests using the following command:


```bash
docker-compose run card-vault-app pytest
```

This command creates a new service that runs the pytest command in a new container.

When the tests have completed, you will see a summary in the terminal. If all the tests pass, then everything is working as expected. If any tests fail, you should see error messages that explain what has gone wrong.

## Coverage Report

If you want to generate a coverage report, you can do so with the following commands:

### Running coverage locally

```bash
pytest --cov=card_vault
```

### Running coverage using Docker

```bash

docker-compose run card-vault-app pytest --cov=card_vault
```
