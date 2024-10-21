IMAGE = my-entries-frontend

run:
	@uv run dotenv run python -m source.frameworks_and_drivers.user_interface

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
		--rm \
		$(IMAGE)
