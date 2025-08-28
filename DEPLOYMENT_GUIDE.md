# GPT Server Enterprise Deployment Guide

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Server Specifications](#server-specifications)
4. [Pre-deployment Checklist](#pre-deployment-checklist)
5. [Step-by-Step Deployment](#step-by-step-deployment)
6. [Configuration Management](#configuration-management)
7. [Model Management](#model-management)
8. [Monitoring and Maintenance](#monitoring-and-maintenance)
9. [Troubleshooting](#troubleshooting)
10. [Security Considerations](#security-considerations)
11. [Performance Optimization](#performance-optimization)

## Overview

This guide provides comprehensive instructions for deploying GPT Server in an enterprise environment. GPT Server is an open-source framework for production-level deployment of Large Language Models (LLMs) and Embedding models with OpenAI-compatible APIs.

### Key Features
- **Multi-Model Support**: Chat, Embedding, ReRanker, Text-Moderation, ASR, TTS, SD models
- **Multiple Backends**: HF, vLLM, LMDeploy, SGLang acceleration engines
- **OpenAI Compatibility**: Drop-in replacement for OpenAI API
- **High Performance**: Optimized for production workloads
- **Scalability**: Support for multiple model instances and load balancing

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

## Conclusion

This deployment guide provides comprehensive instructions for successfully deploying GPT Server in an enterprise environment. Following these guidelines will ensure:

- **Reliable Operation**: Proper hardware sizing and configuration
- **Security**: Network security, access control, and data protection
- **Performance**: Optimized settings for high-throughput workloads
- **Maintainability**: Monitoring, logging, and backup strategies
- **Scalability**: Ability to handle growing workloads

For additional support or questions, please refer to the project's GitHub repository or community forums.