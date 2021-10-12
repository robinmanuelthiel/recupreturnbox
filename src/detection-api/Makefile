.EXPORT_ALL_VARIABLES:
current_dir=$(shell pwd)

SRC=$(PWD)/src

VENV_PATH=$(PWD)/env/bin/activate
ENVIRONMENT_VARIABLE_FILE?=$(PWD)/.env


DOCKER_NAME='detection-api'
DOCKER_TAG?='1.0'
LOGLEVEL?=WARNING


define find.functions
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
endef

help:
	@echo 'The following commands can be used.'
	@echo ''
	$(call find.functions)


init: ## sets up environment and installs requirements
init: install
	pip install -r requirements.txt

install: ## Installs development requirments
install:
	python3 -m pip install --upgrade pip
	# Used for packaging and publishing
	pip install setuptools wheel twine
	# Used for linting
	pip install flake8
	# Used for testing
	pip install pytest
	# Install autopep8
	pip install autopep8

	pip install mypy pycodestyle pydocstyle

format: ## Formats the code with autopep8
format:
	autopep8 $(SRC) --recursive --in-place --pep8-passes 2000 --aggressive --verbose

lint: ## Runs flake8 on src, exit if critical rules are broken
lint:
	# stop the build if there are Python syntax errors or undefined names
	flake8 $(SRC) --count --select=E9,F63,F7,F82 --show-source --statistics
	# exit-zero treats all errors as warnings. The GitHfub editor is 127 chars wide
	flake8 $(SRC) --count --exit-zero --statistics

lint2:
	pylint --rcfile=.pylintrc $(SRC) -f parseable -r n && \
	mypy --silent-imports $(SRC) && \
	pycodestyle $(SRC) --max-line-length=120 && \
	pydocstyle $(SRC)

clean: ## Remove build and cache files
clean:
	rm -rf *.egg-info
	rm -rf build/
	rm -rf dist/
	rm -rf .pytest_cache

	find . -name '*.pyc' | rm -rf
	find . -name '*.pyo' | rm -rf

	# Remove all pycache
	find . | grep -E "__pycache__" | xargs rm -rf

leave: ## Cleanup and deactivate venv
leave: clean
	deactivate

test: ## Run pytest
test:
	pytest . -p no:logging -p no:warnings -k 'not integration'

serve: ## Runs the app locally
serve:
	cd src &&  python3 main.py

build: ## Build docker image
build:
	docker build -t $(DOCKER_NAME) .

run: ## build, start and run docker image
run: # remove
	docker run --name $(DOCKER_NAME) --volume="$(current_dir)/src:/app" --env-file .docker.env -p 3000:80 $(DOCKER_NAME) /start-reload.sh

run.d: ## build, start and run docker image
run.d: # remove
	docker run --name $(DOCKER_NAME) --volume="$(current_dir)/src:/app" --env-file .docker.env -d -p 3000:80 $(DOCKER_NAME) /start-reload.sh
	@echo "Open browser http://localhost:8080/docs"

exec: ## build, start and exec into docker image
exec: start
	docker exec -it $(DOCKER_NAME) python

stop: ## stop docker container fastapi
stop:
	docker stop $(DOCKER_NAME)

remove: ## remove docker container fastapi
remove: stop
	docker rm -f $(DOCKER_NAME)

logs: ## Returns the current docker logs
logs:
	docker logs --follow $(DOCKER_NAME)