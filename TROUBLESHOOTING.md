# Troubleshooting Guide

## Issue: Chat ID Not Changing

### Problem
When you run `/set_chat` in different chats, it always shows the same chat ID.

### Root Cause
You're running `/set_chat` in a **private chat** with the bot instead of in your target **group**.

### Solution

1. **Add the bot to your group:**
   - Open your Telegram group
   - Click on group name → Add members
   - Search for your bot and add it

2. **Run `/set_chat` IN THE GROUP:**
   - Go to the group (not private chat with bot)
   - Type `/set_chat` in the group
   - The bot will capture the group's chat ID

3. **Verify the configuration:**
   ```
   /current_chat    # Shows the currently configured chat
   ```

### How to Tell if You're in the Right Place

**Private Chat (WRONG):**
- Chat type: `private`
- Chat ID: Same as your user ID (e.g., `1469570114`)
- Warning message: "⚠️ Warning: Private Chat Detected"

**Group Chat (CORRECT):**
- Chat type: `group` or `supergroup`
- Chat ID: Negative number (e.g., `-1001234567890`)
- No warning message

### Example Workflow

```bash
# ❌ WRONG: In private chat with bot
You: /set_chat
Bot: ⚠️ Warning: Private Chat Detected
     You're setting the bot to send messages to this private chat.
     ...

# ✅ CORRECT: In your group
You: /set_chat
Bot: ✅ Target chat set successfully!
     📍 Chat Info:
     • ID: `-1001234567890`  (negative = group)
     • Type: supergroup
     • Name: Your Group Name
```

## Issue: Messages Not Being Delivered

### Check Configuration

1. **Verify chat is set:**
   ```
   /current_chat
   ```

2. **Test connection:**
   ```
   /test_connection
   ```

3. **Check schedule:**
   ```
   /show_schedule
   ```

### Common Problems

#### Bot Not in Group
**Symptom:** Connection test fails with "bot is not a member"

**Solution:**
- Add bot to the group
- Make sure bot wasn't removed

#### No Send Permission
**Symptom:** Connection test fails with "no rights to send"

**Solution:**
- Go to group settings → Administrators
- Find your bot
- Enable "Send Messages" permission

#### Wrong Chat ID
**Symptom:** Chat ID is your user ID (positive number)

**Solution:**
- Run `/set_chat` **in the group**, not in private chat

## Issue: Bot Shows Same Chat After Changing

### Debug Steps

1. **Check what's saved:**
   ```bash
   cat config.json
   ```
   Look at the `chat_id` field

2. **Watch the logs:**
   When you run `/set_chat`, you should see:
   ```
   Setting chat_id to: -1001234567890
   ✓ Config saved to config.json
   Chat ID after save: -1001234567890
   ```

3. **Verify it changed:**
   ```
   /current_chat
   ```
   Should show the new chat ID

### If Chat ID Still Not Changing

1. **Check file permissions:**
   ```bash
   ls -l config.json
   # Should be writable
   ```

2. **Check for file errors:**
   Look at bot logs for:
   ```
   ✗ Error saving config: ...
   ```

3. **Manual fix:**
   ```bash
   # Stop the bot
   # Edit config.json
   nano config.json
   # Change "chat_id" to your group's chat ID (negative number)
   # Save and restart bot
   ```

## Issue: Topic Messages Not Working

### Problem
Messages not appearing in the correct topic thread.

### Solution

1. **Get the topic ID:**
   - Reply to a message in the topic
   - The topic ID is in the message thread

2. **Set the topic:**
   ```
   /set_topic 12345
   ```

3. **Test it:**
   ```
   /test_connection
   ```

## Debugging Commands

### Check Current Configuration
```
/current_chat      # Shows configured chat
/show_schedule     # Shows complete configuration
/ping              # Bot health check
```

### Test Functionality
```
/test_connection   # Test if bot can send to configured chat
/quote_now         # Test sending a message immediately
```

### View Logs
Watch the terminal where the bot is running for debug messages:
```
Setting chat_id to: -1001234567890
✓ Config saved to config.json
Chat ID after save: -1001234567890
```

## Understanding Chat IDs

### Private Chat
- **Format:** Positive number
- **Example:** `1469570114`
- **Equals:** Your user ID
- **Use case:** Testing, personal reminders

### Group Chat
- **Format:** Negative number
- **Example:** `-1001234567890`
- **Starts with:** `-100` (supergroup) or just `-` (regular group)
- **Use case:** Team notifications

### How to Get Group Chat ID

**Method 1: Use the bot**
```
# In the group:
/set_chat
# Bot will show the chat ID
```

**Method 2: Forward a message**
- Forward any message from the group to @userinfobot
- It will show the chat ID

**Method 3: Check config.json**
```bash
cat config.json | grep chat_id
```

## Quick Fixes

### Reset Configuration
```bash
# Stop the bot
rm config.json
# Restart bot
# Reconfigure from scratch
```

### Force Set Chat ID
```bash
# Edit config.json manually
nano config.json

# Find "chat_id" and change it:
"chat_id": -1001234567890,  # Your group's ID

# Save and restart bot
```

### Check Bot Permissions
1. Go to group info
2. Administrators
3. Find your bot
4. Ensure these are enabled:
   - Send Messages
   - Send Media
   - Send Stickers & GIFs (optional)

## Still Having Issues?

### Collect Debug Information

1. **Run these commands:**
   ```
   /current_chat
   /show_schedule
   /test_connection
   ```

2. **Check logs:**
   Copy the last 50 lines from terminal

3. **Check config:**
   ```bash
   cat config.json
   ```

4. **Verify bot is in group:**
   - Check group members list
   - Bot should be listed

### Common Mistakes

❌ Running `/set_chat` in private chat
✅ Run `/set_chat` in the target group

❌ Bot not added to group
✅ Add bot to group first

❌ Bot has no permissions
✅ Give bot "Send Messages" permission

❌ Using positive chat ID for groups
✅ Group IDs are always negative

## Prevention Tips

1. **Always check after configuration:**
   ```
   /set_chat
   /current_chat        # Verify it was set correctly
   /test_connection     # Test it works
   ```

2. **Use the right chat:**
   - Private chat: For bot commands and testing
   - Group chat: For `/set_chat` command

3. **Monitor logs:**
   - Watch for "Setting chat_id to: ..."
   - Confirm "✓ Config saved"

4. **Regular testing:**
   ```
   /test_connection     # Run this periodically
   ```

---

*Last updated: 2025-11-01*
*For more help, check README.md and CHAT_CONNECTION_TEST.md*

