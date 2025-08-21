# Spellcheck microservice

[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/xfenix/spellcheck-microservice?label=version)](https://github.com/xfenix/spellcheck-microservice/releases)
[![Docker Pulls](https://img.shields.io/docker/pulls/xfenix/spellcheck-microservice)](https://hub.docker.com/r/xfenix/spellcheck-microservice)
[![Coverage](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/xfenix/spellcheck-microservice/main/.github/badges/coverage.json)](https://xfenix.github.io/spellcheck-microservice/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
<a href="https://github.com/psf/black" target="_blank"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![Imports: isort](https://img.shields.io/badge/imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)
<a href="http://mypy-lang.org/" target="_blank"><img src="https://img.shields.io/badge/mypy-checked-1F5082.svg" alt="Mypy checked"></a>

This is a microservice designed to check the spelling of words. Based on [pyenchant](https://github.com/pyenchant/pyenchant). Exposes a REST API.<br>
Current available languages are: ru_RU, en_US, es_ES, fr_FR, de_DE, pt_PT.<br>
It runs blazingly fast due to the use of pychant in its kernel, LRU cache usage and pypy.<br>
Also it supports feature called «user dictionaries» — user can add his own word-exceptions to personal dictionary.

## Quickstart

- `docker run -p 10113:10113 -t --mount source=spellcheck-dicts,target=/data/ xfenix/spellcheck-microservice:4.2.0`
- check http://localhost:10113/docs/ for full REST documentation
- main REST endpoint you will be needed is http://localhost:10113/api/check/ (this will be available without authorization)

## Configuration

### Config options

You can change config of the service by changing the environment variables. Here is a list of them:
* `SPELLCHECK_SENTRY_DSN` Sentry DSN for integration. Empty field disables integration. Default value is empty string.
* `SPELLCHECK_API_KEY` define api key for users dictionaries mostly. Please, provide, if you want to enable user dictionaries API. Default value is empty string.
* `SPELLCHECK_ENABLE_CORS` enable CORS for all endpoints. In docker container this option is disabled. Default value is `True`.
* `SPELLCHECK_STRUCTURED_LOGGING` enables structured (json) logging. Default value is `True`.
* `SPELLCHECK_WORKERS` define application server workers count. If you plan to use k8s and only scale with replica sets, you might want to reduce this value to `1`. Default value is `8`. Restrictions: `Gt(gt=0)`, `Lt(lt=301)`
* `SPELLCHECK_SERVER_ADDRESS` binding address, default value suitable for docker. Default value is `0.0.0.0`.
* `SPELLCHECK_PORT` binding port. Default value is `10113`. Restrictions: `Gt(gt=1023)`, `Lt(lt=65536)`
* `SPELLCHECK_CACHE_SIZE` define LRU cache size for misspelled word/suggestions cache. Any value less than `1` makes the cache size unlimited, so be careful with this option. Default value is `10000`.
* `SPELLCHECK_API_PREFIX` define all API's URL prefix. Default value is `/api/`.
* `SPELLCHECK_DOCS_URL` define documentation (swagger) URL prefix. Default value is `/docs/`.
* `SPELLCHECK_MAX_SUGGESTIONS` defines how many maximum suggestions for each word will be available. 0 means unlimitied. Default value is `0`. Restrictions: `Ge(ge=0)`
* `SPELLCHECK_DICTIONARIES_PATH` define directory where user dicts is stored. This is inner directory in the docker image, please map it to volume as it shown in the quickstart part of this readme. Default value is `/data`.
* `SPELLCHECK_DICTIONARIES_STORAGE_PROVIDER` define wich engine will store user dictionaries. Default value is `StorageProviders.FILE`.
* `SPELLCHECK_DICTIONARIES_DISABLED` switches off user dictionaries API no matter what. Default value is `False`.
* `SPELLCHECK_USERNAME_MIN_LENGTH` minimum length of username. Default value is `3`.
* `SPELLCHECK_USERNAME_MAX_LENGTH` maximum length of username. Default value is `60`.
* `SPELLCHECK_EXCLUSION_WORDS_STR` String with list of words which will be ignored in /api/check endpoint each request. Example: `'foo, bar'`. Default value is empty string.

### Deployment

Note: all docker & docker-compose variants use named volumes to store user dictionaries.

#### Plain docker

`docker run  -p 10113:10113 -t --mount source=spellcheck-dicts,target=/data/ xfenix/spellcheck-microservice:4.2.0`

#### Docker-compose

- Save this example configuration as `docker-compose.yml`:

```yml
version: "3.9"
services:
  spellcheck:
    image: xfenix/spellcheck-microservice:4.2.0
    ports:
      - "10113:10113"
    volumes:
      - spellcheck-dicts:/data/

volumes:
  spellcheck-dicts:
```

- Then run `docker-compose up`

## Changelog

You cand find it here https://github.com/xfenix/spellcheck-microservice/releases

## Development

### Quickstart

- Clone this repo
- For MacOS X `brew install enchant`
- For Debian/Ubuntu `apt-get install -y enchant-2 hunspell-ru`
- `uv sync --group dev`
- `source .venv/bin/activate`
- Run `touch .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit`
- Paste following contents in file `.git/hooks/pre-commit`:
  ```sh
  uv run make update-readme
  git add README.md
  ```
- Execute `make` command to run local development server

### Notes

Default api-key for local development is `debug` (you will need this to work with user dictionaries API).

Please check [./Makefile](./Makefile) for more details

### Troubleshooting

For MacOS X on Apple Silicon add `PYENCHANT_LIBRARY_PATH=/opt/homebrew/lib/libenchant-2.dylib` to your `.zprofile`
