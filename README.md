# Deploy to k8s with cloud providers
## Build images using docker compose
check source directory

## Cloud volumes
see https://docs.microsoft.com/fr-fr/azure/aks/azure-files-volume for AKS

### Create 4 files share (azurfiles in Azure)
* statfive-nginx-share (conf.d files)
* statfive-letsencrypt-share (certs files)
* statfive-mariadb-share (db data)
* statfive-api-share (match videos)

### Create azure storage account secret
kubectl create secret generic azure-secret --from-literal=azurestorageaccountname=$AKS_PERS_STORAGE_ACCOUNT_NAME --from-literal=azurestorageaccountkey=$STORAGE_KEY
