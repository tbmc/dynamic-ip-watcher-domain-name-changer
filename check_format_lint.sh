isort --profile black --check --diff .
black --check --diff --exclude venv/ . 
flake8 --exclude venv/ .
mypy .
