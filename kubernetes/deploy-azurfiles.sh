#!/bin/bash

AKS_PERS_STORAGE_ACCOUNT_NAME=mystorageaccount99991112
AKS_PERS_RESOURCE_GROUP=statfive
AKS_PERS_LOCATION=francecentral

az storage account create -n $AKS_PERS_STORAGE_ACCOUNT_NAME -g $AKS_PERS_RESOURCE_GROUP -l $AKS_PERS_LOCATION --sku Standard_LRS
export AZURE_STORAGE_CONNECTION_STRING=$(az storage account show-connection-string -n $AKS_PERS_STORAGE_ACCOUNT_NAME -g $AKS_PERS_RESOURCE_GROUP -o tsv)

az storage share create -n statfive-nginx-share --connection-string $AZURE_STORAGE_CONNECTION_STRING
az storage share create -n statfive-letsencrypt-share --connection-string $AZURE_STORAGE_CONNECTION_STRING
az storage share create -n statfive-mariadb-share --connection-string $AZURE_STORAGE_CONNECTION_STRING
az storage share create -n statfive-api-share --connection-string $AZURE_STORAGE_CONNECTION_STRING

STORAGE_KEY=$(az storage account keys list --resource-group $AKS_PERS_RESOURCE_GROUP --account-name $AKS_PERS_STORAGE_ACCOUNT_NAME --query "[0].value" -o tsv)

echo Storage account name: $AKS_PERS_STORAGE_ACCOUNT_NAME
echo Storage account key: $STORAGE_KEY

kubectl create namespace statfive
kubectl create secret generic azure-secret --namespace statfive --from-literal=azurestorageaccountname=$AKS_PERS_STORAGE_ACCOUNT_NAME --from-literal=azurestorageaccountkey=$STORAGE_KEY
