dev:
	@poetry run dotenv run python -m source.frameworks_and_drivers.user_interface

build:
	@docker build --tag my-entries-frontend .

run: build
	@docker run \
		--env-file .env \
		--name=my-entries-frontend-dev-container \
		--network host \
		--rm \
		my-entries-frontend
