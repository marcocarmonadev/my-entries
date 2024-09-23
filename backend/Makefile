dev:
	@poetry run dotenv run python -m source.frameworks_and_drivers.web

build:
	@docker build --tag my-entries-backend .

run: build
	@docker run \
		--env-file .env \
		--name=my-entries-backend-dev-container \
		--network host \
		--volume ./local.db:/workdir/local.db \
		--rm \
		my-entries-backend
