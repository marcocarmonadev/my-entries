dev:
	@poetry run dotenv run python -m source.frameworks_and_drivers.web

build:
	@docker build --tag my-entries-backend .

preview: build
	@docker run \
		--env-file .env \
		--name=my-entries-backend-container \
		--network host \
		--volume ./local.db:/workdir/local.db \
		--rm \
		my-entries-backend

push: build
	@docker tag my-entries-backend marcocarmonapy/my-entries-backend
	@docker push marcocarmonapy/my-entries-backend
