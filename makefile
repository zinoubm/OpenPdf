# Enter Postgres DB
sudo docker exec -it openpdf-db-1 psql -U postgres -d app

# Migreate Postgres DB
sudo docker exec -it openpdf-backend-1 alembic upgrade head

# Generate migrations 
sudo docker exec -it openpdf-backend-1 alembic revision --autogenerate -m "Add column last_name to User model"

# run tests
sudo docker-compose exec backend bash /app/tests-start.sh -x

# react test user
"password": "12341234",
"email": "test@example.com",
"full_name": "string"

# non verified test user
"password": "12341234",
"email": "nonverified@example.com",
"full_name": "non verified"

# this is a dummy comment
# open source reference https://demo-erp-crm.idurarapp.com/

info@salesforza.com
rwLBFMNw84zzViB
