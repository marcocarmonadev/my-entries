dev:
	@poetry run dotenv run python -m source.frameworks_and_drivers.user_interface

build:
	@docker build --tag my-entries-frontend .

preview: build
	@docker run \
		--env-file .env \
		--name=my-entries-frontend-container \
		--network host \
		--rm \
		my-entries-frontend

push: build
	@docker tag my-entries-frontend marcocarmonapy/my-entries-frontend
	@docker push marcocarmonapy/my-entries-frontend
