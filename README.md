# api-testing-framework

This is a simple API testing framework, started on September 9, a nerdy way to celebrate Tester's Day.

## Setup

- Ensure you have pipenv available.
- Once you have cloned this repo go into the project root directory that has the `Pipfile` with definitions of all required dependencies. 
- Execute `pipenv shell` to activate the virtualenv in your terminal
- Execute `pipenv install` to install all dependencies

## Running tests
- Ensure you have `people-api` app running
- Execute `pytest .` to run all tests

> On a windows machine, you may want to replace the host as `127.0.0.1` in the BASE_URL
