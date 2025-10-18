To build and run CodexSun v3 using Docker, follow these steps:

## For Frappe Instance

```
docker build -t codexsun:v3 -f docker/cloud/Dockerfile-frappe docker/cloud
```

## For Node Instance

```
docker build -t codexsun:v3 -f docker/cloud/Dockerfile-node docker/cloud
```

### 2. create network for codexion

```
docker network create codexion-network
```

### 3. create container for mariadb

```
 docker compose -f docker/cloud/mariadb.yml up -d
```

### 4. Check mariadb is installed

```
docker exec -it mariadb mariadb -u root -p
```

# remote access for root user 

```
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```
