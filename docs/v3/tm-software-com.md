
## compose docker image
```
sudo docker compose -f docker/cloud/tm-software-com.yml up -d
```

```
sudo docker exec -it tm_software_com bash
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




