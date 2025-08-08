.PHONY: test
test:
	uv run pytest

.PHONY: run-with-docker
run-with-docker:
	docker compose up --build

.PHONY: run-with-uv
run-with-uv:
	uv run uvicorn app.api_server:app --host localhost --port 8000

