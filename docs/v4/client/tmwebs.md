
## compose docker image
```
docker compose -f docker/client/tmwebs.yml up -d
```

```
tmwebs
```

```
docker exec -it tmwebs bash
```

# for file folder permission

```
 sudo chown -R $USER:$USER .
```

```
sudo chown -R devops:devops .
```

```
sudo su - devops
```

```
git clone https://github.com/aaran-software/codexsun.git
```

```
pnpm install
```
```
cd apps/backend
```

```
cp .env.example .env
```

```
sudo pkill php-fpm8.4 || true
sudo php-fpm8.4 -D

sudo nginx -s reload
```

idomain.py
 ├─ clone repo
 ├─ composer install
 ├─ initial permissions
 ├─ npm install + build
 └─ NEVER touch git again

ideploy.py
 ├─ chown everything → devops
 ├─ git reset / pull
 ├─ npm update + build
 ├─ chown runtime dirs → www-data
 └─ php artisan optimize



```
sudo nano shop.thetirupurtextiles.com
```

```
server {
    listen 80;
    server_name shop.thetirupurtextiles.com;

    location / {
        proxy_pass http://127.0.0.1:7021;

        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header Connection "";
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }
}
```


sudo ln -s /etc/nginx/sites-available/shop.thetirupurtextiles.com /etc/nginx/sites-enabled/


```
sudo certbot --nginx
```

```
sudo nginx -t
```

```
sudo systemctl reload nginx
```