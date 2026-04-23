# Deployment Guide

## Server Deployment Instructions

### 1. Install Python 3.11

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev -y

# CentOS/RHEL
sudo yum install python3.11 python3.11-pip -y

# Or use pyenv
curl https://pyenv.run | bash
pyenv install 3.11.0
pyenv global 3.11.0
```

### 2. Clone Repository

```bash
git clone https://github.com/your-username/telegram_auth_bot.git
cd telegram_auth_bot
```

### 3. Create Virtual Environment

```bash
python3.11 -m venv .venv311
source .venv311/bin/activate
```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Environment

```bash
# Copy example config
cp env_example.txt .env

# Edit .env file with your settings
nano .env
```

**Required settings in .env:**
```bash
BOT_TOKEN=your_bot_token_here
LOG_LEVEL=INFO
RESTRICT_ACCESS=True
AUTHORIZED_USERS=your_telegram_id
```

### 6. Copy Steam Account Data

```bash
# Create directories
mkdir -p accounts accountStash

# Copy your Steam account data from local machine
# Use scp, rsync, or SFTP to transfer files
scp -r /path/to/local/accounts/* user@server:/path/to/telegram_auth_bot/accounts/
```

### 7. Test Bot

```bash
# Test with simple runner (avoids encoding issues)
python run_bot.py
```

### 8. Run in Background

**Option 1: Using nohup**
```bash
nohup python run_bot.py > bot.log 2>&1 &
```

**Option 2: Using screen**
```bash
screen -S steamguardbot
python run_bot.py
# Press Ctrl+A, then D to detach
# Use 'screen -r steamguardbot' to reattach
```

**Option 3: Using tmux**
```bash
tmux new-session -d -s steamguardbot 'python run_bot.py'
# Use 'tmux attach -t steamguardbot' to attach
```

### 9. Systemd Service (Recommended)

Create service file:
```bash
sudo nano /etc/systemd/system/steamguardbot.service
```

Add content:
```ini
[Unit]
Description=Telegram Steam Guard Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/telegram_auth_bot
Environment=PYTHONIOENCODING=utf-8
Environment=LC_ALL=en_US.UTF-8
Environment=LANG=en_US.UTF-8
ExecStart=/path/to/telegram_auth_bot/.venv311/bin/python run_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable steamguardbot
sudo systemctl start steamguardbot
sudo systemctl status steamguardbot
```

### 10. Manage Users

```bash
# Add/remove authorized users
python manage_users.py

# Or edit .env directly
nano .env
```

### 11. Monitor Logs

```bash
# If using nohup
tail -f bot.log

# If using systemd
sudo journalctl -u steamguardbot -f

# Check bot status
sudo systemctl status steamguardbot
```

### 12. Troubleshooting

**Encoding Issues:**
- Use `run_bot.py` instead of `telegram_bot.py`
- Set environment variables: `export PYTHONIOENCODING=utf-8`

**Permission Issues:**
```bash
chmod +x run_bot.py
chmod +x manage_users.py
```

**Port Issues:**
- Bot uses Telegram API, no local ports needed
- Ensure outbound HTTPS (443) is allowed

**Python Version Issues:**
```bash
# Check Python version
python3.11 --version

# Use specific version
python3.11 run_bot.py
```

### 13. Security Considerations

1. **File Permissions:**
```bash
chmod 600 .env
chmod 700 accounts/ accountStash/
```

2. **Firewall:**
```bash
# Only allow SSH access
sudo ufw allow ssh
sudo ufw enable
```

3. **Regular Updates:**
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Update bot code
git pull origin main
```

### 14. Backup

```bash
# Backup configuration
cp .env .env.backup

# Backup account data
tar -czf steam_accounts_backup.tar.gz accounts/ accountStash/
```

### 15. Maintenance

**Restart Bot:**
```bash
# If using systemd
sudo systemctl restart steamguardbot

# If using nohup
pkill -f "python run_bot.py"
nohup python run_bot.py > bot.log 2>&1 &
```

**Update Bot:**
```bash
git pull origin main
pip install --upgrade -r requirements.txt
sudo systemctl restart steamguardbot
```

### 16. Monitoring

**Check if bot is running:**
```bash
ps aux | grep "python run_bot.py"
```

**Check logs for errors:**
```bash
tail -f bot.log | grep ERROR
```

**Monitor disk space:**
```bash
df -h
du -sh accounts/ accountStash/
``` 