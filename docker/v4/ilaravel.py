#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path

# ==================================================
# CONFIG
# ==================================================
APP_DIR = "/var/www/codexsun"
APP_USER = "devops"

# ==================================================
# SAFETY
# ==================================================
if os.geteuid() == 0:
    print("❌ Do not run as root. Use devops user.")
    sys.exit(1)

# ==================================================
# HELPERS
# ==================================================
def run(cmd, cwd=None):
    print(f"\n▶ {cmd}")
    subprocess.run(cmd, shell=True, check=True, cwd=cwd)

def ask(prompt, default):
    val = input(f"{prompt} [{default}]: ").strip()
    return val or default

def exists(cmd):
    return subprocess.run(
        f"command -v {cmd}",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ).returncode == 0

# ==================================================
# VALIDATION
# ==================================================
def validate_runtime():
    required = ["php", "composer"]
    missing = [cmd for cmd in required if not exists(cmd)]

    if missing:
        print(f"❌ Missing required tools: {', '.join(missing)}")
        sys.exit(1)

    run("php -v")
    run("composer -V")

# ==================================================
# APP PREP
# ==================================================
def prepare_env():
    env = Path(APP_DIR) / ".env"

    if not env.exists():
        run("cp .env.example .env", cwd=APP_DIR)

    print("\n--- Database (MariaDB container) ---")
    db_name = ask("DB name", "laravel")
    db_user = ask("DB user", "laravel")
    db_pass = ask("DB password", "secret")
    db_port = ask("DB port", "3306")

    content = env.read_text()
    content = content.replace("DB_HOST=127.0.0.1", "DB_HOST=mariadb")
    content = content.replace("DB_DATABASE=laravel", f"DB_DATABASE={db_name}")
    content = content.replace("DB_USERNAME=root", f"DB_USERNAME={db_user}")
    content = content.replace("DB_PASSWORD=", f"DB_PASSWORD={db_pass}")
    content = content.replace("DB_PORT=3306", f"DB_PORT={db_port}")

    env.write_text(content)

def install_backend():
    run(
        "composer install "
        "--no-dev "
        "--optimize-autoloader "
        "--no-interaction",
        cwd=APP_DIR
    )

def build_frontend():
    if not exists("node"):
        print("ℹ️ Node not present — skipping frontend build")
        return

    run("node -v")
    run("npm -v")
    run("npm install", cwd=APP_DIR)
    run("npm run build", cwd=APP_DIR)

def laravel_finalize():
    run("php artisan key:generate --force", cwd=APP_DIR)
    run("php artisan storage:link", cwd=APP_DIR)
    run("php artisan migrate --force", cwd=APP_DIR)

def permissions():
    run(f"sudo chown -R {APP_USER}:{APP_USER} {APP_DIR}")
    run(f"sudo chmod -R ug+rw {APP_DIR}/storage {APP_DIR}/bootstrap/cache")

# ==================================================
# MAIN
# ==================================================
def main():
    print("\n=== Laravel Production Runtime Prep ===")

    validate_runtime()
    prepare_env()
    install_backend()
    build_frontend()
    laravel_finalize()
    permissions()

    print("\n✅ Laravel is READY (Nginx + PHP-FPM will handle runtime)")

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"\n❌ FAILED: {e}")
        sys.exit(1)
