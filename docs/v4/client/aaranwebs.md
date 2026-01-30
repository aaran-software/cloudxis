
## compose docker image
```
docker compose -f docker/client/aaranwebs.yml up -d
```

```
aaranwebs
```

```
docker exec -it aaranwebs bash
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
