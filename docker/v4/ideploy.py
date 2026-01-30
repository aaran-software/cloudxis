#!/usr/bin/env python3
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

# ==================================================
# CONFIG
# ==================================================
APP_DIR = Path.cwd()

APP_USER = "devops"
WEB_USER = "www-data"

LOCK_FILE = Path("/tmp/ideploy.lock")

# ==================================================
# HELPERS
# ==================================================
def run(cmd, user=None):
    prefix = f"sudo -u {user} " if user else ""
    print(f"\n▶ {prefix}{cmd}")
    subprocess.check_call(
        f"{prefix}{cmd}",
        shell=True,
        cwd=APP_DIR,
    )

def info(msg):
    print(f"\nℹ️  {msg}")

def fail(msg):
    print(f"\n❌ {msg}")
    sys.exit(1)

# ==================================================
# SAFETY
# ==================================================
def ensure_repo():
    if not (APP_DIR / ".git").exists():
        fail(f"Not a git repository: {APP_DIR}")

def ensure_not_root():
    if os.geteuid() == 0:
        fail("Do not run ideploy as root")

def lock():
    if LOCK_FILE.exists():
        fail("Another deploy is already running")
    LOCK_FILE.write_text(str(os.getpid()))

def unlock():
    LOCK_FILE.unlink(missing_ok=True)

# ==================================================
# PERMISSIONS
# ==================================================
def prepare_for_git():
    info("Preparing filesystem for git")
    run("chown -R devops:devops .", user="root")

def restore_runtime_permissions():
    info("Restoring runtime permissions")
    run("chown -R www-data:www-data storage bootstrap/cache", user="root")
    run("chmod -R 775 storage bootstrap/cache", user="root")

# ==================================================
# GIT
# ==================================================
def git_update():
    info("Updating source code")
    branch = subprocess.check_output(
        "git symbolic-ref --short HEAD",
        shell=True,
        cwd=APP_DIR,
        text=True,
    ).strip()

    run("git fetch origin", user=APP_USER)
    run(f"git reset --hard origin/{branch}", user=APP_USER)
    run("git clean -fd", user=APP_USER)

# ==================================================
# NPM
# ==================================================
def npm_update_build():
    if not (APP_DIR / "package.json").exists():
        info("No package.json, skipping npm")
        return

    info("Updating & building frontend")
    run("npm install", user=APP_USER)
    run("npm run build", user=APP_USER)

# ==================================================
# LARAVEL
# ==================================================
def laravel_optimize():
    info("Optimizing Laravel")
    run("php artisan down || true", user=WEB_USER)
    run("php artisan optimize:clear", user=WEB_USER)
    run("php artisan config:cache", user=WEB_USER)
    run("php artisan route:cache", user=WEB_USER)
    run("php artisan view:cache", user=WEB_USER)
    run("php artisan up", user=WEB_USER)

# ==================================================
# MAIN
# ==================================================
def main():
    print("\n==============================")
    print("🚀 DEPLOY STARTED")
    print(datetime.now())
    print("==============================")

    ensure_repo()
    ensure_not_root()
    lock()

    try:
        prepare_for_git()
        git_update()
        npm_update_build()
        restore_runtime_permissions()
        laravel_optimize()
    finally:
        unlock()

    print("\n✅ DEPLOY COMPLETED SUCCESSFULLY")

if __name__ == "__main__":
    main()
