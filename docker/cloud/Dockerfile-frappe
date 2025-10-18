# Base Image
FROM ubuntu:24.04 AS codexion-cloud

LABEL maintainer="codexion"
LABEL author="Sundar < sundar@sundar.com >"
LABEL version="2.0"
LABEL description="Codexion - Custom Ubuntu 24.04 image for ERP + FastAPI + React development"

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=en_US.UTF-8
ENV PYENV_ROOT="/home/devops/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"
ENV NVM_DIR="/home/devops/.nvm"
ENV NODE_VERSION=20.19.2

RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential curl wget git sudo nano unzip ca-certificates bash-completion \
  software-properties-common net-tools iputils-ping tree less watch file rlwrap make \
  htop lsof rsync gnupg2 tar gzip zip bzip2 xz-utils \
  openssh-server openssh-client vsftpd rsync openssl \
  vim locales lsb-release cron supervisor nginx \
  mariadb-client libmariadb-dev \
  postgresql-client libpq-dev \
  redis redis-server redis-tools \
  libssl-dev libffi-dev libpq-dev libldap2-dev libsasl2-dev \
  zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev \
  libncursesw5-dev xz-utils tk-dev liblzma-dev \
  python3.12 python3.12-dev python3.12-venv python3-pip python3 \
  fonts-cantarell xfonts-75dpi xfonts-base \
  libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 libpangocairo-1.0-0 \
  glances iftop psutils gh \
  && ln -sf /usr/bin/python3.12 /usr/bin/python3 \
  && ln -sf /usr/bin/pip3 /usr/bin/pip \
  && locale-gen en_US.UTF-8 && update-locale LANG=en_US.UTF-8 \
  && mkdir -p /var/run/sshd \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN python3.12 -m pip install ansible --break-system-packages

RUN apt-get update && \
    apt-get install -y --no-install-recommends libjpeg-turbo8 libxrender1 xfonts-base xfonts-75dpi && \
    cd /tmp && \
    wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb && \
    apt-get install -y ./wkhtmltox_0.12.6.1-2.jammy_amd64.deb && \
    rm wkhtmltox_0.12.6.1-2.jammy_amd64.deb

RUN groupadd devops && \
    useradd -m -g devops -s /bin/bash devops && \
    echo 'devops:sundar' | chpasswd && \
    echo 'devops ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN mkdir -p /var/log/supervisor && chown -R devops:devops /var/log/supervisor

COPY supervisord.conf /etc/supervisor/supervisord.conf

USER devops
WORKDIR /home/devops

RUN git clone https://github.com/pyenv/pyenv.git "$PYENV_ROOT" && \
    git clone https://github.com/pyenv/pyenv-virtualenv.git "$PYENV_ROOT/plugins/pyenv-virtualenv" && \
    $PYENV_ROOT/bin/pyenv install 3.12.3 && \
    $PYENV_ROOT/bin/pyenv global 3.12.3 && \
    $PYENV_ROOT/versions/3.12.3/bin/pip install --upgrade pip setuptools wheel && \
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc && \
    echo 'export PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"' >> ~/.bashrc && \
    echo 'eval "$(pyenv init --path)"' >> ~/.bashrc && \
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc

RUN mkdir -p "$NVM_DIR" && \
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash && \
    export NVM_DIR="$NVM_DIR" && \
    . "$NVM_DIR/nvm.sh" && \
    nvm install $NODE_VERSION && \
    nvm use $NODE_VERSION && \
    nvm alias default $NODE_VERSION && \
    npm install -g yarn

USER root
RUN echo "export NVM_DIR=\"$NVM_DIR\"" > /etc/profile.d/nvm.sh && \
    echo "[ -s \"\$NVM_DIR/nvm.sh\" ] && . \"\$NVM_DIR/nvm.sh\"" >> /etc/profile.d/nvm.sh && \
    echo "export PATH=\"\$NVM_DIR/versions/node/v$NODE_VERSION/bin:\$PATH\"" >> /etc/profile.d/nvm.sh && \
    chmod +x /etc/profile.d/nvm.sh

USER devops
RUN git clone --depth 1 -b v5.x https://github.com/frappe/bench ~/.bench && \
    $PYENV_ROOT/shims/pip install --user -e ~/.bench && \
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && \
    echo 'export BENCH_DEVELOPER=1' >> ~/.bashrc

USER root
RUN ln -sf /home/devops/.local/bin/bench /usr/local/bin/bench

RUN mkdir -p /home/devops
COPY init_frappe.py /home/devops/ifrappe.py
RUN chmod +x /home/devops/ifrappe.py \
    && ln -s /home/devops/ifrappe.py /usr/local/bin/ifrappe

COPY install_cortex.py /home/devops/icortex.py
RUN chmod +x /home/devops/icortex.py \
    && ln -s /home/devops/icortex.py /usr/local/bin/icortex

USER devops
WORKDIR /home/devops

RUN mkdir -p /home/devops/logs

EXPOSE 8000 8888

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]

SHELL ["/bin/bash", "-c"]
