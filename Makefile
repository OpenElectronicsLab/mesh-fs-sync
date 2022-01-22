SHELL=/bin/bash

.PHONY: check
check: mfs-venv/bin/activate
	python3 -m pytest --cov=meshfssync

requirements.txt:
	source mfs-venv/bin/activate && pipreqs meshfssync

mfs-venv/bin/activate: requirements.txt
	python3 -m venv mfs-venv
	source mfs-venv/bin/activate && \
		pip3 install -r requirements.txt -r dev-requirements.txt
	echo 'now: source mfs-venv/bin/activate'

.PHONY: black
black:
	python -m black --line-length=80 meshfssync
	python -m black --line-length=80 test

.PHONY: tidy
tidy: black
