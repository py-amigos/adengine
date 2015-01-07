.PHONY: deps run-dev tests

update-deps:
	pip install -r dev-requirements.txt
	pip install -r requirements.txt

init: update-deps

run-dev:
	python server.py

clean:
	find . -name "*.pyc" -exec rm -v {} \;

tests:
	py.test -v --tb short -s --looponfail

create-new-user:
	curl -i -H Content-Type: application/json -X POST -d {"title": 10} http://localhost:5000/api/v1.0/users

list-all-users:
	curl -i http://localhost:5000/api/v1.0/users

tox:
	python3.4 -m tox
