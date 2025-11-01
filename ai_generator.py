"""
AI Generator - Handles OpenAI API integration for generating motivational messages
Includes fallback to static quotes if API is unavailable.
"""

import os
from typing import Optional
from openai import OpenAI, APIError


class AIGenerator:
    """Generates motivational messages using OpenAI API with fallback support."""
    
    def __init__(self, api_key: Optional[str] = None, fallback_quotes: list = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = None
        self.fallback_quotes = fallback_quotes or []
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client if API key is available."""
        if self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI client: {e}")
                self.client = None
    
    def is_available(self) -> bool:
        """Check if AI generation is available."""
        return self.client is not None
    
    def generate_motivational_message(self, context: str = "startup founders") -> str:
        """
        Generate a motivational message using OpenAI API.
        Falls back to static quote if API is unavailable.
        
        Args:
            context: Context for the message (e.g., "startup founders")
        
        Returns:
            Generated or fallback motivational message
        """
        if not self.is_available():
            return self._get_fallback_message()
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Using cost-effective model
                messages=[
                    {
                        "role": "system",
                        "content": "You are a motivational coach for startup founders. Write short, inspiring messages (1-2 sentences max) that energize and motivate."
                    },
                    {
                        "role": "user",
                        "content": f"Craft a short motivational message for {context}. Make it authentic, actionable, and inspiring. Keep it under 150 characters."
                    }
                ],
                max_tokens=60,
                temperature=0.8
            )
            
            message = response.choices[0].message.content.strip()
            if message:
                return message
            else:
                return self._get_fallback_message()
        
        except (APIError, Exception) as e:
            print(f"Error generating AI message: {e}")
            return self._get_fallback_message()
    
    def generate_reminder_message(self, reminder_text: str) -> str:
        """
        Generate a creative reminder message using OpenAI API.
        
        Args:
            reminder_text: The base reminder text
        
        Returns:
            Enhanced reminder message or original if API unavailable
        """
        if not self.is_available():
            return reminder_text
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that makes reminders fun and startup-themed. Keep messages short and engaging."
                    },
                    {
                        "role": "user",
                        "content": f"Write a fun, startup-themed reminder for: {reminder_text}. Keep it under 100 characters and include the original reminder meaning."
                    }
                ],
                max_tokens=50,
                temperature=0.7
            )
            
            message = response.choices[0].message.content.strip()
            return message if message else reminder_text
        
        except (APIError, Exception) as e:
            print(f"Error generating reminder message: {e}")
            return reminder_text
    
    def _get_fallback_message(self) -> str:
        """Get a random fallback message from static quotes."""
        import random
        if self.fallback_quotes:
            return random.choice(self.fallback_quotes)
        return "Stay focused and keep building! 🚀"

