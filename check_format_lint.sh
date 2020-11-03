isort --check-only **/*.py
black --check . --exclude venv/
flake8 .
mypy .
