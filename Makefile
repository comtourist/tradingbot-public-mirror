.PHONY: help venv install install-dev lint test up down build run-backfill

help:
	@echo "Targets:"
	@echo "  make install      - Install runtime deps"
	@echo "  make install-dev  - Install runtime + dev deps"
	@echo "  make lint         - Run ruff"
	@echo "  make test         - Run pytest"
	@echo "  make up           - Start local services (postgres)"
	@echo "  make down         - Stop local services"
	@echo "  make build        - Build docker image"
	@echo "  make run-backfill - Run backfill module locally"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

lint:
	ruff check .

test:
	pytest -q

up:
	docker compose up -d

down:
	docker compose down

build:
	docker build -t tradingbot:dev .

run-backfill:
	python -m src.backfill.backfill_job