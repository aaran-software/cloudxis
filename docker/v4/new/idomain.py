#!/usr/bin/env python3
import subprocess
from pathlib import Path

# =====================================================
# GLOBAL CONFIG
# =====================================================

APP_USER = "devops"
PHP_VERSION = "8.4"

APP_BASE = "/home/devops/cloud"
GIT_REPO = "https://github.com/aaran-software/codexsun.git"

DB_ROOT = {
    "HOST": "mariadb",
    "PORT": "3306",
    "USER": "root",
    "PASS": "DbPass1@@",
}

APPS = [
    {"domain": "tmnext.in", "port": 7021, "db": "tmnext_db"},
    {"domain": "logicx.in", "port": 7022, "db": "logicx_db"},
]

# =====================================================
# HELPERS
# =====================================================

def run(cmd, cwd=None):
    print(f"\n▶ {cmd}")
    subprocess.check_call(cmd, shell=True, cwd=cwd)

def sudo(cmd):
    run(f"sudo {cmd}")

def mysql_exec(sql):
    run(
        f"mysql -u{DB_ROOT['USER']} -p{DB_ROOT['PASS']} "
        f"-h {DB_ROOT['HOST']} -P {DB_ROOT['PORT']} --protocol=tcp "
        f"-e \"{sql}\""
    )

def database_exists(db):
    result = subprocess.check_output(
        f"mysql -u{DB_ROOT['USER']} -p{DB_ROOT['PASS']} "
        f"-h {DB_ROOT['HOST']} -P {DB_ROOT['PORT']} --protocol=tcp "
        f"-Nse \"SHOW DATABASES LIKE '{db}';\"",
        shell=True,
        text=True,
    )
    return bool(result.strip())

# =====================================================
# SYSTEM SETUP
# =====================================================

def system_setup():
    sudo("chmod o+x /home /home/devops")

    # base app directory
    sudo(f"mkdir -p {APP_BASE}")
    sudo(f"chown -R {APP_USER}:{APP_USER} {APP_BASE}")

    # php-fpm runtime dirs
    sudo(f"mkdir -p /var/log/php{PHP_VERSION}-fpm /run/php")
    sudo(f"chown -R {APP_USER}:{APP_USER} /var/log/php{PHP_VERSION}-fpm /run/php")

    # 🔑 CRITICAL FIX: allow nginx to access php-fpm sockets
    sudo("usermod -aG devops www-data")

# =====================================================
# FILESYSTEM (DOCKER SAFE)
# =====================================================

def ensure_app_dir(app_dir):
    sudo(f"mkdir -p {app_dir}")
    sudo(f"chown -R {APP_USER}:{APP_USER} {app_dir}")

# =====================================================
# PER APP
# =====================================================

def add_host(domain):
    sudo(
        f"""bash -c "grep -q '{domain}' /etc/hosts || \
echo '127.0.0.1 {domain}' >> /etc/hosts" """
    )

def clone_app(app_dir):
    if not Path(app_dir, ".git").exists():
        run(f"git clone {GIT_REPO} {app_dir}")

def php_fpm_config(domain):
    sudo(
        f"""bash -c 'cat > /etc/php/{PHP_VERSION}/fpm/pool.d/{domain}.conf <<EOF
[{domain}]
user = {APP_USER}
group = {APP_USER}
listen = /run/php/php{PHP_VERSION}-{domain}.sock
listen.owner = {APP_USER}
listen.group = {APP_USER}
listen.mode = 0660
pm = dynamic
pm.max_children = 20
pm.start_servers = 4
pm.min_spare_servers = 2
pm.max_spare_servers = 6
clear_env = no
EOF'
"""
    )

def nginx_config(domain, port, app_dir):
    sudo(
        f"""bash -c 'cat > /etc/nginx/sites-available/{domain} <<EOF
server {{
    listen {port};
    server_name {domain};
    root {app_dir}/public;

    index index.php index.html;

    location / {{
        try_files \\$uri \\$uri/ /index.php?\\$query_string;
    }}

    location ~ \\.php$ {{
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php{PHP_VERSION}-{domain}.sock;
    }}

    location ~ /\\. {{
        deny all;
    }}
}}
EOF'
"""
    )
    sudo(f"ln -sf /etc/nginx/sites-available/{domain} /etc/nginx/sites-enabled/{domain}")

def rewrite_env(app_dir, domain, db):
    env_path = Path(app_dir) / ".env"
    if not env_path.exists():
        run("cp .env.example .env", cwd=app_dir)

    updates = {
        "APP_NAME": domain.upper().replace(".", "_"),
        "APP_ENV": "local",
        "APP_DEBUG": "true",
        "APP_URL": f"http://{domain}",
        "DB_CONNECTION": "mariadb",
        "DB_HOST": DB_ROOT["HOST"],
        "DB_PORT": DB_ROOT["PORT"],
        "DB_DATABASE": db,
        "DB_USERNAME": DB_ROOT["USER"],
        "DB_PASSWORD": DB_ROOT["PASS"],
    }

    lines = env_path.read_text().splitlines()
    new = []
    seen = set()

    for line in lines:
        if "=" in line and not line.startswith("#"):
            k = line.split("=", 1)[0]
            if k in updates:
                new.append(f"{k}={updates[k]}")
                seen.add(k)
                continue
        new.append(line)

    for k, v in updates.items():
        if k not in seen:
            new.append(f"{k}={v}")

    env_path.write_text("\n".join(new) + "\n")

def laravel_setup(app_dir, db):
    run("composer install --no-dev --optimize-autoloader", cwd=app_dir)
    run("php artisan key:generate --force", cwd=app_dir)

    if not database_exists(db):
        if input(f"👉 Create database `{db}`? (y/N): ").lower() == "y":
            mysql_exec(
                f"CREATE DATABASE {db} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
            )

    if Path(app_dir, "package.json").exists():
        run("npm install", cwd=app_dir)
        run("npm run build", cwd=app_dir)

    if input("👉 Run migrations? (y/N): ").lower() == "y":
        run("php artisan migrate --force", cwd=app_dir)
        run("php artisan optimize", cwd=app_dir)

# =====================================================
# MAIN
# =====================================================

def main():
    system_setup()

    for app in APPS:
        domain = app["domain"]
        port = app["port"]
        db = app["db"]

        app_dir = f"{APP_BASE}/{domain}/app"

        print(f"\n=== SETUP {domain} ===")

        ensure_app_dir(app_dir)
        add_host(domain)
        clone_app(app_dir)
        php_fpm_config(domain)
        nginx_config(domain, port, app_dir)
        rewrite_env(app_dir, domain, db)
        laravel_setup(app_dir, db)

    sudo("nginx -t")
    sudo("pkill php-fpm || true")
    sudo("pkill nginx || true")
    sudo(f"php-fpm{PHP_VERSION} -D")
    sudo("nginx")

    print("\n✅ ALL APPLICATIONS INSTALLED (SINGLE USER, DOCKER SAFE)")

if __name__ == "__main__":
    main()
