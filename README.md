# StatFive

## Build and run the project
- `$> sudo certbot certonly --server https://acme-v02.api.letsencrypt.org/directory --manual -d '*.{YOUR_DOMAIN}'`  
- Change conf in nginx/\*.conf files to match the proxy redirection urls with your domain name
- `$> sudo docker-compose up -d`  
- go to https://dashboard.{YOUR_DOMAIN}
