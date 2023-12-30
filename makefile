message = "updating db schema"

db_connect:
	sudo docker exec -it openpdf-db-1 psql -U postgres -d app

migrate:
	sudo docker exec -it openpdf-backend-1 alembic upgrade head

generate_migration:
	sudo docker exec -it openpdf-backend-1 alembic revision --autogenerate -m "${message}"

test:
	sudo docker-compose exec backend bash /app/tests-start.sh -x
