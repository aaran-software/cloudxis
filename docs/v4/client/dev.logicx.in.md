
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




bench --site dev.logicx.in install-app gameplan
bench --site dev.logicx.in install-app slides
