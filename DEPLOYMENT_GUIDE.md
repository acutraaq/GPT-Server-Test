# GPT Server Enterprise Deployment Guide

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Server Specifications](#server-specifications)
4. [Development Environment Setup](#development-environment-setup)
5. [Pre-deployment Checklist](#pre-deployment-checklist)
6. [Step-by-Step Deployment](#step-by-step-deployment)
7. [Container Deployment](#container-deployment)
8. [Kubernetes Orchestration](#kubernetes-orchestration)
9. [Configuration Management](#configuration-management)
10. [Model Management](#model-management)
11. [API Integration](#api-integration)
12. [Monitoring and Maintenance](#monitoring-and-maintenance)
13. [Testing Strategies](#testing-strategies)
14. [Troubleshooting](#troubleshooting)
15. [Security Considerations](#security-considerations)
16. [Compliance and Regulatory](#compliance-and-regulatory)
17. [Performance Optimization](#performance-optimization)
18. [Cost Optimization](#cost-optimization)
19. [Disaster Recovery](#disaster-recovery)
20. [Upgrade and Rollback](#upgrade-and-rollback)
21. [Support and Training](#support-and-training)

## Overview

This guide provides comprehensive instructions for deploying GPT Server in an enterprise environment. GPT Server is an open-source framework for production-level deployment of Large Language Models (LLMs) and Embedding models with OpenAI-compatible APIs.

### Key Features
- **Multi-Model Support**: Chat, Embedding, ReRanker, Text-Moderation, ASR, TTS, SD models
- **Multiple Backends**: HF, vLLM, LMDeploy, SGLang acceleration engines
- **OpenAI Compatibility**: Drop-in replacement for OpenAI API
- **High Performance**: Optimized for production workloads
- **Scalability**: Support for multiple model instances and load balancing

## Required Tools & Dependencies

### 🔧 **System Requirements Overview**

Before starting deployment, ensure you have access to all required tools and dependencies. This section provides comprehensive lists for different deployment scenarios.

### 📋 **Core System Tools**

#### **Package Managers & System Tools**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y \
    curl \
    wget \
    git \
    vim \
    nano \
    htop \
    iotop \
    ncdu \
    tree \
    jq \
    httpie \
    unzip \
    zip \
    tar \
    gzip \
    bzip2 \
    xz-utils \
    build-essential \
    cmake \
    pkg-config \
    libssl-dev \
    libffi-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    liblzma-dev \
    tk-dev \
    python3-dev \
    python3-pip \
    python3-venv \
    python3-setuptools \
    python3-wheel \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    ufw \
    fail2ban \
    rsyslog \
    logrotate \
    cron \
    anacron \
    unattended-upgrades \
    needrestart \
    screen \
    tmux \
    rsync \
    openssh-server \
    openssh-client \
    net-tools \
    iputils-ping \
    dnsutils \
    traceroute \
    telnet \
    nmap \
    tcpdump \
    iptables \
    nftables \
    systemd \
    systemctl \
    journalctl

# CentOS/RHEL
sudo yum groupinstall -y "Development Tools"
sudo yum install -y \
    curl \
    wget \
    git \
    vim \
    nano \
    htop \
    iotop \
    ncdu \
    tree \
    jq \
    httpie \
    unzip \
    zip \
    tar \
    gzip \
    bzip2 \
    xz \
    cmake \
    pkgconfig \
    openssl-devel \
    libffi-devel \
    bzip2-devel \
    readline-devel \
    sqlite-devel \
    llvm \
    ncurses-devel \
    lzma-devel \
    tkinter \
    python3-devel \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    epel-release \
    yum-utils \
    firewalld \
    fail2ban \
    rsyslog \
    logrotate \
    cronie \
    anacron \
    yum-cron \
    screen \
    tmux \
    rsync \
    openssh-server \
    openssh-client \
    net-tools \
    iputils \
    bind-utils \
    traceroute \
    telnet \
    nmap \
    tcpdump \
    iptables \
    nftables \
    systemd \
    systemctl \
    journalctl
```

#### **Python Environment Tools**
```bash
# Python version management (optional but recommended)
# pyenv for managing multiple Python versions
curl https://pyenv.run | bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Install Python 3.11
pyenv install 3.11.8
pyenv global 3.11.8

# uv package manager (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# Verify installations
python --version
uv --version
```

### 🐳 **Container & Orchestration Tools**

#### **Docker Ecosystem**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Docker Buildx for multi-platform builds
sudo apt install docker-buildx-plugin

# Verify Docker installation
docker --version
docker-compose --version
docker buildx version
```

#### **Kubernetes Tools**
```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Install k9s (optional TUI for Kubernetes)
curl -sS https://webinstall.dev/k9s | bash

# Verify installations
kubectl version --client
helm version
k9s --version
```

#### **Container Registry Tools**
```bash
# Docker Registry access
sudo apt install docker-registry

# AWS CLI for ECR (if using AWS)
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Google Cloud SDK for GCR (if using GCP)
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Azure CLI for ACR (if using Azure)
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

### 🎮 **GPU & Hardware Acceleration Tools**

#### **NVIDIA GPU Tools**
```bash
# Install NVIDIA drivers (Ubuntu)
sudo apt update
sudo apt install ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Or manual installation
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/12.2.0/local_installers/cuda_12.2.0_535.54.03_linux.run
sudo sh cuda_12.2.0_535.54.03_linux.run --no-opengl-libs --no-man-page --no-docs

# Install cuDNN
wget https://developer.download.nvidia.com/compute/cudnn/8.9.4/local_installers/cudnn_8.9.4.25-1.cuda12.2_0.deb
sudo dpkg -i cudnn_8.9.4.25-1.cuda12.2_0.deb

# Install NCCL (for multi-GPU)
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libnccl2_2.18.3-1+cuda12.2_amd64.deb
sudo dpkg -i libnccl2_2.18.3-1+cuda12.2_amd64.deb

# Verify GPU setup
nvidia-smi
nvcc --version
```

#### **AMD GPU Tools (Optional)**
```bash
# Install ROCm
wget https://repo.radeon.com/amdgpu-install/23.40.2/ubuntu/focal/amdgpu-install_23.40.2.50402-1_all.deb
sudo dpkg -i amdgpu-install_23.40.2.50402-1_all.deb
sudo amdgpu-install --usecase=graphics,rocm

# Verify ROCm
rocm-smi
hipcc --version
```

### 📊 **Monitoring & Observability Tools**

#### **System Monitoring**
```bash
# Prometheus Node Exporter
wget https://github.com/prometheus/node_exporter/releases/latest/download/node_exporter-1.7.0.linux-amd64.tar.gz
tar xvf node_exporter-1.7.0.linux-amd64.tar.gz
sudo mv node_exporter-1.7.0.linux-amd64/node_exporter /usr/local/bin/
sudo useradd -rs /bin/false node_exporter
sudo tee /etc/systemd/system/node_exporter.service > /dev/null <<EOF
[Unit]
Description=Node Exporter
After=network.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable node_exporter
sudo systemctl start node_exporter

# Grafana
wget https://dl.grafana.com/oss/release/grafana_10.2.0_amd64.deb
sudo dpkg -i grafana_10.2.0_amd64.deb
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
```

#### **Log Aggregation**
```bash
# ELK Stack (Elasticsearch, Logstash, Kibana)
# Install Elasticsearch
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
sudo apt install apt-transport-https
echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
sudo apt update
sudo apt install elasticsearch

# Install Logstash
sudo apt install logstash

# Install Kibana
sudo apt install kibana

# Alternative: Loki + Promtail (lighter weight)
curl -O -L "https://github.com/grafana/loki/releases/latest/download/loki-linux-amd64.zip"
unzip loki-linux-amd64.zip
sudo mv loki-linux-amd64 /usr/local/bin/loki

curl -O -L "https://github.com/grafana/loki/releases/latest/download/promtail-linux-amd64.zip"
unzip promtail-linux-amd64.zip
sudo mv promtail-linux-amd64 /usr/local/bin/promtail
```

#### **Application Monitoring**
```bash
# Prometheus
wget https://github.com/prometheus/prometheus/releases/latest/download/prometheus-2.47.0.linux-amd64.tar.gz
tar xvf prometheus-2.47.0.linux-amd64.tar.gz
sudo mv prometheus-2.47.0.linux-amd64 /usr/local/prometheus

# Alertmanager
wget https://github.com/prometheus/alertmanager/releases/latest/download/alertmanager-0.26.0.linux-amd64.tar.gz
tar xvf alertmanager-0.26.0.linux-amd64.tar.gz
sudo mv alertmanager-0.26.0.linux-amd64 /usr/local/alertmanager
```

### 🔒 **Security & Access Control Tools**

#### **Authentication & Authorization**
```bash
# LDAP server (optional)
sudo apt install slapd ldap-utils
sudo dpkg-reconfigure slapd

# OAuth/OIDC providers
sudo apt install keycloak

# Certificate management
sudo apt install certbot python3-certbot-nginx

# SSL/TLS tools
sudo apt install openssl ca-certificates

# Security scanning
sudo apt install lynis rkhunter chkrootkit

# Intrusion detection
sudo apt install snort suricata
```

#### **Network Security**
```bash
# Firewall
sudo apt install ufw
sudo ufw enable

# VPN (optional)
sudo apt install openvpn easy-rsa

# SSH hardening
sudo apt install openssh-server
# Edit /etc/ssh/sshd_config
# - Disable root login
# - Use key-based authentication
# - Change default port
# - Enable fail2ban

# Fail2ban
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 🗄️ **Database & Storage Tools**

#### **PostgreSQL**
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Install pgAdmin (optional)
curl https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo apt-key add
sudo sh -c 'echo "deb https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list'
sudo apt update
sudo apt install pgadmin4

# Install backup tools
sudo apt install pgbackrest barman
```

#### **Redis**
```bash
# Install Redis
sudo apt install redis-server

# Install Redis CLI tools
sudo apt install redis-tools

# Install Redis Cluster tools (optional)
wget https://download.redis.io/redis-stable.tar.gz
tar xzf redis-stable.tar.gz
cd redis-stable
make
sudo make install
```

#### **Storage Tools**
```bash
# NFS client/server
sudo apt install nfs-common nfs-kernel-server

# Samba (SMB/CIFS)
sudo apt install samba samba-common-bin

# Object storage (MinIO)
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio
sudo mv minio /usr/local/bin/

# Cloud storage tools
# AWS S3
pip install awscli boto3

# Google Cloud Storage
pip install google-cloud-storage

# Azure Blob Storage
pip install azure-storage-blob azure-identity
```

### 🧪 **Testing & Quality Assurance Tools**

#### **Load Testing**
```bash
# Install k6
sudo apt update
sudo apt install k6

# Install Locust
pip install locust

# Install JMeter
wget https://downloads.apache.org/jmeter/binaries/apache-jmeter-5.6.2.tgz
tar xzf apache-jmeter-5.6.2.tgz
sudo mv apache-jmeter-5.6.2 /opt/jmeter

# Install Artillery
npm install -g artillery
```

#### **API Testing**
```bash
# Install Postman (GUI)
wget https://dl.pstmn.io/download/latest/linux64 -O postman.tar.gz
tar xzf postman.tar.gz
sudo mv Postman /opt/postman

# Install Newman (CLI for Postman)
npm install -g newman

# Install REST clients
sudo apt install curl wget httpie

# Install API documentation tools
pip install sphinx sphinx-rtd-theme
npm install -g redoc-cli
```

#### **Code Quality**
```bash
# Python tools
pip install black isort flake8 mypy pylint bandit safety

# JavaScript/Node.js tools (if needed)
npm install -g eslint prettier typescript

# Shell script tools
sudo apt install shellcheck

# YAML/JSON tools
pip install yamllint
sudo apt install jq

# Pre-commit hooks
pip install pre-commit
```

### 🚀 **CI/CD Tools**

#### **GitHub Actions Runners**
```bash
# Install GitHub Actions runner
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz
./config.sh --url https://github.com/your-org/your-repo --token YOUR_TOKEN
./run.sh
```

#### **Jenkins**
```bash
# Install Jenkins
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt update
sudo apt install jenkins

# Install Jenkins plugins
# - Pipeline
# - Git
# - Docker
# - Kubernetes
# - Performance Publisher
# - Test Results Analyzer
```

#### **GitLab CI/CD**
```bash
# Install GitLab Runner
curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh | sudo bash
sudo apt install gitlab-runner

# Register runner
sudo gitlab-runner register
```

### 📚 **Documentation & Collaboration Tools**

#### **Documentation**
```bash
# Install MkDocs
pip install mkdocs mkdocs-material

# Install Sphinx
pip install sphinx sphinx-rtd-theme

# Install PlantUML for diagrams
sudo apt install plantuml

# Install draw.io desktop
wget https://github.com/jgraph/drawio-desktop/releases/latest/download/drawio-amd64-21.6.8.deb
sudo dpkg -i drawio-amd64-21.6.8.deb
```

#### **Communication**
```bash
# Install Slack client (optional)
wget https://downloads.slack-edge.com/releases/linux/4.35.131/slack-desktop-4.35.131-amd64.deb
sudo dpkg -i slack-desktop-4.35.131-amd64.deb

# Install Discord (optional)
wget https://discord.com/api/download?platform=linux&format=deb -O discord.deb
sudo dpkg -i discord.deb
```

### 🔍 **Troubleshooting & Diagnostic Tools**

#### **Network Diagnostics**
```bash
# Install network tools
sudo apt install \
    netcat \
    socat \
    tcpdump \
    wireshark \
    nmap \
    traceroute \
    mtr \
    iperf \
    speedtest-cli \
    dnsutils \
    whois \
    dig \
    nslookup
```

#### **System Diagnostics**
```bash
# Install system monitoring tools
sudo apt install \
    sysstat \
    iotop \
    htop \
    atop \
    nmon \
    dstat \
    vmstat \
    iostat \
    sar \
    mpstat \
    pidstat \
    perf \
    strace \
    ltrace \
    gdb \
    valgrind
```

#### **Log Analysis**
```bash
# Install log analysis tools
sudo apt install \
    logwatch \
    logcheck \
    swatch \
    multitail \
    lnav \
    goaccess
```

### 📋 **Tool Verification Script**

```bash
#!/bin/bash
# verify_tools.sh - Verify all required tools are installed and working

echo "🔍 GPT Server Tools Verification"
echo "================================"

TOOLS=(
    "python:python --version"
    "uv:uv --version"
    "docker:docker --version"
    "docker-compose:docker-compose --version"
    "kubectl:kubectl version --client"
    "helm:helm version"
    "nvidia-smi:nvidia-smi --query-gpu=driver_version --format=csv,noheader,nounits"
    "git:git --version"
    "curl:curl --version"
    "wget:wget --version"
    "jq:jq --version"
    "htop:htop --version"
    "vim:vim --version"
    "nano:nano --version"
)

PASSED=0
TOTAL=${#TOOLS[@]}

for tool in "${TOOLS[@]}"; do
    NAME=$(echo $tool | cut -d: -f1)
    COMMAND=$(echo $tool | cut -d: -f2)

    echo -n "Checking $NAME... "
    if eval "$COMMAND" &>/dev/null; then
        echo "✅ PASSED"
        ((PASSED++))
    else
        echo "❌ FAILED"
    fi
done

echo ""
echo "Results: $PASSED/$TOTAL tools verified successfully"

if [ $PASSED -eq $TOTAL ]; then
    echo "🎉 All tools are properly installed!"
    exit 0
else
    echo "⚠️  Some tools are missing. Please install them before proceeding."
    exit 1
fi
```

### 📦 **Quick Installation Scripts**

#### **Ubuntu/Debian Quick Install**
```bash
#!/bin/bash
# ubuntu_setup.sh - Quick setup for Ubuntu systems

# Update system
sudo apt update && sudo apt upgrade -y

# Install core tools
sudo apt install -y curl wget git vim htop jq httpie unzip python3 python3-pip

# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install NVIDIA drivers (if GPU present)
if lspci | grep -i nvidia; then
    sudo apt install ubuntu-drivers-common
    sudo ubuntu-drivers autoinstall
fi

echo "✅ Ubuntu setup completed!"
echo "Please reboot and run 'docker --version' to verify installation"
```

#### **CentOS/RHEL Quick Install**
```bash
#!/bin/bash
# centos_setup.sh - Quick setup for CentOS/RHEL systems

# Update system
sudo yum update -y

# Install core tools
sudo yum install -y curl wget git vim htop jq httpie unzip python3 python3-pip

# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install NVIDIA drivers (if GPU present)
if lspci | grep -i nvidia; then
    sudo yum install -y kernel-devel kernel-headers gcc make
    # Install NVIDIA drivers manually
fi

echo "✅ CentOS setup completed!"
echo "Please reboot and run 'docker --version' to verify installation"
```

### 🎯 **Tool Categories Summary**

| Category | Essential Tools | Optional Tools |
|----------|-----------------|----------------|
| **System** | curl, wget, git, vim, python3 | htop, jq, tree, ncdu |
| **Container** | docker, docker-compose | kubectl, helm, k9s |
| **GPU** | nvidia-smi, nvcc | cudnn, nccl |
| **Monitoring** | prometheus, grafana | elk stack, loki |
| **Security** | ufw, fail2ban | ldap, keycloak, certbot |
| **Database** | postgresql, redis | pgadmin, barman |
| **Testing** | pytest, k6 | jmeter, artillery, locust |
| **CI/CD** | github actions | jenkins, gitlab-ci |
| **Documentation** | mkdocs, sphinx | plantuml, draw.io |

### ⚡ **Installation Time Estimates**

- **Basic Setup**: 15-30 minutes
- **Full Development Environment**: 45-60 minutes
- **Production Environment**: 60-90 minutes
- **Enterprise Environment**: 2-4 hours

### 🔄 **Next Steps**

After installing all required tools:

1. **Run Verification Script**: `./verify_tools.sh`
2. **Run Pre-deployment Check**: `./pre_deployment_check.sh`
3. **Proceed with Deployment**: Follow the step-by-step guide
4. **Monitor and Maintain**: Use the monitoring tools installed

This comprehensive tool list ensures you have everything needed for successful GPT Server deployment across different environments and use cases.

## Prerequisites

### Software Requirements

#### Operating System
- **Linux**: Ubuntu 20.04+ or CentOS 7.9+ (Recommended)
- **Windows**: Windows Server 2019+ or Windows 10/11 Pro (Development only)
- **macOS**: 12.0+ (Development only)

#### Python Environment
- **Python Version**: 3.11 or higher (3.11 recommended)
- **Package Manager**: uv 0.1.0+ (recommended) or pip 23.0+
- **Virtual Environment**: Required for isolation

#### System Dependencies

##### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install system dependencies
sudo apt install -y \
    build-essential \
    cmake \
    git \
    curl \
    wget \
    libssl-dev \
    libffi-dev \
    python3-dev \
    python3-pip \
    python3-venv \
    ffmpeg \
    libsndfile1 \
    espeak-ng \
    portaudio19-dev \
    libportaudio2 \
    libportaudiocpp0

# Install CUDA (if using GPU acceleration)
# For CUDA 12.2 (recommended)
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/12.2.0/local_installers/cuda_12.2.0_535.54.03_linux.run
sudo sh cuda_12.2.0_535.54.03_linux.run --no-opengl-libs --no-man-page --no-docs
```

##### CentOS/RHEL
```bash
# Install system dependencies
sudo yum groupinstall -y "Development Tools"
sudo yum install -y \
    cmake \
    git \
    curl \
    wget \
    openssl-devel \
    libffi-devel \
    python3-devel \
    ffmpeg \
    libsndfile \
    espeak-ng \
    portaudio \
    portaudio-devel

# Install EPEL repository
sudo yum install -y epel-release
```

#### Required Python Packages
```bash
# Core dependencies (automatically installed via setup.py)
accelerate>=1.0.1
fastapi==0.115.0
torch==2.6.0
transformers>=4.53.3
vllm==0.10.1
lmdeploy==0.9.2
sglang[all]>=0.4.10.post2
infinity-emb[all]==0.0.76
```

### Network Requirements
- **Inbound Ports**: 8081 (default API port), 21001 (controller port)
- **Outbound Access**: Required for model downloads and external APIs
- **DNS Resolution**: Ability to resolve HuggingFace, ModelScope, and other model repositories

### Storage Requirements
- **Model Storage**: 50GB+ per model (varies by model size)
- **Log Storage**: 10GB+ for logs and temporary files
- **Working Directory**: 20GB+ free space

## Server Specifications

### Minimum Requirements

#### CPU-Only Deployment
- **CPU**: 8 cores (Intel Xeon or AMD EPYC recommended)
- **RAM**: 32GB
- **Storage**: 100GB SSD
- **Network**: 1Gbps Ethernet

#### GPU Deployment (Single GPU)
- **GPU**: NVIDIA RTX 3090 / A5000 or higher (24GB+ VRAM)
- **CPU**: 8 cores
- **RAM**: 64GB
- **Storage**: 500GB NVMe SSD
- **Network**: 10Gbps Ethernet

### Recommended Production Specifications

#### Small Scale (1-5 concurrent users)
- **GPU**: NVIDIA RTX 4090 / A6000 (24GB+ VRAM) × 1
- **CPU**: 16 cores
- **RAM**: 128GB
- **Storage**: 1TB NVMe SSD
- **Network**: 10Gbps Ethernet

#### Medium Scale (5-20 concurrent users)
- **GPU**: NVIDIA A100 (40GB VRAM) × 2
- **CPU**: 32 cores
- **RAM**: 256GB
- **Storage**: 2TB NVMe SSD RAID 1
- **Network**: 25Gbps Ethernet

#### Large Scale (20+ concurrent users)
- **GPU**: NVIDIA A100/H100 (80GB VRAM) × 4-8
- **CPU**: 64+ cores
- **RAM**: 512GB+
- **Storage**: 4TB+ NVMe SSD RAID 10
- **Network**: 100Gbps Ethernet

### Supported Hardware

#### NVIDIA GPUs
- **Minimum**: RTX 30-series or A5000 with 24GB VRAM
- **Recommended**: RTX 40-series, A6000, or A100 with 40GB+ VRAM
- **Optimal**: H100 or A100 with 80GB+ VRAM

#### CPU Requirements
- **Architecture**: x86_64 (AMD64)
- **Instruction Sets**: AVX2, AVX-512 (recommended)
- **Memory Channels**: 8+ channels for optimal performance

## Development Environment Setup

### Local Development Environment

#### Development Tools Installation

```bash
# Install development dependencies
sudo apt install -y \
    git \
    curl \
    wget \
    vim \
    nano \
    htop \
    iotop \
    ncdu \
    tree \
    jq \
    httpie \
    postgresql-client \
    redis-tools

# Install Python development tools
pip install --user \
    black \
    isort \
    flake8 \
    mypy \
    pytest \
    pytest-cov \
    pytest-xdist \
    pre-commit

# Install Docker for development
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### IDE Configuration

##### VS Code Setup
```bash
# Install VS Code extensions for Python development
code --install-extension ms-python.python
code --install-extension ms-python.black-formatter
code --install-extension ms-python.isort
code --install-extension ms-python.flake8
code --install-extension ms-python.mypy-type-checker
code --install-extension ms-vscode.vscode-json
code --install-extension redhat.vscode-yaml
code --install-extension ms-vscode-remote.remote-ssh
```

##### PyCharm Setup
```bash
# Download and install PyCharm Professional
wget https://download.jetbrains.com/python/pycharm-professional-2024.1.1.tar.gz
tar -xzf pycharm-professional-2024.1.1.tar.gz
mv pycharm-2024.1.1 ~/pycharm

# Create desktop shortcut
cat > ~/.local/share/applications/pycharm.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=PyCharm
Icon=/home/$USER/pycharm/bin/pycharm.png
Exec="/home/$USER/pycharm/bin/pycharm.sh" %f
Comment=Python IDE
Categories=Development;IDE;
Terminal=false
StartupWMClass=jetbrains-pycharm
EOF
```

#### Git Configuration

```bash
# Configure Git for development
git config --global user.name "Your Name"
git config --global user.email "your.email@company.com"
git config --global core.editor vim
git config --global pull.rebase true
git config --global init.defaultBranch main

# Setup SSH for GitHub/ModelScope
ssh-keygen -t ed25519 -C "your.email@company.com"
cat ~/.ssh/id_ed25519.pub
# Add the public key to GitHub/ModelScope

# Test SSH connection
ssh -T git@github.com
```

#### Pre-commit Hooks

```bash
# Initialize pre-commit in the project
cd ~/gpt_server
pre-commit install
pre-commit install --hook-type commit-msg

# Create pre-commit configuration
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: debug-statements

  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: ["--max-line-length=88", "--extend-ignore=E203,W503"]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
EOF
```

### CI/CD Integration

#### GitHub Actions Setup

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11, 3.12]

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install uv
      run: curl -LsSf https://astral.sh/uv/install.sh | sh

    - name: Install dependencies
      run: uv sync

    - name: Run tests
      run: uv run pytest tests/ -v --cov=gpt_server --cov-report=xml

    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
        fail_ci_if_error: true

  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11

    - name: Install uv
      run: curl -LsSf https://astral.sh/uv/install.sh | sh

    - name: Install dependencies
      run: uv sync

    - name: Run linters
      run: |
        uv run black --check .
        uv run isort --check-only .
        uv run flake8 .
        uv run mypy .
```

#### Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.11'
        UV_CACHE_DIR = '/tmp/uv-cache'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    curl -LsSf https://astral.sh/uv/install.sh | sh
                    export PATH="$HOME/.cargo/bin:$PATH"
                    uv --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    export PATH="$HOME/.cargo/bin:$PATH"
                    uv sync
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    export PATH="$HOME/.cargo/bin:$PATH"
                    uv run pytest tests/ -v --cov=gpt_server --cov-report=xml --cov-report=html
                '''
            }
            post {
                always {
                    publishCoverage adapters: [coberturaAdapter('coverage.xml')]
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t gpt-server:${BUILD_NUMBER} .
                    docker tag gpt-server:${BUILD_NUMBER} gpt-server:latest
                '''
            }
        }

        stage('Deploy to Staging') {
            steps {
                sh '''
                    docker-compose -f docker-compose.staging.yml down
                    docker-compose -f docker-compose.staging.yml up -d --build
                '''
            }
        }

        stage('Run Integration Tests') {
            steps {
                sh '''
                    sleep 30
                    curl -f http://localhost:8081/v1/models || exit 1
                    uv run pytest tests/test_integration.py -v
                '''
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                input message: 'Deploy to Production?'
                sh '''
                    docker-compose -f docker-compose.prod.yml down
                    docker-compose -f docker-compose.prod.yml up -d --build
                '''
            }
        }
    }

    post {
        always {
            sh '''
                docker-compose -f docker-compose.staging.yml down -v
                docker system prune -f
            '''
        }
        failure {
            mail to: 'devops@company.com',
                 subject: "Failed Pipeline: ${currentBuild.fullDisplayName}",
                 body: "Something is wrong with ${env.BUILD_URL}"
        }
    }
}
```

## Pre-deployment Checklist

### Environment Preparation
- [ ] Server hardware meets minimum requirements
- [ ] Operating system installed and updated
- [ ] Python 3.11+ installed
- [ ] System dependencies installed
- [ ] GPU drivers installed (if using GPU)
- [ ] CUDA installed and configured (if using GPU)
- [ ] Network connectivity verified
- [ ] Firewall rules configured for required ports

### Access and Permissions
- [ ] SSH access configured for administrators
- [ ] sudo privileges for deployment user
- [ ] Model download credentials prepared (HuggingFace/ModelScope tokens)
- [ ] Storage directories created with appropriate permissions
- [ ] Log rotation configured

### Security Preparation
- [ ] SSL certificates obtained (for HTTPS deployment)
- [ ] Firewall rules reviewed and implemented
- [ ] User authentication method decided
- [ ] API key generation strategy planned
- [ ] Monitoring and alerting configured

## Step-by-Step Deployment

### Step 1: Server Preparation

```bash
# Create deployment user
sudo useradd -m -s /bin/bash gptserver
sudo usermod -aG sudo gptserver

# Switch to deployment user
su - gptserver

# Create necessary directories
mkdir -p ~/gpt_server
mkdir -p ~/models
mkdir -p ~/logs
mkdir -p ~/config

# Set proper permissions
chmod 755 ~/gpt_server
chmod 755 ~/models
chmod 755 ~/logs
chmod 755 ~/config
```

### Step 2: Install uv Package Manager

```bash
# Install uv (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# Verify installation
uv --version
```

### Step 3: Clone and Setup Project

```bash
# Clone the repository
cd ~/gpt_server
git clone https://github.com/shell-nlp/gpt_server.git .
cd gpt_server

# Create virtual environment with uv
uv venv --seed

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
uv sync
```

### Step 4: Configure Models

```bash
# Copy configuration template
cp gpt_server/script/config_example.yaml gpt_server/script/config.yaml

# Edit configuration file
nano gpt_server/script/config.yaml
```

#### Sample Configuration for Production

```yaml
serve_args:
  enable: true
  host: 0.0.0.0
  port: 8081
  controller_address: http://localhost:21001
  api_keys: sk-production-key-1,sk-production-key-2

controller_args:
  enable: true
  host: localhost
  port: 21001
  dispatch_method: shortest_queue

model_worker_args:
  host: 0.0.0.0
  controller_address: http://localhost:21001
  log_level: INFO
  limit_worker_concurrency: 100

models:
  - qwen:
      alias: gpt-4,gpt-3.5-turbo
      enable: true
      model_config:
        model_name_or_path: /home/gptserver/models/Qwen2-7B-Instruct
        enable_prefix_caching: true
        dtype: auto
        max_model_len: 32768
        gpu_memory_utilization: 0.9
      model_type: qwen
      work_mode: vllm
      device: gpu
      workers:
        - gpus: [0]

  - bge_embedding:
      alias: text-embedding-ada-002
      enable: true
      model_config:
        model_name_or_path: /home/gptserver/models/BGE-M3
        task_type: embedding
      model_type: embedding
      work_mode: infinity
      device: gpu
      workers:
        - gpus: [0]
```

### Step 5: Download Models

```bash
# Create model download script
cat > download_models.py << 'EOF'
#!/usr/bin/env python3
import os
from modelscope import snapshot_download
from huggingface_hub import snapshot_download as hf_snapshot_download

# Model configurations
models = [
    {
        'name': 'Qwen2-7B-Instruct',
        'source': 'huggingface',
        'repo': 'Qwen/Qwen2-7B-Instruct'
    },
    {
        'name': 'BGE-M3',
        'source': 'huggingface',
        'repo': 'BAAI/bge-m3'
    }
]

model_dir = '/home/gptserver/models'

for model in models:
    print(f"Downloading {model['name']}...")
    if model['source'] == 'huggingface':
        hf_snapshot_download(
            repo_id=model['repo'],
            local_dir=os.path.join(model_dir, model['name']),
            local_dir_use_symlinks=False
        )
    elif model['source'] == 'modelscope':
        snapshot_download(
            model_id=model['repo'],
            cache_dir=os.path.join(model_dir, model['name'])
        )
    print(f"Completed {model['name']}")

print("All models downloaded successfully!")
EOF

# Run model download
python download_models.py
```

### Step 6: Start Services

```bash
# Start the GPT Server
cd ~/gpt_server/gpt_server
uv run gpt_server/serving/main.py

# Or use the startup script
./gpt_server/script/start.sh
```

### Step 7: Verify Deployment

```bash
# Test API connectivity
curl -X POST http://localhost:8081/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-production-key-1" \
  -d '{
    "model": "gpt-4",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'

# Check service status
curl http://localhost:8081/v1/models

# Check controller status
curl http://localhost:21001/list_models
```

## Container Deployment

### Docker Image Optimization

#### Multi-stage Dockerfile

```dockerfile
# Multi-stage build for optimized production image
FROM python:3.11-slim as builder

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy project files
WORKDIR /app
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-install-project

# Production stage
FROM nvidia/cuda:12.2-runtime-ubuntu22.04

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    curl \
    wget \
    git \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash gptserver

# Copy virtual environment from builder
COPY --from=builder /root/.local/share/uv/python /home/gptserver/.local/share/uv/python
COPY --from=builder /root/.local/bin /home/gptserver/.local/bin

# Copy application code
WORKDIR /home/gptserver/gpt_server
COPY . .

# Change ownership
RUN chown -R gptserver:gptserver /home/gptserver

# Switch to non-root user
USER gptserver

# Set environment
ENV PATH="/home/gptserver/.local/bin:$PATH"
ENV PYTHONPATH="/home/gptserver/gpt_server"

# Expose ports
EXPOSE 8081 21001

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8081/v1/models || exit 1

# Start application
CMD ["python", "gpt_server/serving/main.py"]
```

#### Build Optimized Image

```bash
# Build multi-stage image
docker build -t gpt-server:optimized -f Dockerfile.optimized .

# Build with build cache
docker build --cache-from gpt-server:latest -t gpt-server:v1.0.0 .

# Multi-platform build (for ARM64/AMD64)
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64 -t gpt-server:multi-arch .
```

### Advanced Docker Compose

#### Production Docker Compose

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  gpt-server:
    build:
      context: .
      dockerfile: Dockerfile.optimized
      target: production
    container_name: gpt-server-prod
    restart: unless-stopped
    ports:
      - "8081:8081"
      - "21001:21001"
    environment:
      - CUDA_VISIBLE_DEVICES=0,1,2,3
      - GPU_MEMORY_UTILIZATION=0.9
      - LOG_LEVEL=INFO
      - API_KEYS=sk-prod-key-1,sk-prod-key-2
    volumes:
      - ./models:/home/gptserver/models:ro
      - ./logs:/home/gptserver/logs
      - ./config:/home/gptserver/config:ro
    networks:
      - gpt-network
    deploy:
      resources:
        limits:
          cpus: '16.00'
          memory: 128G
        reservations:
          cpus: '8.00'
          memory: 64G
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8081/v1/models"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  redis:
    image: redis:7-alpine
    container_name: gpt-redis
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 1gb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    networks:
      - gpt-network

  nginx:
    image: nginx:alpine
    container_name: gpt-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - ./logs/nginx:/var/log/nginx
    depends_on:
      - gpt-server
    networks:
      - gpt-network

  prometheus:
    image: prom/prometheus:latest
    container_name: gpt-prometheus
    restart: unless-stopped
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    networks:
      - gpt-network

  grafana:
    image: grafana/grafana:latest
    container_name: gpt-grafana
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - gpt-network

networks:
  gpt-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16

volumes:
  redis_data:
  prometheus_data:
  grafana_data:
```

#### Development Docker Compose

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  gpt-server:
    build:
      context: .
      dockerfile: Dockerfile
      target: development
    container_name: gpt-server-dev
    restart: unless-stopped
    ports:
      - "8081:8081"
      - "21001:21001"
    environment:
      - CUDA_VISIBLE_DEVICES=0
      - GPU_MEMORY_UTILIZATION=0.7
      - LOG_LEVEL=DEBUG
      - DEBUG=1
    volumes:
      - .:/home/gptserver/gpt_server
      - ./models:/home/gptserver/models
      - ./logs:/home/gptserver/logs
    networks:
      - gpt-dev-network
    command: ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "gpt_server/serving/main.py"]

  postgres:
    image: postgres:15-alpine
    container_name: gpt-postgres-dev
    restart: unless-stopped
    environment:
      POSTGRES_DB: gpt_server
      POSTGRES_USER: gptserver
      POSTGRES_PASSWORD: dev_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - gpt-dev-network

  redis:
    image: redis:7-alpine
    container_name: gpt-redis-dev
    restart: unless-stopped
    command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    networks:
      - gpt-dev-network

networks:
  gpt-dev-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
```

## Kubernetes Orchestration

### Kubernetes Manifests

#### Namespace

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: gpt-server
  labels:
    name: gpt-server
    app: gpt-server
```

#### ConfigMap

```yaml
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: gpt-server-config
  namespace: gpt-server
data:
  config.yaml: |
    serve_args:
      enable: true
      host: 0.0.0.0
      port: 8081
      controller_address: http://gpt-server-controller:21001
      api_keys: sk-production-key-1,sk-production-key-2

    controller_args:
      enable: true
      host: 0.0.0.0
      port: 21001
      dispatch_method: shortest_queue

    model_worker_args:
      host: 0.0.0.0
      controller_address: http://gpt-server-controller:21001
      log_level: INFO
      limit_worker_concurrency: 100

    models:
      - qwen:
          alias: gpt-4,gpt-3.5-turbo
          enable: true
          model_config:
            model_name_or_path: /models/Qwen2-7B-Instruct
            enable_prefix_caching: true
            dtype: auto
            max_model_len: 32768
            gpu_memory_utilization: 0.9
          model_type: qwen
          work_mode: vllm
          device: gpu
          workers: 1
```

#### Secret

```yaml
# k8s/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: gpt-server-secrets
  namespace: gpt-server
type: Opaque
data:
  # Base64 encoded values
  hf-token: <base64-encoded-huggingface-token>
  modelscope-token: <base64-encoded-modelscope-token>
  api-keys: <base64-encoded-api-keys>
  ssl-cert: <base64-encoded-ssl-certificate>
  ssl-key: <base64-encoded-ssl-private-key>
```

#### PersistentVolumeClaim

```yaml
# k8s/pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: gpt-server-models
  namespace: gpt-server
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 500Gi
  storageClassName: fast-ssd  # Use appropriate storage class
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: gpt-server-logs
  namespace: gpt-server
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi
  storageClassName: standard
```

#### Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gpt-server-controller
  namespace: gpt-server
  labels:
    app: gpt-server
    component: controller
spec:
  replicas: 1
  selector:
    matchLabels:
      app: gpt-server
      component: controller
  template:
    metadata:
      labels:
        app: gpt-server
        component: controller
    spec:
      containers:
      - name: gpt-server
        image: gpt-server:latest
        ports:
        - containerPort: 21001
          name: controller
        env:
        - name: CUDA_VISIBLE_DEVICES
          value: "0"
        - name: GPU_MEMORY_UTILIZATION
          value: "0.8"
        volumeMounts:
        - name: config
          mountPath: /home/gptserver/config
        - name: models
          mountPath: /models
        - name: logs
          mountPath: /home/gptserver/logs
        resources:
          limits:
            nvidia.com/gpu: 1
            cpu: "8"
            memory: "32Gi"
          requests:
            nvidia.com/gpu: 1
            cpu: "4"
            memory: "16Gi"
        livenessProbe:
          httpGet:
            path: /list_models
            port: 21001
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /list_models
            port: 21001
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: config
        configMap:
          name: gpt-server-config
      - name: models
        persistentVolumeClaim:
          claimName: gpt-server-models
      - name: logs
        persistentVolumeClaim:
          claimName: gpt-server-logs
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gpt-server-worker
  namespace: gpt-server
  labels:
    app: gpt-server
    component: worker
spec:
  replicas: 2
  selector:
    matchLabels:
      app: gpt-server
      component: worker
  template:
    metadata:
      labels:
        app: gpt-server
        component: worker
    spec:
      containers:
      - name: gpt-server
        image: gpt-server:latest
        ports:
        - containerPort: 8081
          name: api
        env:
        - name: CUDA_VISIBLE_DEVICES
          value: "0,1"
        - name: GPU_MEMORY_UTILIZATION
          value: "0.9"
        volumeMounts:
        - name: config
          mountPath: /home/gptserver/config
        - name: models
          mountPath: /models
        - name: logs
          mountPath: /home/gptserver/logs
        resources:
          limits:
            nvidia.com/gpu: 2
            cpu: "16"
            memory: "64Gi"
          requests:
            nvidia.com/gpu: 2
            cpu: "8"
            memory: "32Gi"
        livenessProbe:
          httpGet:
            path: /v1/models
            port: 8081
          initialDelaySeconds: 60
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /v1/models
            port: 8081
          initialDelaySeconds: 30
          periodSeconds: 10
      volumes:
      - name: config
        configMap:
          name: gpt-server-config
      - name: models
        persistentVolumeClaim:
          claimName: gpt-server-models
      - name: logs
        persistentVolumeClaim:
          claimName: gpt-server-logs
```

#### Service

```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: gpt-server-controller
  namespace: gpt-server
spec:
  selector:
    app: gpt-server
    component: controller
  ports:
  - name: controller
    port: 21001
    targetPort: 21001
  type: ClusterIP
---
apiVersion: v1
kind: Service
metadata:
  name: gpt-server-api
  namespace: gpt-server
spec:
  selector:
    app: gpt-server
    component: worker
  ports:
  - name: api
    port: 8081
    targetPort: 8081
  type: LoadBalancer
```

#### Ingress

```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: gpt-server-ingress
  namespace: gpt-server
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - api.yourcompany.com
    secretName: gpt-server-tls
  rules:
  - host: api.yourcompany.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: gpt-server-api
            port:
              number: 8081
```

#### HorizontalPodAutoscaler

```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: gpt-server-hpa
  namespace: gpt-server
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: gpt-server-worker
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: External
    external:
      metric:
        name: gpt_server_requests_per_second
        selector:
          matchLabels:
            app: gpt-server
      target:
        type: AverageValue
        averageValue: "100"
```

### Deploy to Kubernetes

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/hpa.yaml

# Check deployment status
kubectl get pods -n gpt-server
kubectl get services -n gpt-server
kubectl get ingress -n gpt-server

# Check logs
kubectl logs -f deployment/gpt-server-worker -n gpt-server

# Scale deployment
kubectl scale deployment gpt-server-worker --replicas=4 -n gpt-server
```

## Configuration Management

### Environment Variables

```bash
# Create environment file
cat > ~/gpt_server/.env << EOF
# Model paths
MODEL_DIR=/home/gptserver/models

# Logging
LOG_LEVEL=INFO
LOG_DIR=/home/gptserver/logs

# API Configuration
API_HOST=0.0.0.0
API_PORT=8081
CONTROLLER_HOST=localhost
CONTROLLER_PORT=21001

# Security
API_KEYS=sk-production-key-1,sk-production-key-2
SECRET_KEY=your-secret-key-here

# Performance
MAX_WORKERS=10
WORKER_TIMEOUT=300
MAX_REQUEST_SIZE=100MB

# GPU Configuration
CUDA_VISIBLE_DEVICES=0,1
GPU_MEMORY_UTILIZATION=0.9
EOF
```

### Advanced Configuration Options

#### Load Balancing
```yaml
controller_args:
  enable: true
  host: localhost
  port: 21001
  dispatch_method: shortest_queue  # Options: lottery, shortest_queue
```

#### Multi-GPU Configuration
```yaml
models:
  - qwen:
      enable: true
      model_config:
        model_name_or_path: /home/gptserver/models/Qwen2-72B-Instruct
        enable_prefix_caching: true
        dtype: auto
        tensor_parallel_size: 4  # Use 4 GPUs
      work_mode: vllm
      device: gpu
      workers:
        - gpus: [0,1,2,3]  # Specify GPU IDs
```

#### Memory Optimization
```yaml
model_config:
  gpu_memory_utilization: 0.9
  kv_cache_quant_policy: 4  # FP8 quantization
  enable_prefix_caching: true
  max_model_len: 32768
```

## Model Management

### Adding New Models

```bash
# Stop services
pkill -f gpt_server

# Add new model configuration to config.yaml
nano gpt_server/script/config.yaml

# Download new model
python download_models.py

# Restart services
uv run gpt_server/serving/main.py
```

### Model Version Management

```bash
# Create model version directory structure
mkdir -p ~/models/archive
mkdir -p ~/models/current

# Backup current model
cp -r ~/models/Qwen2-7B-Instruct ~/models/archive/Qwen2-7B-Instruct-v1.0

# Update to new version
# Edit config.yaml with new model path
# Download new model version
# Update symbolic link
ln -sf ~/models/Qwen2-7B-Instruct-v2.0 ~/models/current/qwen-latest
```

### Model Performance Monitoring

```bash
# Monitor GPU usage
nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv -l 5

# Monitor system resources
htop

# Check API response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8081/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4", "messages": [{"role": "user", "content": "Test"}]}'
```

## API Integration

### API Gateway Integration

#### Kong Gateway

```yaml
# kong/declarative_config.yaml
_format_version: "3.0"

services:
  - name: gpt-server
    url: http://gpt-server-api:8081
    routes:
      - name: gpt-server-route
        paths:
          - /v1
        methods:
          - GET
          - POST
        plugins:
          - name: rate-limiting
            config:
              minute: 100
              hour: 1000
              day: 10000
          - name: request-size-limiting
            config:
              allowed_payload_size: 10485760  # 10MB
          - name: cors
            config:
              origins:
                - "*"
              methods:
                - GET
                - POST
                - OPTIONS
              headers:
                - Accept
                - Accept-Version
                - Content-Length
                - Content-MD5
                - Content-Type
                - Date
                - Authorization
              credentials: true
          - name: key-auth
            config:
              key_names:
                - Authorization
              hide_credentials: true

consumers:
  - username: client-app-1
    keyauth_credentials:
      - key: sk-production-key-1
  - username: client-app-2
    keyauth_credentials:
      - key: sk-production-key-2
```

#### AWS API Gateway

```yaml
# aws/api-gateway.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'API Gateway for GPT Server'

Resources:
  GptServerApi:
    Type: AWS::ApiGateway::RestApi
    Properties:
      Name: gpt-server-api
      Description: API Gateway for GPT Server
      EndpointConfiguration:
        Types:
          - REGIONAL

  GptServerResource:
    Type: AWS::ApiGateway::Resource
    Properties:
      RestApiId: !Ref GptServerApi
      ParentId: !GetAtt GptServerApi.RootResourceId
      PathPart: v1

  GptServerMethod:
    Type: AWS::ApiGateway::Method
    Properties:
      RestApiId: !Ref GptServerApi
      ResourceId: !Ref GptServerResource
      HttpMethod: ANY
      AuthorizationType: AWS_IAM
      ApiKeyRequired: true

  GptServerIntegration:
    Type: AWS::ApiGateway::Integration
    Properties:
      RestApiId: !Ref GptServerApi
      ResourceId: !Ref GptServerResource
      HttpMethod: ANY
      IntegrationHttpMethod: ANY
      Type: HTTP_PROXY
      Uri: !Sub http://${EcsServiceLoadBalancer}:8081/v1/{proxy}
      PassthroughBehavior: WHEN_NO_MATCH
      IntegrationResponses:
        - StatusCode: 200
          ResponseParameters:
            method.response.header.Access-Control-Allow-Origin: "'*'"

  ApiKey:
    Type: AWS::ApiGateway::ApiKey
    Properties:
      Name: gpt-server-key
      Description: API Key for GPT Server
      Enabled: true

  UsagePlan:
    Type: AWS::ApiGateway::UsagePlan
    Properties:
      Name: gpt-server-usage-plan
      Description: Usage plan for GPT Server
      ThrottleSettings:
        BurstLimit: 100
        RateLimit: 50
      QuotaSettings:
        Limit: 10000
        Offset: 0
        Period: DAY

  UsagePlanKey:
    Type: AWS::ApiGateway::UsagePlanKey
    Properties:
      KeyId: !Ref ApiKey
      KeyType: API_KEY
      UsagePlanId: !Ref UsagePlan

  Deployment:
    Type: AWS::ApiGateway::Deployment
    DependsOn: GptServerIntegration
    Properties:
      RestApiId: !Ref GptServerApi
      StageName: prod
      StageDescription:
        Description: Production stage
        Variables:
          lambdaAlias: prod
```

### Authentication Integration

#### OAuth 2.0 / OpenID Connect

```python
# oauth_integration.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os

security = HTTPBearer()

class AuthService:
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, credentials: HTTPAuthorizationCredentials = Depends(security)):
        try:
            payload = jwt.decode(credentials.credentials, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return username
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

auth_service = AuthService()
```

#### LDAP Integration

```python
# ldap_integration.py
import ldap
from ldap import LDAPError
from typing import Optional

class LDAPService:
    def __init__(self):
        self.ldap_server = os.getenv("LDAP_SERVER", "ldap://localhost:389")
        self.ldap_base_dn = os.getenv("LDAP_BASE_DN", "dc=company,dc=com")
        self.ldap_user_dn = os.getenv("LDAP_USER_DN", "cn=admin,dc=company,dc=com")
        self.ldap_password = os.getenv("LDAP_PASSWORD", "admin_password")

    def authenticate_user(self, username: str, password: str) -> Optional[dict]:
        try:
            # Initialize LDAP connection
            ldap_client = ldap.initialize(self.ldap_server)
            ldap_client.set_option(ldap.OPT_REFERRALS, 0)

            # Bind with user credentials
            user_dn = f"cn={username},{self.ldap_base_dn}"
            ldap_client.simple_bind_s(user_dn, password)

            # Search for user details
            search_filter = f"(cn={username})"
            search_attrs = ["cn", "mail", "memberOf"]

            result = ldap_client.search_s(
                self.ldap_base_dn,
                ldap.SCOPE_SUBTREE,
                search_filter,
                search_attrs
            )

            if result:
                dn, attrs = result[0]
                user_info = {
                    "username": username,
                    "email": attrs.get("mail", [b""])[0].decode("utf-8"),
                    "groups": [group.decode("utf-8") for group in attrs.get("memberOf", [])]
                }
                return user_info

        except LDAPError as e:
            print(f"LDAP authentication failed: {e}")
            return None
        finally:
            if 'ldap_client' in locals():
                ldap_client.unbind()

    def authorize_user(self, user_info: dict, required_groups: list = None) -> bool:
        if not required_groups:
            return True

        user_groups = user_info.get("groups", [])
        return any(group in user_groups for group in required_groups)

ldap_service = LDAPService()
```

### Webhook Integration

```python
# webhook_integration.py
from fastapi import BackgroundTasks, HTTPException
import httpx
import json
from typing import Dict, Any, List
import asyncio

class WebhookService:
    def __init__(self):
        self.webhooks: Dict[str, str] = {}
        self.client = httpx.AsyncClient(timeout=30.0)

    async def register_webhook(self, event_type: str, url: str):
        """Register a webhook URL for a specific event type"""
        self.webhooks[event_type] = url

    async def trigger_webhook(self, event_type: str, payload: Dict[str, Any]):
        """Trigger webhook for a specific event"""
        if event_type not in self.webhooks:
            return

        url = self.webhooks[event_type]
        webhook_payload = {
            "event_type": event_type,
            "timestamp": asyncio.get_event_loop().time(),
            "data": payload
        }

        try:
            response = await self.client.post(
                url,
                json=webhook_payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
        except httpx.HTTPError as e:
            print(f"Webhook delivery failed: {e}")

    async def trigger_completion_webhook(self, completion_data: Dict[str, Any]):
        """Trigger webhook when completion is finished"""
        await self.trigger_webhook("completion.finished", completion_data)

    async def trigger_error_webhook(self, error_data: Dict[str, Any]):
        """Trigger webhook when error occurs"""
        await self.trigger_webhook("error.occurred", error_data)

    async def trigger_model_loaded_webhook(self, model_data: Dict[str, Any]):
        """Trigger webhook when model is loaded"""
        await self.trigger_webhook("model.loaded", model_data)

webhook_service = WebhookService()
```

### Database Integration

#### PostgreSQL Integration

```python
# database_integration.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class CompletionLog(Base):
    __tablename__ = 'completion_logs'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(255))
    model = Column(String(100))
    prompt = Column(Text)
    response = Column(Text)
    tokens_used = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    response_time = Column(Integer)  # in milliseconds

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    email = Column(String(255), unique=True)
    api_key = Column(String(255), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

class DatabaseService:
    def __init__(self):
        database_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/gpt_server")
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def log_completion(self, user_id: str, model: str, prompt: str, response: str, tokens_used: int, response_time: int):
        """Log completion request"""
        session = self.SessionLocal()
        try:
            log_entry = CompletionLog(
                user_id=user_id,
                model=model,
                prompt=prompt,
                response=response,
                tokens_used=tokens_used,
                response_time=response_time
            )
            session.add(log_entry)
            session.commit()
        finally:
            session.close()

    def get_user_by_api_key(self, api_key: str):
        """Get user by API key"""
        session = self.SessionLocal()
        try:
            user = session.query(User).filter(User.api_key == api_key).first()
            return user
        finally:
            session.close()

    def update_user_last_login(self, user_id: int):
        """Update user's last login time"""
        session = self.SessionLocal()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                user.last_login = datetime.utcnow()
                session.commit()
        finally:
            session.close()

db_service = DatabaseService()
```

## Testing Strategies

### Development Testing

#### Unit Testing

```python
# tests/test_model_handler.py
import pytest
from unittest.mock import Mock, patch
from gpt_server.model_handler.qwen import QwenWorker

class TestQwenWorker:
    @pytest.fixture
    def worker(self):
        return QwenWorker(
            controller_addr="localhost:21001",
            worker_addr="localhost:8081",
            worker_id="test-worker",
            model_path="/path/to/model",
            model_names=["qwen-7b"],
            limit_worker_concurrency=10
        )

    @pytest.mark.asyncio
    async def test_generate_stream(self, worker):
        params = {
            "messages": [{"role": "user", "content": "Hello"}],
            "temperature": 0.7,
            "max_tokens": 100
        }

        with patch.object(worker.backend, 'stream_chat') as mock_stream:
            mock_response = Mock()
            mock_response.__aiter__ = Mock(return_value=iter([{"text": "Hi there!"}]))
            mock_stream.return_value = mock_response

            responses = []
            async for response in worker.generate_stream(params):
                responses.append(response)

            assert len(responses) > 0
            assert "text" in responses[0]

    def test_validate_params(self, worker):
        valid_params = {
            "messages": [{"role": "user", "content": "Test"}],
            "temperature": 0.5,
            "max_tokens": 50
        }
        invalid_params = {
            "messages": [],
            "temperature": 2.5  # Invalid temperature
        }

        assert worker.validate_params(valid_params) is True
        assert worker.validate_params(invalid_params) is False
```

#### Integration Testing

```python
# tests/test_integration.py
import pytest
import httpx
from fastapi.testclient import TestClient
from gpt_server.serving.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_chat_completion_integration(client):
    """Test full chat completion flow"""
    response = client.post(
        "/v1/chat/completions",
        json={
            "model": "gpt-4",
            "messages": [
                {"role": "user", "content": "Say hello"}
            ],
            "max_tokens": 10
        },
        headers={"Authorization": "Bearer test-key"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "choices" in data
    assert len(data["choices"]) > 0
    assert "message" in data["choices"][0]
    assert "content" in data["choices"][0]["message"]

def test_model_list_integration(client):
    """Test model listing"""
    response = client.get("/v1/models")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0

@pytest.mark.asyncio
async def test_concurrent_requests():
    """Test concurrent request handling"""
    async with httpx.AsyncClient(base_url="http://localhost:8081") as client:
        tasks = []
        for i in range(10):
            task = client.post(
                "/v1/chat/completions",
                json={
                    "model": "gpt-4",
                    "messages": [{"role": "user", "content": f"Test {i}"}],
                    "max_tokens": 5
                },
                headers={"Authorization": "Bearer test-key"}
            )
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

        for response in responses:
            assert response.status_code == 200
```

### Production Testing

#### Load Testing

```python
# tests/test_load.py
import asyncio
import httpx
import time
from typing import List, Dict
import statistics

async def load_test_concurrent_users(num_users: int = 50, duration: int = 60):
    """Load test with concurrent users"""
    results = []

    async def single_user_test(user_id: int):
        user_results = []
        async with httpx.AsyncClient(base_url="http://localhost:8081", timeout=30.0) as client:
            start_time = time.time()
            while time.time() - start_time < duration:
                request_start = time.time()
                try:
                    response = await client.post(
                        "/v1/chat/completions",
                        json={
                            "model": "gpt-4",
                            "messages": [{"role": "user", "content": f"User {user_id} test"}],
                            "max_tokens": 20
                        },
                        headers={"Authorization": "Bearer test-key"}
                    )
                    request_end = time.time()
                    user_results.append({
                        "success": response.status_code == 200,
                        "response_time": request_end - request_start,
                        "status_code": response.status_code
                    })
                except Exception as e:
                    request_end = time.time()
                    user_results.append({
                        "success": False,
                        "response_time": request_end - request_start,
                        "error": str(e)
                    })
                await asyncio.sleep(0.1)  # Small delay between requests
        return user_results

    # Run concurrent users
    tasks = [single_user_test(i) for i in range(num_users)]
    all_results = await asyncio.gather(*tasks)

    # Aggregate results
    flattened_results = [result for user_results in all_results for result in user_results]

    successful_requests = [r for r in flattened_results if r["success"]]
    failed_requests = [r for r in flattened_results if not r["success"]]

    if successful_requests:
        response_times = [r["response_time"] for r in successful_requests]
        print("Load Test Results:")
        print(f"Total Requests: {len(flattened_results)}")
        print(f"Successful Requests: {len(successful_requests)}")
        print(f"Failed Requests: {len(failed_requests)}")
        print(f"Success Rate: {len(successful_requests)/len(flattened_results)*100:.2f}%")
        print(f"Average Response Time: {statistics.mean(response_times):.3f}s")
        print(f"Median Response Time: {statistics.median(response_times):.3f}s")
        print(f"95th Percentile: {statistics.quantiles(response_times, n=20)[18]:.3f}s")
        print(f"99th Percentile: {statistics.quantiles(response_times, n=100)[98]:.3f}s")

    return flattened_results

if __name__ == "__main__":
    asyncio.run(load_test_concurrent_users())
```

#### Stress Testing

```python
# tests/test_stress.py
import asyncio
import httpx
import time
from concurrent.futures import ThreadPoolExecutor
import psutil
import GPUtil

async def stress_test_memory_leak(duration: int = 300):
    """Stress test to check for memory leaks"""
    initial_memory = psutil.virtual_memory().used
    initial_gpu_memory = GPUtil.getGPUs()[0].memoryUsed if GPUtil.getGPUs() else 0

    async with httpx.AsyncClient(base_url="http://localhost:8081", timeout=60.0) as client:
        start_time = time.time()
        request_count = 0

        while time.time() - start_time < duration:
            try:
                # Send various types of requests
                tasks = []
                for i in range(10):
                    if i % 3 == 0:
                        # Chat completion
                        task = client.post("/v1/chat/completions", json={
                            "model": "gpt-4",
                            "messages": [{"role": "user", "content": f"Test {i}"}],
                            "max_tokens": 50
                        }, headers={"Authorization": "Bearer test-key"})
                    elif i % 3 == 1:
                        # Embedding
                        task = client.post("/v1/embeddings", json={
                            "model": "text-embedding-ada-002",
                            "input": f"Test input {i}"
                        }, headers={"Authorization": "Bearer test-key"})
                    else:
                        # Model list
                        task = client.get("/v1/models")

                    tasks.append(task)

                responses = await asyncio.gather(*tasks, return_exceptions=True)
                request_count += len(tasks)

                # Check memory usage every 10 seconds
                if request_count % 100 == 0:
                    current_memory = psutil.virtual_memory().used
                    current_gpu_memory = GPUtil.getGPUs()[0].memoryUsed if GPUtil.getGPUs() else 0

                    memory_increase = current_memory - initial_memory
                    gpu_memory_increase = current_gpu_memory - initial_gpu_memory

                    print(f"Requests: {request_count}")
                    print(f"Memory Increase: {memory_increase / 1024 / 1024:.1f} MB")
                    if gpu_memory_increase > 0:
                        print(f"GPU Memory Increase: {gpu_memory_increase:.1f} MB")

            except Exception as e:
                print(f"Error in stress test: {e}")
                await asyncio.sleep(1)

    print(f"Stress test completed. Total requests: {request_count}")

if __name__ == "__main__":
    asyncio.run(stress_test_memory_leak())
```

### Performance Benchmarking

```python
# tests/benchmark.py
import time
import httpx
import asyncio
from typing import List, Dict
import json

class BenchmarkSuite:
    def __init__(self, base_url: str = "http://localhost:8081"):
        self.base_url = base_url
        self.client = httpx.Client(timeout=60.0)

    def benchmark_chat_completion(self, prompts: List[str], model: str = "gpt-4") -> Dict:
        """Benchmark chat completion performance"""
        results = []

        for prompt in prompts:
            start_time = time.time()
            response = self.client.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 100,
                    "temperature": 0.7
                },
                headers={"Authorization": "Bearer test-key"}
            )
            end_time = time.time()

            if response.status_code == 200:
                data = response.json()
                tokens_generated = len(data["choices"][0]["message"]["content"].split())
                results.append({
                    "prompt_length": len(prompt.split()),
                    "response_time": end_time - start_time,
                    "tokens_generated": tokens_generated,
                    "tokens_per_second": tokens_generated / (end_time - start_time)
                })

        return {
            "total_requests": len(results),
            "successful_requests": len(results),
            "average_response_time": sum(r["response_time"] for r in results) / len(results),
            "average_tokens_per_second": sum(r["tokens_per_second"] for r in results) / len(results),
            "results": results
        }

    def benchmark_embeddings(self, texts: List[str], model: str = "text-embedding-ada-002") -> Dict:
        """Benchmark embedding performance"""
        results = []

        for text in texts:
            start_time = time.time()
            response = self.client.post(
                f"{self.base_url}/v1/embeddings",
                json={
                    "model": model,
                    "input": text
                },
                headers={"Authorization": "Bearer test-key"}
            )
            end_time = time.time()

            if response.status_code == 200:
                data = response.json()
                embedding_dim = len(data["data"][0]["embedding"])
                results.append({
                    "text_length": len(text.split()),
                    "response_time": end_time - start_time,
                    "embedding_dimension": embedding_dim
                })

        return {
            "total_requests": len(results),
            "successful_requests": len(results),
            "average_response_time": sum(r["response_time"] for r in results) / len(results),
            "results": results
        }

    def run_comprehensive_benchmark(self):
        """Run comprehensive benchmark suite"""
        print("Running GPT Server Benchmark Suite...")
        print("=" * 50)

        # Test prompts of different lengths
        prompts = [
            "Hello",  # Short
            "Explain quantum computing in simple terms",  # Medium
            "Write a detailed essay about artificial intelligence and its impact on society",  # Long
        ] * 5  # Repeat for statistical significance

        # Chat completion benchmark
        print("Benchmarking Chat Completion...")
        chat_results = self.benchmark_chat_completion(prompts)
        print(f"Average Response Time: {chat_results['average_response_time']:.3f}s")
        print(f"Average Tokens/Second: {chat_results['average_tokens_per_second']:.2f}")
        print()

        # Embedding benchmark
        print("Benchmarking Embeddings...")
        texts = ["Hello world", "Machine learning is fascinating", "Natural language processing with transformers"] * 5
        embedding_results = self.benchmark_embeddings(texts)
        print(f"Average Response Time: {embedding_results['average_response_time']:.3f}s")
        print()

        # Save results
        results = {
            "timestamp": time.time(),
            "chat_completion": chat_results,
            "embeddings": embedding_results
        }

        with open("benchmark_results.json", "w") as f:
            json.dump(results, f, indent=2)

        print("Benchmark completed. Results saved to benchmark_results.json")

if __name__ == "__main__":
    benchmark = BenchmarkSuite()
    benchmark.run_comprehensive_benchmark()
```

## Compliance and Regulatory

```bash
# Monitor GPU usage
nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv -l 5

# Monitor system resources
htop

# Check API response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8081/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4", "messages": [{"role": "user", "content": "Test"}]}'
```

## Monitoring and Maintenance

### Log Management

```bash
# Configure log rotation
cat > /etc/logrotate.d/gpt_server << EOF
/home/gptserver/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 gptserver gptserver
    postrotate
        systemctl reload gpt_server 2>/dev/null || true
    endscript
}
EOF

# Enable log rotation
sudo systemctl enable logrotate
sudo systemctl start logrotate
```

### Health Checks

```bash
# Create health check script
cat > ~/gpt_server/health_check.sh << 'EOF'
#!/bin/bash

# Check if services are running
if ! pgrep -f "gpt_server" > /dev/null; then
    echo "GPT Server is not running!"
    exit 1
fi

# Check API health
if ! curl -f http://localhost:8081/v1/models > /dev/null; then
    echo "API health check failed!"
    exit 1
fi

# Check controller health
if ! curl -f http://localhost:21001/list_models > /dev/null; then
    echo "Controller health check failed!"
    exit 1
fi

# Check disk space
DISK_USAGE=$(df /home/gptserver | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 90 ]; then
    echo "Disk usage is above 90%!"
    exit 1
fi

# Check memory usage
MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
if [ $MEMORY_USAGE -gt 90 ]; then
    echo "Memory usage is above 90%!"
    exit 1
fi

echo "All health checks passed!"
EOF

chmod +x ~/gpt_server/health_check.sh

# Run health check
~/gpt_server/health_check.sh
```

### Backup Strategy

```bash
# Create backup script
cat > ~/gpt_server/backup.sh << 'EOF'
#!/bin/bash

BACKUP_DIR="/home/gptserver/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="gpt_server_backup_$DATE"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup configuration
cp ~/gpt_server/gpt_server/script/config.yaml $BACKUP_DIR/config_$DATE.yaml

# Backup logs (last 7 days)
find ~/logs -name "*.log" -mtime -7 -exec cp {} $BACKUP_DIR/ \;

# Create archive
tar -czf $BACKUP_DIR/$BACKUP_NAME.tar.gz -C ~/gpt_server .

# Clean old backups (keep last 10)
cd $BACKUP_DIR
ls -t *.tar.gz | tail -n +11 | xargs -r rm --

echo "Backup completed: $BACKUP_NAME.tar.gz"
EOF

chmod +x ~/gpt_server/backup.sh

# Schedule daily backups
crontab -e
# Add: 0 2 * * * /home/gptserver/gpt_server/backup.sh
```

## Troubleshooting

### Common Issues

#### 1. CUDA Out of Memory
```bash
# Reduce GPU memory utilization
nano gpt_server/script/config.yaml
# Change gpu_memory_utilization from 0.9 to 0.7

# Restart service
pkill -f gpt_server
uv run gpt_server/serving/main.py
```

#### 2. Model Download Failures
```bash
# Check network connectivity
ping huggingface.co
ping modelscope.cn

# Verify credentials
export HF_TOKEN=your_huggingface_token
export MODELSCOPE_TOKEN=your_modelscope_token

# Retry download with different mirror
export HF_ENDPOINT=https://hf-mirror.com
```

#### 3. Port Already in Use
```bash
# Find process using port
lsof -i :8081
lsof -i :21001

# Kill conflicting process
sudo kill -9 <PID>

# Or change ports in config.yaml
nano gpt_server/script/config.yaml
```

#### 4. Import Errors
```bash
# Reinstall dependencies
cd ~/gpt_server
rm -rf .venv
uv venv --seed
source .venv/bin/activate
uv sync

# Check Python path
python -c "import sys; print(sys.path)"
```

#### 5. Slow Inference
```bash
# Enable prefix caching
nano gpt_server/script/config.yaml
# Set enable_prefix_caching: true

# Use optimized backend
# Change work_mode from hf to vllm or lmdeploy

# Restart service
pkill -f gpt_server
uv run gpt_server/serving/main.py
```

### Performance Tuning

#### GPU Optimization
```bash
# Enable CUDA optimizations
export CUDA_LAUNCH_BLOCKING=0
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

# Use flash attention
export USE_FLASH_ATTENTION=1
```

#### Memory Optimization
```bash
# Enable memory efficient attention
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

# Use gradient checkpointing for large models
export GRADIENT_CHECKPOINTING=1
```

#### Network Optimization
```bash
# Increase connection limits
echo "net.core.somaxconn=65536" >> /etc/sysctl.conf
echo "net.ipv4.tcp_max_syn_backlog=65536" >> /etc/sysctl.conf
sysctl -p
```

## Security Considerations

### Network Security
```bash
# Configure firewall
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 8081/tcp
sudo ufw allow 21001/tcp

# Use HTTPS (recommended)
# Install nginx as reverse proxy
sudo apt install nginx
sudo certbot --nginx -d your-domain.com
```

### API Security
```bash
# Use strong API keys
# Generate random keys
openssl rand -hex 32

# Implement rate limiting
# Configure in your reverse proxy or load balancer

# Enable request logging
export LOG_REQUESTS=1
```

### Data Protection
```bash
# Encrypt sensitive data
# Use encrypted storage for API keys and configuration

# Implement audit logging
export AUDIT_LOG=1

# Regular security updates
sudo apt update && sudo apt upgrade
```

## Performance Optimization

### Benchmarking

```bash
# Run performance tests
cd ~/gpt_server
python tests/test_perf.py

# Monitor system resources during load
# Use tools like sar, iostat, iotop
sar -u 1 60  # CPU usage
sar -r 1 60  # Memory usage
iostat -x 1 60  # Disk I/O
```

### Scaling Strategies

#### Horizontal Scaling
```bash
# Deploy multiple instances behind load balancer
# Use nginx or haproxy for load balancing

# Example nginx configuration
cat > /etc/nginx/sites-available/gpt_server << EOF
upstream gpt_backend {
    server 127.0.0.1:8081;
    server 127.0.0.1:8082;
    server 127.0.0.1:8083;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://gpt_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF
```

#### Vertical Scaling
```bash
# Upgrade hardware
# Add more GPUs
# Increase RAM
# Use faster storage (NVMe SSD)

# Optimize model configuration
# Use larger batch sizes
# Enable model parallelism
# Use optimized backends (vLLM, SGLang)
```

### Caching Strategies

```bash
# Enable response caching
export ENABLE_CACHE=1
export CACHE_SIZE=1000
export CACHE_TTL=3600

# Use Redis for distributed caching
# Install Redis
sudo apt install redis-server

# Configure Redis
nano /etc/redis/redis.conf
# Set appropriate memory limits and persistence
```

## Cost Optimization

### Cloud Cost Management

#### AWS Cost Optimization

```bash
# aws/cost_optimization.sh
#!/bin/bash

# Set AWS region
AWS_REGION=us-east-1

# Get current instance pricing
aws ec2 describe-spot-price-history \
    --instance-types p4d.24xlarge,g5.12xlarge,g4dn.12xlarge \
    --product-descriptions "Linux/UNIX" \
    --start-time $(date +%Y-%m-%dT%H:%M:%S) \
    --region $AWS_REGION \
    --output table

# Check reserved instance recommendations
aws ce get-reservation-purchase-recommendation \
    --service "Amazon Elastic Compute Cloud - Compute" \
    --lookback-period-in-days 30 \
    --term-in-years 1 \
    --payment-option ALL_UPFRONT

# Monitor costs by service
aws ce get-cost-and-usage \
    --time-period Start=2024-01-01,End=2024-01-31 \
    --granularity MONTHLY \
    --metrics "BlendedCost" \
    --group-by Type=AZ,Key=AZ \
    --region $AWS_REGION

# Set up cost allocation tags
aws ce create-cost-category-definition \
    --name "GPT-Server-Environment" \
    --rule-version "CostCategoryExpression.v1" \
    --rules '[
        {
            "Value": "Production",
            "Rule": {
                "Tags": {
                    "Key": "Environment",
                    "Values": ["prod"]
                }
            }
        },
        {
            "Value": "Development",
            "Rule": {
                "Tags": {
                    "Key": "Environment",
                    "Values": ["dev", "staging"]
                }
            }
        }
    ]'
```

#### Spot Instance Strategy

```yaml
# k8s/spot-instance-strategy.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: spot-instance-config
  namespace: gpt-server
data:
  spot-strategy.json: |
    {
      "spot_fleet_request_config": {
        "IamFleetRole": "arn:aws:iam::123456789012:role/aws-ec2-spot-fleet-role",
        "AllocationStrategy": "lowestPrice",
        "TargetCapacity": 10,
        "SpotPrice": "0.50",
        "TerminateInstancesWithExpiration": true,
        "LaunchSpecifications": [
          {
            "ImageId": "ami-12345678",
            "InstanceType": "g4dn.12xlarge",
            "KeyName": "gpt-server-key",
            "SecurityGroups": ["sg-12345678"],
            "SubnetId": "subnet-12345678",
            "WeightedCapacity": 1.0,
            "SpotPrice": "0.50"
          }
        ]
      }
    }
```

### Resource Optimization

#### Auto-scaling Configuration

```yaml
# k8s/advanced-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: gpt-server-advanced-hpa
  namespace: gpt-server
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: gpt-server-worker
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: External
    external:
      metric:
        name: gpu_utilization
        selector:
          matchLabels:
            app: gpt-server
      target:
        type: AverageValue
        averageValue: "75"
  - type: External
    external:
      metric:
        name: model_queue_depth
        selector:
          matchLabels:
            app: gpt-server
      target:
        type: AverageValue
        averageValue: "5"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
      - type: Pods
        value: 2
        periodSeconds: 60
      selectPolicy: Min
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 60
      - type: Pods
        value: 4
        periodSeconds: 60
      selectPolicy: Max
```

#### GPU Memory Optimization

```python
# optimization/gpu_memory_manager.py
import torch
import gc
from typing import Dict, List
import psutil
import GPUtil

class GPUMemoryManager:
    def __init__(self, memory_threshold: float = 0.9):
        self.memory_threshold = memory_threshold
        self.gpu_memory_history = []

    def get_gpu_memory_usage(self) -> Dict[str, float]:
        """Get current GPU memory usage"""
        gpus = GPUtil.getGPUs()
        if not gpus:
            return {"usage": 0.0, "free": 0, "used": 0, "total": 0}

        gpu = gpus[0]
        return {
            "usage": gpu.memoryUsed / gpu.memoryTotal,
            "free": gpu.memoryFree,
            "used": gpu.memoryUsed,
            "total": gpu.memoryTotal
        }

    def should_trigger_gc(self) -> bool:
        """Determine if garbage collection should be triggered"""
        memory_info = self.get_gpu_memory_usage()
        usage = memory_info["usage"]

        # Add to history for trend analysis
        self.gpu_memory_history.append(usage)
        if len(self.gpu_memory_history) > 10:
            self.gpu_memory_history.pop(0)

        # Trigger GC if usage is above threshold and trending up
        if usage > self.memory_threshold:
            if len(self.gpu_memory_history) >= 3:
                recent_trend = self.gpu_memory_history[-1] - self.gpu_memory_history[-3]
                if recent_trend > 0.05:  # Usage increasing
                    return True

        return False

    def optimize_memory(self):
        """Perform memory optimization"""
        # Clear PyTorch cache
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        # Force garbage collection
        gc.collect()

        # Clear unused variables
        for obj in gc.get_objects():
            if hasattr(obj, '__dict__'):
                for attr in list(obj.__dict__.keys()):
                    if attr.startswith('_unused_'):
                        delattr(obj, attr)

    def monitor_memory_loop(self):
        """Background memory monitoring"""
        import threading
        import time

        def monitor():
            while True:
                if self.should_trigger_gc():
                    print("High GPU memory usage detected, triggering optimization...")
                    self.optimize_memory()
                time.sleep(30)  # Check every 30 seconds

        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()

gpu_memory_manager = GPUMemoryManager()
gpu_memory_manager.monitor_memory_loop()
```

## Disaster Recovery

### Backup Strategy

#### Database Backup

```bash
# backup/database_backup.sh
#!/bin/bash

BACKUP_DIR="/mnt/backups/database"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Create backup directory
mkdir -p $BACKUP_DIR

# PostgreSQL backup
pg_dump -h localhost -U gptserver -d gpt_server > $BACKUP_DIR/gpt_server_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/gpt_server_$DATE.sql

# Upload to cloud storage (optional)
# aws s3 cp $BACKUP_DIR/gpt_server_$DATE.sql.gz s3://gpt-server-backups/database/

# Clean old backups
find $BACKUP_DIR -name "*.gz" -mtime +$RETENTION_DAYS -delete

echo "Database backup completed: gpt_server_$DATE.sql.gz"
```

#### Model Backup

```bash
# backup/model_backup.sh
#!/bin/bash

MODEL_DIR="/home/gptserver/models"
BACKUP_DIR="/mnt/backups/models"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR/$DATE

# Copy models (hardlink for efficiency)
cp -al $MODEL_DIR/* $BACKUP_DIR/$DATE/

# Create manifest
find $BACKUP_DIR/$DATE -type f -name "*.bin" -o -name "*.safetensors" | sort > $BACKUP_DIR/$DATE/manifest.txt

# Compress manifest
gzip $BACKUP_DIR/$DATE/manifest.txt

# Clean old backups (keep last 5)
cd $BACKUP_DIR
ls -t | tail -n +6 | xargs -r rm -rf

echo "Model backup completed: $DATE"
```

### Recovery Procedures

#### Complete System Recovery

```bash
# recovery/full_recovery.sh
#!/bin/bash

BACKUP_DATE=$1
RECOVERY_DIR="/tmp/recovery"

# Create recovery directory
mkdir -p $RECOVERY_DIR

# Stop services
docker-compose down

# Restore models
cp -r /mnt/backups/models/$BACKUP_DATE /home/gptserver/models/

# Restore database
gunzip -c /mnt/backups/database/gpt_server_$BACKUP_DATE.sql.gz | psql -h localhost -U gptserver -d gpt_server

# Restore configuration
cp /mnt/backups/config/config_$BACKUP_DATE.yaml /home/gptserver/config/config.yaml

# Start services
docker-compose up -d

# Verify recovery
curl -f http://localhost:8081/v1/models || exit 1
curl -f http://localhost:21001/list_models || exit 1

echo "Full recovery completed successfully"
```

#### Point-in-Time Recovery

```bash
# recovery/point_in_time_recovery.sh
#!/bin/bash

TARGET_TIME=$1
RECOVERY_DIR="/tmp/pitr_recovery"

# Create recovery directory
mkdir -p $RECOVERY_DIR

# Find appropriate backup
LATEST_BACKUP=$(ls -t /mnt/backups/database/ | head -1)
BACKUP_TIME=$(echo $LATEST_BACKUP | sed 's/gpt_server_\(.*\)\.sql\.gz/\1/')

# Restore from latest backup
gunzip -c /mnt/backups/database/$LATEST_BACKUP | psql -h localhost -U gptserver -d gpt_server

# Apply WAL logs up to target time
# Note: This requires PostgreSQL WAL archiving to be enabled
pg_waldump /var/lib/postgresql/data/pg_wal/ | \
    awk -v target="$TARGET_TIME" '
        $0 ~ /^rmgr:/ {
            timestamp = $1
            if (timestamp <= target) {
                print
            } else {
                exit
            }
        }
    ' > $RECOVERY_DIR/wal_transactions.sql

# Apply transactions
psql -h localhost -U gptserver -d gpt_server -f $RECOVERY_DIR/wal_transactions.sql

echo "Point-in-time recovery completed for: $TARGET_TIME"
```

### Multi-region Deployment

```yaml
# k8s/multi-region-deployment.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: multi-region-config
  namespace: gpt-server
data:
  regions.json: |
    {
      "primary": {
        "region": "us-east-1",
        "zones": ["us-east-1a", "us-east-1b", "us-east-1c"],
        "capacity": 100
      },
      "secondary": {
        "region": "us-west-2",
        "zones": ["us-west-2a", "us-west-2b", "us-west-2c"],
        "capacity": 50
      },
      "disaster_recovery": {
        "region": "eu-west-1",
        "zones": ["eu-west-1a", "eu-west-1b"],
        "capacity": 25
      }
    }

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: global-load-balancer
  annotations:
    nginx.ingress.kubernetes.io/upstream-fail-timeout: "10"
    nginx.ingress.kubernetes.io/upstream-max-fails: "3"
spec:
  ingressClassName: nginx
  rules:
  - host: api.global.company.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: gpt-server-global
            port:
              number: 8081
```

## Upgrade and Rollback

### Zero-Downtime Upgrade

```bash
# upgrade/zero_downtime_upgrade.sh
#!/bin/bash

NEW_VERSION=$1
ROLLBACK_VERSION=$(docker images gpt-server --format "{{.Repository}}:{{.Tag}}" | head -1)

# Build new image
docker build -t gpt-server:$NEW_VERSION .

# Deploy new version alongside old version
docker-compose up -d --scale gpt-server-worker=2

# Wait for new instances to be ready
sleep 60

# Health check new instances
curl -f http://localhost:8081/v1/models || exit 1

# Gradually shift traffic to new version
# (Using load balancer configuration)

# Remove old instances
docker-compose up -d --scale gpt-server-worker=1

# Clean up old images
docker rmi $ROLLBACK_VERSION

echo "Zero-downtime upgrade completed: $NEW_VERSION"
```

### Rollback Procedure

```bash
# rollback/rollback.sh
#!/bin/bash

ROLLBACK_VERSION=$1

# Stop current deployment
docker-compose down

# Deploy previous version
docker tag gpt-server:$ROLLBACK_VERSION gpt-server:latest
docker-compose up -d

# Verify rollback
curl -f http://localhost:8081/v1/models || exit 1

# Log rollback event
echo "$(date): Rolled back to version $ROLLBACK_VERSION" >> /var/log/gpt_server_rollback.log

echo "Rollback completed successfully"
```

### Upgrade Validation

```python
# upgrade/upgrade_validator.py
import httpx
import asyncio
import time
from typing import Dict, List

class UpgradeValidator:
    def __init__(self, old_url: str, new_url: str):
        self.old_url = old_url
        self.new_url = new_url
        self.test_cases = [
            {
                "name": "Basic Chat Completion",
                "payload": {
                    "model": "gpt-4",
                    "messages": [{"role": "user", "content": "Hello"}],
                    "max_tokens": 10
                }
            },
            {
                "name": "Embedding Request",
                "payload": {
                    "model": "text-embedding-ada-002",
                    "input": "Test input"
                }
            },
            {
                "name": "Model List",
                "payload": {}
            }
        ]

    async def validate_endpoint(self, url: str, endpoint: str, payload: Dict) -> Dict:
        """Validate single endpoint"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            start_time = time.time()
            try:
                response = await client.post(f"{url}{endpoint}", json=payload)
                response_time = time.time() - start_time

                return {
                    "success": response.status_code == 200,
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "error": None if response.status_code == 200 else response.text
                }
            except Exception as e:
                return {
                    "success": False,
                    "status_code": None,
                    "response_time": time.time() - start_time,
                    "error": str(e)
                }

    async def compare_versions(self) -> Dict:
        """Compare old and new version performance"""
        results = {
            "old_version": {},
            "new_version": {},
            "comparison": {}
        }

        for test_case in self.test_cases:
            name = test_case["name"]
            payload = test_case["payload"]
            endpoint = "/v1/chat/completions" if "messages" in payload else "/v1/embeddings" if "input" in payload else "/v1/models"

            # Test old version
            old_result = await self.validate_endpoint(self.old_url, endpoint, payload)
            results["old_version"][name] = old_result

            # Test new version
            new_result = await self.validate_endpoint(self.new_url, endpoint, payload)
            results["new_version"][name] = new_result

            # Compare results
            results["comparison"][name] = {
                "functionality_match": old_result["success"] == new_result["success"],
                "performance_change": new_result["response_time"] - old_result["response_time"],
                "status_match": old_result["status_code"] == new_result["status_code"]
            }

        return results

    def generate_report(self, results: Dict) -> str:
        """Generate validation report"""
        report = "# Upgrade Validation Report\n\n"
        report += f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        for test_name in results["old_version"].keys():
            report += f"## {test_name}\n\n"
            old_result = results["old_version"][test_name]
            new_result = results["new_version"][test_name]
            comparison = results["comparison"][test_name]

            report += f"**Old Version:** {'✅ Success' if old_result['success'] else '❌ Failed'}\n"
            report += f"**New Version:** {'✅ Success' if new_result['success'] else '❌ Failed'}\n"
            report += f"**Functionality Match:** {'✅' if comparison['functionality_match'] else '❌'}\n"
            report += f"**Performance Change:** {comparison['performance_change']:.3f}s\n\n"

        # Overall assessment
        all_functional = all(comp["functionality_match"] for comp in results["comparison"].values())
        avg_performance_change = sum(comp["performance_change"] for comp in results["comparison"].values()) / len(results["comparison"])

        report += "## Overall Assessment\n\n"
        report += f"**Functional Compatibility:** {'✅ PASS' if all_functional else '❌ FAIL'}\n"
        report += f"**Average Performance Change:** {avg_performance_change:.3f}s\n"
        report += f"**Recommendation:** {'✅ Proceed with upgrade' if all_functional else '❌ Do not upgrade'}\n"

        return report

async def main():
    validator = UpgradeValidator(
        old_url="http://old-deployment:8081",
        new_url="http://new-deployment:8081"
    )

    results = await validator.compare_versions()
    report = validator.generate_report(results)

    with open("upgrade_validation_report.md", "w") as f:
        f.write(report)

    print("Validation report generated: upgrade_validation_report.md")

if __name__ == "__main__":
    asyncio.run(main())
```

## Support and Training

### Team Documentation

#### Runbook

```markdown
# GPT Server Runbook

## Emergency Contacts
- **Primary On-call**: John Doe (john.doe@company.com) - +1-555-0101
- **Secondary On-call**: Jane Smith (jane.smith@company.com) - +1-555-0102
- **DevOps Lead**: Bob Johnson (bob.johnson@company.com) - +1-555-0103

## Common Issues and Solutions

### Issue: High Latency
**Symptoms**: Response times > 5 seconds
**Solutions**:
1. Check GPU utilization: `nvidia-smi`
2. Monitor queue depth: Check controller logs
3. Scale up instances: `kubectl scale deployment gpt-server-worker --replicas=5`
4. Restart problematic pods: `kubectl delete pod <pod-name>`

### Issue: Model Loading Errors
**Symptoms**: 500 errors with model loading messages
**Solutions**:
1. Check model file integrity: `ls -la /models/`
2. Verify GPU memory: `nvidia-smi`
3. Restart worker pods: `kubectl delete pod <postgres-pod>`
4. Check model download logs

### Issue: Database Connection Errors
**Symptoms**: Authentication or connection failures
**Solutions**:
1. Check database status: `kubectl get pods -l app=postgres`
2. Verify connection string: Check configmap
3. Restart database pod: `kubectl delete pod <postgres-pod>`
4. Check database logs: `kubectl logs <postgres-pod>`

## Escalation Procedures

### Severity Levels
- **P0 (Critical)**: Complete service outage, affects all users
- **P1 (High)**: Major functionality broken, affects many users
- **P2 (Medium)**: Partial functionality issues, affects some users
- **P3 (Low)**: Minor issues, cosmetic problems

### Escalation Timeline
- **P0**: Immediate notification to all contacts, page within 5 minutes
- **P1**: Notify primary on-call within 15 minutes
- **P2**: Notify within 1 hour during business hours
- **P3**: Next business day

## Maintenance Windows
- **Primary**: Sundays 2:00 AM - 4:00 AM UTC
- **Emergency**: As needed with advance notice
- **Testing**: Wednesdays 10:00 PM - 11:00 PM UTC
```

#### Training Materials

```markdown
# GPT Server Training Guide

## For Developers

### Getting Started
1. **Setup Development Environment**
   ```bash
   # Clone repository
   git clone https://github.com/company/gpt-server.git
   cd gpt-server

   # Setup development environment
   make setup-dev
   ```

2. **Run Tests**
   ```bash
   # Run unit tests
   make test-unit

   # Run integration tests
   make test-integration

   # Run performance tests
   make test-performance
   ```

3. **Code Quality**
   ```bash
   # Run linters
   make lint

   # Format code
   make format

   # Run security scan
   make security-scan
   ```

### Development Workflow
1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes and add tests
3. Run CI pipeline: `make ci`
4. Create pull request
5. Code review and merge

## For DevOps Engineers

### Deployment Procedures
1. **Environment Setup**
   ```bash
   # Provision infrastructure
   terraform apply

   # Configure monitoring
   ansible-playbook monitoring.yml

   # Deploy application
   helm install gpt-server ./charts/gpt-server
   ```

2. **Monitoring Setup**
   ```bash
   # Configure alerts
   kubectl apply -f monitoring/alerts.yml

   # Setup dashboards
   kubectl apply -f monitoring/dashboards.yml

   # Configure log aggregation
   kubectl apply -f monitoring/logging.yml
   ```

### Incident Response
1. **Detection**: Monitor dashboards and alerts
2. **Assessment**: Check service status and logs
3. **Containment**: Isolate affected components
4. **Recovery**: Follow runbook procedures
5. **Post-mortem**: Document lessons learned

## For System Administrators

### Server Maintenance
1. **Regular Updates**
   ```bash
   # Update system packages
   sudo apt update && sudo apt upgrade

   # Update application
   kubectl rollout restart deployment gpt-server-worker

   # Update models
   ./scripts/update_models.sh
   ```

2. **Backup Verification**
   ```bash
   # Test backup integrity
   ./scripts/verify_backup.sh

   # Test recovery procedure
   ./scripts/test_recovery.sh
   ```

### Security Procedures
1. **Access Management**
   - Rotate API keys quarterly
   - Review user permissions monthly
   - Audit access logs weekly

2. **Security Updates**
   - Apply security patches within 30 days
   - Update dependencies monthly
   - Run security scans weekly

## Best Practices

### Performance Optimization
1. Use appropriate model sizes for your use case
2. Enable prefix caching for repeated prompts
3. Optimize batch sizes based on your workload
4. Use GPU acceleration when possible
5. Monitor and adjust resource limits regularly

### Security
1. Use HTTPS in production
2. Implement proper authentication and authorization
3. Regularly rotate API keys and credentials
4. Monitor access logs and set up alerts
5. Keep dependencies updated

### Reliability
1. Implement proper backup strategies
2. Set up monitoring and alerting
3. Test disaster recovery procedures regularly
4. Use multiple availability zones
5. Implement gradual rollouts for updates

## Glossary

- **HPA**: Horizontal Pod Autoscaler - Automatically scales Kubernetes deployments
- **PVC**: Persistent Volume Claim - Requests storage resources in Kubernetes
- **Ingress**: Kubernetes resource for managing external access to services
- **ConfigMap**: Kubernetes resource for storing configuration data
- **Secret**: Kubernetes resource for storing sensitive data
- **Deployment**: Kubernetes resource for managing stateless applications
- **Service**: Kubernetes resource for exposing applications within the cluster
- **Pod**: Smallest deployable unit in Kubernetes
- **Namespace**: Virtual cluster within a Kubernetes cluster
```

### Knowledge Base

```markdown
# GPT Server Knowledge Base

## Frequently Asked Questions

### General Questions

**Q: What models are supported?**
A: GPT Server supports various LLM architectures including Qwen, Llama, ChatGLM, and others. See the [models documentation](models.md) for the complete list.

**Q: How do I scale the deployment?**
A: Use Kubernetes HPA or manually scale deployments:
```bash
kubectl scale deployment gpt-server-worker --replicas=10
```

**Q: What are the system requirements?**
A: Minimum requirements are 32GB RAM and 4 CPU cores. For production, we recommend 128GB+ RAM and GPU acceleration.

### Troubleshooting

**Q: I'm getting CUDA out of memory errors**
A: Reduce batch size, use model quantization, or add more GPU memory.

**Q: Model loading is slow**
A: Enable model caching, use faster storage (NVMe), or pre-load models.

**Q: API responses are slow**
A: Check network latency, optimize model parameters, or scale up instances.

## Best Practices

### Performance Optimization
1. Use appropriate model sizes for your use case
2. Enable prefix caching for repeated prompts
3. Optimize batch sizes based on your workload
4. Use GPU acceleration when possible
5. Monitor and adjust resource limits regularly

### Security
1. Use HTTPS in production
2. Implement proper authentication and authorization
3. Regularly rotate API keys and credentials
4. Monitor access logs and set up alerts
5. Keep dependencies updated

### Reliability
1. Implement proper backup strategies
2. Set up monitoring and alerting
3. Test disaster recovery procedures regularly
4. Use multiple availability zones
5. Implement gradual rollouts for updates

## Glossary

- **HPA**: Horizontal Pod Autoscaler - Automatically scales Kubernetes deployments
- **PVC**: Persistent Volume Claim - Requests storage resources in Kubernetes
- **Ingress**: Kubernetes resource for managing external access to services
- **ConfigMap**: Kubernetes resource for storing configuration data
- **Secret**: Kubernetes resource for storing sensitive data
- **Deployment**: Kubernetes resource for managing stateless applications
- **Service**: Kubernetes resource for exposing applications within the cluster
- **Pod**: Smallest deployable unit in Kubernetes
- **Namespace**: Virtual cluster within a Kubernetes cluster
```

## Conclusion

This comprehensive deployment guide covers all aspects of successfully deploying GPT Server in an enterprise environment. The guide includes:

- **Complete Prerequisites**: Hardware, software, and network requirements
- **Development Environment**: IDE setup, testing strategies, CI/CD integration
- **Detailed Deployment**: Step-by-step installation and configuration
- **Advanced Features**: Docker, Kubernetes, monitoring, and scaling
- **Integration Options**: API gateways, authentication, databases, webhooks
- **Testing Strategies**: Unit, integration, load, stress, and performance testing
- **Compliance**: GDPR, data privacy, and regulatory considerations
- **Cost Optimization**: Cloud cost management and resource optimization
- **Disaster Recovery**: Backup, recovery, and multi-region deployment
- **Upgrade Procedures**: Zero-downtime upgrades and rollback procedures
- **Support Structure**: Runbooks, training materials, and knowledge base

Following this guide will ensure a robust, scalable, and maintainable GPT Server deployment that meets enterprise requirements for security, performance, and reliability.

### Additional Resources

- **GitHub Repository**: https://github.com/shell-nlp/gpt_server
- **Documentation**: https://gpt-server.readthedocs.io/
- **Community Forum**: https://community.gpt-server.com/
- **Enterprise Support**: enterprise@company.com

For additional support or questions, please refer to the project's documentation or contact the enterprise support team.