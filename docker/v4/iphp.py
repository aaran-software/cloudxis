#!/usr/bin/env python3
import subprocess
import sys
import os

PHP_VERSION = "8.4"

# -------------------------------------------------
# AUTO SUDO
# -------------------------------------------------
def ensure_root():
    if os.geteuid() != 0:
        print("🔐 Re-running with sudo...")
        os.execvp("sudo", ["sudo", sys.executable] + sys.argv)

ensure_root()

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def run(cmd):
    print(f"\n▶ {cmd}")
    subprocess.run(cmd, shell=True, check=True)

# -------------------------------------------------
# INSTALL PHP + EXTENSIONS
# -------------------------------------------------
def install_php():
    print(f"\n=== Installing PHP {PHP_VERSION} + Extensions ===")

    # Fix apt for minimal systems / containers
    run("mkdir -p /var/lib/apt/lists/partial")
    run("chmod -R 755 /var/lib/apt/lists")

    # Base packages
    run("apt-get update")
    run("apt-get install -y software-properties-common curl ca-certificates")

    # PHP repo
    run("add-apt-repository -y ppa:ondrej/php")
    run("apt-get update")

    # PHP core + extensions
    run(
        "apt-get install -y "
        f"php{PHP_VERSION}-cli "
        f"php{PHP_VERSION}-fpm "
        f"php{PHP_VERSION}-common "

        # PDO + Databases
        f"php{PHP_VERSION}-pdo "
        f"php{PHP_VERSION}-sqlite3 "
        f"php{PHP_VERSION}-mysql "
        f"php{PHP_VERSION}-pgsql "

        # Files / archives / uploads
        f"php{PHP_VERSION}-zip "
        f"php{PHP_VERSION}-fileinfo "

        # Strings / encoding
        f"php{PHP_VERSION}-mbstring "
        f"php{PHP_VERSION}-intl "

        # HTTP / networking
        f"php{PHP_VERSION}-curl "

        # XML / parsing
        f"php{PHP_VERSION}-xml "

        # Images
        f"php{PHP_VERSION}-gd "
        f"php{PHP_VERSION}-exif "

        # Math / utils
        f"php{PHP_VERSION}-bcmath "

        # Performance
        f"php{PHP_VERSION}-opcache"
    )

# -------------------------------------------------
# COMPOSER
# -------------------------------------------------
def install_composer():
    print("\n=== Installing Composer ===")

    if os.path.exists("/usr/local/bin/composer"):
        print("✔ Composer already installed")
        run("composer -V")
        return

    run("curl -sS https://getcomposer.org/installer -o composer-setup.php")
    run("php composer-setup.php --install-dir=/usr/local/bin --filename=composer")
    run("rm -f composer-setup.php")

    run("composer -V")

# -------------------------------------------------
# HEALTH CHECK
# -------------------------------------------------
def health():
    print("\n🩺 Health checks")

    run("php -v")
    run("php -m | sort")

    print("\n🔍 PDO drivers")
    run("php -r \"print_r(PDO::getAvailableDrivers());\"")

    run("composer -V")

# -------------------------------------------------
# MAIN
# -------------------------------------------------
def main():
    print("\n=== PHP + PDO + FILE SUPPORT INSTALLER ===")

    install_php()
    install_composer()
    health()

    print("\n✅ DONE — PHP environment fully ready")

if __name__ == "__main__":
    main()
