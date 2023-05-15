/usr/bin/virtualenv:
	sudo apt install python3-virtualenv


dist/responses_server-?.?.?-*.whl: $(SRC)
	python3 setup.py bdist_wheel


build: dist/responses_server-?.?.?-*.whl
	python3 setup.py bdist_wheel


.venv: requirements.txt /usr/bin/virtualenv
	virtualenv -p python3 .venv
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pip install flake8
	touch .venv


.PHONY: test
test: .venv
	.venv/bin/python3 -m unittest tests/test_*.py


.PHONY: lint
lint: .venv
	.venv/bin/python3 -m flake8 responses_server


.PHONY: ci
ci: lint test


.PHONY: clean
clean:
	rm -rf build/ dist/ .venv/ responses_server.egg-info/
