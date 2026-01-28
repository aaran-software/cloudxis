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
    sudo("apt install -y")

    sudo("add-apt-repository ppa:ondrej/php -y")

    sudo(
        "apt install -y "
        "git nginx "
        f"php{PHP_VERSION}-fpm "
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
        f"php{PHP_VERSION}-opcache "
        f"php{PHP_VERSION}-redis "
        "imagemagick "
        "sqlite3"
    )


def install_composer():
    run("php -r \"copy('https://getcomposer.org/installer', 'composer-setup.php');\"")
    sudo("php composer-setup.php --install-dir=/usr/local/bin --filename=composer")
    run("php -r \"unlink('composer-setup.php');\"")
    run("composer --version")


def enable_services():
    sudo(f"systemctl enable php{PHP_VERSION}-fpm")
    sudo("systemctl enable nginx")


def main():
    print("\n=== SYSTEMD-SAFE PACKAGE INSTALL ===")
    install_packages()
    install_composer()
    enable_services()
    print("\n✅ PACKAGES INSTALLED SUCCESSFULLY")


if __name__ == "__main__":
    main()
