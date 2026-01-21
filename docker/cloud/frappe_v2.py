#!/usr/bin/env python3

import os
import subprocess

# =====================================================
# CORE CONFIG
# =====================================================
FRAPPE_BRANCH = "version-16"

ERPNext_VERSION = "version-16"
CRM_VERSION = "develop"
HRMS_VERSION = "version-16"
INDIA_COMPLIANCE_VERSION = "version-16"

SITE_NAME = "tm.software.com"
ADMIN_PASS = "admin"

DB_USER = "root"
DB_PASS = "DbPass1@@"
DB_HOST = "mariadb"
DB_NAME = "tm_software_db"

BENCH_DIR = "/home/devops/cloud/frappe-bench"
SUPERVISOR_CONF = "/etc/supervisor/conf.d/frappe.conf"
LOG_DIR = "/home/devops/logs"
EMAIL = f"admin@{SITE_NAME}"


# =====================================================
# COLOR LOGGING
# =====================================================
class Log:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    CYAN = '\033[0;36m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'

    @staticmethod
    def print(msg): print(f"{Log.CYAN}{msg}{Log.NC}")

    @staticmethod
    def success(msg): print(f"{Log.GREEN}{msg}{Log.NC}")

    @staticmethod
    def error(msg): print(f"{Log.RED}{msg}{Log.NC}")

    @staticmethod
    def warn(msg): print(f"{Log.YELLOW}{msg}{Log.NC}")


# =====================================================
# UTILITIES
# =====================================================
def run(cmd, cwd=None, check=True):
    try:
        subprocess.run(cmd, shell=True, cwd=cwd, check=check)
    except subprocess.CalledProcessError:
        Log.error(f"❌ Command failed: {cmd}")
        if check:
            exit(1)


def confirm(msg):
    return input(f"{msg} (y/N): ").strip().lower() == 'y'


def bench_running():
    return subprocess.run(
        "pgrep -f 'bench start'",
        shell=True,
        stdout=subprocess.DEVNULL
    ).returncode == 0


def confirm_bench_running():
    while not bench_running():
        Log.warn("⚠️ Bench is not running!")
        input("📣 Run `bench start` in another terminal and press ENTER...")
    Log.success("✅ Bench is running")


# =====================================================
# SETUP FUNCTIONS
# =====================================================
def setup_bench():
    parent_dir = os.path.dirname(BENCH_DIR)
    bench_name = os.path.basename(BENCH_DIR)

    if os.path.exists(BENCH_DIR):
        Log.warn("⚠️ Bench already exists")
        if not confirm("🔁 Reinstall bench? This will DELETE existing data"):
            return
        run(f"rm -rf {BENCH_DIR}")

    os.makedirs(parent_dir, exist_ok=True)
    Log.print("🌀 Initializing Frappe Bench")
    run(f"bench init {bench_name} --frappe-branch {FRAPPE_BRANCH}", cwd=parent_dir)


def create_site():
    global SITE_NAME, DB_NAME

    site = input(f"Site Name (default: {SITE_NAME}): ").strip().lower()
    if site:
        SITE_NAME = site
        DB_NAME = SITE_NAME.replace('.', '_') + "_db"

    site_path = os.path.join(BENCH_DIR, "sites", SITE_NAME)
    if os.path.exists(site_path):
        Log.warn("⚠️ Site already exists")
        if not confirm("🔁 Drop & recreate site?"):
            return
        run(f"bench drop-site {SITE_NAME} --force", cwd=BENCH_DIR)

    Log.print(f"🌐 Creating site {SITE_NAME}")
    run(
        f"bench new-site {SITE_NAME} "
        f"--admin-password {ADMIN_PASS} "
        f"--mariadb-root-username {DB_USER} "
        f"--mariadb-root-password {DB_PASS} "
        f"--db-host {DB_HOST} "
        f"--db-name {DB_NAME} "
        f"--mariadb-user-host-login-scope='%'",
        cwd=BENCH_DIR
    )

    run(f"bench use {SITE_NAME}", cwd=BENCH_DIR)


