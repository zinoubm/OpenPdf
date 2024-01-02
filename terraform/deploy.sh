#!/bin/bash
echo "working"
## Simulated hash per deployment, normally used by CI/CD system
HASH=$(openssl rand -hex 12)

cd terraform

terraform init

## Generate Terraform plan file
# terraform plan -var-file=".tfvars" -var hash=${HASH} -out=infrastructure.tf.plan
terraform plan -var-file=".tfvars" -var hash=${HASH} -out=infrastructure.tf.plan

## Provision resources
terraform apply -auto-approve infrastructure.tf.plan
rm -rf infrastructure.tf.plan