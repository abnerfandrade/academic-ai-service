VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
UVICORN = $(VENV)/bin/uvicorn
PYTEST = $(VENV)/bin/pytest
ALEMBIC = $(VENV)/bin/alembic

.PHONY: dev smith infra-up infra-down up down logs install install-dev tests migrate

install:
	$(PIP) install -r requirements-dev.txt

dev:
	$(UVICORN) --factory src.main:create_app --host 0.0.0.0 --port 8000 --reload

smith:
	langgraph dev

infra-up:
	docker compose up postgres qdrant -d

infra-down:
	docker compose down

migrate:
	PYTHONPATH=. $(ALEMBIC) upgrade head

migrate-docker:
	docker compose exec api bash -c "PYTHONPATH=. alembic upgrade head"

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs api -f

tests:
	$(PYTEST) -vvl tests/unit
