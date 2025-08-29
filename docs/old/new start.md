
🧱 1. Build Docker and Tag the Image
Even though you named the stage codexion-cloud, Docker won’t tag it by default. You need to build and tag it manually:

if not in root folder

```
docker build -t codexion-cloud:v1 -f docker/frappe/Dockerfile  docker/frappe
```

if in server at docker folder

```
docker build -t codexion-cloud:v1 .
```

Now, codexion-cloud:v1 is a full Docker image that you can use anywhere.

### Step 2 : To create custom network to share between containers 
```
docker network create codexion-network
```

```
 docker compose -f mariadb.yml up -d
```
```
docker exec -it mariadb mariadb -u root -p
```

remote access for root user 

```
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

```
SELECT user, host FROM mysql.user WHERE user = 'root';
```
You should see something like:

```
+------+-----------+
| user | host      |
+------+-----------+
| root | localhost |
| root | %         |
+------+-----------+
```

If 'root'@'%' exists and has privileges, you're ready to connect remotely.

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


# 5 To run a specific Docker Compose file
```
docker compose -f soft-aaran-org.yml up -d
```
```
docker compose -f sukraa-codexsun-com.yml up -d
```
```
docker compose -f flexcon-codexsun-com.yml up -d
```
```
docker compose -f smile-codexsun-com.yml up -d
```
```
docker compose -f ganapathi-codexsun-com.yml up -d
```
```
docker compose -f erp-lifeshoppy-com.yml up -d
```

```
docker compose -f dev-aaranerp-com.yml up -d
```

# 6 To open soft-aaran-org in bash
```
docker exec -it soft_aaran_org bash
```

```
docker exec -it sukraa_codexsun_com bash
```

```
docker exec -it flexcon_codexsun_com bash
```

```
docker exec -it smile_codexsun_com bash
```

```
docker exec -it ganapathi_codexsun_com bash
```

```
docker exec -it erp_lifeshoppy_com bash
```

```
docker exec -it dev_aaranerp_com bash
```

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
sudo certbot --nginx
```


sudo ln -s /etc/nginx/sites-available/soft.aaran.org /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/sukraa.codexsun.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/flexcon.codexsun.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/smile.codexsun.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/ganapathi.codexsun.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/erp.lifeshoppy.com /etc/nginx/sites-enabled/



sudo ln -s /etc/nginx/sites-available/software.aaran.org /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/dev.aaranerp.com /etc/nginx/sites-enabled/



sudo ln -s /etc/nginx/sites-available/dev.aaranerp.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/shop.aaranerp.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/server.aaranerp.com /etc/nginx/sites-enabled/

sudo ln -s /etc/nginx/sites-available/demo.codexsun.com /etc/nginx/sites-enabled/

sudo nginx -t
sudo systemctl reload nginx




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

```
server {
    listen 80;
    server_name sukraa.codexsun.com;

    location / {
        proxy_pass http://127.0.0.1:8002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
```
server {
    listen 80;
    server_name demo.codexsun.com;

    location / {
        proxy_pass http://127.0.0.1:8005;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```



```
server {
    listen 80;
    server_name flexcon.codexsun.com;

    location / {
        proxy_pass http://127.0.0.1:8003;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```
server {
    listen 80;
    server_name smile.codexsun.com;

    location / {
        proxy_pass http://127.0.0.1:8004;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```
server {
    listen 80;
    server_name ganapathi.codexsun.com;

    location / {
        proxy_pass http://127.0.0.1:8005;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```
server {
    listen 80;
    server_name erp.lifeshoppy.com;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```
server {
    listen 80;
    server_name dev.aaranerp.com;

    location / {
        proxy_pass http://127.0.0.1:8007;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
```
server {
    listen 80;
    server_name shop.aaranerp.com;

    location / {
        proxy_pass http://127.0.0.1:4001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
```
server {
    listen 80;
    server_name server.aaranerp.com;

    location / {
        proxy_pass http://127.0.0.1:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```




Here's the direct one-liner bash command to zip and copy the frappe-bench directory to /home/devops/shared:
```
cd /home/devops && zip -r frappe-bench.zip frappe-bench && mkdir -p /home/devops/shared && mv frappe-bench.zip /home/devops/shared/
``

 bench get-app https://github.com/frappe/lms --branch develop
 bench --site dev.aaranerp.com install-app lms

npm install frappe-ui

 
 bench get-app https://github.com/frappe/gameplan --branch develop
 bench --site erp.logicx.in install-app gameplan
 
 bench get-app https://github.com/frappe/wiki 
 bench --site soft.aaranerp.com install-app wiki
 
 
  bench get-app https://github.com/frappe/lending --branch develop
  bench --site dev.aaranerp.com install-app lending

  bench get-app https://github.com/frappe/helpdesk --branch develop
  bench --site dev.aaranerp.com install-app helpdesk
  
  bench --site erp.tmnext.in install-app helpdesk
  
  bench get-app https://github.com/frappe/print_designer  --branch develop
  bench --site erp.aaranerp.com install-app print_designer 
  
  bench get-app https://github.com/frappe/education  --branch develop
  bench --site dev.aaranerp.com install-app education 
  
  bench get-app https://github.com/frappe/blogs  --branch develop
  bench --site dev.aaranerp.com install-app blogs 

  bench get-app https://github.com/frappe/payments
  bench --site dev.aaranerp.com install-app payments
  
  bench get-app https://github.com/frappe/webshop  --branch develop
  bench --site dev.aaranerp.com install-app webshop 

yarn install

yarn audit

yarn audit fix

cd apps/gameplan
yarn build


npm install @iconify-json/lucide
# or if you're using yarn
yarn add @iconify-json/lucide
# or pnpm
pnpm add @iconify-json/lucide


rm -rf node_modules
rm pnpm-lock.yaml # or yarn.lock
pnpm install # or yarn install