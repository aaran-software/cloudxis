```
cd /home/devops/cloud/codexsun
```

```
php artisan key:generate --force
```
```
php artisan storage:link
```
```
php artisan storage:unlink
```

```
php artisan optimize:clear
```

```
php artisan optimize
```
```
sudo chown -R www-data:www-data storage bootstrap/cache
```

```
sudo chmod -R 775 storage bootstrap/cache
```