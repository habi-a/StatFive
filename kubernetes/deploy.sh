#!/bin/bash

set -e


# Deploy storage
AKS_PERS_STORAGE_ACCOUNT_NAME=mystorageaccount$(( $RANDOM % 99999999 + 00000001 ))
AKS_PERS_RESOURCE_GROUP=statfive
AKS_PERS_LOCATION=francecentral
az storage account create -n $AKS_PERS_STORAGE_ACCOUNT_NAME -g $AKS_PERS_RESOURCE_GROUP -l $AKS_PERS_LOCATION --sku Standard_LRS
export AZURE_STORAGE_CONNECTION_STRING=$(az storage account show-connection-string -n $AKS_PERS_STORAGE_ACCOUNT_NAME -g $AKS_PERS_RESOURCE_GROUP -o tsv)
az storage share create -n statfive-mariadb-share --connection-string $AZURE_STORAGE_CONNECTION_STRING
az storage share create -n statfive-api-share --connection-string $AZURE_STORAGE_CONNECTION_STRING
STORAGE_KEY=$(az storage account keys list --resource-group $AKS_PERS_RESOURCE_GROUP --account-name $AKS_PERS_STORAGE_ACCOUNT_NAME --query "[0].value" -o tsv)
echo Storage account name: $AKS_PERS_STORAGE_ACCOUNT_NAME
echo Storage account key: $STORAGE_KEY


# Create K8S resources
kubectl create namespace monitoring
kubectl create namespace statfive
kubectl create namespace traefik
kubectl create secret generic azure-secret --namespace statfive --from-literal=azurestorageaccountname=$AKS_PERS_STORAGE_ACCOUNT_NAME --from-literal=azurestorageaccountkey=$STORAGE_KEY

kubectl apply -f ovh-config.yaml
kubectl apply -f mariadb.yaml
kubectl apply -f redis.yaml
kubectl apply -f phpmyadmin.yaml
kubectl apply -f api.yaml
kubectl apply -f tracker.yaml
kubectl apply -f web.yaml

# Install traefik
helm repo add traefik https://helm.traefik.io/traefik
helm repo update
helm install traefik traefik/traefik --namespace=traefik --values=traefik-values.yml
kubectl apply -f traefik-ingress.yaml

# Install Monitoring
rm -rf kube-prometheus
git clone https://github.com/prometheus-operator/kube-prometheus.git
cd kube-prometheus
kubectl create -f manifests/setup
until kubectl get servicemonitors --all-namespaces ; do date; sleep 1; echo ""; done
kubectl create -f manifests/
cd ../
rm -rf kube-prometheus
kubectl apply -f prometheus-monitor.yaml
