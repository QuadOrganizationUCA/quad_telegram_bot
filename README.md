# 🚀 Quad Telegram Bot - Your Team's AI-Powered Motivational Coach

## Why We Built This

When working in a small team, it's **difficult to keep the atmosphere energized** and constantly remind each other to stay focused on the mission. Someone always has to be "that person" who sends motivational messages or reminds everyone about meetings.

**We get it.** We're Amirbek, Manuchehr, and Asiljon — a small startup team building an educational platform to make learning accessible everywhere. We faced this exact problem.

So we built this bot.

## What It Does

Connect this bot to your **Telegram supergroup**, and it becomes your team's personal supervisor:

- 🔥 **Sends personalized motivational messages** throughout the day (AI-generated or static quotes)
- ⏰ **Custom weekly reminders** (standup calls, weekly reviews, sprint planning, etc.)
- 🤖 **AI-powered messages** that understand your team's mission and speak like a supportive supervisor
- 📊 **Track progress** with weekly statistics
- 🎯 **Topic support** for organized group chats
- ⚙️ **Easy configuration** — all via Telegram commands

No one has to be "the reminder person" anymore. The bot keeps your team motivated, focused, and accountable.

---

## 🎯 Features

### 1. Motivational Messages
- **Scheduled messages** sent at configurable times (e.g., 9 AM, 2 PM, 8 PM)
- **Two modes:**
  - **AI mode:** Uses OpenAI GPT-4 to generate personalized, mission-aware messages
  - **Manual mode:** Uses your custom quote library
- Messages feel personal, like they're from a caring supervisor who knows your mission

### 2. Custom Reminders
- Schedule **recurring weekly reminders**:
  - "Monday 10:00 AM → Weekly Standup 🚀"
  - "Friday 6:00 PM → Reflect on the week 💡"
- AI can enhance reminders to make them more engaging
- All times respect your configured timezone

### 3. AI Integration (Optional)
- Uses **OpenAI GPT-4o-mini** for cost-effective AI generation
- AI knows your team context:
  - Team member names
  - Your startup mission
  - Your goals and vision
- Generates messages that feel authentic and personal
- Automatic fallback to static quotes if API is unavailable

### 4. Easy Configuration
Everything is configured via Telegram commands:
```
/set_group          → Set bot to send messages to current group
/set_motivation_times 09:00, 14:00, 20:00
/set_mode ai        → Switch to AI-generated messages
/add_reminder Monday 10:00 "Weekly Standup 🚀"
/list_reminders     → See all configured reminders
/show_schedule      → View full schedule
/quote_now          → Generate and send a motivational message now
/test_connection    → Test if bot can send messages to group
```

### 5. Persistence
All settings are saved to `config.json` and persist across restarts.

### 6. Admin Controls
Only authorized admin(s) can change configurations. Group administrators automatically have permission to configure the bot in their groups.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- OpenAI API Key (optional, for AI features)

### Installation

1. **Clone the repository:**
```bash
git clone git@github.com:QuadOrganizationUCA/quad_telegram_bot.git
cd quad_telegram_bot
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
Create a `.env` file:
```bash
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_ID=your_telegram_user_id
OPENAI_API_KEY=your_openai_api_key_here  # Optional
TIMEZONE=Asia/Tashkent  # Or your timezone
```

**How to get your Telegram User ID:**
- Message [@userinfobot](https://t.me/userinfobot) on Telegram
- It will reply with your user ID

4. **Run the bot:**
```bash
python3 main.py
```

5. **Configure the bot in Telegram:**
```
1. Add bot to your Telegram supergroup
2. Send: /set_group
3. Send: /set_motivation_times 09:00, 14:00, 20:00
4. Send: /set_mode ai
5. Send: /add_reminder Monday 10:00 "Weekly Standup 🚀"
6. Done! ✅
```

---

## 🚀 Deployment

### ⭐ Recommended: Deploy to Fly.io (FREE 24/7!)

**Why Fly.io?**
- ✅ Truly free tier with 24/7 uptime (no sleeping!)
- ✅ 3 shared VMs included (256MB RAM each)
- ✅ 160GB bandwidth/month
- ✅ Better for bots than Render's free tier

**Quick Deploy:**

1. **Install Fly CLI:**
```bash
curl -L https://fly.io/install.sh | sh
```

2. **Stop local bot:**
```bash
pkill -f "python3 main.py"
```

3. **Deploy:**
```bash
flyctl auth login
flyctl launch  # Choose region, say No to databases
flyctl secrets set BOT_TOKEN="8218401569:AAGoEpaiDo_7o4HCRFI4zufviKY5sUD4GO8"
flyctl secrets set ADMIN_ID="your_telegram_user_id"
flyctl deploy
```

4. **Configure in Telegram:**
- Add bot to your group
- Send `/set_group`
- Send `/test_connection`
- Done! 🎉

**📖 Full Instructions:** See [FLY_DEPLOYMENT.md](FLY_DEPLOYMENT.md)

---

## 🌐 Alternative: Deploy to Render

Render's free tier may sleep after inactivity. If you prefer Render:

### Render Deployment Steps

1. **Push to GitHub** (if not already):
```bash
git push origin main
```

2. **Create a Web Service on Render:**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `quad_telegram_bot` repo

3. **Configure the service:**
   - **Name:** `quad-telegram-bot`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python3 main.py`
   - **Instance Type:** Free
   
   **Note:** The bot includes a health check server to satisfy Render's port requirement on the free tier.

