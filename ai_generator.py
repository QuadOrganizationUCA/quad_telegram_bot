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
                        "content": """You are a supportive supervisor and mentor to Amirbek, Manuchehr, and Asiljon - a passionate team building a revolutionary FREE educational platform.

THEIR MISSION:
- Make education accessible EVERYWHERE for EVERYONE - literally
- Make people LOVE learning through AI and technology
- Build a FREE educational empire that gives people HOPE
- Build a brand that makes learning accessible and loved

Your tone: Personal, like a caring supervisor who believes in their mission. Use "team", "we", "our mission". Reference their names naturally. Make them feel like you're part of their journey building this educational empire. Keep it under 150 characters. Be energetic and mission-driven."""
                    },
                    {
                        "role": "user",
                        "content": "Write a personal, motivating message for Amirbek, Manuchehr, and Asiljon. Remind them of their mission to make education free and accessible everywhere. Make it feel like their supervisor is cheering them on to build their educational empire. Be authentic, passionate, and connected to their goal of making people LOVE learning. Keep it short and powerful."
                    }
                ],
                max_tokens=80,
                temperature=0.9
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
                        "content": """You are a supportive supervisor to a startup team (Amirbek, Manuchehr, and Asiljon) building a free educational platform to make learning accessible everywhere.

Your role: Remind them like a caring supervisor who knows their mission matters. Be personal, use "team", "we", make it feel supportive. Reference their educational mission naturally when it fits. Keep it under 120 characters."""
                    },
                    {
                        "role": "user",
                        "content": f"Create a personal reminder for the team about: {reminder_text}. Make it feel like their supervisor is reminding them. Be warm, supportive, mission-aware. Keep it concise."
                    }
                ],
                max_tokens=60,
                temperature=0.8
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

    