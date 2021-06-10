# Deploy to k8s with cloud providers
## Build images using docker compose
check source/ directory

## Cloud volumes
see https://docs.microsoft.com/fr-fr/azure/aks/azure-files-volume for AKS

### Create 4 files share (azurfiles in Azure)
* statfive-nginx-share (conf.d files)
* statfive-letsencrypt-share (certs files)
* statfive-mariadb-share (db data)
* statfive-api-share (match videos)

### Create Azure storage account secret
$> kubectl create secret generic azure-secret --namespace statfive --from-literal=azurestorageaccountname=$AKS_PERS_STORAGE_ACCOUNT_NAME --from-literal=azurestorageaccountkey=$STORAGE_KEY

## Create Kubernetes resources
$> kubectl apply -f <every .yaml files in kubernetes directories>

## Expose to internet
Get external ip of loadbalancer provided by your Cloud Provider and add entries to your domain DNS
