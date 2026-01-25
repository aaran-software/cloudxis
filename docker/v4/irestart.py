#!/usr/bin/env python3
import subprocess
import sys

def run(cmd, check=True):
    print(f"\n▶ {cmd}")
    subprocess.run(cmd, shell=True, check=check)

def main():
    print("\n🔄 Restarting Nginx and PHP-FPM (Docker-safe)")

    # -------------------------------
    # Stop services (ignore errors)
    # -------------------------------
    run("sudo pkill nginx || true", check=False)
    run("sudo pkill php-fpm || true", check=False)

    # -------------------------------
    # Cleanup stale PID/socket
    # -------------------------------
    run("sudo rm -f /run/nginx.pid", check=False)

    # -------------------------------
    # Start PHP-FPM first
    # -------------------------------
    run("sudo php-fpm8.4 -D")

    # Verify socket
    run("ls -l /run/php/php8.4-fpm.sock")

    # -------------------------------
    # Start Nginx
    # -------------------------------
    run("sudo nginx")

    # -------------------------------
    # Verification
    # -------------------------------
    print("\n✅ Verification")
    run("ps aux | grep nginx")
    run("ps aux | grep php-fpm")

    print("\n🎉 Services restarted successfully")
    print("🌐 Test with: curl http://localhost:7001")

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print("\n❌ Restart failed")
        sys.exit(e.returncode)
