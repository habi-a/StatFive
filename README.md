# StatFive
![statfive](https://github.com/user-attachments/assets/e3777b19-1f2e-4e58-90fd-476de6cdb9f9)

## Start the project

### Azure AKS
#### Prerequisites
- 1 Azure Account
- 1 Azure AKS Cluster
- Azure CLI
- Kubectl
- Helm CLI
- OVH Account with a Domain Name
- Generate API OVH Credentials

#### Deploy
- `$> az login`
- `$> az account set --subscription xxxxxxxxxxxxxxxxxxxxxxxx`
- `$> az aks get-credentials --resource-group xxxxxxxx --name xxxxxxxx`
- `$> cd Statfive/kubernetes`
- Edit Traefik Ingress Files to match the proxy redirection urls with your domain name
- Edit Ovh API credentials
- `$> ./deploy.sh`
- go to https://dashboard.{YOUR_DOMAIN}/

### Docker-compose
#### Prerequisites
- Docker
- Docker-Compose
- Letsencrypt
- Certbot

#### Generate Certificates
- `$> sudo certbot certonly --server https://acme-v02.api.letsencrypt.org/directory --manual -d '*.{YOUR_DOMAIN}'`  
- Change conf in nginx/\*.conf files to match the proxy redirection urls with your domain name

#### Deploy:
- `$> sudo docker-compose up -d`  
- go to https://dashboard.{YOUR_DOMAIN}/