4. **Add Environment Variables:**
   Go to "Environment" tab and add:
   ```
   BOT_TOKEN=your_bot_token_here
   ADMIN_ID=your_telegram_user_id
   OPENAI_API_KEY=your_openai_api_key  # Optional
   TIMEZONE=Asia/Tashkent
   ```

5. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically deploy your bot
   - The bot will expose a health check endpoint on the assigned port
   - Visit your service URL to see bot status

6. **⚠️ Important: Stop local bot instance**
   Before the bot works on Render, you MUST stop any local instances:
   ```bash
   # Find and stop local bot
   pkill -f "python3 main.py"
   ```
   **Only ONE bot instance can run at a time** (Telegram limitation)

7. **Configure in Telegram:**
   - Add bot to your group
   - Send `/set_group` to configure it
   - Send `/test_connection` to verify it's working

**Note:** The free tier Web Service may spin down after 15 minutes of inactivity on the HTTP endpoint. The bot will restart automatically when Render detects activity. For true 24/7 uptime, consider upgrading to a paid plan ($7/month).

---

## 📖 Command Reference

### Setup Commands
| Command | Description | Example |
|---------|-------------|---------|
| `/set_group` | Set bot to send messages to current group | `/set_group` |
| `/set_chat` | Alias for `/set_group` | `/set_chat` |
| `/set_topic [id]` | Set specific topic/thread for messages | `/set_topic 123` |
| `/set_motivation_times` | Configure when to send motivational messages | `/set_motivation_times 09:00, 14:00, 20:00` |
| `/set_mode` | Switch between 'ai' and 'manual' mode | `/set_mode ai` |
| `/toggle_ai` | Quick toggle between AI and manual mode | `/toggle_ai` |

### Reminder Commands
| Command | Description | Example |
|---------|-------------|---------|
| `/add_reminder` | Add a weekly reminder | `/add_reminder Monday 10:00 "Standup 🚀"` |
| `/remove_reminder` | Remove a reminder by text | `/remove_reminder "Standup"` |
| `/list_reminders` | Show all configured reminders | `/list_reminders` |

### Quote Commands
| Command | Description | Example |
|---------|-------------|---------|
| `/add_quote` | Add a custom quote to the library | `/add_quote "Keep building!"` |
| `/quote_now` | Generate and send a quote immediately | `/quote_now` |

### Info Commands
| Command | Description |
|---------|-------------|
| `/show_schedule` | View full schedule (motivation times + reminders) |
| `/current_chat` | Show currently configured chat details |
| `/summary` | Weekly statistics (messages sent, etc.) |
| `/test_connection` | Test if bot can send messages to configured group |
| `/ping` | Quick uptime check |
| `/help` | Show help message with all commands |

---

## 🛠️ Configuration Files

### `.env` File
```bash
BOT_TOKEN=8218401569:AAGoEpaiDo_7o4HCRFI4zufviKY5sUD4GO8
ADMIN_ID=1469570114
OPENAI_API_KEY=sk-proj-...  # Optional
TIMEZONE=Asia/Tashkent
```

