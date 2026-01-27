#!/usr/bin/env python3
import subprocess
import sys
import os
import pwd
import shutil
import argparse
from datetime import datetime
from pathlib import Path

# ==================================================
# CONFIG
# ==================================================
APP_DIR = Path("/home/devops/cloud/codexsun")
DEPLOY_USER = "www-data"
LOCK_FILE = Path("/tmp/codexsun.deploy.lock")

REQUIRED_NODE_MAJOR = 20
REQUIRED_NPM_MAJOR = 10

NPM_CACHE_CANDIDATES = [
    Path("/var/www/.npm"),
    Path("/tmp/npm-cache-www-data"),
]

# ==================================================
# HELPERS
# ==================================================
def run(cmd: str, env=None):
    print(f"\n▶ {cmd}")
    subprocess.check_call(
        cmd,
        shell=True,
        cwd=APP_DIR,
        env=env or os.environ.copy(),
    )

def info(msg: str):
    print(f"\nℹ️  {msg}")

def fail(msg: str):
    print(f"\n❌ {msg}")
    sys.exit(1)

# ==================================================
# SAFETY CHECKS
# ==================================================
def ensure_repo():
    if not (APP_DIR / ".git").exists():
        fail("Not a git repository")

def ensure_user():
    uid = os.geteuid()
    user = pwd.getpwuid(uid).pw_name

    if uid == 0:
        fail("Do not run deploy as root")

    if user != DEPLOY_USER:
        fail(f"Run deploy as '{DEPLOY_USER}', current user is '{user}'")

def acquire_lock():
    if LOCK_FILE.exists():
        fail("Another deploy is already running")
    LOCK_FILE.write_text(str(os.getpid()))

def release_lock():
    LOCK_FILE.unlink(missing_ok=True)

# ==================================================
# VERSION CHECKS
# ==================================================
def check_node_npm_versions():
    node_version = subprocess.check_output("node -v", shell=True, text=True).strip()
    npm_version = subprocess.check_output("npm -v", shell=True, text=True).strip()

    node_major = int(node_version.lstrip("v").split(".")[0])
    npm_major = int(npm_version.split(".")[0])

    print(f"Node: {node_version} | npm: {npm_version}")

    if node_major != REQUIRED_NODE_MAJOR:
        fail(f"Node {REQUIRED_NODE_MAJOR}.x required")

    if npm_major != REQUIRED_NPM_MAJOR:
        fail(f"npm {REQUIRED_NPM_MAJOR}.x required")

# ==================================================
# NODE / NPM MANAGEMENT
# ==================================================
def install_node():
    info("Installing Node.js (20.x)")
    run("curl -fsSL https://deb.nodesource.com/setup_20.x | bash -")
    run("apt-get install -y nodejs")

def update_npm():
    info("Updating npm to latest 10.x")
    run("npm install -g npm@10")

# ==================================================
# NPM CACHE (NO .npmrc)
# ==================================================
def resolve_npm_cache_dir() -> Path:
    for path in NPM_CACHE_CANDIDATES:
        try:
            path.mkdir(parents=True, exist_ok=True)
            test = path / ".write-test"
            test.write_text("ok")
            test.unlink()
            return path
        except Exception:
            continue
    fail("No writable npm cache directory available")

def npm_env() -> dict:
    env = os.environ.copy()
    cache_dir = resolve_npm_cache_dir()
    info(f"Using npm cache: {cache_dir}")
    env["npm_config_cache"] = str(cache_dir)
    return env

def clean_node_modules(env):
    info("Resetting node_modules")
    shutil.rmtree(APP_DIR / "node_modules", ignore_errors=True)
    (APP_DIR / "package-lock.json").unlink(missing_ok=True)
    run("npm cache clean --force", env=env)

# ==================================================
# DEPLOY STEPS
# ==================================================
def git_update():
    info("Updating source code")
    run("git fetch origin")
    run("git pull --ff-only")

def npm_install(run_install: bool, env):
    if not run_install:
        info("Skipping npm install (flag disabled)")
        return

    if not (APP_DIR / "package.json").exists():
        info("No package.json found, skipping npm install")
        return

    try:
        run("npm install", env=env)
    except subprocess.CalledProcessError:
        info("npm install failed — auto-healing")
        clean_node_modules(env)
        run("npm install", env=env)

def npm_build(run_build: bool, env):
    if not run_build:
        info("Skipping npm build (flag disabled)")
        return

    run("npm run build", env=env)

def laravel_optimize():
    info("Optimizing Laravel")
    run("php artisan down || true")
    run("php artisan optimize:clear")
    run("php artisan config:cache")
    run("php artisan route:cache")
    run("php artisan view:cache")
    run("php artisan up")

# ==================================================
# ARGUMENTS
# ==================================================
def parse_args():
    parser = argparse.ArgumentParser(description="Manual deploy controller")

    parser.add_argument("--install-node", choices=["y", "n"], default="n")
    parser.add_argument("--update-npm", choices=["y", "n"], default="n")
    parser.add_argument("--npm-install", choices=["y", "n"], default="y")
    parser.add_argument("--build-npm", choices=["y", "n"], default="y")

    return parser.parse_args()

# ==================================================
# MAIN
# ==================================================
def main():
    args = parse_args()

    print("\n==============================")
    print("🚀 DEPLOY STARTED")
    print(f"🕒 {datetime.now()}")
    print("==============================")

    ensure_repo()
    ensure_user()
    acquire_lock()

    try:
        git_update()

        if args.install_node == "y":
            install_node()

        if args.update_npm == "y":
            update_npm()

        check_node_npm_versions()
        env = npm_env()

        npm_install(args.npm_install == "y", env)
        npm_build(args.build_npm == "y", env)

        laravel_optimize()

    except subprocess.CalledProcessError as e:
        fail(f"Command failed: {e}")

    finally:
        release_lock()

    print("\n✅ DEPLOY COMPLETED SUCCESSFULLY")

# ==================================================
if __name__ == "__main__":
    main()
