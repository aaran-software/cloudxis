#!/usr/bin/env python3
import subprocess
import os
from pathlib import Path
import sys

APP_BASE = "/home/devops/cloud"
APP_DIR = f"{APP_BASE}/codexsun"
GIT_REPO = "https://github.com/sundar-aaran/cxlaravel.git"

APP_USER = "devops"
WEB_USER = "www-data"
PHP_VERSION = "8.4"
NGINX_PORT = 7001
DOMAIN = "techmedia.in"


# -------------------------
# HELPERS
# -------------------------
def run(cmd, cwd=None, check=True):
    print(f"\n▶ {cmd}")
    subprocess.run(cmd, shell=True, check=check, cwd=cwd)


def sudo(cmd, check=True):
    run(f"sudo {cmd}", check=check)


def has_systemd():
    return os.path.exists("/run/systemd/system")


def fatal(msg):
    print(f"\n❌ FATAL: {msg}")
    sys.exit(1)


# -------------------------
# INSTALL SYSTEM PACKAGES
# -------------------------
def install_packages():
    sudo("apt update")
    sudo("apt install -y software-properties-common curl ca-certificates git")

    sudo("add-apt-repository ppa:ondrej/php -y")
    sudo("curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -")

    sudo("apt remove -y composer || true")

    sudo(
        "apt install -y "
        "nginx nodejs "
        f"php{PHP_VERSION}-fpm php{PHP_VERSION}-cli "
        f"php{PHP_VERSION}-mysql php{PHP_VERSION}-xml "
        f"php{PHP_VERSION}-curl php{PHP_VERSION}-mbstring "
        f"php{PHP_VERSION}-zip php{PHP_VERSION}-gd"
    )

    run("php -r \"copy('https://getcomposer.org/installer', 'composer-setup.php');\"")
    sudo("php composer-setup.php --install-dir=/usr/local/bin --filename=composer")
    run("php -r \"unlink('composer-setup.php');\"")

    run("composer --version")


# -------------------------
# CLONE + VERIFY APP
# -------------------------
def clone_app():
    os.makedirs(APP_BASE, exist_ok=True)

    if not os.path.isdir(APP_DIR):
        print("📥 Cloning repository...")
        run(f"git clone {GIT_REPO} {APP_DIR}")
    else:
        print("📁 App directory exists, skipping clone")

    # ---- HARD VALIDATION ----
    if not (Path(APP_DIR) / "composer.json").exists():
        fatal("composer.json not found – repo is not a Laravel project")

    if not (Path(APP_DIR) / "artisan").exists():
        fatal("artisan not found – invalid Laravel structure")


# -------------------------
# PHP-FPM CONFIG
# -------------------------
def configure_php():
    sudo(
        rf"""bash -c 'cat > /etc/php/{PHP_VERSION}/fpm/pool.d/www.conf <<EOF
[www]
user = {WEB_USER}
group = {WEB_USER}

listen = /run/php/php{PHP_VERSION}-fpm.sock
listen.owner = {WEB_USER}
listen.group = {WEB_USER}
listen.mode = 0660

pm = dynamic
pm.max_children = 30
pm.start_servers = 6
pm.min_spare_servers = 4
pm.max_spare_servers = 10
pm.max_requests = 1000
request_terminate_timeout = 120s
clear_env = no
EOF'
"""
    )

    sudo(
        rf"""bash -c 'cat > /etc/php/{PHP_VERSION}/fpm/conf.d/99-production.ini <<EOF
display_errors=Off
log_errors=On
error_reporting=E_ALL & ~E_DEPRECATED & ~E_STRICT
EOF'
"""
    )

    if has_systemd():
        sudo(f"systemctl restart php{PHP_VERSION}-fpm")
    else:
        sudo("pkill php-fpm || true")
        sudo(f"php-fpm{PHP_VERSION} --nodaemonize &")


# -------------------------
# NGINX CONFIG
# -------------------------
def configure_nginx():
    sudo(
        rf"""bash -c 'cat > /etc/nginx/sites-available/codexsun <<EOF
server {{
    listen {NGINX_PORT};
    server_name {DOMAIN};
    root {APP_DIR}/public;
    index index.php index.html;

    location / {{
        try_files \$uri \$uri/ /index.php?\$query_string;
    }}

    location ~ \.php$ {{
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php{PHP_VERSION}-fpm.sock;
        fastcgi_read_timeout 300;
    }}

    location ~ /\. {{
        deny all;
    }}
}}
EOF'
"""
    )

    sudo("ln -sf /etc/nginx/sites-available/codexsun /etc/nginx/sites-enabled/codexsun")
    sudo("rm -f /etc/nginx/sites-enabled/default")

    sudo("nginx -t")

    if has_systemd():
        sudo("systemctl restart nginx")
    else:
        sudo("pkill nginx || true")
        sudo("nginx")


# -------------------------
# LARAVEL BUILD
# -------------------------
def build_laravel():
    env = Path(APP_DIR) / ".env"
    env_example = Path(APP_DIR) / ".env.example"

    if not env.exists():
        if env_example.exists():
            run("cp .env.example .env", cwd=APP_DIR)
        else:
            fatal(".env.example missing – provide .env manually")

    sudo(f"chown -R {APP_USER}:{WEB_USER} {APP_DIR}")
    sudo(f"find {APP_DIR} -type d -exec chmod 775 {{}} \\;")
    sudo(f"find {APP_DIR} -type f -exec chmod 664 {{}} \\;")

    run("composer install --no-dev --optimize-autoloader", cwd=APP_DIR)
    run("php artisan key:generate --force", cwd=APP_DIR)
    run("php artisan storage:link", cwd=APP_DIR)

    if (Path(APP_DIR) / "package.json").exists():
        run("npm install", cwd=APP_DIR)
        run("npm run build", cwd=APP_DIR)

    run("php artisan optimize", cwd=APP_DIR)

    sudo(f"chown -R {WEB_USER}:{WEB_USER} {APP_DIR}/storage {APP_DIR}/bootstrap/cache")
    sudo(f"chmod -R 775 {APP_DIR}/storage {APP_DIR}/bootstrap/cache")


# -------------------------
# MAIN
# -------------------------
def main():
    print("\n=== Laravel + Nginx + PHP 8.4 (FULL SAFE INSTALL) ===")
    install_packages()
    clone_app()
    configure_php()
    configure_nginx()
    build_laravel()
    print(f"\n✅ DONE → http://localhost:{NGINX_PORT}")


if __name__ == "__main__":
    main()
