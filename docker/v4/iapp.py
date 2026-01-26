#!/usr/bin/env python3
import subprocess
import os
import sys
from pathlib import Path

# ================= CONFIG =================
BASE_DIR = Path("/home/devops/cloud")
NGINX_AVAILABLE = Path("/etc/nginx/sites-available")
NGINX_ENABLED = Path("/etc/nginx/sites-enabled")

APP_USER = "devops"
WEB_USER = "www-data"
PHP_VERSION = "8.4"

# ================= HELPERS =================
def run(cmd, cwd=None, check=True):
    print(f"\n▶ {cmd}")
    subprocess.run(cmd, shell=True, cwd=cwd, check=check)

def sudo(cmd, cwd=None, check=True):
    run(f"sudo {cmd}", cwd=cwd, check=check)

def has_cmd(cmd):
    return subprocess.run(
        f"command -v {cmd}",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ).returncode == 0

def require_root():
    if os.geteuid() != 0:
        print("\n❌ This action requires sudo")
        print("👉 Re-run with: sudo python3 iapp.py")
        sys.exit(1)

def ask(prompt, default=None):
    if default:
        v = input(f"{prompt} [{default}]: ").strip()
        return v if v else default
    return input(f"{prompt}: ").strip()

def app_dir(name):
    return BASE_DIR / name

# ================= NGINX SAFE APPLY =================
def nginx_apply():
    # Always test config
    sudo("nginx -t")

    # If nginx running → reload, else start
    if subprocess.run(
        "pgrep -x nginx",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ).returncode == 0:
        print("🔄 Reloading nginx")
        sudo("nginx -s reload", check=False)
    else:
        print("🚀 Starting nginx")
        sudo("nginx")

# ================= NODE INSTALL =================
def ensure_node():
    if has_cmd("npm"):
        return

    print("\n⚙ npm not found — installing Node.js LTS")
    require_root()

    run("curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -")
    run("sudo apt-get install -y nodejs")

    if not has_cmd("npm"):
        print("❌ npm installation failed")
        sys.exit(1)

    run("node -v")
    run("npm -v")

# ================= CREATE APP =================
def create_app():
    require_root()

    print("\n🚀 Create New Laravel App")

    name = ask("App name (directory)")
    repo = ask("Git repository URL")
    domain = ask("Domain / server_name", "localhost")
    port = ask("Port", "7001")

    target = app_dir(name)

    if target.exists():
        print("\n❌ App already exists")
        sys.exit(1)

    run(f"git clone {repo} {target}")

    if not (target / ".env").exists():
        run("cp .env.example .env", cwd=target)

    sudo(f"chown -R {APP_USER}:{WEB_USER} {target}")
    sudo(f"find {target} -type d -exec chmod 775 {{}} \\;")
    sudo(f"find {target} -type f -exec chmod 664 {{}} \\;")

    run("composer install --no-dev --optimize-autoloader", cwd=target)
    run("php artisan key:generate --force", cwd=target)
    run("php artisan storage:link", cwd=target)

    # ---------- FRONTEND ----------
    if (target / "package.json").exists():
        ensure_node()
        run("npm install", cwd=target)
        run("npm run build", cwd=target)

    run("php artisan optimize", cwd=target)

    sudo(f"chown -R {WEB_USER}:{WEB_USER} {target}")
    sudo(f"chmod -R 775 {target}/storage {target}/bootstrap/cache")

    nginx_conf = f"""
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
    conf_path = NGINX_AVAILABLE / name
    sudo(f"bash -c 'cat > {conf_path} <<EOF\n{nginx_conf}\nEOF'")
    sudo(f"ln -sf {conf_path} {NGINX_ENABLED / name}")

    nginx_apply()

    print(f"\n✅ App created successfully")
    print(f"🌐 URL: http://{domain}:{port}")

# ================= REDEPLOY APP =================
def redeploy_app():
    print("\n🔄 Redeploy Laravel App")

    name = ask("App name")
    target = app_dir(name)

    if not target.exists():
        print("\n❌ App not found")
        sys.exit(1)

    run("git pull", cwd=target)
    run("composer install --no-dev --optimize-autoloader", cwd=target)

    if (target / "package.json").exists():
        ensure_node()
        run("npm install", cwd=target)
        run("npm run build", cwd=target)

    run("php artisan migrate --force", cwd=target, check=False)
    run("php artisan optimize", cwd=target)

    sudo(f"chown -R {WEB_USER}:{WEB_USER} {target}")
    sudo(f"chmod -R 775 {target}/storage {target}/bootstrap/cache")

    print("\n✅ Redeploy complete")

# ================= REMOVE APP =================
def remove_app():
    require_root()

    print("\n🗑 Remove Laravel App")

    name = ask("App name")
    target = app_dir(name)

    if not target.exists():
        print("\n❌ App not found")
        sys.exit(1)

    confirm = ask(f"Type '{name}' to confirm deletion")
    if confirm != name:
        print("❌ Confirmation failed")
        sys.exit(1)

    sudo(f"rm -rf {target}")
    sudo(f"rm -f {NGINX_AVAILABLE / name}")
    sudo(f"rm -f {NGINX_ENABLED / name}")

    nginx_apply()

    print("\n✅ App removed successfully")

# ================= LIST APPS =================
def list_apps():
    print("\n📦 Installed Laravel Apps:")
    if BASE_DIR.exists():
        for d in BASE_DIR.iterdir():
            if d.is_dir():
                print(" -", d.name)

# ================= MENU =================
def main():
    print("\n=== Interactive Laravel App Manager ===")
    print("1) Create app")
    print("2) Redeploy app")
    print("3) Remove app")
    print("4) List apps")
    print("5) Exit")

    choice = ask("Select option")

    if choice == "1":
        create_app()
    elif choice == "2":
        redeploy_app()
    elif choice == "3":
        remove_app()
    elif choice == "4":
        list_apps()
    else:
        print("Bye 👋")

if __name__ == "__main__":
    main()
