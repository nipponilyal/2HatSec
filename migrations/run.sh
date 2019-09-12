#! /bin/bash

docker build . -t migration
kubectl apply -f deployment/migration.yaml
sleep 20
kubectl delete -f deployment/migration.yaml
