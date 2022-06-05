# Spellcheck microservice
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/xfenix/spellcheck-microservice?label=version)](https://github.com/xfenix/spellcheck-microservice/releases)
[![Docker Pulls](https://img.shields.io/docker/pulls/xfenix/spellcheck-microservice)](https://hub.docker.com/r/xfenix/spellcheck-microservice)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/297c021d5a464b9fafa410b509286507)](https://www.codacy.com/gh/xfenix/spellcheck-microservice/dashboard?utm_source=github.com&utm_medium=referral&utm_content=xfenix/spellcheck-microservice&utm_campaign=Badge_Coverage)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![Imports: isort](https://img.shields.io/badge/imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)

This is a microservice designed to check the spelling of words. Based on [pyspellcheker](https://pypi.org/project/pyspellchecker/). Exposes a REST API.

## Quickstart
* `docker run -t xfenix/spellcheck-microservice:latest -p 10113:10113`
* open http://localhost:10113/docs/ for more information about REST API
* main REST endpoint you will be needed is http://localhost:10113/api/check/

## Development quickstart
* Clone this repo
* `poetry install`
* `poetry shell`
* And `make` will run local development server

Please check [./Makefile](./Makefile) for more details
