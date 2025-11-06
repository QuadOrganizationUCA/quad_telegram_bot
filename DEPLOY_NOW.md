# 🚀 Quick Deploy to Fly.io - Step by Step

## ✅ Fly CLI is Installed!

Run these commands **one by one** in your terminal:

---

## Step 1: Add flyctl to your PATH

```bash
export FLYCTL_INSTALL="/home/student/.fly"
export PATH="$FLYCTL_INSTALL/bin:$PATH"
```

**Make it permanent** (optional but recommended):
```bash
echo 'export FLYCTL_INSTALL="/home/student/.fly"' >> ~/.bashrc
echo 'export PATH="$FLYCTL_INSTALL/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

## Step 2: Login to Fly.io

```bash
flyctl auth login
```

This will open your browser. Sign up or log in to Fly.io (it's free!)

---

## Step 3: Navigate to project

```bash
cd /home/student/Documents/QUAD_DYNAMICS/quad_telegram_bot
```

---

## Step 4: Stop local bot (IMPORTANT!)

```bash
pkill -f "python3 main.py"
```

Only ONE bot instance can run at a time!

---

## Step 5: Launch the app

```bash
flyctl launch --no-deploy
```

**Answer the prompts:**
- ✅ App name: Press Enter (or type: `quad-telegram-bot`)
- ✅ Region: Choose closest (e.g., `ams` for Amsterdam, or just press Enter)
- ❌ PostgreSQL database: **No**
- ❌ Redis database: **No**
- ❌ Deploy now: **No** (we need to set secrets first)

---

## Step 6: Get your Telegram User ID

1. Open Telegram
2. Message this bot: [@userinfobot](https://t.me/userinfobot)
3. It will reply with your User ID (e.g., `123456789`)

---

## Step 7: Set secrets (environment variables)

```bash
flyctl secrets set BOT_TOKEN="8218401569:AAGoEpaiDo_7o4HCRFI4zufviKY5sUD4GO8"
flyctl secrets set ADMIN_ID="YOUR_USER_ID_HERE"
flyctl secrets set TIMEZONE="Asia/Tashkent"
```

**(Optional) Add OpenAI API key if you want AI-generated messages:**
```bash
flyctl secrets set OPENAI_API_KEY="your_openai_api_key"
```

---

## Step 8: Deploy! 🚀

```bash
flyctl deploy
```

This will:
- Build the Docker image
- Push to Fly.io
- Start your bot
- Bot runs 24/7 for FREE!

---

## Step 9: Verify it's working

```bash
# Check status
flyctl status

# View logs (real-time)
flyctl logs

# Open health dashboard in browser
flyctl open
```

You should see: **"🤖 Quad Telegram Bot is Running!"**

---

## Step 10: Configure in Telegram

1. Open your Telegram group
2. Make sure the bot is added to the group
3. Send: `/set_group`
4. Send: `/test_connection`
5. Bot should respond! ✅

---

## 🎉 You're Done!

Your bot is now running 24/7 on Fly.io's free tier!

### Useful Commands:

```bash
# View real-time logs
flyctl logs

# Restart the bot
flyctl apps restart

# Update after code changes
git push origin main
flyctl deploy

# SSH into the container
flyctl ssh console

# Check app status
flyctl status

# Open dashboard
flyctl dashboard
```

---

## 🐛 Troubleshooting

### "Conflict: terminated by other getUpdates request"
- Another instance is running
- Make sure you stopped the local bot: `pkill -f "python3 main.py"`

### Bot not responding
- Check logs: `flyctl logs`
- Verify secrets: `flyctl secrets list`
- Make sure bot is admin in your group

### Need to change something?
- Update secrets: `flyctl secrets set KEY="value"`
- Edit code, then: `flyctl deploy`

---

**Need more help?** Check the full guide: [FLY_DEPLOYMENT.md](FLY_DEPLOYMENT.md)

