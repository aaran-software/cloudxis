#!/usr/bin/env python3
import subprocess

PHP_VERSION = "8.4"


def run(cmd, check=True):
    print(f"\n▶ {cmd}")
    subprocess.run(cmd, shell=True, check=check)


def sudo(cmd):
    run(f"sudo {cmd}")


def install_packages():
    sudo("apt update")
    sudo("apt install -y software-properties-common curl ca-certificates gnupg")

    sudo("add-apt-repository ppa:ondrej/php -y")
    sudo("apt update")

    sudo(
        "apt install -y "
        "git "
        f"php{PHP_VERSION} "
        f"php{PHP_VERSION}-cli "
        f"php{PHP_VERSION}-common "
        f"php{PHP_VERSION}-bcmath "
        f"php{PHP_VERSION}-curl "
        f"php{PHP_VERSION}-gd "
        f"php{PHP_VERSION}-intl "
        f"php{PHP_VERSION}-mbstring "
        f"php{PHP_VERSION}-mysql "
        f"php{PHP_VERSION}-pgsql "
        f"php{PHP_VERSION}-sqlite3 "
        f"php{PHP_VERSION}-xml "
        f"php{PHP_VERSION}-zip "
        f"php{PHP_VERSION}-redis "
        "imagemagick "
        "sqlite3"
    )

def install_frankenphp():
    print("\n=== Installing FrankenPHP ===")
    sudo(
        "curl -L https://github.com/dunglas/frankenphp/releases/latest/download/frankenphp-linux-x86_64 "
        "-o /usr/local/bin/frankenphp"
    )
    sudo("chmod +x /usr/local/bin/frankenphp")
    run("frankenphp --version")

def install_composer():
    run("curl -sS https://getcomposer.org/installer -o composer-setup.php")
    sudo("php composer-setup.php --install-dir=/usr/local/bin --filename=composer")
    run("rm composer-setup.php")
    run("composer --version")


def main():
    print("\n=== DOCKER-SAFE PACKAGE INSTALL (PHP 8.4) ===")
    install_packages()
    install_composer()
    print("\n✅ PHP 8.4 + NGINX INSTALLED AND STARTED")


if __name__ == "__main__":
    main()
