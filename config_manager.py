"""
Configuration Manager - Handles persistence of bot settings
Stores all settings in a JSON file for persistence across restarts.
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime


class ConfigManager:
    """Manages bot configuration with JSON persistence."""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load configuration from JSON file, create default if not exists."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                # If file is corrupted, start fresh
                return self._get_default_config()
        return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Returns default configuration structure."""
        return {
            "admin_id": None,
            "chat_id": None,
            "topic_id": None,
            "motivation_times": ["09:00", "14:00", "20:00"],
            "mode": "manual",  # 'manual' or 'ai'
            "reminders": [],
            "quotes": [
                "Team, remember why we started: making education free and accessible for everyone. Keep building! 🚀",
                "Amirbek, Manuchehr, Asiljon - every line of code brings us closer to our educational empire. Keep pushing! 💪",
                "We're not just building an app - we're giving people hope through education. Let's keep going! ✨",
                "Every person who learns through our platform is a win for our mission. Stay focused, team! 🎯",
                "Education should be free. Learning should be loved. Let's make it happen together! 🔥"
            ],
            "stats": {
                "messages_sent": 0,
                "reminders_sent": 0,
                "last_reset": datetime.now().isoformat()
            }
        }
    
    def _save_config(self):
        """Save current configuration to JSON file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            print(f"✓ Config saved to {self.config_file}")
        except IOError as e:
            print(f"✗ Error saving config: {e}")
    
    # Admin and chat settings
    def set_admin(self, admin_id: int):
        """Set the admin user ID."""
        self.config["admin_id"] = admin_id
        self._save_config()
    
    def is_admin(self, user_id: int) -> bool:
        """Check if user ID is the admin."""
        return self.config.get("admin_id") == user_id
    
    def set_chat(self, chat_id: int, topic_id: Optional[int] = None):
        """Set the target chat ID and optional topic ID."""
        print(f"Setting chat_id to: {chat_id}")
        self.config["chat_id"] = chat_id
        if topic_id is not None:
            print(f"Setting topic_id to: {topic_id}")
            self.config["topic_id"] = topic_id
        else:
            # Clear topic_id when setting a new chat without specifying topic
            if "topic_id" in self.config:
                print("Clearing previous topic_id")
                self.config["topic_id"] = None
        self._save_config()
        print(f"Chat ID after save: {self.config.get('chat_id')}")
        print(f"Topic ID after save: {self.config.get('topic_id')}")
    
    def get_chat(self) -> tuple[Optional[int], Optional[int]]:
        """Get chat ID and topic ID."""
        return (self.config.get("chat_id"), self.config.get("topic_id"))
    
    # Motivation settings
    def set_motivation_times(self, times: List[str]):
        """Set the times when motivational messages should be sent."""
        self.config["motivation_times"] = times
        self._save_config()
    
    def get_motivation_times(self) -> List[str]:
        """Get list of motivation times."""
        return self.config.get("motivation_times", [])
    
    def set_mode(self, mode: str):
        """Set the mode: 'manual' or 'ai'."""
        if mode.lower() in ['manual', 'ai']:
            self.config["mode"] = mode.lower()
            self._save_config()
    
    def get_mode(self) -> str:
        """Get current mode."""
        return self.config.get("mode", "manual")
    
    # Quotes management
    def add_quote(self, quote: str):
        """Add a new quote to the list."""
        if "quotes" not in self.config:
            self.config["quotes"] = []
        self.config["quotes"].append(quote)
        self._save_config()
    
    def get_quotes(self) -> List[str]:
        """Get all quotes."""
        return self.config.get("quotes", [])
    
    def get_random_quote(self) -> Optional[str]:
        """Get a random quote from the list."""
        import random
        quotes = self.get_quotes()
        return random.choice(quotes) if quotes else None
    
    # Reminders management
    def add_reminder(self, day: str, time: str, message: str) -> bool:
        """Add a new reminder. Returns True if added successfully."""
        day = day.capitalize()
        valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        if day not in valid_days:
            return False
        
        # Check for duplicate
        reminders = self.config.get("reminders", [])
        for reminder in reminders:
            if reminder["day"] == day and reminder["time"] == time and reminder["message"] == message:
                return False
        
        reminders.append({
            "day": day,
            "time": time,
            "message": message
        })
        self.config["reminders"] = reminders
        self._save_config()
        return True
    
    def remove_reminder(self, message: str) -> bool:
        """Remove a reminder by matching the message text."""
        reminders = self.config.get("reminders", [])
        original_count = len(reminders)
        self.config["reminders"] = [r for r in reminders if r["message"] != message]
        removed = len(reminders) != len(self.config["reminders"])
        if removed:
            self._save_config()
        return removed
    
    def get_reminders(self) -> List[Dict]:
        """Get all reminders."""
        return self.config.get("reminders", [])
    
    # Statistics
    def increment_messages(self):
        """Increment motivational messages counter."""
        if "stats" not in self.config:
            self.config["stats"] = {}
        self.config["stats"]["messages_sent"] = self.config["stats"].get("messages_sent", 0) + 1
        self._save_config()
    
    def increment_reminders(self):
        """Increment reminders counter."""
        if "stats" not in self.config:
            self.config["stats"] = {}
        self.config["stats"]["reminders_sent"] = self.config["stats"].get("reminders_sent", 0) + 1
        self._save_config()
    
    def get_stats(self) -> Dict:
        """Get statistics."""
        return self.config.get("stats", {})

