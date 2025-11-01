"""
Main entry point for the Startup Motivation Telegram Bot
Initializes bot, handlers, scheduler, and manages all scheduled tasks.
"""

import os
import logging
import asyncio
from telegram import Bot
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv

from config_manager import ConfigManager
from ai_generator import AIGenerator
from scheduler import Scheduler
from handlers import CommandHandlers

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class StartupMotivationBot:
    """Main bot class that orchestrates all components."""
    
    def __init__(self, token: str, timezone: str = "UTC"):
        self.token = token
        self.timezone = timezone
        
        # Initialize components
        self.config = ConfigManager()
        self.ai = AIGenerator(fallback_quotes=self.config.get_quotes())
        # Scheduler will be initialized with event loop later
        self.scheduler = None
        self.bot = None
        self.app = None
        self.handlers = None
        self._reschedule_callback = None
    
    async def test_chat_connection(self) -> bool:
        """
        Test if bot can send messages to the configured chat.
        Returns True if successful, False otherwise.
        """
        chat_id, topic_id = self.config.get_chat()
        
        if not chat_id:
            logger.warning("Chat ID not configured. Cannot test connection.")
            return False
        
        try:
            # Try to get chat information
            chat = await self.bot.get_chat(chat_id)
            logger.info(f"✓ Chat connection verified: {chat.title or chat.username or chat_id}")
            
            # Optionally send a test message
            kwargs = {}
            if topic_id:
                kwargs['message_thread_id'] = topic_id
            
            test_message = await self.bot.send_message(
                chat_id=chat_id,
                text="✅ Bot connection test successful! Ready to send scheduled messages.",
                **kwargs
            )
            logger.info(f"✓ Test message sent successfully to chat {chat_id}")
            return True
            
        except Exception as e:
            logger.error(f"✗ Failed to connect to chat {chat_id}: {e}")
            return False
    
    async def send_motivational_message(self):
        """Send a motivational message based on current mode."""
        chat_id, topic_id = self.config.get_chat()
        
        if not chat_id:
            logger.warning("Chat ID not set. Skipping motivational message.")
            return
        
        try:
            # Generate message based on mode
            mode = self.config.get_mode()
            if mode == 'ai' and self.ai.is_available():
                message = self.ai.generate_motivational_message("startup founders")
            else:
                message = self.config.get_random_quote()
            
            if not message:
                message = "Stay focused and keep building! 🚀"
            
            # Prepare message parameters
            kwargs = {}
            if topic_id:
                kwargs['message_thread_id'] = topic_id
            
            # Send message
            await self.bot.send_message(chat_id=chat_id, text=message, **kwargs)
            self.config.increment_messages()
            logger.info(f"Sent motivational message to {chat_id}")
        
        except Exception as e:
            logger.error(f"Error sending motivational message: {e}")
    
    async def send_reminder(self, reminder_message: str):
        """Send a reminder message."""
        chat_id, topic_id = self.config.get_chat()
        
        if not chat_id:
            logger.warning("Chat ID not set. Skipping reminder.")
            return
        
        try:
            # Optionally enhance reminder with AI if in AI mode
            mode = self.config.get_mode()
            if mode == 'ai' and self.ai.is_available():
                enhanced_message = self.ai.generate_reminder_message(reminder_message)
                # Use enhanced only if it's different and not too long
                if enhanced_message != reminder_message and len(enhanced_message) < 200:
                    message = enhanced_message
                else:
                    message = reminder_message
            else:
                message = reminder_message
            
            kwargs = {}
            if topic_id:
                kwargs['message_thread_id'] = topic_id
            
            await self.bot.send_message(chat_id=chat_id, text=message, **kwargs)
            self.config.increment_reminders()
            logger.info(f"Sent reminder to {chat_id}: {message}")
        
        except Exception as e:
            logger.error(f"Error sending reminder: {e}")
    
    def setup_scheduled_jobs(self):
        """Setup all scheduled jobs based on current configuration."""
        # Check if scheduler is initialized
        if self.scheduler is None:
            logger.warning("Scheduler not initialized yet, skipping job setup")
            return
        
        # Clear existing jobs
        self.scheduler.remove_all_jobs()
        
        # Add motivational message jobs
        motivation_times = self.config.get_motivation_times()
        for time_str in motivation_times:
            job_id = f"motivation_{time_str.replace(':', '_')}"
            self.scheduler.add_daily_job(
                func=self.send_motivational_message,
                time_str=time_str,
                job_id=job_id
            )
        
        # Add reminder jobs
        reminders = self.config.get_reminders()
        for reminder in reminders:
            job_id = f"reminder_{reminder['day']}_{reminder['time'].replace(':', '_')}"
            self.scheduler.add_weekly_job(
                func=self.send_reminder,
                day=reminder['day'],
                time_str=reminder['time'],
                job_id=job_id,
                kwargs={'reminder_message': reminder['message']}
            )
        
        logger.info(f"Setup {len(motivation_times)} motivation jobs and {len(reminders)} reminder jobs")
    
    def setup_handlers(self):
        """Setup all command handlers."""
        # Create a temporary scheduler reference (will be updated in post_init)
        # We'll pass None and update it later since scheduler needs event loop
        from scheduler import Scheduler
        temp_scheduler = Scheduler(timezone=self.timezone)
        
        self.handlers = CommandHandlers(
            config_manager=self.config,
            ai_generator=self.ai,
            scheduler=temp_scheduler,  # Will be updated in post_init
            bot_instance=self.bot
        )
        # Pass reschedule callback to handlers
        self.handlers.set_reschedule_callback(self.setup_scheduled_jobs)
        # Pass test connection callback to handlers
        self.handlers.set_test_connection_callback(self.test_chat_connection)
        
        # Register all command handlers
        command_map = {
            'start': self.handlers.start,
            'help': self.handlers.help,
            'set_motivation_times': self.handlers.set_motivation_times,
            'set_mode': self.handlers.set_mode,
            'toggle_ai': self.handlers.toggle_ai,
            'add_reminder': self.handlers.add_reminder,
            'remove_reminder': self.handlers.remove_reminder,
            'list_reminders': self.handlers.list_reminders,
            'show_schedule': self.handlers.show_schedule,
            'add_quote': self.handlers.add_quote,
            'quote_now': self.handlers.quote_now,
            'summary': self.handlers.summary,
            'ping': self.handlers.ping,
            'set_chat': self.handlers.set_chat,
            'set_topic': self.handlers.set_topic,
            'test_connection': self.handlers.test_connection,
        }
        
        for command, handler in command_map.items():
            self.app.add_handler(CommandHandler(command, handler))
        
        logger.info("Command handlers registered")
    
    async def post_init(self, application: Application):
        """Called after application initialization."""
        self.bot = application.bot
        
        # Initialize scheduler - it will use the current running event loop
        if self.scheduler is None:
            # Reinitialize with proper scheduler
            from scheduler import Scheduler
            self.scheduler = Scheduler(timezone=self.timezone)
            # Start scheduler - it will attach to the current event loop
            self.scheduler.start()
        
        # Update handlers with scheduler reference
        if self.handlers:
            self.handlers.scheduler = self.scheduler
        
        self.setup_scheduled_jobs()
    
    async def run(self):
        """Run the bot."""
        # Create application
        self.app = Application.builder().token(self.token).build()
        
        # Setup handlers first
        self.setup_handlers()
        
        # Initialize the application
        await self.app.initialize()
        self.bot = self.app.bot
        
        # Initialize scheduler after bot is initialized
        from scheduler import Scheduler
        if self.scheduler is None:
            self.scheduler = Scheduler(timezone=self.timezone)
            self.scheduler.start()
        
        # Update handlers with scheduler reference
        if self.handlers:
            self.handlers.scheduler = self.scheduler
        
        # Setup scheduled jobs
        self.setup_scheduled_jobs()
        
        # Start the bot
        await self.app.start()
        logger.info("Starting bot...")
        
        # Test chat connection if configured
        chat_id, _ = self.config.get_chat()
        if chat_id:
            logger.info("Testing chat connection...")
            connection_ok = await self.test_chat_connection()
            if not connection_ok:
                logger.warning("⚠️ Chat connection test failed. Please verify chat configuration with /set_chat")
        else:
            logger.info("ℹ️ No chat configured yet. Use /set_chat in your target group to configure.")
        
        # Start polling - allow all update types to handle commands properly
        await self.app.updater.start_polling()
        
        # Keep running until stopped
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        finally:
            await self.app.updater.stop()
            await self.app.stop()
            await self.app.shutdown()
            if self.scheduler:
                self.scheduler.stop()


async def main():
    """Main entry point."""
    # Get environment variables
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN environment variable is required")
    
    admin_id = os.getenv("ADMIN_ID")
    timezone = os.getenv("TIMEZONE", "UTC")
    
    # Initialize bot
    bot = StartupMotivationBot(token=token, timezone=timezone)
    
    # Set admin ID if provided
    if admin_id:
        try:
            bot.config.set_admin(int(admin_id))
        except ValueError:
            logger.warning(f"Invalid ADMIN_ID: {admin_id}")
    
    # Run bot
    await bot.run()


if __name__ == "__main__":
    asyncio.run(main())

