# Motor API

API to manage the raspery pi motor unit.

## Development Setup
Set up a virtual environment and install requirements:

```bash
# sudo apt update
# apt-get install python3-venv
python3 -m venv env
source env/bin/activate
make init
# Run locally - see Dockerize and deploy
make serve
```

## Docker

Create a .docker.env file for the docker.

```bash
# Make sure .docker.env is present
make build

# Run docker
make run

# Run as deamon
make run.d
make logs

# Open http://localhost:3000/docs in your browser.
```