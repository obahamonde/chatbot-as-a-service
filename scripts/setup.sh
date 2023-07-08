apt update && \
apt upgrade -y && \
apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python-is-python3 \
    git \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    software-properties-common && \
curl https://get.docker.com/ | bash && \
#NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash && \
source ~/.bashrc && \
nvm install 16
nvm use 16
npm install -g npm
npm install -g yarn
