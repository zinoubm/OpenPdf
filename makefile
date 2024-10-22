# include .env
# $(eval export $(shell sed -ne 's/ *#.*$$//; /./ s/=.*$$// p' .env))

# # provider secrets
# export TF_VAR_aws_access_key_id=$(ACCESS_KEY_ID)
# export TF_VAR_aws_secret_access_key=$(SECRET_ACCESS_KEY)
# export TF_VAR_region=$(AWS_REGION)
# export TF_VAR_tld_zone_id=$(AWS_DNS_ZONE_ID)

# export TF_VAR_ecs_task_desired_count = 2
# export TF_VAR_service_name = backend
# export AWS_DEFAULT_REGION = $(TF_VAR_region)

# default message for generated migration
message = "updating db schema"

# psql -U {user} -d {db name} -h {host} -p 5432
db_connect:
	sudo docker exec -it openpdf-db-1 psql -U postgres -d app

migrate:
	sudo docker exec -it openpdf-backend-1 alembic upgrade head

downgrade_migration:
	sudo docker exec -it openpdf-backend-1 alembic downgrade -1

generate_migration:
	sudo docker exec -it openpdf-backend-1 alembic revision --autogenerate -m ${message}

test:
	sudo docker compose exec backend bash /app/tests-start.sh -x

deploy:
	./terraform/deploy.sh

destroy:
	cd ./terraform && terraform destroy -var hash=null -auto-approve
	
