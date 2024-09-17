dev:
	@dotenv \
		--file .envs/development.env \
		run poetry run streamlit run source/frameworks_and_drivers/user_interface/__main__.py --server.port 8502 --server.runOnSave true

start:
	@dotenv \
		--file .envs/production.env \
		run poetry run streamlit run source/frameworks_and_drivers/user_interface/__main__.py
