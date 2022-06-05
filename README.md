# Spellcheck microservice
![Docker Pulls](https://img.shields.io/docker/pulls/xfenix/xfenix-ru-front-v2)<br>
This is a microservice designed to check the spelling of words. Based on [pyspellcheker](https://pypi.org/project/pyspellchecker/). Exposes a REST API.

## Quickstart
`docker run -t xfenix/spellcheck-microservice:latest -p 10113:10113`

## Development quickstart
* Clone this repo
* `poetry install`
* `poetry shell`
* And `make` will run local development server

Please check [./Makefile](./Makefile) for more details
