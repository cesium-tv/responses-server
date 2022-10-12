/usr/bin/virtualenv:
	sudo apt install python3-virtualenv


.venv: requirements.txt /usr/bin/virtualenv
	virtualenv -p python3 .venv
	.venv/local/bin/pip install -r requirements.txt
	.venv/local/bin/pip install flake8
	touch .venv


.PHONY: test
test: .venv
	.venv/local/bin/python3 -m unittest tests/test_*.py


.PHONY: lint
lint: .venv
	.venv/local/bin/python3 -m flake8 responses_server


.PHONY: ci
ci: lint test
