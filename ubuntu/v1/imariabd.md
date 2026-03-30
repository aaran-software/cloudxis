Below is a **matching Ubuntu 24.04 install script** to install **MariaDB 11.8**, 
set the root password to **`DBPass1@@`**, enable **remote database access**, 
and apply your **`50-server.cnf` configuration**.

It assumes you are logged in as **`tmadmin`** and will use **sudo** like your previous script.

---

# MariaDB 11.8 Installer Script

Save as:

```bash
sudo nano imariadb.sh
```

Run:

```bash
sudo chmod +x imariadb.sh
```


```bash
./imariadb.sh
```

---

```bash
#!/usr/bin/env bash

# =========================================================
# MariaDB 11.8 Installer – Ubuntu 24.04
# Remote access enabled + custom config
# =========================================================

set -e

DBPASS="DbPass1@@"

echo "Installing MariaDB repository..."

sudo apt update
sudo apt install -y curl gnupg ca-certificates

curl -LsS https://r.mariadb.com/downloads/mariadb_repo_setup | sudo bash -s -- --mariadb-server-version=11.8

echo "Installing MariaDB server..."

sudo apt update
sudo apt install -y mariadb-server mariadb-client

echo "Stopping MariaDB..."

sudo systemctl stop mariadb

echo "Writing configuration..."

sudo tee /etc/mysql/mariadb.conf.d/50-server.cnf > /dev/null <<EOF
[server]
user = mysql
pid-file = /run/mysqld/mysqld.pid
socket = /run/mysqld/mysqld.sock
basedir = /usr
datadir = /var/lib/mysql
tmpdir = /tmp
lc-messages-dir = /usr/share/mysql
bind-address = 0.0.0.0
log_error = /var/log/mysql/error.log

[mysqld]
innodb_file_format = Barracuda
innodb_file_per_table = 1
innodb_large_prefix = 1
bind-address = 0.0.0.0
max_connections = 200
wait_timeout = 60
interactive_timeout = 60
thread_cache_size = 50
table_open_cache = 4000
innodb_buffer_pool_size = 2G

# Character Set Settings
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

# Performance
query_cache_size = 24M
query_cache_type = 1

[mysql]
default-character-set = utf8mb4

[client]
default-character-set = utf8mb4
connect_timeout = 30
EOF

echo "Creating log directory..."

sudo mkdir -p /var/log/mysql
sudo chown mysql:mysql /var/log/mysql

echo "Starting MariaDB..."

sudo systemctl start mariadb
sudo systemctl enable mariadb

echo "Configuring root password..."

sudo mysql <<MYSQL_SCRIPT

ALTER USER 'root'@'localhost' IDENTIFIED BY '${DBPASS}';
CREATE USER 'root'@'%' IDENTIFIED BY '${DBPASS}';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;

FLUSH PRIVILEGES;

MYSQL_SCRIPT

echo "Opening firewall for remote access..."

sudo ufw allow 3306/tcp || true

echo
echo "======================================"
echo "MariaDB 11.8 Installed Successfully"
echo "======================================"
echo
echo "Root Password:"
echo "$DBPASS"
echo
echo "Remote access enabled on port 3306"
echo
echo "Test connection:"
echo
echo "mysql -u root -p -h SERVER_IP"
echo
```

---

# What This Script Does

### 1️⃣ allow 3306/tcp remote

```bash
sudo ufw allow 3306/tcp || true
```


# After Installation

Test locally:

```bash
mariadb -u root -p
```

---

# Important Security Note ⚠️

Allowing **`root@%`** is **not recommended for production**.

Better approach:

```sql
CREATE USER 'devops'@'%' IDENTIFIED BY 'Devops@1234';
GRANT ALL PRIVILEGES ON *.* TO 'devops'@'%';
```

---

✅ If you'd like, I can also give you a **much better MariaDB config for ERPNext/Frappe** that improves:

* worker queue speed
* background jobs
* large reports
* 10k+ concurrent users

It performs **much faster than the default ERPNext database tuning.**
