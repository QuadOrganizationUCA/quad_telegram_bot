# Quick Start Guide

## Super Simple Setup (3 Steps)

### Step 1: Add Bot to Your Group
1. Open your Telegram group
2. Click on group name → **Add members**
3. Search for your bot and add it

### Step 2: Set the Group
**In your group**, type:
```
/set_group
```

That's it! The bot will automatically:
- ✅ Capture the group chat ID
- ✅ Save it to configuration
- ✅ Show you the group details
- ✅ Clear any previous invalid settings

### Step 3: Configure Schedule (Optional)
```
/set_motivation_times 09:00, 14:00, 20:00
```

## Done! 🎉

Your bot is now configured and will send motivational messages to your group at the scheduled times.

---

## Verify It Works

Test the connection:
```
/test_connection
```

You should see:
```
✅ Bot connection test successful!
Bot can send messages to chat `-1234567890`.
Scheduled messages will be delivered correctly.
```

---

## Common Commands

### Setup Commands (Run in Group)
```
/set_group                           # Set this group as target
/set_motivation_times 09:00, 14:00   # Set message times
/test_connection                     # Test if it works
```

### Info Commands
```
/current_chat        # See configured group
/show_schedule       # See complete setup
/help                # All commands
```

### Reminder Commands
```
/add_reminder Monday 10:00 "Weekly Standup 🚀"
/list_reminders
```

---

## Troubleshooting

### "Same chat ID every time"
❌ **Problem:** You're running `/set_group` in **private chat** with the bot

✅ **Solution:** Run `/set_group` **in your group**, not in private chat

### "Message thread not found"
❌ **Problem:** Invalid topic ID set

✅ **Solution:** Run `/set_topic clear` or just `/test_connection` (auto-fixes)

### "Bot not responding"
✅ **Check:**
1. Bot is added to the group
2. Bot has "Send Messages" permission
3. Bot is running (`python main.py`)

---

## Example Session

```bash
# In your Telegram group:

You: /set_group

Bot: 🎉 Target chat set successfully!
     ✨ Perfect! This is a group chat.
     
     📍 Chat Info:
     • ID: `-5033189782`
     • Type: supergroup
     • Name: Startup Team
     
     Bot will send scheduled messages here.
     Use /test_connection to verify bot can send messages.

You: /test_connection

Bot: ✅ Bot connection test successful!
     Bot can send messages to chat `-5033189782`.
     Scheduled messages will be delivered correctly.

You: /set_motivation_times 09:00, 14:00, 20:00

Bot: ✅ Motivation times updated: 09:00, 14:00, 20:00
     Bot will send messages at these times daily.
```

---

## Advanced Setup

### Enable AI Mode (Optional)
```
# Add OpenAI API key to .env file
OPENAI_API_KEY=your_key_here

# Then in Telegram:
/set_mode ai
```

### Add Custom Reminders
```
/add_reminder Monday 10:00 "Weekly Standup 🚀"
/add_reminder Friday 18:00 "Week Reflection 💡"
```

### Use Topic Threads (Optional)
```
# If your group uses topics:
/set_topic 12345      # Set specific topic
/set_topic clear      # Clear topic (main chat)
```

---

## Key Points

✅ **Always run `/set_group` IN THE GROUP** (not private chat)
✅ Group chat IDs are **negative numbers** (e.g., `-5033189782`)
✅ Private chat IDs are **positive numbers** (e.g., `1469570114`)
✅ Use `/test_connection` to verify everything works
✅ Bot auto-fixes invalid topic configurations

---

## Need Help?

- `/help` - See all commands
- Check `README.md` - Full documentation
- Check `TROUBLESHOOTING.md` - Common issues
- Check logs in terminal for errors

---

*That's it! Your bot is ready to motivate your team! 🚀*

