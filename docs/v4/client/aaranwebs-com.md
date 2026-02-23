
## compose docker image
```
docker compose -f docker/client/demo-codexsun-com.yml up -d
```

```
demo.codexsun.com
```

```
docker exec -it demo_codexsun_com bash
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
 cd etc/nginx/sites-available/
```

```
sudo nano thetirupurtextiles.com
```

```
server {
    listen 80;
    server_name thetirupurtextiles.com;

    location / {
        proxy_pass http://127.0.0.1:7023;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
```
sudo ln -s /etc/nginx/sites-available/thetirupurtextiles.com /etc/nginx/sites-enabled/
```

```
sudo certbot --nginx
```

```
sudo nginx -t
```

```
sudo systemctl reload nginx
```

