build:
	@docker compose build

preview:
	@docker compose up --build

push:
	@cd backend && make push
	@cd frontend && make push

clean:
	@docker compose down