#!/bin/bash

echo "### Failed Jobs ###"
kubectl -n default get jobs $(kubectl get jobs -o=jsonpath='{.items[?(@.status.failed>0)].metadata.name}')

echo "### Running Jobs ###"
kubectl -n default get jobs $(kubectl get jobs -o=jsonpath='{.items[?(@.status.active==1)].metadata.name}')
