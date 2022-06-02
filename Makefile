run-dev:
	uvicorn whole_app.__main__:SPELL_APP --reload
build-dev:
	docker build -t spellcheck-microservice .
exec-dev:
	docker run -it spellcheck-microservice bash
run-prod:
	docker run -it spellcheck-microservice
test:
	pytest .
lint:
	pylint whole_app
	mypy .
