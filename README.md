# Spellcheck microservice
![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/xfenix/spellcheck-microservice?label=version)
![Docker Pulls](https://img.shields.io/docker/pulls/xfenix/spellcheck-microservice)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/297c021d5a464b9fafa410b509286507)](https://www.codacy.com/gh/xfenix/spellcheck-microservice/dashboard?utm_source=github.com&utm_medium=referral&utm_content=xfenix/spellcheck-microservice&utm_campaign=Badge_Coverage)
<br>
This is a microservice designed to check the spelling of words. Based on [pyspellcheker](https://pypi.org/project/pyspellchecker/). Exposes a REST API.

## Quickstart
* `docker run -t xfenix/spellcheck-microservice:latest -p 10113:10113`
* open <a href="http://localhost:10113/docs/" target="_blank">http://localhost:10113/docs/</a> for more information about REST API
* main REST endpoint you will be needed is <a href="http://localhost:10113/api/check/" target="_blank">http://localhost:10113/api/check/</a>

## Development quickstart
* Clone this repo
* `poetry install`
* `poetry shell`
* And `make` will run local development server

Please check [./Makefile](./Makefile) for more details