### `config.json` (Auto-generated)
```json
{
  "admin_id": 1469570114,
  "chat_id": -5033189782,
  "topic_id": null,
  "motivation_times": ["09:00", "14:00", "20:00"],
  "mode": "ai",
  "reminders": [
    {
      "day": "Monday",
      "time": "10:00",
      "text": "Weekly Standup 🚀"
    }
  ],
  "quotes": [
    "Team, every feature we build brings us closer to our mission! 🚀",
    "Keep pushing! We're building something that matters. 💪"
  ],
  "stats": {
    "messages_sent": 42,
    "reminders_sent": 12,
    "last_reset": "2024-11-01T00:00:00"
  }
}
```

---

## 🏗️ Project Structure

```
quad_telegram_bot/
├── main.py                 # Main bot entry point
├── handlers.py             # Command handlers
├── scheduler.py            # APScheduler integration
├── config_manager.py       # Configuration persistence
├── ai_generator.py         # OpenAI integration
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── .env.example            # Environment template
├── config.json             # Bot configuration (auto-generated)
├── README.md               # This file
├── QUICK_START.md          # Quick setup guide
├── TROUBLESHOOTING.md      # Common issues and solutions
├── FIXES.md                # Bug fix history
└── CHAT_CONNECTION_TEST.md # Connection testing guide
```

---

## 🤖 AI Customization

The bot's AI is pre-configured to understand your team's mission. To customize it for your team:

1. **Edit `ai_generator.py`:**
   - Update the system prompt with your team details
   - Change team member names
   - Modify your mission statement

2. **Example customization:**
```python
{
    "role": "system",
    "content": """You are a supportive supervisor to [YOUR TEAM NAMES] building [YOUR MISSION].

THEIR MISSION:
- [Your goal 1]
- [Your goal 2]
- [Your vision]

Your tone: Personal, encouraging, mission-aware."""
}
```

---

## 📊 Weekly Statistics

The bot tracks:
- Total motivational messages sent this week
- Total reminders sent this week
- Last reset date (resets every Monday)

View with `/summary` command.

---

## 🔒 Security

- Only configured admin(s) can modify bot settings
- Group administrators automatically have permission in their groups
- Bot token and API keys stored in environment variables (never commit to git)
- `config.json` contains no sensitive data

---

## 🐛 Troubleshooting

### Bot doesn't send messages to group
1. Check if bot is added to the group
2. Run `/set_group` in the target group
3. Run `/test_connection` to verify
4. Check bot has permission to send messages

### AI messages not working
1. Verify `OPENAI_API_KEY` is set correctly
2. Check OpenAI account has credits
3. Bot automatically falls back to manual mode if API fails

### Reminders not triggering
1. Verify timezone is set correctly in `.env`
2. Check `/show_schedule` to see configured times
3. Ensure bot process is running

### "Only admin can set group" error
- Make sure you're an administrator in the supergroup
- The bot checks both bot admin and group admin permissions

For more help, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 📝 Example Workflow

Here's how we use it in our team:

**Morning (9:00 AM):**
> "Good morning team! Every line of code brings free education closer to millions. Let's build something that matters today! 🚀"

**Afternoon (2:00 PM):**
> "Amirbek, Manuchehr, Asiljon - remember why we started. We're making education accessible everywhere. Keep pushing! 💪"

**Monday (10:00 AM):**
> "Team reminder: Time for our weekly standup! Let's sync up on our educational mission. 📞"

**Evening (8:00 PM):**
> "End of day check: We're not just coding, we're building an educational empire. Every commit counts! ✨"

---

## 🌟 Contributing

Found a bug? Want to add a feature? PRs are welcome!

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

This project is open source and available for anyone building their dream with a small team.

---

## 💬 Support

- **Issues:** [GitHub Issues](https://github.com/QuadOrganizationUCA/quad_telegram_bot/issues)
- **Telegram:** Contact [@QuadOrganization](https://t.me/QuadOrganization)

---

## 🎉 Credits

Built with ❤️ by **Amirbek, Manuchehr, and Asiljon** at Quad Organization.

Our mission: **Make education accessible everywhere for everyone — literally.**

We're building a FREE educational empire that makes people **LOVE learning** through AI and technology.

---

**Now go build something amazing with your team! 🚀**
