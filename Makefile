run-dev:
	uvicorn whole-app.__main__:SPELL_APP --reload
build-dev:
	docker build -t spellcheck-microservice .
exec-dev:
	docker run -it spellchec-microservice bash
test:
	pytest .
lint:
	pylint whole-app
	mypy .
