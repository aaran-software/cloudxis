#!/usr/bin/env python3
import argparse
import subprocess
import os
import sys
from pathlib import Path

# ---------------- CONFIG ----------------
BASE_DIR = Path("/home/devops/cloud")
NGINX_AVAILABLE = Path("/etc/nginx/sites-available")
NGINX_ENABLED = Path("/etc/nginx/sites-enabled")

APP_USER = "devops"
WEB_USER = "www-data"
PHP_VERSION = "8.4"

# ---------------- HELPERS ----------------
def run(cmd, cwd=None, check=True):
    print(f"\n▶ {cmd}")
    subprocess.run(cmd, shell=True, cwd=cwd, check=check)

def sudo(cmd, cwd=None):
    run(f"sudo {cmd}", cwd=cwd)

def ensure_root_for_nginx():
    if os.geteuid() != 0:
        print("⚠ nginx config requires sudo")
        print("👉 re-run with: sudo python3 ilaravel.py ...")
        sys.exit(1)

# ---------------- APP LOGIC ----------------
def app_dir(name):
    return BASE_DIR / name

def nginx_conf(name):
    return NGINX_AVAILABLE / name

# ---------------- CREATE APP ----------------
def create_app(args):
    ensure_root_for_nginx()

    name = args.name
    repo = args.repo
    domain = args.domain
    port = args.port

    target = app_dir(name)

    if target.exists():
        print("❌ App already exists")
        sys.exit(1)

    print(f"\n🚀 Creating Laravel app: {name}")

    # Clone
    run(f"git clone {repo} {target}")

    # .env
    if not (target / ".env").exists():
        run("cp .env.example .env", cwd=target)

    # Permissions (build-time)
    sudo(f"chown -R {APP_USER}:{WEB_USER} {target}")
    sudo(f"find {target} -type d -exec chmod 775 {{}} \\;")
    sudo(f"find {target} -type f -exec chmod 664 {{}} \\;")

    # Build
    run("composer install --no-dev --optimize-autoloader", cwd=target)
    run("php artisan key:generate --force", cwd=target)
    run("php artisan storage:link", cwd=target)

    if (target / "package.json").exists():
        run("npm install", cwd=target)
        run("npm run build", cwd=target)

    run("php artisan optimize", cwd=target)

    # Runtime permissions
    sudo(f"chown -R {WEB_USER}:{WEB_USER} {target}")
    sudo(f"chmod -R 775 {target}/storage {target}/bootstrap/cache")

    # Nginx
    nginx_block = f"""
server {{
    listen {port};
    server_name {domain};
    root {target}/public;
    index index.php index.html;

    location / {{
        try_files $uri $uri/ /index.php?$query_string;
    }}

    location ~ \\.php$ {{
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php{PHP_VERSION}-fpm.sock;
    }}

    location ~ /\\. {{
        deny all;
    }}
}}
"""
    sudo(f"bash -c 'cat > {nginx_conf(name)} <<EOF\n{nginx_block}\nEOF'")
    sudo(f"ln -sf {nginx_conf(name)} {NGINX_ENABLED / name}")

    sudo("nginx -t")
    sudo("nginx -s reload")

    print(f"\n✅ App created: {name}")
    print(f"🌐 http://{domain}:{port}")

# ---------------- DELETE APP ----------------
def delete_app(args):
    ensure_root_for_nginx()

    name = args.name
    target = app_dir(name)

    if not target.exists():
        print("❌ App not found")
        sys.exit(1)

    print(f"\n🗑 Deleting app: {name}")

    sudo(f"rm -rf {target}")
    sudo(f"rm -f {NGINX_AVAILABLE / name}")
    sudo(f"rm -f {NGINX_ENABLED / name}")

    sudo("nginx -t")
    sudo("nginx -s reload")

    print("✅ App deleted")

# ---------------- REDEPLOY APP ----------------
def redeploy_app(args):
    name = args.name
    target = app_dir(name)

    if not target.exists():
        print("❌ App not found")
        sys.exit(1)

    print(f"\n🔄 Redeploying app: {name}")

    run("git pull", cwd=target)
    run("composer install --no-dev --optimize-autoloader", cwd=target)

    if (target / "package.json").exists():
        run("npm install", cwd=target)
        run("npm run build", cwd=target)

    run("php artisan migrate --force", cwd=target, check=False)
    run("php artisan optimize", cwd=target)

    sudo(f"chown -R {WEB_USER}:{WEB_USER} {target}")
    sudo(f"chmod -R 775 {target}/storage {target}/bootstrap/cache")

    print("✅ Redeploy complete")

# ---------------- LIST APPS ----------------
def list_apps(_):
    print("\n📦 Installed apps:")
    if not BASE_DIR.exists():
        return
    for d in BASE_DIR.iterdir():
        if d.is_dir():
            print(" -", d.name)

# ---------------- CLI ----------------
def main():
    parser = argparse.ArgumentParser(description="Multi Laravel App Manager")
    sub = parser.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("create")
    c.add_argument("--name", required=True)
    c.add_argument("--repo", required=True)
    c.add_argument("--domain", default="localhost")
    c.add_argument("--port", required=True)
    c.set_defaults(func=create_app)

    d = sub.add_parser("delete")
    d.add_argument("--name", required=True)
    d.set_defaults(func=delete_app)

    r = sub.add_parser("redeploy")
    r.add_argument("--name", required=True)
    r.set_defaults(func=redeploy_app)

    l = sub.add_parser("list")
    l.set_defaults(func=list_apps)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
