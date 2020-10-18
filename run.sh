#! /bin/bash
set -e

docker build . -t handler
kubectl apply -f deployment/handler.yaml
# sleep 60
# kubectl delete -f deployment/handler.yaml


