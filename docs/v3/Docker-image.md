To build and run CodexSun v3 using Docker, follow these steps:

## For Frappe Instance

```
docker build -t codexsun:v3 -f docker/cloud/Dockerfile-frappe docker/cloud
```

## For Node Instance

```
docker build -t codexsun:v3 -f docker/cloud/Dockerfile-node docker/cloud
```

### 2. create network for codexion

```
docker network create codexion-network
```

### 3. create container for mariadb

```
 docker compose -f docker/cloud/mariadb.yml up -d
```

### 4. Check mariadb is installed

```
docker exec -it mariadb mariadb -u root -p
```

# remote access for root user 

```
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

4. Allow access on your Ubuntu host (firewall):
If using UFW:

```
sudo ufw allow 3306/tcp
```
```
sudo ufw reload
```
```
sudo ufw status
```
status : inactive


# Step 1: Install SSL with Certbot (Recommended for Nginx)
Step 1: Install Certbot and Nginx plugin


```
sudo apt update
sudo apt install certbot python3-certbot-nginx -y
```
```
sudo systemctl status nginx
```
```
sudo ufw allow 'Nginx Full'
sudo ufw reload
```


```
server {
    listen 80;
    server_name soft.aaran.org;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

sudo ln -s /etc/nginx/sites-available/demo.codexsun.com /etc/nginx/sites-enabled/


```
sudo certbot --nginx
```

sudo nginx -t
sudo systemctl reload nginx
