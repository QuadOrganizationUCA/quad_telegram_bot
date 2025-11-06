# 🚀 Deploying to Fly.io

Fly.io offers a generous free tier perfect for running the Quad Telegram Bot 24/7!

## 📋 Prerequisites

1. **Install Fly CLI:**
```bash
# Linux/WSL
curl -L https://fly.io/install.sh | sh

# macOS
brew install flyctl

# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex
```

2. **Sign up and authenticate:**
```bash
flyctl auth signup
# or if you have an account:
flyctl auth login
```

## 🚀 Deployment Steps

### 1. Stop Local Bot Instance
```bash
# IMPORTANT: Only one bot instance can run at a time
pkill -f "python3 main.py"
```

### 2. Launch the App
```bash
cd /home/student/Documents/QUAD_DYNAMICS/quad_telegram_bot
flyctl launch
```

**When prompted:**
- "Would you like to copy its configuration?" → **No**
- "Choose an app name:" → Press Enter (use `quad-telegram-bot` or let Fly generate)
- "Choose a region:" → Select closest to your team (e.g., `ams` for Amsterdam)
- "Would you like to set up a PostgreSQL database?" → **No**
- "Would you like to set up an Upstash Redis database?" → **No**
- "Would you like to deploy now?" → **No** (we need to set secrets first)

### 3. Set Environment Variables (Secrets)
```bash
# Required
flyctl secrets set BOT_TOKEN="8218401569:AAGoEpaiDo_7o4HCRFI4zufviKY5sUD4GO8"
flyctl secrets set ADMIN_ID="your_telegram_user_id"

# Optional
flyctl secrets set OPENAI_API_KEY="your_openai_api_key"
flyctl secrets set TIMEZONE="Asia/Tashkent"
```

**To get your Telegram User ID:**
1. Message [@userinfobot](https://t.me/userinfobot) on Telegram
2. It will reply with your user ID

### 4. Deploy the Bot
```bash
flyctl deploy
```

This will:
- Build the Docker image
- Deploy to Fly.io
- Start the bot
- Keep it running 24/7

### 5. Verify Deployment
```bash
# Check bot status
flyctl status

# View logs
flyctl logs

# Check health endpoint
flyctl open
```

You should see the bot status page in your browser!

### 6. Configure in Telegram
1. Add the bot to your Telegram group/supergroup
2. Send `/set_group` in the group chat
3. Send `/test_connection` to verify
4. Bot is now ready! 🎉

## 📊 Monitoring

### View Real-time Logs:
```bash
flyctl logs
```

### Check App Status:
```bash
flyctl status
```

### SSH into the Container:
```bash
flyctl ssh console
```

### View Health Dashboard:
```bash
flyctl dashboard
```

## 💰 Free Tier Details

Fly.io free tier includes:
- ✅ **3 shared-cpu-1x VMs** (256MB RAM each)
- ✅ **3GB persistent volume storage**
- ✅ **160GB outbound data transfer**
- ✅ **24/7 uptime** (no sleeping!)

Perfect for a small team bot! 🚀

## 🔧 Useful Commands

### Update the Bot (after code changes):
```bash
git push origin main
flyctl deploy
```

### Scale the bot (if needed):
```bash
# Add more VMs
flyctl scale count 2

# Adjust memory
flyctl scale memory 512
```

### Restart the bot:
```bash
flyctl apps restart
```

### Delete the app (if needed):
```bash
flyctl apps destroy quad-telegram-bot
```

## 🐛 Troubleshooting

### "Conflict: terminated by other getUpdates request"
- Another bot instance is running somewhere
- Check: `flyctl logs` to see if duplicate instances exist
- Stop local instance: `pkill -f "python3 main.py"`

### Bot not responding to commands:
- Check logs: `flyctl logs`
- Verify secrets: `flyctl secrets list`
- Test health endpoint: `flyctl open`
- Run `/test_connection` in your Telegram group

### "Message thread not found":
- Send `/set_topic clear` in your group
- Or reconfigure with `/set_group`

## 📝 Configuration Changes

To update environment variables:
```bash
flyctl secrets set KEY="value"
# Bot will automatically restart
```

To change regions:
```bash
# Edit fly.toml, change primary_region
flyctl deploy
```

## 🎯 Next Steps

1. ✅ Bot is deployed and running 24/7
2. Configure reminders: `/add_reminder Monday 10:00 "Weekly Standup 🚀"`
3. Set motivation times: `/set_motivation_times 09:00, 14:00, 20:00`
4. Enable AI mode: `/set_mode ai` (if you added OPENAI_API_KEY)
5. View schedule: `/show_schedule`

---

**Need help?** Check Fly.io docs: https://fly.io/docs/

