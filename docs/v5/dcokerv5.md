To build and run CodexSun v3 using Docker, follow these steps:

### 2. create network for codexion if not

```
docker network create codexion-network
```

## For php image

```
docker build --no-cache -t codexsun:v6 -f docker/cloud/Dockerfile-php docker/cloud
```

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