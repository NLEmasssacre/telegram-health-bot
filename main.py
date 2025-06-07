import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram_api import TelegramBot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    # Initialize bot
    bot = TelegramBot()
    
    # Initialize scheduler
    scheduler = AsyncIOScheduler()
    
    # Schedule daily post at 10:00 MSK (07:00 UTC)
    scheduler.add_job(
        bot.publish_scheduled_post,
        trigger=CronTrigger(hour=7, minute=0, timezone='UTC'),
        id='daily_post',
        name='Publish daily post to channel'
    )
    
    # Start scheduler
    scheduler.start()
    logger.info("Scheduler started")
    
    try:
        # Start bot
        await bot.start()
    except Exception as e:
        logger.error(f"Error running bot: {e}")
    finally:
        scheduler.shutdown()

if __name__ == "__main__":
    asyncio.run(main()) 