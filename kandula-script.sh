#!/bin/bash

export ID="$(aws secretsmanager --region us-east-1 get-secret-value --secret-id kandula/aws/creds | jq -r '.SecretString' | jq -r '.ID')"

export KEY="$(aws secretsmanager --region us-east-1 get-secret-value --secret-id kandula/aws/creds | jq -r '.SecretString' | jq -r '.KEY')"

sed -i -e "s/AWSID/${ID}/g" kandula-deploy.yaml

sed -i -e "s@AWSKEY@${KEY}@g" kandula-deploy.yaml

kubectl apply -f kandula-deploy.yaml

kubectl apply -f service.yaml

# sed -i -e "s/${ID}/AWSID/g" kandula-deploy.yaml
# sed -i -e "s@${KEY}@AWSKEY@g" kandula-deploy.yaml
