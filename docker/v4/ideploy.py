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
LOCK_FILE = Path("/tmp/ideploy.lock")

# ==================================================
# HELPERS
# ==================================================
def run(cmd):
    print(f"\n▶ {cmd}")
    subprocess.check_call(cmd, shell=True, cwd=APP_DIR)

def ask(question):
    return input(f"{question} (y/N): ").strip().lower() == "y"

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

def ensure_user():
    if os.geteuid() == 0:
        fail("Do not run ideploy as root")
    if os.getlogin() != APP_USER:
        fail(f"Run ideploy as `{APP_USER}`")

def lock():
    if LOCK_FILE.exists():
        fail("Another deploy is already running")
    LOCK_FILE.write_text(str(os.getpid()))

def unlock():
    LOCK_FILE.unlink(missing_ok=True)

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

    run("git fetch origin")
    run(f"git reset --hard origin/{branch}")
    run("git clean -fd")

# ==================================================
# NPM
# ==================================================
def npm_build():
    if not (APP_DIR / "package.json").exists():
        info("No package.json found, skipping npm")
        return

    if ask("Run npm build?"):
        try:
            run("npm run build")
        except subprocess.CalledProcessError:
            info("Build failed — running npm install")
            run("npm install")
            run("npm run build")
    else:
        info("Skipped npm build")

# ==================================================
# LARAVEL
# ==================================================
def run_migrations():
    if not (APP_DIR / "artisan").exists():
        info("Not a Laravel app, skipping migration")
        return

    if ask("Run database migration?"):
        run("php artisan down || true")
        run("php artisan migrate --force")
        run("php artisan up")
    else:
        info("Skipped migrations")

def laravel_optimize():
    if not (APP_DIR / "artisan").exists():
        return

    info("Optimizing Laravel")
    run("php artisan optimize:clear")
    run("php artisan config:cache")
    run("php artisan route:cache")
    run("php artisan view:cache")

# ==================================================
# MAIN
# ==================================================
def main():
    print("\n==============================")
    print("🚀 DEPLOY STARTED")
    print(datetime.now())
    print("==============================")

    ensure_repo()
    ensure_user()
    lock()

    try:
        git_update()
        npm_build()
        run_migrations()
        laravel_optimize()
    finally:
        unlock()

    print("\n✅ DEPLOY COMPLETED SUCCESSFULLY")

if __name__ == "__main__":
    main()
