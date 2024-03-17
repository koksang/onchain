#!/bin/sh
kubectl -n onchain get secret console-sa-secret -o jsonpath="{.data.token}" | base64 --decode
kubectl --namespace onchain port-forward svc/console 9090:9090