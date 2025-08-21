run:
        SPELLCHECK_DICTIONARIES_PATH=/tmp/sm-dicts/ SPELLCHECK_API_KEY=debug granian --reload --interface asgi whole_app.views:SPELL_APP

build:
	docker build -t spellcheck-microservice .

prepare-buildx:
	docker buildx create --use --name newbuilder

build-buildx:
	docker buildx build --platform linux/amd64,linux/arm64 -t spellcheck-microservice .

exec:
	docker run -it spellcheck-microservice bash

test:
	pytest . -n3

test-in-docker:
	docker run -t spellcheck-microservice bash -c "COVERAGE_FILE=/tmp/junk.coverage pytest . -n3"

lint:
	ruff check . --no-fix
	mypy .
	vulture whole_app --min-confidence 100

lint-in-docker:
	docker run -t spellcheck-microservice bash -c "RUFF_CACHE_DIR=/tmp/ruff-cache ruff check . --no-fix && mypy . && vulture whole_app --min-confidence 100"

run-prod:
	docker run -p 10113:10113 -e SPELLCHECK_WORKERS=1 -t spellcheck-microservice:latest

check-languages:
	python -c "import enchant; print(enchant.Broker().list_languages());"

check-languages-docker:
	docker run -it spellcheck-microservice python -c "import enchant; print(enchant.Broker().list_languages());"

update-readme:
	python -m scripts update-readme

update-dockerhub-readme:
	python -m scripts update-dockerhub-readme
