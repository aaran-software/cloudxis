
## compose docker image
```
docker compose -f docker/client/dev-logicx-in.yml up -d
```

```
dev.logicx.in
```

```
docker exec -it dev_logicx_in bash
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


bench get-app gameplan
bench get-app slides
bench get-app telephony


bench --site dev.logicx.in install-app gameplan
bench --site dev.logicx.in install-app slides


bench get-app lms
bench get-app helpdesk

bench --site dev.logicx.in install-app lms
bench --site dev.logicx.in install-app telephony
bench --site dev.logicx.in install-app helpdesk


```
 cd etc/nginx/sites-available/
```

```
sudo nano dev.logicx.in
```

```
server {
    listen 80;
    server_name dev.logicx.in;

    location / {
        proxy_pass http://127.0.0.1:8040;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```


sudo ln -s /etc/nginx/sites-available/dev.logicx.in /etc/nginx/sites-enabled/


```
sudo certbot --nginx
```

```
sudo nginx -t
```

```
sudo systemctl reload nginx
```

bench migrate
bench build