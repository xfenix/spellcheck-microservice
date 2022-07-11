# Spellcheck microservice
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/xfenix/spellcheck-microservice?label=version)](https://github.com/xfenix/spellcheck-microservice/releases)
[![Docker Pulls](https://img.shields.io/docker/pulls/xfenix/spellcheck-microservice)](https://hub.docker.com/r/xfenix/spellcheck-microservice)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/297c021d5a464b9fafa410b509286507)](https://www.codacy.com/gh/xfenix/spellcheck-microservice/dashboard?utm_source=github.com&utm_medium=referral&utm_content=xfenix/spellcheck-microservice&utm_campaign=Badge_Coverage)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![Imports: isort](https://img.shields.io/badge/imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)<br>
This is a microservice designed to check the spelling of words. Based on [pyenchant](https://github.com/pyenchant/pyenchant). Exposes a REST API.<br>
Current available languages are: ru_RU, en_US, es_ES, fr_FR, de_DE, pt_PT

## Quickstart
* `docker run  -p 10113:10113 -t --mount source=spellcheck-dicts,target=/data/ xfenix/spellcheck-microservice:latest`
* open http://localhost:10113/docs/ for more information about REST API
* main REST endpoint you will be needed is http://localhost:10113/api/check/

## Configuration
You can change config of the service by changing the environment variables. Here is a list of them:
* `SPELLCHECK_WORKERS` define application server workers count (default `8`). If you plan to use k8s and only scale with replica sets, you might want to reduce this value to 1 (allowed range from `1` to `300`).
* `SPELLCHECK_PORT` binding port (default `10113`, allowed range from `1024` to `65535`).
* `SPELLCHECK_API_PREFIX` define all API's prefix (default `/api/`)
* `SPELLCHECK_DOCS_URL` define swagger/documentation prefix (default `/docs/`)
* `SPELLCHECK_MAX_SUGGESTIONS` defines how many maximum suggestions for each word will be available (default is `None` means unlimited, can be any valid integer)
* `SPELLCHECK_MINIMUM_LENGTH_FOR_CORRECTION` if the word length is less than this option, the word will not be checked (default `3`)
* `SPELLCHECK_CACHE_SIZE` define LRU cache size for misspelled word/suggestions cache (default `10000`, any value less than `1` makes the cache size unlimited, so be careful with this option)
* `SPELLCHECK_ENABLE_CORS` defines if CORS is enabled (default `True`, in docker container is `False`)
* `SPELLCHECK_DICTIONARIES_DISABLED` switches off user dictionaries API (default `False`)
* `SPELLCHECK_DICTIONARIES_PROVIDER` define user dicts storage provider (default `file`, available: `file`, `dummy`)
* `SPELLCHECK_DICTIONARIES_PATH` define directory where user dicts is stored (default `/data/`)
* `SPELLCHECK_API_KEY` define api key for users dictionaries mostly. Please, provide, if you want to enable user dicts.

## Development
### Quickstart
* Clone this repo
* For MacOS X `brew install pyenchant`
* `poetry install`
* `poetry shell`
* And `make` will run local development server

Please check [./Makefile](./Makefile) for more details

### Troubleshooting
For MacOS X on Apple Silicon add `PYENCHANT_LIBRARY_PATH=/opt/homebrew/lib/libenchant-2.dylib` to your `.zprofile`
