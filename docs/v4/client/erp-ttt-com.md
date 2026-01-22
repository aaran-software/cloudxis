
## compose docker image
```
docker compose -f docker/client/erp-ttt-com.yml up -d
```

```
erp.thetirupurtextiles.com
```

```
docker exec -it erp_ttt_com bash
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




