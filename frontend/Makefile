IMAGE_NAME = marcocarmonapy/my-entries-frontend
IMAGE_TAG = preview
IMAGE = $(IMAGE_NAME):$(IMAGE_TAG)

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
		--name=my-entries-frontend-$(IMAGE_TAG) \
		--network host \
		--rm \
		$(IMAGE)
