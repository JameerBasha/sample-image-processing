.PHONY: runapis
runapis: ## Run the Grock APIs
	uvicorn src.api.main:app --reload --port 9080

.PHONY:
makemigrations:
	alembic revision --autogenerate -m "add image table"

.PHONY:
add_sample_fixtures:
	python -m utils.fixtures.image_fixtures

.PHONY: migrate
migrate:
	alembic upgrade head

.PHONY: run
run:
	docker compose up --build

.PHONY: run_background
run_background:
	docker compose up --build --detach