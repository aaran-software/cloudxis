```
sudo chown -R devops:devops .
```


# 1  Lifeshoppy

```
docker compose -f docker/cloud/client/lifeshoppy_com.yml up -d
```
### To open lifeshoppy_com in bash

```
docker exec -it lifeshoppy_com bash
```

# 2 sukraa garments

```
docker compose -f docker/cloud/client/sukraa_codexsun_com.yml up -d
```
### To open sukraa_codexsun_com in bash
```
docker exec -it sukraa_codexsun_com bash
```

# 3  ganapathi

```
docker compose -f docker/cloud/client/ganapathi_codexsun_com.yml up -d
```
### To open ganapathi_codexsun_com in bash

```
docker exec -it ganapathi_codexsun_com bash
```


# 4  flexcon_codexsun_com

```
docker compose -f docker/cloud/client/flexcon_codexsun_com.yml up -d
```
### To open flexcon_codexsun_com in bash

```
docker exec -it flexcon_codexsun_com bash
```


# 5  demo_codexsun_com

```
docker compose -f docker/cloud/client/demo_codexsun_com.yml up -d
```
### To open demo_codexsun_com in bash

```
docker exec -it demo_codexsun_com bash
```


# 6  smile_codexsun_com

```
docker compose -f docker/cloud/client/smile_codexsun_com.yml up -d
```
### To open smile_codexsun_com in bash

```
docker exec -it smile_codexsun_com bash
```

















```
cd /cloud/frappe-bench/sites/techmedia.in
```

```
cd /cloud/frappe-bench
```

```
bench start
```

```
bench migrate
```

```
bench clear-cache
```

```
bench clear-website-cache
```

```
bench clear-website-cache
```


```
bench update --patch
```

bench --site techmedia.in  set-maintenance-mode off

bench --site techmedia.in clear-cache
bench --site techmedia.in destroy-all-sessions



```
{
 "db_host": "mariadb",
 "db_name": "erp_tmnext_db",
 "db_password": "1JEOj5LlSYATfp9m",
 "db_type": "mariadb",
 "db_user": "erp_tmnext_db",
 "encryption_key": "KqMHdGdd40t7kIMi1dQ8QdnHR-B5fSjc6BKwSNmgtiI=",
 "nginx_port": 8000,
 "allow_cors":"*",
 "allow_signup":true,
 "cookie_samesite":"Lax",
 "cookie_secure":true,
 "user_type_doctype_limit": {
  "employee_self_service": 40
 }
}
```


```
server {
    listen 80;
    server_name techmedia.in;

    location / {
        proxy_pass http://127.0.0.1:3005;
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
        proxy_pass http://127.0.0.1:8006;
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
        proxy_pass http://127.0.0.1:8004;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

```





sudo ln -s /etc/nginx/sites-available/techmedia.in /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/erp.techmedia.in /etc/nginx/sites-enabled/

sudo ln -s /etc/nginx/sites-available/ganapathi.codexsun.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/smile.codexsun.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/flexcon.codexsun.com /etc/nginx/sites-enabled/

sudo nginx -t
sudo systemctl reload nginx


```
sudo certbot --nginx
```




curl -I http://techmedia.in

dig -I http://erp.techmedia.in

curl -I -v http://techmedia.in 2>&1 | grep "Connected to"

curl -I -v http://erp.techmedia.in 2>&1 | grep "Connected to"

nslookup techmedia.in 8.8.8.8

nslookup erp.techmedia.in 8.8.8.8

nslookup techmedia.in 1.1.1.1






history -c        # Clear the current session's history
history -w        # Write the empty history to the file

If you also want to remove the history file entirely:


rm ~/.bash_history


