build:
	@docker compose build

preview:
	@docker compose up --build

push:
	@docker compose push

clean:
	@docker compose down