# Spellcheck microservice
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/xfenix/spellcheck-microservice?label=version)](https://github.com/xfenix/spellcheck-microservice/releases)
[![Docker Pulls](https://img.shields.io/docker/pulls/xfenix/spellcheck-microservice)](https://hub.docker.com/r/xfenix/spellcheck-microservice)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/297c021d5a464b9fafa410b509286507)](https://www.codacy.com/gh/xfenix/spellcheck-microservice/dashboard?utm_source=github.com&utm_medium=referral&utm_content=xfenix/spellcheck-microservice&utm_campaign=Badge_Coverage)
<a href="https://github.com/psf/black" target="_blank"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![Imports: isort](https://img.shields.io/badge/imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)
<a href="http://mypy-lang.org/" target="_blank"><img src="https://img.shields.io/badge/mypy-checked-1F5082.svg" alt="Mypy checked"></a>

This is a microservice designed to check the spelling of words. Based on [pyenchant](https://github.com/pyenchant/pyenchant). Exposes a REST API.<br>
Current available languages are: ru_RU, en_US, es_ES, fr_FR, de_DE, pt_PT.<br>
It runs blazingly fast due to the use of pychant in its kernel and LRU cache usage.<br>
Also it supports feature called «user dictionaries» — user can add his own word-exceptions to personal dictionary.

## Quickstart
* `docker run -p 10113:10113 -t --mount source=spellcheck-dicts,target=/data/ xfenix/spellcheck-microservice:2.1.2`
* check http://localhost:10113/docs/ for full REST documentation
* main REST endpoint you will be needed is http://localhost:10113/api/check/ (this will be available without authorization)

## Configuration
### Config options
You can change config of the service by changing the environment variables. Here is a list of them:
* `SPELLCHECK_SENTRY_DSN` Sentry DSN for integration. Empty field disables integration. Default is `''`
* `SPELLCHECK_API_KEY` define api key for users dictionaries mostly. Please, provide, if you want to enable user dictionaries API. Default is `''`
* `SPELLCHECK_ENABLE_CORS` enable CORS for all endpoints. In docker container this option is disabled. Default is `True`
* `SPELLCHECK_STRUCTURED_LOGGING` enables structured (json) logging. Default is `True`
* `SPELLCHECK_WORKERS` define application server workers count. If you plan to use k8s and only scale with replica sets, you might want to reduce this value to `1`. Default is `8`, allowed values from `1`to `300`
* `SPELLCHECK_PORT` binding port. Default is `10113`, allowed values from `1024`to `65535`
* `SPELLCHECK_CACHE_SIZE` define LRU cache size for misspelled word/suggestions cache. Any value less than `1` makes the cache size unlimited, so be careful with this option. Default is `10000`
* `SPELLCHECK_API_PREFIX` define all API's URL prefix. Default is `/api/`
* `SPELLCHECK_DOCS_URL` define documentation (swagger) URL prefix. Default is `/docs/`
* `SPELLCHECK_MAX_SUGGESTIONS` defines how many maximum suggestions for each word will be available. `None` means unlimitied. Default is `None`, allowed values from `1`
* `SPELLCHECK_DICTIONARIES_PATH` define directory where user dicts is stored. This is inner directory in the docker image, please map it to volume as it shown in the quickstart part of this readme. Default is `/data`
* `SPELLCHECK_DICTIONARIES_STORAGE_PROVIDER` define wich engine will store user dictionaries. Default is `file`
* `SPELLCHECK_DICTIONARIES_DISABLED` switches off user dictionaries API no matter what. Default is `False`
* `SPELLCHECK_USERNAME_MIN_LENGTH` minimum length of username. Default is `3`
* `SPELLCHECK_USERNAME_MAX_LENGTH` maximum length of username. Default is `60`

### Deployment
Note: all docker & docker-compose variants use named volumes to store user dictionaries.
#### Plain docker
`docker run  -p 10113:10113 -t --mount source=spellcheck-dicts,target=/data/ xfenix/spellcheck-microservice:2.1.2`
#### Docker-compose
* Save this example configuration as `docker-compose.yml`:
```yml
version: "3.9"
services:
    spellcheck:
        image: xfenix/spellcheck-microservice:2.1.2
        ports:
        - "10113:10113"
        volumes:
        - spellcheck-dicts:/data/

volumes:
    spellcheck-dicts:
```
* Then run `docker-compose up`

## Changelog
You cand find it here https://github.com/xfenix/spellcheck-microservice/releases

## Development
### Quickstart
* Clone this repo
* For MacOS X `brew install enchant`
* `poetry install`
* `poetry shell`
* Run `touch .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit`
* Paste following contents in file `.git/hooks/pre-commit`:
    ```sh
    poetry run make update-readme
    git add README.md
    ```
* Execute `make` command to run local development server

### Notes
Default api-key for local development is `debug` (you will need this to work with user dictionaries API).

Please check [./Makefile](./Makefile) for more details

### Troubleshooting
For MacOS X on Apple Silicon add `PYENCHANT_LIBRARY_PATH=/opt/homebrew/lib/libenchant-2.dylib` to your `.zprofile`
