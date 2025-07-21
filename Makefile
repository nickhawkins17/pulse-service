SRC_DIR=src/
TEST_DIR=tests/
VENV=.venv
MAX_LINE_LENGTH=120

help:  ## Display all make targets
	@cat Makefile | grep -E '^[a-zA-Z0-9\/_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Code Quality and Testing

format:  ## Format code and documentation
	autoflake --in-place --remove-all-unused-imports --remove-unused-variables --recursive $(SRC_DIR) $(TEST_DIR)
	isort $(SRC_DIR) $(TEST_DIR) --profile black --line-length $(MAX_LINE_LENGTH)
	black $(SRC_DIR) $(TEST_DIR) --line-length $(MAX_LINE_LENGTH)
	mdformat .

lint:  ## Run linters to check code quality
	autoflake --check --remove-all-unused-imports --remove-unused-variables --recursive $(SRC_DIR) $(TEST_DIR)
	isort --check-only $(SRC_DIR) $(TEST_DIR) --profile black --line-length $(MAX_LINE_LENGTH)
	black --check $(SRC_DIR) $(TEST_DIR) --line-length $(MAX_LINE_LENGTH)
	mdformat --check .

test:  ## Run tests, ensure services are running
	@if ! docker-compose ps | grep -q "app\|postgres"; then \
		echo "Starting services..."; \
		make up; \
	fi
	pytest -vv --cov=$(SRC_DIR). --cov=$(TEST_DIR). --cov-report term-missing  tests/

# Services

build: ## Build and start services
	docker-compose up --build -d

up: ## Start services
	docker-compose up -d

down:  ## Stop services
	docker-compose down

upgrade-db:
	alembic upgrade head

# Spotify API

generate-token:  ## Generate new access token for Spotify Web API. Stored in Redis.
	python -m src.utils.spotify.access_token --generate

get-token:  ## Get the existing access token for Spotify Web API.
	python -m src.utils.spotify.access_token

ingest-tracks:
	python -m src.utils.spotify.spotify_api $(playlist_id)