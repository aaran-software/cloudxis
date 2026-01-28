#!/usr/bin/env python3
import subprocess
import os
from pathlib import Path

# ================= CONFIG =================
APP_USER = "devops"
WEB_USER = "www-data"
PHP_VERSION = "8.4"

NGINX_PORT = 7001
DOMAIN = "techmedia.in"

APP_BASE = "/home/devops/cloud"
APP_DIR = f"{APP_BASE}/codexsun"
GIT_REPO = "https://github.com/aaran-software/codexsun.git"
# =========================================


def run(cmd, cwd=None):
    print(f"\n▶ {cmd}")
    subprocess.run(cmd, shell=True, check=True, cwd=cwd)


def sudo(cmd):
    run(f"sudo {cmd}")


def add_host():
    sudo(
        f"""bash -c "grep -q '{DOMAIN}' /etc/hosts || echo '127.0.0.1 {DOMAIN}' >> /etc/hosts" """
    )


def fix_fs():
    sudo("chmod o+x /home /home/devops /home/devops/cloud")
    sudo(f"mkdir -p /var/log/php{PHP_VERSION}-fpm")
    sudo(f"chown -R {WEB_USER}:{WEB_USER} /var/log/php{PHP_VERSION}-fpm")


def clone_app():
    os.makedirs(APP_BASE, exist_ok=True)
    if not os.path.isdir(APP_DIR):
        run(f"git clone {GIT_REPO} {APP_DIR}")


def php_config():
    sudo(
        f"""bash -c 'cat > /etc/php/{PHP_VERSION}/fpm/pool.d/{DOMAIN}.conf <<EOF
[{DOMAIN}]
user = {WEB_USER}
group = {WEB_USER}
listen = /run/php/php{PHP_VERSION}-{DOMAIN}.sock
listen.owner = {WEB_USER}
listen.group = {WEB_USER}
listen.mode = 0660
pm = dynamic
pm.max_children = 20
clear_env = no
EOF'
"""
    )
    sudo(f"systemctl restart php{PHP_VERSION}-fpm")


def nginx_config():
    sudo(
        f"""bash -c 'cat > /etc/nginx/sites-available/{DOMAIN} <<EOF
server {{
    listen {NGINX_PORT};
    server_name {DOMAIN};
    root {APP_DIR}/public;

    index index.php index.html;

    location / {{
        try_files \\$uri \\$uri/ /index.php?\\$query_string;
    }}

    location ~ \\.php$ {{
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php{PHP_VERSION}-{DOMAIN}.sock;
    }}

    location ~ /\\. {{
        deny all;
    }}
}}
EOF'
"""
    )

    sudo(f"ln -sf /etc/nginx/sites-available/{DOMAIN} /etc/nginx/sites-enabled/{DOMAIN}")
    sudo("nginx -t")
    sudo("systemctl restart nginx")


def laravel_build():
    env = Path(APP_DIR) / ".env"
    if not env.exists():
        run("cp .env.example .env", cwd=APP_DIR)

    sudo(f"chown -R {APP_USER}:{WEB_USER} {APP_DIR}")
    run("composer install --no-dev --optimize-autoloader", cwd=APP_DIR)
    run("php artisan key:generate --force", cwd=APP_DIR)
    run("php artisan optimize", cwd=APP_DIR)

    sudo(f"chown -R {WEB_USER}:{WEB_USER} {APP_DIR}")
    sudo(f"chmod -R 775 {APP_DIR}/storage {APP_DIR}/bootstrap/cache")


def main():
    print(f"\n=== SETUP {DOMAIN} ===")
    add_host()
    fix_fs()
    clone_app()
    php_config()
    nginx_config()
    laravel_build()
    print(f"\n✅ http://{DOMAIN}:{NGINX_PORT}")


if __name__ == "__main__":
    main()
