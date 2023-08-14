# Enter Postgres DB
sudo docker exec -it openpdf-backend-1 psql -U postgres -d app

# Migreate Postgres DB
sudo docker exec -it openpdf-backend-1 alembic upgrade head

# run tests
sudo docker-compose exec backend bash /app/tests-start.sh -x

# react test user
"password": "12341234",
"email": "lolo@example.com",
"full_name": "string"
