Perfect 👍 since you want to **keep your current container** and just reinstall **Nginx cleanly**, here is a safe, clean reset procedure.

---

# 🧹 STEP 1 — Completely Remove Old Nginx

```bash
sudo systemctl stop nginx
sudo apt remove --purge nginx nginx-common nginx-core -y
sudo rm -rf /etc/nginx
sudo rm -rf /var/www/html
sudo apt autoremove -y
```

This removes:

* Old configs
* Old SSL references
* Old site files

---

# 🧹 STEP 2 — Reinstall Fresh Nginx

```bash
sudo apt update
sudo apt install nginx -y
```

Enable it:

```bash
sudo systemctl enable nginx
sudo systemctl start nginx
```

Test:

```bash
sudo nginx -t
```

---

# 🧹 STEP 3 — Clean Default Config

Remove default site:

```bash
sudo rm /etc/nginx/sites-enabled/default
sudo rm /etc/nginx/sites-available/default
```

---

# 🚀 STEP 4 — Create Clean Reverse Proxy Config

Create new file:

```bash
sudo nano /etc/nginx/sites-available/thetirupurtextiles
```

Paste this clean version:

```nginx
server {
    listen 80;
    server_name thetirupurtextiles.com www.thetirupurtextiles.com shop.thetirupurtextiles.com;

    location / {
        proxy_pass http://127.0.0.1:7021;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header Connection "";
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_read_timeout 300;
    }
}
```

Enable it:

```bash
sudo ln -s /etc/nginx/sites-available/thetirupurtextiles /etc/nginx/sites-enabled/
```

Test & reload:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

# 🔐 STEP 5 — Reinstall Certbot Cleanly

```bash
sudo snap install core
sudo snap refresh core
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

Generate SSL:

```bash
sudo certbot --nginx -d thetirupurtextiles.com -d www.thetirupurtextiles.com -d shop.thetirupurtextiles.com
```

It will automatically:

* Create HTTPS block
* Add redirect
* Reload nginx

---

# 🔥 STEP 6 — Secure Ports

Make sure only 80 & 443 are open:

```bash
sudo ufw allow 80
sudo ufw allow 443
sudo ufw deny 7021
```

---

# 🧠 Final Architecture (Clean)

```
Browser → 443 → Nginx → 7021 (FrankenPHP container)
```

Port 7021 should NOT be publicly exposed.

---

# 🏁 Test

After setup:

```
https://thetirupurtextiles.com
```

Should work without :7021

---

If you want, next I can:

* Optimize Nginx for Octane performance
* Add gzip + security headers
* Add HTTP/2
* Add caching rules
* Tune for your VPS RAM

Tell me your VPS RAM + CPU cores 🚀
