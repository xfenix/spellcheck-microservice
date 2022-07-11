run-dev:
	SPELLCHECK_dictionaries_path=/tmp/sm-dicts/ uvicorn whole_app.__main__:SPELL_APP --reload
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
	pylint whole_app tests
	mypy .
	vulture whole_app --min-confidence 100
	isort -c .
	black . --check
lint-in-docker:
	docker run -t spellcheck-microservice bash -c "pylint whole_app tests && mypy . && vulture whole_app --min-confidence 100"
run-prod:
	docker run  -p 10113:10113 -t spellcheck-microservice:latest
check-languages:
	python -c "import enchant; print(enchant.Broker().list_languages());"
check-languages-docker:
	docker run -it spellcheck-microservice python -c "import enchant; print(enchant.Broker().list_languages());"
