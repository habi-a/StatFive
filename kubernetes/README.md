# Deploy to k8s with cloud providers
## Cloud volumes (see https://docs.microsoft.com/fr-fr/azure/aks/azure-files-volume for Azure)
### Create 4 file share
* statfive-nginx-share (conf.d files)
* statfive-letsencrypt-share (certs files)
* statfive-mariadb-share (db data)
* statfive-api-share (match videos)

### create azure storage account secret
kubectl create secret generic azure-secret --from-literal=azurestorageaccountname=$AKS_PERS_STORAGE_ACCOUNT_NAME --from-literal=azurestorageaccountkey=$STORAGE_KEY
