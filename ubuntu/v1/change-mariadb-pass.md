It looks like the password reset **did not actually update the root authentication plugin**. On Ubuntu, MariaDB often uses the **`unix_socket` authentication plugin**, which ignores passwords and only allows `sudo` login.

Let’s fix it properly.

---

# 1️⃣ Login using sudo (socket authentication)

Try this first:

```bash
sudo mariadb
```

If it opens the MariaDB shell, continue.

---

# 2️⃣ Check root authentication

Run:

```sql
SELECT user,host,plugin FROM mysql.user WHERE user='root';
```

You will likely see something like:

```
root | localhost | unix_socket
```

---

# 3️⃣ Change root to password authentication

Run:

```sql
ALTER USER 'root'@'localhost'
IDENTIFIED VIA mysql_native_password
USING PASSWORD('DBPass1@@');
```

Then run:

```sql
CREATE USER IF NOT EXISTS 'root'@'%' IDENTIFIED BY 'DBPass1@@';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;

FLUSH PRIVILEGES;
```

Exit:

```sql
EXIT;
```

---

# 4️⃣ Test login again

```bash
mariadb -u root -p
```

Password:

```
DBPass1@@
```

---

# 5️⃣ Verify remote access

Inside MariaDB:

```sql
SELECT host,user FROM mysql.user;
```

You should see:

```
root  localhost
root  %
```

---

# ⚠️ If `sudo mariadb` **does not work**

Then we will use the **guaranteed reset method**:

```bash
sudo systemctl stop mariadb
sudo mariadbd-safe --skip-grant-tables --skip-networking &
mariadb
```

Then reset again.

---

✅ If you'd like, I can also show you a **single command that completely resets MariaDB root access on Ubuntu in ~10 seconds** (much faster than the manual safe-mode method).


Your MariaDB root account is **broken (no password + no unix_socket)**, so even `sudo mariadb` cannot log in. We need to reset it **again properly using skip-grant-tables** and directly update the `mysql.user` table.

Follow this **exact sequence**.

---

# 1️⃣ Stop MariaDB

```bash
sudo systemctl stop mariadb
```

---

# 2️⃣ Start MariaDB in recovery mode

Use the new binary name (since `mysqld_safe` is deprecated):

```bash
sudo mariadbd-safe --skip-grant-tables --skip-networking &
```

Wait **5–10 seconds**.

---

# 3️⃣ Login without password

```bash
mariadb
```

You should now get:

```
MariaDB [(none)]>
```

---

# 4️⃣ Reset root authentication

Run these commands:

```sql
FLUSH PRIVILEGES;

UPDATE mysql.user
SET plugin='mysql_native_password'
WHERE User='root' AND Host='localhost';

SET PASSWORD FOR 'root'@'localhost' = PASSWORD('DBPass1@@');

CREATE USER IF NOT EXISTS 'root'@'%' IDENTIFIED BY 'DBPass1@@';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;

FLUSH PRIVILEGES;
```

Exit:

```sql
EXIT;
```

---

# 5️⃣ Stop the recovery server

```bash
sudo pkill mariadbd
```

or

```bash
sudo killall mariadbd
```

---

# 6️⃣ Start MariaDB normally

```bash
sudo systemctl start mariadb
```

---

# 7️⃣ Test login

```bash
mariadb -u root -p
```

Password:

```
DBPass1@@
```

---

# 8️⃣ Verify remote access

Inside MariaDB:

```sql
SELECT user,host FROM mysql.user;
```

You should see:

```
root   localhost
root   %
```

---

✅ After this, these will work:

Local login

```
mariadb -u root -p
```

Remote login

```
mariadb -u root -p -h SERVER_IP
```

---

💡 **Important for ERPNext:**
Your `50-server.cnf` is missing **two critical settings required by Frappe**. Without them, **site creation may fail**.

If you want, I can give you the **correct ERPNext MariaDB 11 configuration used in production servers** (much faster and fully compatible).
