IMAGE_NAME = marcocarmonapy/my-entries-backend
IMAGE_TAG = preview
IMAGE = $(IMAGE_NAME):$(IMAGE_TAG)

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
		--name=my-entries-backend-$(IMAGE_TAG) \
		--network host \
		--volume ./local.db:/app/local.db \
		--rm \
		$(IMAGE)
