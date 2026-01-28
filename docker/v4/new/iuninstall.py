#!/usr/bin/env python3
import subprocess
import os

# ================ CONFIG =================
DOMAIN = "techmedia.in"
NGINX_PORT = 7021
PHP_VERSION = "8.4"
# ========================================


def run(cmd):
    print(f"\n▶ {cmd}")
    subprocess.run(cmd, shell=True, check=False)


def sudo(cmd):
    run(f"sudo {cmd}")


def remove_hosts_entry():
    sudo(
        f"""bash -c "sed -i '/[[:space:]]{DOMAIN}$/d' /etc/hosts" """
    )


def remove_nginx_site():
    sudo(f"rm -f /etc/nginx/sites-enabled/{DOMAIN}")
    sudo(f"rm -f /etc/nginx/sites-available/{DOMAIN}")
    sudo("nginx -t")
    sudo("systemctl reload nginx")


def remove_php_pool():
    sudo(f"rm -f /etc/php/{PHP_VERSION}/fpm/pool.d/{DOMAIN}.conf")
    sudo(f"rm -f /run/php/php{PHP_VERSION}-{DOMAIN}.sock")
    sudo(f"systemctl restart php{PHP_VERSION}-fpm")


def main():
    print(f"\n=== UNINSTALL DOMAIN: {DOMAIN} ===")

    remove_nginx_site()
    remove_php_pool()
    remove_hosts_entry()

    print("\n✅ DOMAIN REMOVED")
    print(f"❌ http://{DOMAIN}:{NGINX_PORT} is no longer active")


if __name__ == "__main__":
    main()
