run-dev:
	uvicorn whole_app.__main__:SPELL_APP --reload
build:
	docker build -t spellcheck-microservice .
exec:
	docker run -it spellcheck-microservice bash
test:
	pytest . -n3
test-in-docker:
	docker run -t spellcheck-microservice bash -c "COVERAGE_FILE=/tmp/junk.coverage pytest . -n3"
lint:
	pylint whole_app tests
	mypy .
lint-in-docker:
	docker run -t spellcheck-microservice bash -c "pylint whole_app tests && mypy ."
