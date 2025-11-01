"""
Handlers - Command handlers for the Telegram bot
All user-facing commands and interactions.
"""

import logging
from typing import Optional
from telegram import Update
from telegram.ext import ContextTypes

from config_manager import ConfigManager
from ai_generator import AIGenerator
from scheduler import Scheduler

logger = logging.getLogger(__name__)


class CommandHandlers:
    """Handles all Telegram bot commands."""
    
    def __init__(
        self,
        config_manager: ConfigManager,
        ai_generator: AIGenerator,
        scheduler: Scheduler,
        bot_instance
    ):
        self.config = config_manager
        self.ai = ai_generator
        self.scheduler = scheduler
        self.bot = bot_instance
        self.send_message_func = None  # Will be set by main.py
        self.reschedule_callback = None  # Callback to reschedule jobs
        self.test_connection_func = None  # Callback to test chat connection
    
    def set_send_message_func(self, func):
        """Set the function to send messages (for scheduled tasks)."""
        self.send_message_func = func
    
    def set_reschedule_callback(self, func):
        """Set the callback to reschedule jobs when settings change."""
        self.reschedule_callback = func
    
    def set_test_connection_callback(self, func):
        """Set the callback to test chat connection."""
        self.test_connection_func = func
    
    def _trigger_reschedule(self):
        """Trigger job rescheduling if callback is set."""
        if self.reschedule_callback:
            self.reschedule_callback()
    
    def _check_admin(self, user_id: int) -> bool:
        """Check if user is admin."""
        if not self.config.is_admin(user_id):
            return False
        return True
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        user_id = update.effective_user.id
        
        # Set as admin if not set yet
        if not self.config.config.get("admin_id"):
            self.config.set_admin(user_id)
            await update.message.reply_text(
                f"👋 Welcome! You've been set as the admin.\n\n"
                f"Use /help to see all available commands."
            )
        else:
            await update.message.reply_text(
                "👋 Startup Motivation Bot is running!\n\n"
                "Use /help to see available commands."
            )
    
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_text = """
🤖 *Startup Motivation Bot - Commands*

*Configuration Commands:*
/set\\_motivation\\_times 09:00, 14:00, 20:00 - Set daily motivation times
/set\\_mode ai or manual - Switch between AI and static quotes
/set\\_chat - Set this chat as target (use in the group)
/set\\_topic topic\\_id - Set topic thread ID (optional)

*Reminder Commands:*
/add\\_reminder Monday 10:00 "Your message" - Add weekly reminder
/remove\\_reminder "Your message" - Remove a reminder
/list\\_reminders - Show all reminders

*Quote Commands:*
/add\\_quote "Your quote" - Add custom quote
/quote\\_now - Generate and send AI quote now

*Info Commands:*
/show\\_schedule - Show current schedule
/summary - Show weekly stats
/ping - Check bot status
/current\\_chat - Show currently configured chat

*Utility:*
/toggle\\_ai - Quick toggle AI mode on/off
/test\\_connection - Test if bot can send messages to configured chat

📝 Note: Only admin can use configuration commands.
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def set_motivation_times(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /set_motivation_times command."""
        if not self._check_admin(update.effective_user.id):
            await update.message.reply_text("❌ Only admin can change settings.")
            return
        
        if not context.args:
            await update.message.reply_text(
                "❌ Usage: /set_motivation_times 09:00, 14:00, 20:00"
            )
            return
        
        times_str = ' '.join(context.args)
        times = [t.strip() for t in times_str.split(',')]
        
        # Validate times
        valid_times = []
        for t in times:
            try:
                hour, minute = map(int, t.split(':'))
                if 0 <= hour <= 23 and 0 <= minute <= 59:
                    valid_times.append(f"{hour:02d}:{minute:02d}")
                else:
                    await update.message.reply_text(f"❌ Invalid time: {t}")
                    return
            except ValueError:
                await update.message.reply_text(f"❌ Invalid time format: {t}")
                return
        
        self.config.set_motivation_times(valid_times)
        self._trigger_reschedule()
        
        await update.message.reply_text(
            f"✅ Motivation times updated: {', '.join(valid_times)}\n\n"
            f"Bot will send messages at these times daily."
        )
    
    async def set_mode(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /set_mode command."""
        if not self._check_admin(update.effective_user.id):
            await update.message.reply_text("❌ Only admin can change settings.")
            return
        
        if not context.args:
            await update.message.reply_text("❌ Usage: /set_mode ai|manual")
            return
        
        mode = context.args[0].lower()
        if mode not in ['ai', 'manual']:
            await update.message.reply_text("❌ Mode must be 'ai' or 'manual'")
            return
        
        if mode == 'ai' and not self.ai.is_available():
            await update.message.reply_text(
                "⚠️ AI mode requested but OpenAI API key not configured.\n"
                "Set OPENAI_API_KEY environment variable to use AI mode."
            )
            return
        
        self.config.set_mode(mode)
        mode_display = "AI-generated" if mode == 'ai' else "Static quotes"
        await update.message.reply_text(f"✅ Switched to {mode_display} motivational messages.")
    
    async def toggle_ai(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /toggle_ai command - quick toggle between AI and manual."""
        if not self._check_admin(update.effective_user.id):
            await update.message.reply_text("❌ Only admin can change settings.")
            return
        
        current_mode = self.config.get_mode()
        new_mode = 'manual' if current_mode == 'ai' else 'ai'
        
        if new_mode == 'ai' and not self.ai.is_available():
            await update.message.reply_text(
                "⚠️ Cannot enable AI mode: OpenAI API key not configured."
            )
            return
        
        self.config.set_mode(new_mode)
        mode_display = "AI-generated" if new_mode == 'ai' else "Static quotes"
        await update.message.reply_text(f"✅ Switched to {mode_display} mode.")
    
    async def add_reminder(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /add_reminder command."""
        if not self._check_admin(update.effective_user.id):
            await update.message.reply_text("❌ Only admin can add reminders.")
            return
        
        if not context.args or len(context.args) < 3:
            await update.message.reply_text(
                '❌ Usage: /add_reminder Monday 10:00 "Your reminder message"'
            )
            return
        
        day = context.args[0]
        time_str = context.args[1]
        message = ' '.join(context.args[2:]).strip('"').strip("'")
        
        if self.config.add_reminder(day, time_str, message):
            self._trigger_reschedule()
            await update.message.reply_text(
                f"✅ Reminder added for {day} {time_str} — \"{message}\""
            )
        else:
            await update.message.reply_text(
                f"❌ Failed to add reminder. Check day name (Monday-Sunday) and time format (HH:MM)."
            )
    
    async def remove_reminder(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /remove_reminder command."""
        if not self._check_admin(update.effective_user.id):
            await update.message.reply_text("❌ Only admin can remove reminders.")
            return
        
        if not context.args:
            await update.message.reply_text('❌ Usage: /remove_reminder "Your reminder message"')
            return
        
        message = ' '.join(context.args).strip('"').strip("'")
        
        if self.config.remove_reminder(message):
            self._trigger_reschedule()
            await update.message.reply_text(f"✅ Reminder removed: \"{message}\"")
        else:
            await update.message.reply_text(f"❌ Reminder not found: \"{message}\"")
    
    async def list_reminders(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /list_reminders command."""
        reminders = self.config.get_reminders()
        
        if not reminders:
            await update.message.reply_text("📋 No reminders scheduled.")
            return
        
        text = "📋 *Current Reminders:*\n\n"
        for i, reminder in enumerate(reminders, 1):
            # Escape special characters in reminder messages
            safe_msg = reminder['message'].replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace('`', '\\`')
            text += f"{i}\\. {reminder['day']} {reminder['time']} → {safe_msg}\n"
        
        await update.message.reply_text(text, parse_mode='Markdown')
    
    async def show_schedule(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /show_schedule command."""
        times = self.config.get_motivation_times()
        reminders = self.config.get_reminders()
        mode = self.config.get_mode()
        chat_id, topic_id = self.config.get_chat()
        
        text = "📅 *Current Schedule:*\n\n"
        text += f"*Mode:* {mode.upper()}\n"
        
        if chat_id:
            text += f"*Chat ID:* `{chat_id}`\n"
            if topic_id:
                text += f"*Topic ID:* `{topic_id}`\n"
        else:
            text += "⚠️ *Chat not set\\. Use /set\\_chat in your group\\.*\n"
        
        text += f"\n*Motivation Times:* {', '.join(times)}\n"
        
        if reminders:
            text += "\n*Reminders:*\n"
            for reminder in reminders:
                # Escape special characters in reminder messages
                safe_msg = reminder['message'].replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace('`', '\\`')
                text += f"  • {reminder['day']} {reminder['time']} → {safe_msg}\n"
        else:
            text += "\n*Reminders:* None\n"
        
        await update.message.reply_text(text, parse_mode='Markdown')
    
    async def add_quote(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /add_quote command."""
        if not context.args:
            await update.message.reply_text('❌ Usage: /add_quote "Your quote here"')
            return
        
        quote = ' '.join(context.args).strip('"').strip("'")
        self.config.add_quote(quote)
        await update.message.reply_text(f"✅ Quote added: \"{quote}\"")
    
    async def quote_now(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /quote_now command - generate and send AI quote immediately."""
        if not self._check_admin(update.effective_user.id):
            await update.message.reply_text("❌ Only admin can generate quotes.")
            return
        
        chat_id, topic_id = self.config.get_chat()
        if not chat_id:
            await update.message.reply_text(
                "❌ Chat not configured. Use /set_chat in your target group first."
            )
            return
        
        try:
            message = self.ai.generate_motivational_message("startup founders")
            
            kwargs = {}
            if topic_id:
                kwargs['message_thread_id'] = topic_id
            
            await self.bot.send_message(chat_id=chat_id, text=message, **kwargs)
            self.config.increment_messages()
            
            await update.message.reply_text(f"✅ Sent motivational message to group!")
        
        except Exception as e:
            logger.error(f"Error sending quote: {e}")
            await update.message.reply_text(f"❌ Error: {e}")
    
    async def summary(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /summary command - show weekly statistics."""
        stats = self.config.get_stats()
        messages = stats.get("messages_sent", 0)
        reminders = stats.get("reminders_sent", 0)
        
        text = "📊 *Weekly Summary*\n\n"
        text += f"Motivational messages sent: {messages}\n"
        text += f"Reminders sent: {reminders}\n"
        text += f"\n*Mode:* {self.config.get_mode().upper()}\n"
        text += f"*Total quotes:* {len(self.config.get_quotes())}\n"
        text += f"*Total reminders:* {len(self.config.get_reminders())}\n"
        
        await update.message.reply_text(text, parse_mode='Markdown')
    
    async def ping(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /ping command - health check."""
        ai_status = "✅ Available" if self.ai.is_available() else "❌ Not configured"
        scheduler_status = "✅ Running" if self.scheduler.scheduler.running else "❌ Stopped"
        
        text = "🏓 *Bot Status*\n\n"
        text += f"AI Generation: {ai_status}\n"
        text += f"Scheduler: {scheduler_status}\n"
        text += f"Mode: {self.config.get_mode().upper()}\n"
        
        await update.message.reply_text(text, parse_mode='Markdown')
    
    async def set_chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /set_chat command - set current chat as target."""
        if not self._check_admin(update.effective_user.id):
            await update.message.reply_text("❌ Only admin can set chat.")
            return
        
        # Get current chat information
        chat_id = update.effective_chat.id
        chat_type = update.effective_chat.type
        chat_title = update.effective_chat.title or "Private Chat"
        
        # Warn if setting to private chat
        if chat_type == "private":
            await update.message.reply_text(
                "⚠️ *Warning: Private Chat Detected*\n\n"
                "You're setting the bot to send messages to this private chat.\n\n"
                "💡 *Tip:* To send to a group:\n"
                "1. Add this bot to your group\n"
                "2. Run `/set\\_chat` **in the group**, not here\n\n"
                "Continue anyway? The chat has been set to this private chat.",
                parse_mode='Markdown'
            )
        
        # Get old chat ID for comparison
        old_chat_id, old_topic_id = self.config.get_chat()
        
        # Set the new chat ID
        self.config.set_chat(chat_id)
        
        # Verify it was saved correctly
        saved_chat_id, saved_topic_id = self.config.get_chat()
        
        # Build response message
        if old_chat_id and old_chat_id != chat_id:
            change_msg = f"📝 Changed from chat `{old_chat_id}` to `{chat_id}`\n\n"
        else:
            change_msg = ""
        
        await update.message.reply_text(
            f"✅ Target chat set successfully!\n\n"
            f"{change_msg}"
            f"📍 *Chat Info:*\n"
            f"• ID: `{saved_chat_id}`\n"
            f"• Type: {chat_type}\n"
            f"• Name: {chat_title}\n\n"
            f"Bot will send scheduled messages here.\n"
            f"Use /test\\_connection to verify bot can send messages.",
            parse_mode='Markdown'
        )
    
    async def set_topic(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /set_topic command - set topic thread ID."""
        if not self._check_admin(update.effective_user.id):
            await update.message.reply_text("❌ Only admin can set topic.")
            return
        
        if not context.args:
            await update.message.reply_text("❌ Usage: /set_topic <topic_id>")
            return
        
        try:
            topic_id = int(context.args[0])
            chat_id = update.effective_chat.id
            self.config.set_chat(chat_id, topic_id)
            await update.message.reply_text(f"✅ Topic thread ID set to: {topic_id}")
        except ValueError:
            await update.message.reply_text("❌ Topic ID must be a number.")
    
    async def test_connection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /test_connection command - test chat connectivity."""
        if not self._check_admin(update.effective_user.id):
            await update.message.reply_text("❌ Only admin can test connection.")
            return
        
        chat_id, topic_id = self.config.get_chat()
        
        if not chat_id:
            await update.message.reply_text(
                "❌ No chat configured yet.\n"
                "Use /set_chat in your target group first."
            )
            return
        
        await update.message.reply_text("🔄 Testing connection to configured chat...")
        
        # Call the test connection function if available
        if self.test_connection_func:
            try:
                success = await self.test_connection_func()
                if success:
                    await update.message.reply_text(
                        "✅ Connection test successful!\n\n"
                        f"Bot can send messages to chat `{chat_id}`"
                        + (f" in topic `{topic_id}`" if topic_id else "") + ".\n\n"
                        "Scheduled messages will be delivered correctly.",
                        parse_mode='Markdown'
                    )
                else:
                    await update.message.reply_text(
                        "❌ Connection test failed!\n\n"
                        f"Bot cannot send messages to chat `{chat_id}`.\n\n"
                        "Possible issues:\n"
                        "• Bot not added to the group\n"
                        "• Bot doesn't have send message permission\n"
                        "• Chat ID is incorrect\n"
                        "• Topic ID is invalid (if using topics)\n\n"
                        "Please check the configuration and try again.",
                        parse_mode='Markdown'
                    )
            except Exception as e:
                await update.message.reply_text(
                    f"❌ Error during connection test:\n`{str(e)}`",
                    parse_mode='Markdown'
                )
        else:
            await update.message.reply_text("❌ Test connection function not available.")
    
    async def current_chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /current_chat command - show currently configured chat."""
        chat_id, topic_id = self.config.get_chat()
        
        if not chat_id:
            await update.message.reply_text(
                "❌ No chat configured yet.\n\n"
                "Use /set\\_chat in your target group to configure it.",
                parse_mode='Markdown'
            )
            return
        
        # Try to get chat info
        try:
            chat = await self.bot.get_chat(chat_id)
            chat_type = chat.type
            chat_title = chat.title or chat.username or "Private Chat"
            
            text = "📍 *Currently Configured Chat:*\n\n"
            text += f"• ID: `{chat_id}`\n"
            text += f"• Type: {chat_type}\n"
            text += f"• Name: {chat_title}\n"
            
            if topic_id:
                text += f"• Topic ID: `{topic_id}`\n"
            
            text += f"\n✅ Bot will send scheduled messages to this chat."
            
            await update.message.reply_text(text, parse_mode='Markdown')
        
        except Exception as e:
            await update.message.reply_text(
                f"⚠️ *Configured Chat Info:*\n\n"
                f"• ID: `{chat_id}`\n"
                + (f"• Topic ID: `{topic_id}`\n" if topic_id else "") +
                f"\n❌ Could not fetch chat details: `{str(e)}`\n\n"
                f"The chat may no longer exist or bot was removed.",
                parse_mode='Markdown'
            )

