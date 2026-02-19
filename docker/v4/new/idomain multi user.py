#!/usr/bin/env python3
import subprocess
import os
from pathlib import Path

# =====================================================
# GLOBAL CONFIG
# =====================================================

APP_USER = "devops"
WEB_USER = "www-data"
PHP_VERSION = "8.4"

APP_BASE = "/home/devops/cloud"
GIT_REPO = "https://github.com/aaran-software/codexsun.git"

# ---------- DATABASE ROOT ACCESS ----------
DB_ROOT = {
    "HOST": "mariadb",
    "PORT": "3306",
    "USER": "root",
    "PASS": "DbPass1@@",
}

# ---------- MULTI APP DEFINITIONS ----------
APPS = [
    {
        "domain": "codexsun.com",
        "port": 7021,
        "db": "codexsun_db",
    },
    {
        "domain": "tmnext.in",
        "port": 7022,
        "db": "tmnext_db",
    },
]


# =====================================================
# HELPERS
# =====================================================

def run(cmd, cwd=None, check=True):
    print(f"\n▶ {cmd}")
    subprocess.run(cmd, shell=True, check=check, cwd=cwd)


def sudo(cmd, check=True):
    run(f"sudo {cmd}", check=check)


def mysql_exec(sql, check=True):
    cmd = [
        "mysql",
        f"-u{DB_ROOT['USER']}",
        f"-p{DB_ROOT['PASS']}",
        "-h", DB_ROOT["HOST"],
        "-P", DB_ROOT["PORT"],
        "--protocol=tcp",
    ]
    print("\n▶ mysql (TCP)")
    subprocess.run(cmd, input=sql, text=True, check=check)


def database_exists(db):
    result = subprocess.run(
        [
            "mysql",
            f"-u{DB_ROOT['USER']}",
            f"-p{DB_ROOT['PASS']}",
            "-h", DB_ROOT["HOST"],
            "-P", DB_ROOT["PORT"],
            "--protocol=tcp",
            "-Nse",
            f"SHOW DATABASES LIKE '{db}';",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
    )
    return bool(result.stdout.strip())


# =====================================================
# SYSTEM SETUP (ONCE)
# =====================================================

def system_setup():
    sudo("chmod o+x /home /home/devops /home/devops/cloud", check=False)
    sudo(f"mkdir -p /var/log/php{PHP_VERSION}-fpm /run/php")
    sudo(f"chown -R {WEB_USER}:{WEB_USER} /var/log/php{PHP_VERSION}-fpm /run/php")
    sudo("mkdir -p /var/log/nginx /run/nginx")
    sudo("chown -R root:root /var/log/nginx /run/nginx")
    sudo("chmod 755 /var/log/nginx /run/nginx")


# =====================================================
# PER-APP STEPS
# =====================================================

def add_host(domain):
    sudo(f"""bash -c "grep -q '{domain}' /etc/hosts || echo '127.0.0.1 {domain}' >> /etc/hosts" """)


def clone_app(app_dir):
    if not os.path.isdir(f"{app_dir}/.git"):
        run(f"git clone {GIT_REPO} {app_dir}")


def php_fpm_config(domain):
    sudo(
        f"""bash -c 'cat > /etc/php/{PHP_VERSION}/fpm/pool.d/{domain}.conf <<EOF
[{domain}]
user = {WEB_USER}
group = {WEB_USER}
listen = /run/php/php{PHP_VERSION}-{domain}.sock
listen.owner = {WEB_USER}
listen.group = {WEB_USER}
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
    new_lines = []
    seen_keys = set()

    for line in lines:
        if "=" in line and not line.strip().startswith("#"):
            key, _ = line.split("=", 1)
            if key in updates:
                new_lines.append(f"{key}={updates[key]}")
                seen_keys.add(key)
                continue
        new_lines.append(line)

    # append missing keys
    for k, v in updates.items():
        if k not in seen_keys:
            new_lines.append(f"{k}={v}")

    env_path.write_text("\n".join(new_lines) + "\n")


def laravel_setup(app_dir, db):
    sudo(f"chown -R {APP_USER}:{WEB_USER} {app_dir}")
    run("composer install --no-dev --optimize-autoloader", cwd=app_dir)
    run("php artisan key:generate --force", cwd=app_dir)
    run("php artisan optimize", cwd=app_dir)

    if not database_exists(db):
        print(f"⚠️  Database `{db}` does not exist")
        if input("👉 Create database now? (y/N): ").lower() == "y":
            mysql_exec(f"CREATE DATABASE {db} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        else:
            return

    if not (Path(app_dir) / "package.json").exists():
        print("ℹ️  No package.json, skipping npm")
        return
    run("npm install", cwd=app_dir)
    run("npm run build", cwd=app_dir)

    if input("👉 Run migrations? (y/N): ").lower() == "y":
        run("php artisan migrate --force", cwd=app_dir)

        if (Path(app_dir) / "package.json").exists():
            run("npm install", cwd=app_dir)
            run("npm run build", cwd=app_dir)

    sudo(f"chown -R {WEB_USER}:{WEB_USER} {app_dir}")
    sudo(f"chown -R {WEB_USER}:{WEB_USER} {app_dir}/storage {app_dir}/bootstrap/cache")
    sudo(f"chmod -R 775 {app_dir}/storage {app_dir}/bootstrap/cache")


def restart_php():
    print("\n🔄 Restarting PHP-FPM")
    if is_systemd():
        sudo(f"systemctl restart php{PHP_VERSION}-fpm")
    else:
        sudo("pkill php-fpm || true")
        sudo(f"php-fpm{PHP_VERSION} -D")


def restart_nginx():
    print("\n🔄 Restarting Nginx")
    if is_systemd():
        sudo("systemctl restart nginx")
    else:
        sudo("pkill nginx || true")
        sudo("nginx")


# =====================================================
# MAIN
# =====================================================

def main():
    system_setup()

    for app in APPS:
        domain = app["domain"]
        port = app["port"]
        db = app["db"]

        app_dir = f"{APP_BASE}/{domain}"
        os.makedirs(app_dir, exist_ok=True)

        print(f"\n=== SETUP {domain} ===")

        add_host(domain)
        clone_app(app_dir)
        php_fpm_config(domain)
        nginx_config(domain, port, app_dir)
        rewrite_env(app_dir, domain, db)
        laravel_setup(app_dir, db)

        restart_nginx()
        restart_php()

print("\n✅ ALL APPLICATIONS INSTALLED")

if __name__ == "__main__":
    main()
