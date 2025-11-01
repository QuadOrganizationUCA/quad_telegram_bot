# 🤖 Startup Motivation & Reminder Telegram Bot

A production-ready Telegram bot that helps startup teams stay motivated and organized with scheduled motivational messages and custom reminders. Supports both static quotes and AI-generated messages using OpenAI's API.

## ✨ Features

- **📨 Motivational Messages**: Send inspirational quotes at scheduled times (multiple times per day)
- **⏰ Custom Reminders**: Set weekly recurring reminders for team events, standups, reflections, etc.
- **🤖 AI Integration**: Generate dynamic motivational messages using OpenAI API (optional)
- **💬 Topic Support**: Send messages to specific topic threads in Telegram groups
- **⚙️ Fully Configurable**: All settings manageable via Telegram commands
- **💾 Persistent Storage**: All settings saved in JSON for persistence across restarts
- **📊 Statistics**: Track messages and reminders sent

## 🚀 Quick Start

### 1. Create Your Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the instructions
3. Copy the bot token (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Get Your User ID (Optional)

1. Search for [@userinfobot](https://t.me/userinfobot) on Telegram
2. Start a conversation and it will reply with your user ID

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and fill in your values:

```bash
cp env.example .env
```

Edit `.env`:

```env
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_ID=your_telegram_user_id_here
OPENAI_API_KEY=your_openai_api_key_here  # Optional
TIMEZONE=UTC  # Optional, defaults to UTC
```

### 5. Run the Bot

```bash
python main.py
```

## 📝 Commands

### Configuration Commands (Admin Only)

- `/set_motivation_times 09:00, 14:00, 20:00` - Set daily motivation message times
- `/set_mode ai|manual` - Switch between AI-generated and static quotes
- `/set_chat` - Set current chat as target (run this in your group)
- `/set_topic <topic_id>` - Set topic thread ID for topic-specific messages

### Reminder Commands

- `/add_reminder Monday 10:00 "Weekly Standup 🚀"` - Add a weekly recurring reminder
- `/remove_reminder "Weekly Standup 🚀"` - Remove a reminder
- `/list_reminders` - Show all scheduled reminders

### Quote Commands

- `/add_quote "Your custom quote here"` - Add a static quote to the collection
- `/quote_now` - Generate and send an AI quote immediately (Admin only)

### Information Commands

- `/show_schedule` - View current schedule and configuration
- `/summary` - Show weekly statistics
- `/ping` - Check bot status and health
- `/help` - Show all available commands

### Utility Commands

- `/toggle_ai` - Quick toggle between AI and static quote mode (Admin only)

## 🎯 Usage Examples

### Basic Setup

1. Start the bot with `/start` in a private chat or group
2. If you're the first user, you'll automatically become admin
3. Go to your target group and run `/set_chat` to configure where messages will be sent
4. Set motivation times: `/set_motivation_times 09:00, 14:00, 20:00`

### Using AI Mode

1. Set your OpenAI API key in `.env` file
2. Switch to AI mode: `/set_mode ai`
3. The bot will now generate unique motivational messages at scheduled times

### Setting Up Reminders

```bash
/add_reminder Monday 10:00 "Join the standup call 🚀"
/add_reminder Friday 18:00 "Week reflection time 💡"
```

### Using Topic Threads (Optional)

If your group uses topics:

1. Reply to a message in the topic thread
2. Copy the topic ID (message thread ID)
3. Run `/set_topic <topic_id>`

## 📁 Project Structure

```
quad_telegram_bot/
├── main.py              # Entry point, bot initialization
├── handlers.py          # Command handlers for Telegram
├── scheduler.py         # APScheduler integration
├── config_manager.py   # Configuration and persistence
├── ai_generator.py      # OpenAI API integration
├── config.json          # Auto-generated config storage
├── requirements.txt     # Python dependencies
├── env.example          # Environment variables template
└── README.md           # This file
```

## 🔧 Advanced Configuration

### Timezone Support

Set your timezone in `.env`:

```env
TIMEZONE=America/New_York
```

Use timezone names from the [tz database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

### Persistence

All settings are automatically saved to `config.json`. This file is created on first run and includes:

- Admin user ID
- Chat ID and topic ID
- Motivation times
- Current mode (AI/manual)
- All reminders
- Custom quotes
- Statistics

### Extending the Bot

#### Adding a New Command

1. Add handler method in `handlers.py`:

```python
async def my_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("My command response")
```

2. Register in `main.py` `setup_handlers()`:

```python
command_map = {
    # ... existing commands
    'my_command': self.handlers.my_command,
}
```

#### Adding a New Scheduled Task Type

1. Create async function in `main.py`:

```python
async def my_scheduled_task(self):
    # Your task logic
    pass
```

2. Schedule it in `setup_scheduled_jobs()`:

```python
self.scheduler.add_daily_job(
    func=self.my_scheduled_task,
    time_str="12:00",
    job_id="my_task_noon"
)
```

## 🐛 Troubleshooting

### Bot not responding

- Check that `BOT_TOKEN` is correct
- Verify the bot is running (check logs)
- Make sure you've started the bot with `/start`

### Messages not being sent

- Verify chat is set: `/show_schedule`
- Check if chat ID is configured: use `/set_chat` in your group
- Ensure bot is added to the group and has permission to send messages

### AI mode not working

- Verify `OPENAI_API_KEY` is set in `.env`
- Check API key is valid and has credits
- Bot will fallback to static quotes if API fails

### Reminders not triggering

- Check timezone setting matches your local timezone
- Verify day names are correct (capitalized, e.g., "Monday")
- Check time format is HH:MM (24-hour format)

## 📦 Deployment

### Running on a VPS

1. Install Python 3.8+ on your server
2. Clone or upload this repository
3. Install dependencies: `pip install -r requirements.txt`
4. Configure `.env` file
5. Run with a process manager like `systemd` or `supervisor`

#### Example systemd service

Create `/etc/systemd/system/motivation-bot.service`:

```ini
[Unit]
Description=Startup Motivation Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/quad_telegram_bot
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl enable motivation-bot
sudo systemctl start motivation-bot
```

### Using Docker (Optional)

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Build and run:

```bash
docker build -t motivation-bot .
docker run -d --env-file .env motivation-bot
```

## 📄 License

This project is open source and available for personal and commercial use.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 💡 Tips

- Start with static mode to test functionality, then switch to AI mode
- Use `/quote_now` to test AI generation immediately
- Set reminders for important recurring events (standups, reviews, etc.)
- Monitor `/summary` to track engagement
- Customize quotes in `config.json` or via `/add_quote` command

---

Built with ❤️ for startup teams who need consistent motivation and reminders.

