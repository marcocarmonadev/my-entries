start:
	@docker build \
		--tag my-api-image-production \
		.
	@docker run \
		--publish 8000:8000 \
		--name=my-api-container-production \
		--env-file=envs/production.env \
		--rm \
		sinecta-api-image-production