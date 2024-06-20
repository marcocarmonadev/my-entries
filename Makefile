CURRENT_BRANCH=$(shell git branch --show-current)
start:
	@if [ $(CURRENT_BRANCH) = main ]; then \
		docker compose \
		-f docker-compose.yml \
		-f docker-compose.base.yml \
		up --build; \
	else \
		echo "Error: switch to the 'main' branch to start."; \
	fi;
down:
	@docker compose \
	-f docker-compose.yml \
	-f docker-compose.base.yml \
	down;
	@docker compose \
	-f .devcontainer/docker-compose.yml \
	-f docker-compose.base.yml \
	down;