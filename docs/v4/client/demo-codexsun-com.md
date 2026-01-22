
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




