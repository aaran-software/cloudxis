import subprocess
from pathlib import Path

REPO_URL = "https://github.com/AARAN-SOFTWARE/codexion.git"
PROJECT_DIR = Path("/home/devops/cloud/codexion")


def run_command(cmd):
    """Run a shell command."""
    print(f"[~] Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)


def main():
    if PROJECT_DIR.exists():
        print(f"[✔] Repository already exists at {PROJECT_DIR}")
    else:
        print(f"[+] Cloning repository into {PROJECT_DIR}...")
        run_command(f"git clone --depth 1 {REPO_URL} {PROJECT_DIR}")


if __name__ == "__main__":
    main()
