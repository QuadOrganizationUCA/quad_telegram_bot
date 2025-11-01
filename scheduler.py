"""
Scheduler - Manages timed tasks using APScheduler
Handles motivational messages and reminders scheduling.
"""

import logging
from datetime import datetime, time
from typing import Optional, Callable
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


logger = logging.getLogger(__name__)


class Scheduler:
    """Manages all scheduled tasks using APScheduler."""
    
    def __init__(self, timezone: str = "UTC"):
        self.scheduler = AsyncIOScheduler(timezone=timezone)
        self.job_ids = set()
    
    def start(self):
        """Start the scheduler."""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Scheduler started")
    
    def stop(self):
        """Stop the scheduler."""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler stopped")
    
    def add_daily_job(
        self,
        func: Callable,
        time_str: str,
        job_id: str,
        args: tuple = (),
        kwargs: dict = None
    ):
        """
        Add a daily job at a specific time.
        
        Args:
            func: Async function to call
            time_str: Time in HH:MM format (e.g., "09:00")
            job_id: Unique identifier for the job
            args: Positional arguments to pass to func
            kwargs: Keyword arguments to pass to func
        """
        try:
            hour, minute = map(int, time_str.split(':'))
            
            # Remove existing job with same ID if it exists
            if job_id in self.job_ids:
                self.remove_job(job_id)
            
            self.scheduler.add_job(
                func,
                trigger=CronTrigger(hour=hour, minute=minute),
                id=job_id,
                args=args,
                kwargs=kwargs or {},
                replace_existing=True
            )
            self.job_ids.add(job_id)
            logger.info(f"Added daily job '{job_id}' at {time_str}")
        
        except ValueError as e:
            logger.error(f"Invalid time format '{time_str}': {e}")
    
    def add_weekly_job(
        self,
        func: Callable,
        day: str,
        time_str: str,
        job_id: str,
        args: tuple = (),
        kwargs: dict = None
    ):
        """
        Add a weekly recurring job on a specific day and time.
        
        Args:
            func: Async function to call
            day: Day of week (Monday, Tuesday, etc.)
            time_str: Time in HH:MM format
            job_id: Unique identifier for the job
            args: Positional arguments to pass to func
            kwargs: Keyword arguments to pass to func
        """
        try:
            day_map = {
                'Monday': 0,
                'Tuesday': 1,
                'Wednesday': 2,
                'Thursday': 3,
                'Friday': 4,
                'Saturday': 5,
                'Sunday': 6
            }
            
            day_of_week = day_map.get(day.capitalize())
            if day_of_week is None:
                logger.error(f"Invalid day: {day}")
                return
            
            hour, minute = map(int, time_str.split(':'))
            
            # Remove existing job with same ID if it exists
            if job_id in self.job_ids:
                self.remove_job(job_id)
            
            self.scheduler.add_job(
                func,
                trigger=CronTrigger(day_of_week=day_of_week, hour=hour, minute=minute),
                id=job_id,
                args=args,
                kwargs=kwargs or {},
                replace_existing=True
            )
            self.job_ids.add(job_id)
            logger.info(f"Added weekly job '{job_id}' on {day} at {time_str}")
        
        except ValueError as e:
            logger.error(f"Invalid time format '{time_str}': {e}")
    
    def remove_job(self, job_id: str):
        """Remove a scheduled job."""
        try:
            if job_id in self.job_ids:
                self.scheduler.remove_job(job_id)
                self.job_ids.remove(job_id)
                logger.info(f"Removed job '{job_id}'")
                return True
        except Exception as e:
            logger.error(f"Error removing job '{job_id}': {e}")
        return False
    
    def remove_all_jobs(self):
        """Remove all scheduled jobs."""
        for job_id in list(self.job_ids):
            self.remove_job(job_id)
    
    def get_job_count(self) -> int:
        """Get the number of scheduled jobs."""
        return len(self.job_ids)

