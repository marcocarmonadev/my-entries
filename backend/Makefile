IMAGE = my-entries-backend

run:
	@uv run dotenv run python -m source.frameworks_and_drivers.web

check:
	@uv run ruff check

format:
	@uv run ruff format

preview:
	@docker build --tag $(IMAGE) .
	@docker run \
		--env-file .env \
		--name=$(IMAGE) \
		--network host \
		--volume ./local.db:/app/local.db \
		--rm \
		$(IMAGE)
