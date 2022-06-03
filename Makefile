run-dev:
	uvicorn whole_app.__main__:SPELL_APP --reload
build:
	docker build -t spellcheck-microservice .
exec:
	docker run -it spellcheck-microservice bash
run:
	docker run -it spellcheck-microservice ${ARGS}
test:
	pytest . -n3
lint:
	pylint whole_app tests
	mypy .