# =====================================================
# CI / CD CHECKPOINT (MANUAL)
# =====================================================
def cicd_checkpoint(app_name):
    Log.print(f"🚦 CI/CD checkpoint for {app_name}")

    if confirm("🔄 Run migrate now?"):
        run(f"bench --site {SITE_NAME} migrate", cwd=BENCH_DIR)

    if confirm("🏗️ Run bench build?"):
        run("bench build --force", cwd=BENCH_DIR)

    if confirm("🧪 Run tests for this app?"):
        run(
            f"bench --site {SITE_NAME} run-tests --app {app_name}",
            cwd=BENCH_DIR,
            check=False
        )

    if not confirm("➡️ Continue to next app?"):
        Log.warn("⛔ Deployment stopped by user")
        exit(0)

    Log.success(f"✅ CI/CD completed for {app_name}")


# =====================================================
# APP INSTALLER (INTERACTIVE)
# =====================================================
def install_app(name, folder, repo, branch):
    app_path = os.path.join(BENCH_DIR, "apps", folder)

    if os.path.exists(app_path):
        Log.warn(f"⚠️ {name} already exists")
        if not confirm(f"🔁 Re-clone {name}?"):
            return
        run(f"rm -rf apps/{folder}", cwd=BENCH_DIR)

    if not confirm(f"📥 Install {name}?"):
        return

    run(
        f"bench get-app {folder} {repo} --branch {branch}",
        cwd=BENCH_DIR
    )

    confirm_bench_running()

    if confirm(f"🔧 Install {name} to site {SITE_NAME}?"):
        run(f"bench --site {SITE_NAME} install-app {folder}", cwd=BENCH_DIR)
        cicd_checkpoint(folder)


# =====================================================
# BUILD + CONFIG
# =====================================================
def build_and_config():
    Log.print("⚙️ Final build & config")
    run("bench build --force", cwd=BENCH_DIR)
    run("bench set-config -g developer_mode 1", cwd=BENCH_DIR)
    run("bench set-config -g host_name http://0.0.0.0:8000", cwd=BENCH_DIR)


def configure_site():
    Log.print("🔧 Site configuration")
    run(f"bench --site {SITE_NAME} set-config allow_signup true", cwd=BENCH_DIR)
    run(f"bench --site {SITE_NAME} set-config cookie_samesite Lax", cwd=BENCH_DIR)
    run(f"bench --site {SITE_NAME} set-config cookie_secure true", cwd=BENCH_DIR)


# =====================================================
# SUPERVISOR
# =====================================================
def setup_supervisor():
    Log.print("🧩 Setting up Supervisor")
    os.makedirs(LOG_DIR, exist_ok=True)

    conf = f"""
[program:frappe]
command=/bin/bash -c "cd {BENCH_DIR} && bench start"
directory={BENCH_DIR}
autostart=true
autorestart=true
stdout_logfile={LOG_DIR}/bench.log
stderr_logfile={LOG_DIR}/bench.err.log
user=devops
"""

    with open("/tmp/frappe.conf", "w") as f:
        f.write(conf)

    run(f"sudo mv /tmp/frappe.conf {SUPERVISOR_CONF}")
    run("sudo supervisorctl reread")
    run("sudo supervisorctl update")
    run("sudo supervisorctl start frappe")


# =====================================================
# MAIN
# =====================================================
if __name__ == "__main__":
    setup_bench()
    create_site()

    install_app(
        "ERPNext",
        "erpnext",
        "https://github.com/frappe/erpnext.git",
        ERPNext_VERSION
    )

    install_app(
        "CRM",
        "crm",
        "https://github.com/frappe/crm.git",
        CRM_VERSION
    )

    install_app(
        "HRMS",
        "hrms",
        "https://github.com/frappe/hrms.git",
        HRMS_VERSION
    )

    install_app(
        "India Compliance",
        "india_compliance",
        "https://github.com/resilient-tech/india-compliance.git",
        INDIA_COMPLIANCE_VERSION
    )

    build_and_config()
    configure_site()
    setup_supervisor()

    Log.success("✅ Frappe setup completed successfully")
    Log.print(f"🌐 Access: http://{SITE_NAME}")
