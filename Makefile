start:
	@if [ $(shell git branch --show-current) = main ]; then \
		docker compose up \
		--build \
		--no-log-prefix; \
	else \
		echo "Error: switch to the 'main' branch to start."; \
	fi;

down:
	@if [ "$(shell docker ps -aq -f name=marcocarmonadev-backend-devcontainer)" ]; then \
		docker stop marcocarmonadev-backend-devcontainer; \
		docker rm marcocarmonadev-backend-devcontainer; \
	fi
	@if [ "$(shell docker ps -aq -f name=marcocarmonadev-backend-database)" ]; then \
		docker stop marcocarmonadev-backend-database; \
		docker rm marcocarmonadev-backend-database; \
	fi
	@docker compose down;

reopen: down
	@if [ $(shell git branch --show-current) = main ]; then \
		echo "Error: switch to another branch to start."; \
		exit 1; \
	fi;
