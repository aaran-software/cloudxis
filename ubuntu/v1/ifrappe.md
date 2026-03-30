Since you are **already logged in as `tmadmin`**, we should:

* ✅ install everything under the **current user (`tmadmin`)**

Below is the **cleaned script for a logged-in user**.

---

# Ubuntu Installer (Uses Current User)

Run:

```bash
sudo nano isetup.sh
```

```bash
chmod +x isetup.sh
```

```bash
./isetup.sh
```

---

```bash
#!/usr/bin/env bash

# =========================================================
# Codexion Cloud – Ubuntu 24.04 + Python 3.14 + Frappe Bench
# Native installation (Current user install)
# =========================================================

set -e
export DEBIAN_FRONTEND=noninteractive

echo "Updating system..."

sudo apt update

sudo apt install -y \
  build-essential curl wget git nano unzip ca-certificates bash-completion \
  software-properties-common net-tools iputils-ping tree less watch file rlwrap make \
  htop lsof rsync gnupg2 tar gzip zip bzip2 xz-utils \
  openssh-server openssh-client vsftpd openssl \
  vim locales lsb-release cron supervisor nginx \
  postgresql-client libpq-dev \
  redis redis-server redis-tools \
  libssl-dev libffi-dev libldap2-dev libsasl2-dev \
  zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev \
  libncursesw5-dev libncurses5-dev tk-dev liblzma-dev llvm \
  fonts-cantarell xfonts-75dpi xfonts-base \
  libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 libpangocairo-1.0-0 \
  libjpeg-turbo8 libxrender1 \
  pkg-config media-types \
  glances iftop psutils gh

sudo locale-gen en_US.UTF-8

echo "Installing wkhtmltopdf..."

cd /tmp
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
sudo apt install -y ./wkhtmltox_0.12.6.1-2.jammy_amd64.deb
rm wkhtmltox_0.12.6.1-2.jammy_amd64.deb

# ---------------------------------------------------------
# pyenv + Python 3.14
# ---------------------------------------------------------

echo "Installing pyenv..."

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"

git clone --depth 1 https://github.com/pyenv/pyenv.git ~/.pyenv

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.profile
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"

pyenv install 3.14.2
pyenv global 3.14.2

pip install --upgrade pip setuptools wheel virtualenv

# ---------------------------------------------------------
# Node.js via NVM
# ---------------------------------------------------------

echo "Installing Node.js..."

export NVM_DIR="$HOME/.nvm"

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

source "$HOME/.nvm/nvm.sh"

nvm install 24.12.0
nvm use 24.12.0
nvm alias default 24.12.0

npm install -g yarn

# ---------------------------------------------------------
# Install Frappe Bench
# ---------------------------------------------------------

echo "Installing Frappe Bench..."

export PATH="$HOME/.local/bin:$PATH"

git clone --depth 1 -b v5.x https://github.com/frappe/bench ~/.bench

pip install --user -e ~/.bench

echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
echo 'export BENCH_DEVELOPER=1' >> ~/.bashrc

mkdir -p ~/logs

# ---------------------------------------------------------
# Global bench command
# ---------------------------------------------------------

sudo ln -sf $HOME/.local/bin/bench /usr/local/bin/bench

sudo mkdir -p /var/log/supervisor

echo
echo "Installation completed."
echo
echo "Reload shell:"
echo
echo "source ~/.bashrc"
echo
echo "Create frappe bench:"
echo
echo "bench init frappe-bench"
echo
echo "Run server:"
echo
echo "cd frappe-bench && bench start"
```

```
/home/tmadmin
```

sudo apt update

sudo apt install -y \
  libmariadb-dev \
  libmariadb-dev-compat \
  pkg-config \
  python3-dev \
  build-essential

sudo apt install -y \
  libmariadb-dev \
  libmariadb-dev-compat \
  pkg-config \
  python3-dev \
  redis-server \
  libffi-dev \
  libssl-dev \
  libjpeg-dev \
  zlib1g-dev \
  libpq-dev


