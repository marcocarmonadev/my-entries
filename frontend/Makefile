dev:
	@dotenv \
		--file .envs/development.env \
		run poetry run streamlit run source/frameworks_and_drivers/user_interface/pages/home.py --server.port 8502 --server.runOnSave true

start:
	@dotenv \
		--file .envs/production.env \
		run poetry run streamlit run source/frameworks_and_drivers/user_interface/pages/home.py
