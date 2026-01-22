
## compose docker image
```
docker compose -f docker/client/erp-techmedia-in.yml up -d
```

```
erp.techmedia.in
```

```
docker exec -it erp_techmedia_in bash
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




