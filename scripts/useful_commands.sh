#!/bin/sh
kubectl -n onchain get secret console-sa-secret -o jsonpath="{.data.token}" | base64 --decode
kubectl --namespace onchain port-forward svc/console 9090:9090

microk8s install --cpu 6 --mem 15 --disk 100 --image lts
microk8s enable hostpath-storage host-access dashboard minio rbac ingress
microk8s config > ~/.kube/config

multipass mount /opt/data microk8s-vm:/data

