VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
UVICORN = $(VENV)/bin/uvicorn
PYTEST = $(VENV)/bin/pytest

.PHONY: dev infra-up infra-down up down logs install install-dev tests

install:
	$(PIP) install -r requirements.txt

dev:
	$(UVICORN) --factory src.main:create_app --host 0.0.0.0 --port 8000 --reload

infra-up:
	docker compose up postgres qdrant -d

infra-down:
	docker compose down

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs api -f

tests:
	$(PYTEST) -vvl tests/unit
