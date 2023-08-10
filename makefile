# Enter Postgres DB
sudo docker exec -it a100ba549fd0 psql -U postgres -d app

# Migreate Postgres DB
sudo docker exec -it openpdf-backend-1 alembic upgrade head